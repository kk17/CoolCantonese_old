#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TranslateResult import TranslateResult
import urllib,urllib2,bs4

class TranslationException(Exception):
	pass
		

def pasar_response_text(data):
	soup = bs4.BeautifulSoup(data, "lxml")
	texts = soup.select("div.generated_text")
	if texts and len(texts) > 0:
		result = TranslateResult()
		span_list = texts[0].select("span")
		for span in span_list:
			word = span.text.encode("utf-8")
			pronounce = span["title"].encode("utf-8")
			if "null" == pronounce:
				pronounce = None
			result.add(word,pronounce)
		return result
	raise TranslationException("暂无翻译结果")

_traslate_url = "http://www.l2china.com/yueyu/"
_text_len_limit = 100

def get_translation(text):
	if len(text.decode("utf-8")) > _text_len_limit:
		raise TranslationException("需要翻译的文本超过" + str(_text_len_limit) + "个字符")
	params = {}
	params["srctxt"] = text
	params["RadioGroup1"] = "tocan"
	data = urllib.urlencode(params)
	resp = urllib2.urlopen(_traslate_url, data).read()
	if resp:
		return pasar_response_text(resp)
	return None
	
def main():
	text = """本片讲述一个男孩从6岁到18岁的成长历程，导演理查德·林克莱特花了12"""
	print get_translation(text)

if __name__ == '__main__':
	main()

