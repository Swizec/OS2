import os

# kle namest tega chdira pac nastavis ta os. na zeljen direktorij,
# in pol dobis v l-ju dictionary full pathov pa last modified cajtov
os.chdir('test')

cwd = os.getcwd()
l = {}

def izpis(bla,d,flst):
	for f in flst:
		fullf = os.path.join(d,f)
		if os.path.isfile(fullf):
			l[fullf]=os.path.getmtime(fullf)

os.path.walk(cwd,izpis,None)

print l