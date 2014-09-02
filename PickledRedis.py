#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pickle
from redis import StrictRedis


class PickledRedis(StrictRedis):
	def get(self, name):
		pickled_value = super(PickledRedis, self).get(name)
		if pickled_value is None:
				return None
		return pickle.loads(pickled_value)

	def set(self, name, value, ex=None, px=None, nx=False, xx=False):
		return super(PickledRedis, self).set(name, pickle.dumps(value), ex, px, nx, xx)

def main():
	r = PickledRedis()
	key = "test"
	value = {"a":10,"b":"dfdfd","c":[1.3]}
	print value
	r.set(key,value)
	print r.get(key)
	r.delete(key)

if __name__ == "__main__":
	main()


