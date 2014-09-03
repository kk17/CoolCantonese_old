#!/usr/bin/env python
# -*- coding:utf-8 -*-

import werobot,werobot.client
from Translator import *
import argparse,ConfigParser
from PickledRedis import PickledRedis
import os.path
import logging
from audio import AudioFetcher
	
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 创建一个handler，用于输出到控制台  
ch = logging.StreamHandler()  
ch.setLevel(logging.DEBUG)  
FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
formatter = logging.Formatter(FORMAT)
ch.setFormatter(formatter)

logger = logging.getLogger("wechat")
logger.addHandler(ch)
logger.setLevel(logging.DEBUG)  

config_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser(description="Cantonese Tranlation Wechat Robot")
parser.add_argument("-e", "--env", help = "set environment, default value is 'Dev'.", default = "Dev", metavar = "ENV")

args = parser.parse_args()
cfg = ConfigParser.ConfigParser()
cfg_path = os.path.join(config_dir, "env.cfg")
cfg.read(cfg_path)

host = cfg.get(args.env,"host")
port = cfg.get(args.env,"port")
enable_client = cfg.getboolean(args.env,"enable_client")
if enable_client:
	appid = cfg.get(args.env, "appid")
	appsecret = cfg.get(args.env, "appsecret")
	client = werobot.client.Client(appid, appsecret)

redis_client = None
enable_redis = cfg.getboolean(args.env,"enable_redis")
if enable_redis:
	redis_cfg = ConfigParser.ConfigParser()
	redis_cfg_path = os.path.join(config_dir,"redis.cfg")
	redis_cfg.read(redis_cfg_path)
	redis_host = redis_cfg.get(args.env, "host")
	redis_port = redis_cfg.getint(args.env, "port")
	db = redis_cfg.getint(args.env, "db")
	password = redis_cfg.get(args.env, "password")
	redis_client = PickledRedis(redis_host,redis_port,db,password)
	translation_expire_seconds = eval(cfg.get(args.env,"translation_expire_seconds"))
	mediaid_expire_seconds = eval(cfg.get(args.env, "mediaid_expire_seconds"))


subscribe_msg = cfg.get(args.env,"subscribe_msg")
wav_folder = cfg.get(args.env,"wav_folder")
mp3_folder = cfg.get(args.env,"mp3_folder")
words_audio_folder = cfg.get(args.env,"words_audio_folder")
wechat_token = cfg.get(args.env,"token")
audio_fetcher = AudioFetcher(wav_folder, mp3_folder, words_audio_folder)
robot = werobot.WeRoBot(token=wechat_token)

def get_cache_translation(content):
	if enable_redis:
		key = "tansalation:" + content
		try:
			result = redis_client.get(key)
		except:
			logger.exception("get cache translation error")
		if result:
			return result
		else:
			result = get_translation(content)
			if result:
				redis_client.set(key, result)
				redis_client.expire(key, translation_expire_seconds)
			return result
	else:
		return get_translation(content)
		
def get_mediaid(pronounce_list):
	key = ""
	for p in pronounce_list:
		if p:
			key += p
	if "" == key:
		return None
	key = "mediaid:" + key
	mediaid = redis_client.get(key)
	if  mediaid:
		return mediaid
	try:
		audio_filename = audio_fetcher.get_pronounces_mp3(pronounce_list)
		if audio_filename:
			resp = client.upload_media("voice",open(audio_filename,"rb"))
			mediaid = resp["media_id"]
	except:
		logger.exception("upload audio file error")
	if mediaid:
		redis_client.set(key, mediaid)
		redis_client.expire(key, mediaid_expire_seconds)
	return mediaid


@robot.text
def translate(txtMsg):
	try:
		userid = txtMsg.source
		content = txtMsg.content
		if type(content) == unicode:
			content = content.encode('utf-8')
		logger.info("revice text message from %s, content: %s" % (userid,content))
		result = get_cache_translation(content) 
		logger.info("get translation:%s" % result.words)
		if enable_client:
			client.send_text_message(userid, result.words)
			mediaid = get_mediaid(result.pronounce_list)
			if mediaid:
				client.send_voice_message(userid,mediaid)
			return result.get_format_result()
		else:
			return result.words +"\n\n" + result.get_format_result()
	except TranslationException, e:
		logger.exception(e.message)
		return e.message	
	
@robot.subscribe
def subscribe(message):
	return subscribe_msg.decode("utf-8")

robot.run(None,host,port)


