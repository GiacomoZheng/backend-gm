import sys

from contents import HtmlTree, MdTree, PlainTree
from index import getRaw, getHtml


def main():
	ROOT = sys.argv[0]

	if len(sys.argv) > 1:
		if sys.argv[1] == "contents":
			if len(sys.argv) > 2:
				if sys.argv[2] == "html":
					tree = HtmlTree()
				elif sys.argv[1] == "md":
					tree = MdTree()
			else:
				tree = PlainTree()
			tree.run(ROOT + "/gm", sys.argv[2])
		if sys.argv[1] == "html":
			getHtml(ROOT, sys.argv[2])
		if sys.argv[1] == "raw":
			getRaw(ROOT, sys.argv[2])

	else:
		print("help: TODO")

if __name__ == "__main__":
	main()

