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

	def get_format_result(self):
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

	def __str__(self):
		return self.get_format_result()

def main():
	result = TranslateResult()
	result.add("我", "ou2")
	print result

if __name__ == '__main__':
	main()
