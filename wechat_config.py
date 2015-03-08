#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
from util import check_create_dir

class WechatConfig(object):
	"""docstring for WechatConfig"""
	def __init__(self, env, env_cfg_path, redis_cfg_path):
		super(WechatConfig, self).__init__()
		self.env_cfg_path = env_cfg_path
		self.redis_cfg_path = redis_cfg_path
		# print env_cfg_path,redis_cfg_path
		self.env = env
		cfg = ConfigParser.ConfigParser()
		cfg.read(env_cfg_path)

		self.host = cfg.get(env,"host")
		self.port = cfg.get(env,"port")
		self.translation_service = cfg.get(env,"translation_service")
		self.enable_client = cfg.getboolean(env,"enable_client")
		self.appid = cfg.get(env, "appid")
		self.appsecret = cfg.get(env, "appsecret")

		self.enable_redis = cfg.getboolean(env,"enable_redis")
		redis_cfg = ConfigParser.ConfigParser()
		redis_cfg.read(redis_cfg_path)
		self.redis_host = redis_cfg.get(env, "host")
		self.redis_port = redis_cfg.getint(env, "port")
		self.redis_db = redis_cfg.getint(env, "db")
		self.redis_password = redis_cfg.get(env, "password")
		self.translation_expire_seconds = eval(cfg.get(env,"translation_expire_seconds"))
		self.mediaid_expire_seconds = eval(cfg.get(env, "mediaid_expire_seconds"))
		
		self.subscribe_msg = cfg.get(env,"subscribe_msg").decode("utf-8")
		self.wav_folder = cfg.get(env,"wav_folder")
		check_create_dir(self.wav_folder)
		self.mp3_folder = cfg.get(env,"mp3_folder")
		check_create_dir(self.mp3_folder)
		self.words_audio_folder = cfg.get(env,"words_audio_folder")
		check_create_dir(self.words_audio_folder)
		self.wechat_token = cfg.get(env,"token")
		self.audio_file_url_prefix = cfg.get(env,"audio_file_url_prefix")
	
		self.enable_ekho = cfg.getboolean(env,"enable_ekho")
		self.baidu_translate_client_id = cfg.get(env,"baidu_translate_client_id")

