#!/usr/bin/env python
# -*- coding: utf-8 -*-

from TranslateResult import TranslateResult
import urllib,urllib2,bs4,json

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
_text_len_limit = 1000

def get_translation_old(text):
	uni = type(text) == unicode
	if uni:
		txt_len = len(text)
		utf8_txt = text.encode('utf-8')
	else:
		txt_len = len(text.decode('utf-8'))
		utf8_txt = text
	if txt_len > _text_len_limit:
		raise TranslationException("需要翻译的文本超过" + str(_text_len_limit) + "个字符")
	params = {}
	params["srctxt"] = utf8_txt
	params["RadioGroup1"] = "tocan"
	data = urllib.urlencode(params)
	headers = {"Referer":_traslate_url}
	req = urllib2.Request(_traslate_url, data, headers)
	resp = urllib2.urlopen(req).read()
	if resp:
		result =  pasar_response_text(resp)
		return result
	return None

# from	源语言语种：语言代码或auto	仅支持特定的语言组合，下面会单独进行说明
# to	目标语言语种：语言代码或auto	仅支持特定的语言组合，下面会单独进行说明
# client_id	开发者在百度开发者中心注册得到的授权API key	请阅读如何获取api keyhttp://developer.baidu.com/console#app/project
# q	待翻译内容	该字段必须为UTF-8编码，并且以GET方式调用API时，需要进行urlencode编码。
_baidu_translate_api = "http://openapi.baidu.com/public/2.0/bmt/translate"
_baidu_translate_client_id = "foAIGL40ZOCv2lrZhnRQ1QCf"
def get_translation(text):
	uni = type(text) == unicode
	if uni:
		txt_len = len(text)
		utf8_txt = text.encode('utf-8')
	else:
		txt_len = len(text.decode('utf-8'))
		utf8_txt = text
	if txt_len > _text_len_limit:
		raise TranslationException("需要翻译的文本超过" + str(_text_len_limit) + "个字符")
	params = {}
	params["from"] = "zh"
	params["to"] = "yue"
	params["client_id"] = _baidu_translate_client_id
	params["q"] = utf8_txt

	data = urllib.urlencode(params)
	headers = {"Referer":_baidu_translate_api}
	req = urllib2.Request(_baidu_translate_api, data, headers)
	resp = urllib2.urlopen(req).read()
	if resp:
		try:
			node = json.loads(resp)
		except Exception, e:
			print resp
			raise e
		trans_result = node["trans_result"]
		result_text = ""
		for t in trans_result:
			dst = t["dst"]
			if type(dst)==unicode:
				dst = dst.encode("utf-8")
				# print dst
			result_text = result_text + "\n" + dst 
		return result_text[1:]
	return None
	
def main():
	text = """本片讲述一个男孩从6岁到18岁的成长历程，导演理查德·林克莱特花了12
	ni无法理解，真好"""
	print get_translation(text)

if __name__ == '__main__':
	main()

