import os

def transparent(s):
	return s.startswith("_") and s.endswith("_")

def eprint(s):
	print("[DEBUG]:", s)

class Unimplement(Exception):
	def __str__(self):
		return f"functionality unimplement yet"

class NoSuchFile(Exception):
	def __init__(self, name):
		self.name = name
		super().__init__("no file named " + str(self.name))

def analyze(name : str, directory : str, root = ".", file = ".gm", ext = ".gm") -> str:
	"""
	"gm.h.group" ⇒ "./gm/h/_/group/.gm"
	"""

	path = directory
	locations = name.split(".")
	location = locations[0]
	# eprint("location:", location)

	if os.path.isfile(os.path.join(path, location + ext)):
		# + I guess this functionality is wrong, only work for theorem
		if len(locations) > 1:
			raise Unimplement()
		return os.path.join(path, location + ext)

	if os.path.isdir(os.path.join(path, location)):
		return analyze(".".join(locations[1:]), os.path.join(path, location), root)

	for item in filter(transparent, [filepath for filepath in os.listdir(directory)]):
		try:
			return analyze(name, os.path.join(path, item), root)
		except Unimplement:
			print("Unimplement")
			exit()
		except NoSuchFile:
			pass
		except Exception as e:
			raise Exception(e)

	raise NoSuchFile(name)
