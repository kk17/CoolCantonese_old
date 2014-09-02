#!/usr/bin/env python
# -*- coding:utf-8 -*-

import urllib,os.path,os,logging
from pydub import AudioSegment
import ConfigParser

class AudioFetcher(object):
	logger = logging.getLogger("wechat")
	
	def __init__(self,wav_folder="wav",mp3_folder="mp3",words_audio_folder="words_audio"):
		super(AudioFetcher, self).__init__()
		#_url_prefix = "http://www.l2china.com/yueyu/sounds/"
		self.url_prefix = "http://humanum.arts.cuhk.edu.hk/Lexis/lexi-can/sound/"
		self.wav_folder = wav_folder
		self.mp3_folder = mp3_folder
		self.words_audio_folder = words_audio_folder
		
	def download_pronounce_file(self, pronounce):
		filename = pronounce + ".wav"
		url = self.url_prefix + filename
		urllib.urlretrieve(url,os.path.join(self.wav_folder,filename))
		self.logger.info("{0} downloaded".format(filename))
	
	def get_wav_pronounce(self, pronounce):
		filepath = os.path.join(self.wav_folder,pronounce+".wav")
		exist = os.path.isfile(filepath)
		if not exist:
			self.download_pronounce_file(pronounce)
		try:
			wav = AudioSegment.from_wav(filepath)
			return wav
		except Exception, e:
			self.logger.error("read {0} from disk failed".format(filepath))
			os.remove(filepath)
			raise e
	
	def get_mp3_pronounce(self, pronounce):
		filepath = os.path.join(self.mp3_folder,pronounce+".mp3")
		exist = os.path.isfile(filepath)
		if not exist:
			wav = self.get_wav_pronounce(pronounce)
			wav.export(filepath, format="mp3")
		mp3 = AudioSegment.from_mp3(filepath)
		return mp3
	
	def get_pronounces_mp3(self, pronounce_list):
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
						if first:
							pronounces_mp3 = mp3
							first = False
						else:
							pronounces_mp3 = pronounces_mp3 + mp3
			if not pronounces_mp3:
				return None
			else:
				pronounces_mp3.export(filepath,format="mp3")
				return filepath


def main():
	fetcher = AudioFetcher()
	pronounces = ["hou2",None,"sai1","lei6","haa1","mo2"]
	filepath = fetcher.get_pronounces_mp3(pronounces)
	print filepath

if __name__ == "__main__":
	main()
