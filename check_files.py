
# checking for changes in a file
# store last known metadata
# traverse dir
# - if file changed after last known change
#   - compare hash to last hash
#   - if hash is different then make a commit and push
#
# check if it's possible to be notified of file changes
#
# what happens when there are conflicts?
# what about branches?
# how to present all of this to the user?

# how to install everything? Mkae sure it works?
# needs git
# git is weird on windows ...

import sys, hashlib, os
import cPickle as pickle

from get_list import files

def checksum(path):
    hash = hashlib.sha512()

    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(128*hash.block_size), ''):
            hash.update(chunk)
    return hash.hexdigest()

def load():
    try:
        return pickle.load(open('meta.p', 'rb'))
    except IOError:
        return {}

def store(changed, old):
    data = old
    
    for f in changed:
        data[f] = {'time': os.path.getmtime(f),
                   'checksum': checksum(f)}
        
    pickle.dump(data, open('meta.p', 'wb'))

def changed(dir):
    old_meta = load()

    suspects = []

    data = files(dir)
    for path in data.keys():
        try:
            if data[path] != old_meta[path]['time']:
                suspects.append(path)
        except KeyError:
            suspects.append(path)

    def check(path):
        try:
            print path
            return checksum(path) != old_meta[path]['checksum']
        except KeyError:
            return True

    suspects = filter(check, suspects)

    store(suspects, old_meta)

    return suspects

if __name__ == '__main__':
    try:
        print changed(sys.argv[1])
    except IndexError:
        print "You need to give a directory mate"
