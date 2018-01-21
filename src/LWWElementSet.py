#!/usr/bin/env python3
import unittest
from time import time
from random import randint



class LWWElementSetPrimitive(object):
	def __init__(self):
		self.add_ = 	{}
		self.remove_ = {}

	def add(self, payload, ts=None):
		if ts == None:
			ts = time()
		self.add_[payload] = ts
		return 
	def remove(self, payload, ts=None):
		if ts == None:
			ts = time()
		self.remove_[payload] = ts
		return
	def value(self):
		return set(e for (e, ts) in self.add_.items()
					if ts >= self.remove_.get(e, 0)
				)		 

	def __repr__(self):
		return self.value

	def __str__(self):
		return "Add list: %s, Remove List: %s" % (str(self.add_), str(self.remove_))

class LWWElementSetDictionary(dict):
	def __init__(self, *args, **kwargs):
		self.data = LWWElementSetPrimitive()

	def create(self):
		payload = {k:v for (k, v) in self.data.value()}
		return payload

	def __getitem__(self, key):
		payload = self.create()
		return payload[key]

	def __setitem__(self, key, val):
		self.data.add((key, val))

	def __delitem__(self, key):
		payload = self.create()
		val = payload[key]
		self.data.remove((key, val))

	def __repr__(self):
		return self.create()

	def __eq__(self, other):
		return self.create() == other

	def __str__(self):
		return str(self.create())


class TestLWWElementSet(unittest.TestCase):
	def testSimpleLWWElementSet(self):
		a = ["Hello", "World"]
		r = ["World"]
		s = LWWElementSetPrimitive()
		s.add(a[0])
		s.add(a[1])
		s.remove(r[0])
		s.add(a[1])
		self.assertEqual(s.value(), set(["Hello", "World"]))
		return




class TestLWWElementSetDictionary(unittest.TestCase):
	def testCopyData(self):
		ld = LWWElementSetDictionary()
		ld['a'] = 'a'
		ld['b'] = 'b'
		ld['c'] = 'c'
		del ld['b']
		self.assertEqual(ld,{'a': 'a', 'c': 'c'})

	def testComplexDict(self):
		ld = LWWElementSetDictionary()
		add1 = ['1', '2', '3', '4']
		rm1 = ['2', '3']
		add2 = ['3']
		for a in add1:
			ld[a] = a
		for r in rm1:
			del ld[r]
		for a in add2:
			ld[a] = a
		self.assertEqual(ld, {'1':'1', '3':'3', '4': '4'})
if __name__ == '__main__':
	unittest.main()