#!/usr/bin/env python
# -*- coding:utf-8 -*-

import werobot,werobot.client
from Translator import *
import argparse,ConfigParser
from PickledRedis import PickledRedis
import os.path
import logging
from audio import AudioFetcher
import phonetic
from util import to_utf8,to_unicode,check_create_dir
from ekho import Ekho

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
translation_service = cfg.get(args.env,"translation_service")
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
check_create_dir(wav_folder)
mp3_folder = cfg.get(args.env,"mp3_folder")
check_create_dir(mp3_folder)
words_audio_folder = cfg.get(args.env,"words_audio_folder")
check_create_dir(words_audio_folder)
wechat_token = cfg.get(args.env,"token")
audio_file_url_prefix = cfg.get(args.env,"audio_file_url_prefix")

ekho = None
enable_ekho = cfg.getboolean(args.env,"enable_ekho")
if enable_ekho:
	ekho = Ekho(words_audio_folder)

audio_fetcher = AudioFetcher(wav_folder, mp3_folder, words_audio_folder)
robot = werobot.WeRoBot(token=wechat_token)

def get_cache_translation(content):
	result = None
	if enable_redis and redis_client:
		key = "tansalation:" + content
		try:
			logger.debug("try get cached translation")
			result = redis_client.get(key)
			if result:
				logger.debug("find cached translation")
			else:
				logger.debug("no cached translation found")
				logger.debug("try get translation using %s service" % translation_service)
				result = get_translation(content,translation_service)
				if result:
					redis_client.set(key, result)
					redis_client.expire(key, translation_expire_seconds)
		except:
			logger.exception("get cache translation error")

	if not result:
		logger.debug("try get translation using %s service" % translation_service)
		result = get_translation(content,translation_service)
	return result
		
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

def get_audio_url(result):
	if ekho:
		audio_filename = ekho.get_pronounces_mp3(result)
	else:
		audio_filename = audio_fetcher.get_pronounces_mp3(result.pronounce_list)
	name = os.path.basename(audio_filename)
	return audio_file_url_prefix + name

def get_audio_url2(pronounce_list):
	audio_filename = audio_fetcher.get_pronounces_mp3(pronounce_list)
	name = os.path.basename(audio_filename)
	return audio_file_url_prefix + name

text_menu = u"""\
功能：
* ：收听电台
# ：获得上一条翻译的语音
？：获得帮助
1 ：进入微社区论坛
2 ：星爷粉丝大考验
输入文字获得文字翻译
输入#+文字获得语音翻译
输入单个中文字符获得注音及解析
输入注音获得语音及对应发音的字

tips:
如果语音没有声音，请暂停再播放
"""
import re

@robot.filter(re.compile(u"[\?？]"))
def get_menu():
	return text_menu

@robot.filter(re.compile(u"^[a-z]+\d$"))
def get_chars(txtMsg):
	content = txtMsg.content
	print content
	r = phonetic.get_characters_result(content)
	if r:
		try:
			url = get_audio_url([content])
			return [content,r.pretty(),url]
		except Exception, e:
			logger.exception("get_chars error")
			return r.pretty()
		
	else:
		return u"暂无解析"

def cache_user_msg(userid, msg):
	if enable_redis and redis_client:
		key = userid + "_last_content"
		redis_client.set(key, msg)
		redis_client.expire(key, translation_expire_seconds)
		return True
	else:
		return False

chn = re.compile(u"^[\u4e00-\u9fa5]$")

@robot.filter(chn)
def get_pronus(txtMsg):
	userid = txtMsg.source
	content = txtMsg.content
	r = phonetic.get_pronunciations_result(content)
	if r:
		if cache_user_msg(userid,content):
			return r.pretty() + u"\n--回复#获得语音--"
		else:
			return r.pretty()
	else:
		return u"暂无解析1"


@robot.filter("*")
def get_radio():
	return [[u"《粤讲粤酷》电台",
	u"《粤讲粤酷》电台在网易云音乐开播啦！每期邀请嘉宾以脱口秀的形式教学粤语，"
	u"希望大家能够在轻松愉快的氛围中学会粤语。喜欢的朋友更课使用网易"
	u"云音乐客户端订阅电台，这样每期更新都会有提醒哟！",
	"http://7sbpek.com1.z0.glb.clouddn.com/img/radio.jpg",
	"http://music.163.com/djradio?id=225001"]]

@robot.filter("1")
def get_radio():
	return [[u"粤讲粤酷交流论坛",
	u"欢迎反馈公众号问题，交流粤语学习经验，分享粤语学习资源",
	"http://dzqun.gtimg.cn/qpanel/images/banner1.jpg",
	"http://m.wsq.qq.com/264028609"]]

@robot.filter("2")
def get_radio():
	return [[u"星爷粉丝大考验",
	u"听对白答电影，星爷粉丝大考验",
	"http://7sbpek.com1.z0.glb.clouddn.com/img/stephen.jpg",
	"http://stephen.kkee.tk"]]

def get_last_translation_audio(userid):
	key = userid + "_last_content"
	content = redis_client.get(key)
	if content:
		if chn.search(content): #单个汉字
			r = phonetic.get_pronunciations_result(content)
			prons = []
			for p in r.plist:
				prons.append(p.pronunciation)
			url = get_audio_url2(prons)
			return [content, ",".join(prons), url]
		else:
			result = get_cache_translation(content) 
			return get_music_msg(result)
	else:
		return u"抱歉，找不到上一条消息"

def get_music_msg(result):
	if result.has_pronounce:
		url = get_audio_url(result)
		return [result.words,result.get_words_with_pronounces(),url]
	else:
		return u"暂无语音翻译,下面是文字翻译\n" + result.words

@robot.text
def translate(txtMsg):
	try:
		userid = txtMsg.source
		content = txtMsg.content
		if "#" == content:
			return get_last_translation_audio(userid)
		# if type(content) == unicode:
		# 	content = content.encode('utf-8')
		logger.info("revice text message from %s, content: %s" % (userid,to_utf8(content)))
		return_audio = False
		if content.startswith("#"):
			content = content[1:]
			return_audio = True
		result = get_cache_translation(content) 
		logger.info("get translation:%s" % result.words)
		if enable_client:
			client.send_text_message(userid, result.words)
			mediaid = get_mediaid(result.pronounce_list)
			if mediaid:
				client.send_voice_message(userid,mediaid)
			return result.pretty()
		elif return_audio:
			return get_music_msg(result)
		else:
			if enable_redis and redis_client:
				key = userid + "_last_content"
				redis_client.set(key, content)
				redis_client.expire(key, translation_expire_seconds)
				return result.pretty() + u"\n--回复#获得语音--"
			else:
				return result.pretty()
			

	except TranslationException, e:
		logger.exception(e.message)
		return e.message	
	
@robot.subscribe
def subscribe(message):
	return subscribe_msg.decode("utf-8")

robot.run(None,host,port)


