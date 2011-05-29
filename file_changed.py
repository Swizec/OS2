
# this is called after a thread detects a file change
def file_changed(full_filename, action, dataz):
        #what to do when a file is changed
        #print action
        #print "File changed: %s"%full_filename
        pass
        #
        # @ SWIZC
        #to se laufa ko se spremeni fajl, mas pa dictionary "dataz" z naslednjo vsebino:
        #{'Username': u'user', 'Password': u'pass', 'Location': u'D:\\Games', 'Repository': u'rep_name'}
        #
        #action spremenljivka (tipa int) ti pove kaj je bil action izveden nad fajlom. moznosti so sledece:
        #  1 : "Created"
        #  2 : "Deleted"
        #  3 : "Updated"
        #  4 : "Renamed from something"
        #  5 : "Renamed to something"
        #
        # pazi: 
        # - ob spremembi imena fajla se tole klice trikrat; enkrat 4 za star fajl, pol pa 5 za tanovga, pol pa se 3 za tanovga >_< deal with it, men se neda :P
        #
 