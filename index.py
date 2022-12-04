#! python3
# coding:utf-8
from __init__ import *

from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments_gm import GMLexer

def getRaw(root, title : str):
	try:
		with open(analyze(str(title), root), "r") as handle:
			print(handle.read().replace("\t", "    ")) # TODO)
	except NoSuchFile as e:
		print(str(e))

def getHtml(root, title : str):
	try:
		path_raw = analyze(str(title), root)
		path_src = root + "/src_cache/" + str(title) + ".html"
		if (not os.path.isfile(path_src)) or (os.path.getmtime(path_src) < os.path.getmtime(path_raw)):
			with open(path_raw, "r") as handle:
				raw = handle.read().replace("\t", "    ") # TODO
			with open(path_src, "w") as handle:
				handle.write(highlight(raw, GMLexer(), HtmlFormatter(linenos="table")))
		with open(path_src, "r") as handle:
			print(handle.read())
	except NoSuchFile as e:
		print(str(e))