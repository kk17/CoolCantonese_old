#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os.path,os,logging,sh
from pydub import AudioSegment

class Ekho(object):
	logger = logging.getLogger("wechat")

	def __init__(self,words_audio_folder="words_audio"):
		super(Ekho, self).__init__()
		self.words_audio_folder = words_audio_folder
		
	def export_pronounces_wav(self, wavfilepath, words):
		return sh.ekho("-v", "Cantonese", "-o", wavfilepath, words)

	def export_pronounces_mp3(self, mpefilepath, words):
		return sh.ekho("-v", "Cantonese", "-t", "mp3", "-o", mpefilepath, words)
	
	def get_pronounces_mp3(self, result, playback_speed=None):
		mp3_filename = result.get_filename()
		if mp3_filename is None:
			return None	
		mp3filepath = os.path.join(self.words_audio_folder,mp3_filename)
		mp3_exist = os.path.isfile(mp3filepath)
		if mp3_exist:
			return mp3filepath
		else:
			self.export_pronounces_mp3(mp3filepath, result.words)
			if playback_speed:
				mp3Audio = AudioSegment.from_mp3(mp3filepath)
				mp3Audio = speedup(mp3Audio,playback_speed)
				mp3Audio.export(mp3filepath, format="mp3")
			return mp3filepath

def main():
	ekho = Ekho(".")
	r = ekho.export_pronounces_mp3("test.mp3",u"我喜欢你")
	print r

if __name__ == '__main__':
	main()
