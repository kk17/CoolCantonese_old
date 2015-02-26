#!/usr/bin/env python
# -*- coding:utf-8 -*-	

import urllib2,os.path

def to_utf8(in_str):
	return in_str.encode("utf-8")

def to_unicode(in_str):
	return in_str.decode("utf-8")

class RedirectHandler(urllib2.HTTPRedirectHandler):
	def http_error_301(self, req, fp, code, msg, headers):  
		result = urllib2.HTTPRedirectHandler.http_error_301( 
			self, req, fp, code, msg, headers)              
		result.status = code                                 
		raise Exception("Permanent Redirect: %s" % 301)

	def http_error_302(self, req, fp, code, msg, headers):
		result = urllib2.HTTPRedirectHandler.http_error_302(
			self, req, fp, code, msg, headers)              
		result.status = code                                
		raise Exception("Temporary Redirect: %s" % 302)

_opener = urllib2.build_opener(RedirectHandler)

def urlretrieve(url,filepath):
	resp = _opener.open(url)
	with open(filepath,"wb") as f:
		data = resp.read()
		if len(data) > 0:
			f.write(data)
		else:
			raise Exception("File size is zero")

def check_create_dir(directory):
	if not os.path.exists(directory):
   		os.makedirs(directory)
