#!/usr/bin/env python
# -*- coding:utf-8 -*-

# class TextMenu(object):
# 	"""docstring for TextMenu"""
# 	def __init__(self, robot):
# 		super(TextMenu, self).__init__()
# 		self.robot = robot

text_menu = """
* ：收听电台
# ：获得上一条翻译的语音
？：获得帮助
直接输入文字获得文字翻译
直接输入#+文字获得文字翻译
"""
@robot.text("?")