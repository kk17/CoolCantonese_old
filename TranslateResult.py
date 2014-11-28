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

	def get_format_result(self):
		if not self.has_pronounce:
			return self.words
		return self.words + "\n\n" + self.get_words_with_pronounces()

	def get_words_with_pronounces(self):
		words = self.words.decode("utf-8")
		result = ""
		for i, w in enumerate(words):
			result += w.encode("utf-8")
			pronounce = self.pronounce_list[i]
			if pronounce:
				result += "(" + pronounce +")"
		return result

	def add(self, word, pronounce):
		self.words+= word
		self.pronounce_list.append(pronounce)
		if pronounce:
			self.has_pronounce = True

	def __str__(self):
		return self.get_format_result()

def main():
	result = TranslateResult()
	result.add("我", "ou2")
	print result.get_format_result()

if __name__ == '__main__':
	main()
