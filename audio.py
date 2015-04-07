#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,os.path,os,logging
from pydub import AudioSegment
from pydub.effects import speedup
from util import urlretrieve
from qiniu_storage import QiniuStorage



class AudioFetcher(object):
	logger = logging.getLogger("wechat")

	def __init__(self, cfg):
		super(AudioFetcher, self).__init__()
		self.ekho = None
		if cfg.enable_ekho:
			from ekho import Ekho
			self.ekho = Ekho(cfg.words_audio_folder)
		self.qiniq = None
		if cfg.enable_qiniu:
			self.qiniu = QiniuStorage(cfg)

		# wav_folder="wav",mp3_folder="mp3",words_audio_folder="words_audio"
		#_url_prefix = "http://www.l2china.com/yueyu/sounds/"
		self.url_prefixs = ["http://www.yueyv.cn/sound/","http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/sound/"]
		self.wav_folder = cfg.wav_folder
		self.mp3_folder = cfg.mp3_folder
		self.words_audio_folder = cfg.words_audio_folder
		self.audio_file_url_prefix = cfg.audio_file_url_prefix


	def get_result_audio_url(self, result):
		if self.qiniu:
			url = self.qiniu.check_existance_and_get_url(result.get_filename())
			if url:
				return url
		if self.ekho:
			audio_filepath = self.ekho.get_pronounces_mp3(result)
		else:
			audio_filepath = self.get_pronounces_mp3(result.pronounce_list)
		
		if self.qiniu:
			return self.qiniu.upload_and_get_url(audio_filepath)
		else:
			name = os.path.basename(audio_filepath)	
			return self.audio_file_url_prefix + name
	
	def get_pronounces_audio_url(self, pronounce_list):
		audio_filepath = self.get_pronounces_mp3(pronounce_list)
		if self.qiniu:
			return self.qiniu.upload_and_get_url(audio_filepath)
		else:
			name = os.path.basename(audio_filepath)
			return cfg.audio_file_url_prefix + name

	def download_pronounce_file(self, pronounce):
		for url_prefix in self.url_prefixs:
			try:
				filename = pronounce + ".wav"
				url = url_prefix + filename
				urlretrieve(url,os.path.join(self.wav_folder,filename))
				self.logger.info("{0} downloaded".format(filename))
				return
			except Exception, e:
				self.logger.exception("downloaded pronounce %s from %s error" % (url_prefix, pronounce))
		raise Exception("downloaded pronounce %s error" % pronounce)
		
	
	def get_wav_pronounce(self, pronounce):
		filepath = os.path.join(self.wav_folder,pronounce+".wav")
		exist = os.path.isfile(filepath)
		try:
			if not exist:
				self.download_pronounce_file(pronounce)
			wav = AudioSegment.from_wav(filepath)
			return wav
		except Exception, e:
			self.logger.error("read {0} from disk failed".format(filepath))
			if exist:
				os.remove(filepath)
			raise e
	
	def get_mp3_pronounce(self, pronounce):
		filepath = os.path.join(self.mp3_folder,pronounce+".mp3")
		exist = os.path.isfile(filepath)
		try:
			if not exist:
				wav = self.get_wav_pronounce(pronounce)
				wav.export(filepath, format="mp3")
			mp3 = AudioSegment.from_mp3(filepath)
			return mp3
		except:
			logging.exception("get {0} pronounce mp3 error.".format(pronounce))
			return None
	
	def get_pronounces_mp3(self, pronounce_list, playback_speed=2):
		filename = ""
		for pronounce in pronounce_list:
			if pronounce:
				filename += pronounce
		if "" == filename:
			return None
		filename += ".mp3"	
		filepath = os.path.join(self.words_audio_folder,filename)
		exist = os.path.isfile(filepath)
		if exist:
			return filepath
		else:
			pronounces_mp3 = None
			first = True
		
			for pronounce in pronounce_list:
				if pronounce:
						mp3 = self.get_mp3_pronounce(pronounce)
						if mp3:
							if first:
								pronounces_mp3 = mp3
								first = False
							else:
								pronounces_mp3 = pronounces_mp3 + mp3
			if not pronounces_mp3:
				return None
			else:
				pronounces_mp3 = speedup(pronounces_mp3,playback_speed)
				# #判断如果超过60秒截断为60秒，微信允许60秒内语音
				# seconds = len(pronounces_mp3) / 1000
				# if seconds > 60:
				# 	pronounces_mp3 = pronounces_mp3[:1000*60]
				# 	logging.info("{0} play time over 60 seconds".format(filename))
				pronounces_mp3.export(filepath, format="mp3")
				return filepath


def main():
	from wechat_config import WechatConfig
	cfg = WechatConfig("Dev", "configs/env.cfg")
	fetcher = AudioFetcher(cfg)
	# pronounces = ["hou2",None,"sai1","lei6","haa1","mo2"]
	pronounces = ["hou2"]
	# filepath = fetcher.get_pronounces_mp3(pronounces)
	# print filepath
	url = fetcher.get_pronounces_audio_url(pronounces)
	print url

def main2():
	home = "D:\\cantonese_data"
	wav_folder = os.path.join(home,"wavs")
	mp3_folder = os.path.join(home,"mp3s")
	word_folder = os.path.join(home,"words")
	fetcher = AudioFetcher(wav_folder, mp3_folder,word_folder)
	pronounces = ["hou2",None,"sai1","lei6","haa1","mo2"]
	filepath = fetcher.get_pronounces_mp3(pronounces)
	print filepath
if __name__ == "__main__":
	main()
