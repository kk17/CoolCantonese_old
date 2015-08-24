#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
from util import check_create_dir
from os import environ
import json

def get_from_env(key):
	if environ.has_key(key):
		return environ[key]
	return None


class WechatConfig(object):
	"""docstring for WechatConfig"""
	def __init__(self, env, env_cfg_path):
		super(WechatConfig, self).__init__()
		self.env_cfg_path = env_cfg_path
		self.env = env
		cfg = ConfigParser.ConfigParser()
		cfg.read(env_cfg_path)
		self._cfg = cfg

		self.wechat_token = self.__get_str_from_env_or_config("WECHAT_TOKEN", "token")
		self.host = cfg.get(env,"host")
		self.port = cfg.get(env,"port")
		self.translation_service = cfg.get(env,"translation_service")
		self.enable_client = self.__get_bool_from_env_or_config("ENABLE_WECHAT_CLIENT_API", "enable_client")
		self.appid = self.__get_str_from_env_or_config("WECHAT_APPID", "appid")
		self.appsecret = self.__get_str_from_env_or_config("WECHAT_APPSECRET", "appsecret")

		self.enable_redis = self.__get_bool_from_env_or_config("ENABLE_REDIS","enable_redis")
		self.redis_host = self.__get_str_from_env_or_config("COOLCANTONESE_REDIS_PORT_6379_TCP_ADDR","redis_host")
		self.redis_port = self.__get_int_from_env_or_config("COOLCANTONESE_REDIS_PORT_6379_TCP_PORT","redis_port")
		self.redis_password = self.__get_str_from_env_or_config("COOLCANTONESE_REDIS_PASSWORD","redis_password")
		self.redis_db = cfg.getint(env, "redis_db")
		self.translation_expire_seconds = eval(cfg.get(env,"translation_expire_seconds"))
		self.mediaid_expire_seconds = eval(cfg.get(env, "mediaid_expire_seconds"))
		
		self.subscribe_msg = cfg.get(env,"subscribe_msg").decode("utf-8")
		self.wav_folder = cfg.get(env,"wav_folder")
		check_create_dir(self.wav_folder)
		self.mp3_folder = cfg.get(env,"mp3_folder")
		check_create_dir(self.mp3_folder)
		self.words_audio_folder = cfg.get(env,"words_audio_folder")
		check_create_dir(self.words_audio_folder)
		
		self.audio_file_url_prefix = cfg.get(env,"audio_file_url_prefix")
	
		self.enable_ekho = cfg.getboolean(env,"enable_ekho")
		self.baidu_translate_client_id = self.__get_str_from_env_or_config("BAIDU_TRANSLATE_CLIENT_ID", "baidu_translate_client_id")

		self.enable_qiniu = self.__get_bool_from_env_or_config("ENABLE_QINIU","enable_qiniu")
		self.qiniu_access_key = self.__get_str_from_env_or_config("QINIU_ACCESS_KEY","qiniu_access_key")
		self.qiniu_secret_key = self.__get_str_from_env_or_config("QINIU_SECRET_KEY","qiniu_secret_key")
		self.qiniu_bucket_name = self.__get_str_from_env_or_config("QINIU_BUCKET_NAME","qiniu_bucket_name")
		self.qiniu_bucket_domain = self.__get_str_from_env_or_config("QINIU_BUCKET_DOMAIN","qiniu_bucket_domain")

		self.enable_record_services = self.__get_bool_from_env_or_config("ENABLE_RECORD_SERVICES","enable_record_services")
		self.record_services_url_prefix = self.__get_str_from_env_or_config("RECORD_SERVICES_URL_PREFIX","record_services_url_prefix")
		
		self.enable_tuling_robot = self.__get_bool_from_env_or_config("ENABLE_TULING_ROBOT","enable_tuling_robot")
		self.tuling_robot_api_key = self.__get_str_from_env_or_config("TULING_ROBOT_API_KEY","tuling_robot_api_key")



	def __get_str_from_env_or_config(self, env_key, config_name):
		val = get_from_env(env_key)
		if val is None:
			val = self._cfg.get(self.env, config_name)
		return val

	def __get_bool_from_env_or_config(self, env_key, config_name):
		val = self.__get_str_from_env_or_config(env_key, config_name)
		if val == "1" or val == "true" or val == "True":
			return True
		return False

	def __get_int_from_env_or_config(self, env_key, config_name):
		val = self.__get_str_from_env_or_config(env_key, config_name)
		return int(val)

	def __str__(self):
		result = json.dumps(self, ensure_ascii=False,sort_keys=True,indent=4, separators=(',', ': '))
		# 从unicode类型变成str类型
		result = result.encode("utf-8")
		return result


def main():
	cfg = WechatConfig("Dev", "configs/env.cfg")
	print cfg.__dict__


if __name__ == '__main__':
	main()