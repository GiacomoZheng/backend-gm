# please cd to `gm` and run this file
import os
if not os.getcwd().endswith("gm"): raise Exception("invalid location")

import sys
lis = sys.argv[1]
print("the printed aim is: " + lis)
with open(lis, "r", encoding = 'utf8') as file:
	text = file.read()

x = []
for item in text.split("\n"):
	# print(item)
	if not item == '':
		y = item.split("\t")
		# print(y)
		x.append((int(y[0]), y[1]))

x.sort(key=(lambda i: i[0]))
x.reverse()

with open(lis, "w", encoding = "utf8") as file:
	for item in x:
		file.write(str(item[0]) + "\t" + item[1] + "\n")