#!/usr/bin/python
# -*- coding: utf-8 -*-
# Source: https://github.com/kddeisz/tree/blob/master/tree.py

import os

from __init__ import *

class Flags:
	def __init__(self):
		self.others = False
		self.gm = False
		self.theorem = False
		self.dir = False
		self.trans = False

	def register(self, absolute, item):
		if item.startswith("."):
			self.others = True
		elif os.path.isdir(absolute):
			self.dir = True
			if os.path.isfile(os.path.join(absolute, ".gm")):					
				self.gm = True
			elif transparent(item):
				self.trans = True
			else:
				self.others = True
		else:
			if item == "theorem.gm":
				self.theorem = True
			elif item.endswith(".gm"):
				self.gm = True
			else:
				self.others = True

def sorted(ls):
	def lstrip(s, prefix = "_"):
		if s.startswith(prefix):
			return lstrip(s[len(prefix):], prefix)
		else:
			return s

	ls.sort(key=lambda s: lstrip(s, "_"))
	return ls

class Tree:
	""" trait """
	def __init__(self):
		self.count = 0
		self.theorem_count = 0

	def summary(self):
		return str(self.count) + " concepts, " + str(self.theorem_count) + " theorem files"
	
	def header(self): pass
	def prefix_last(self): pass
	def prefix_mid(self): pass
	def prefix_tabs(self, tabs): pass
	def flags_gm(self, path, item): pass
	def flags_theorem(self, path, item): pass
	def flags_trans(self, item): pass
	def surfix(self): 
		print() # newline

	def walk(self, directory, root, tabs = 0):
		filepaths = sorted([filepath for filepath in os.listdir(directory)])

		for index in range(len(filepaths)):
			flags = Flags()

			item = filepaths[index]
			absolute = os.path.join(directory, item)
			path = "." + absolute[len(root):]
			# print("path: ", path)

			flags.register(absolute, item)
			if flags.others:
				continue
			
			self.prefix_tabs(tabs)

			if index == len(filepaths) - 1:
				self.prefix_last()
			else:
				self.prefix_mid()

			if flags.gm:
				self.flags_gm(path, item)
				self.count += 1
			
			if flags.theorem:
				self.flags_theorem(path, item)
				self.theorem_count += 1
			
			if flags.trans:
				self.flags_trans(item)
				# self.count += 1
			
			self.surfix()

			if flags.dir:
				self.walk(absolute, root, tabs + 1)

	def run(self, root, title : str = ""):
		self.header()
		try:
			path = analyze(title, root)
		except NoSuchFile as e:
			print(e)
			exit()

		self.walk(root, root + path)
		print("\n" + self.summary())

class PlainTree(Tree):
	def header(self):
		print("gm")
	def prefix_last(self):
		print("└── ", end="") # none
	def prefix_mid(self):
		print("├── ", end="") # none
	def prefix_tabs(self, tabs):
		print(tabs * "    ", end="") # none # md
	def flags_gm(self, path, item):
		print(item, end="") # none
	def flags_theorem(self, path, item):
		print(item, end="") # none
	def flags_trans(self, item):
		print(item, end="") # none # md

class MdTree(Tree):
	def header(self):
		print("gm")
	def prefix_last(self):
		print("* ", end="") # md
	def prefix_mid(self):
		print("* ", end="") # md
	def prefix_tabs(self, tabs):
		print(tabs * "    ", end="") # none # md
	def flags_gm(self, path, item):
		print("[" + item + "](" + os.path.join(path, ".gm") + ")", end="") # md
	def flags_theorem(self, path, item):
		print("[" + item + "](" + path + ")", end="") # md
	def flags_trans(self, item):
		print(item, end="") # none # md

def analyze_inv(path, root = "https://doc.gm-lang.org/src/", ext : str = ".gm"):
	""" get web from path """
	web = "gm"
	ls = path.split("/")
	# print("")
	for item in ls[1:]: # remove the "." position
		if transparent(item):
			continue
		if item.endswith(ext):
			item = item[:-len(ext)]
			if item == "":
				continue
		web += "." + item
	return root + web

class HtmlTree(Tree):
	def header(self):
		print("<p> gm </p>")
	def prefix_last(self):
		print("└ ", end="") # html
	def prefix_mid(self):
		print("├ ", end="") # html
	def prefix_tabs(self, tabs):
		print("<p style=\"text-indent: " + str(tabs * 40) + "px\">", end="") # html
	def flags_gm(self, path, item):
		print("<a href=" + analyze_inv(os.path.join(path, ".gm")) + "> " + item + " </a>", end="") # html
	def flags_theorem(self, path, item):
		print("<a href=" + analyze_inv(path) + "> " + item + " </a>", end="") # html
	def flags_trans(self, item):
		print(item, end="") # html
	def surfix(self):
		print("</p>") # html

