#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,os.path,os,logging
from pydub import AudioSegment
from pydub.effects import speedup
from util import urlretrieve

class AudioFetcher(object):
	logger = logging.getLogger("wechat")

	def __init__(self,wav_folder="wav",mp3_folder="mp3",words_audio_folder="words_audio"):
		super(AudioFetcher, self).__init__()
		#_url_prefix = "http://www.l2china.com/yueyu/sounds/"
		self.url_prefixs = ["http://www.yueyv.cn/sound/","http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/sound/"]
		self.wav_folder = wav_folder
		self.mp3_folder = mp3_folder
		self.words_audio_folder = words_audio_folder
		
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
	fetcher = AudioFetcher()
	pronounces = ["hou2",None,"sai1","lei6","haa1","mo2"]
	filepath = fetcher.get_pronounces_mp3(pronounces)
	print filepath

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
	main2()
