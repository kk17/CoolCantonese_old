#!/usr/bin/env python
# -*- coding:utf-8 -*-

class TranslateResult(object):
	"""docstring for TranslateResult"""
	def __init__(self, words = "", pronounce_list = None):
		super(TranslateResult, self).__init__()
		self.words = words
		self.pronounce_list = pronounce_list
		if self.pronounce_list == None:
			self.pronounce_list = []
		self.has_pronounce = False

	def pretty(self):
		if not self.has_pronounce:
			return self.words
		return self.words + "\n\n" + self.get_words_with_pronounces()

	def get_words_with_pronounces(self):
		words = self.words
		result = ""
		for i, w in enumerate(words):
			result += w
			pronounce = self.pronounce_list[i]
			if pronounce:
				result += "(" + pronounce +")"
		return result

	def add(self, word, pronounce):
		self.words+= word
		self.pronounce_list.append(pronounce)
		if pronounce:
			self.has_pronounce = True

	def get_filename(self, ext=".mp3"):
		filename = ""
		for pronounce in self.pronounce_list:
			if pronounce:
				filename += pronounce
		if "" == filename:
			return None
		filename += ext
		return filename	

	def __str__(self):
		return self.pretty().encode("utf-8")

def main():
	result = TranslateResult()
	result.add(u"我", "ou2")
	print result

if __name__ == '__main__':
	main()
