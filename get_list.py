import os

def files(dir):
	l = {}

	def izpis(bla,d,flst):
		for f in flst:
			fullf = os.path.join(d,f)
			if os.path.isfile(fullf):
				l[fullf]=os.path.getmtime(fullf)

	os.path.walk(dir, izpis, None)

	return l
