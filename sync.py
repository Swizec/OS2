
import os, sys, ConfigParser

from dulwich import client
from dulwich.repo import Repo

def fetch(root):
    repo = Repo(root)

    (remote, path) = client.get_transport_and_path('git@github.com:Swizec/OS2.git')

    def progress(arg):
        print ".", arg

    print remote

    remote.fetch(path, repo, progress=progress)

if __name__ == '__main__':
    remote = client.get_transport_and_path('git@github.com:Swizec/OS2.git')

    try:
        path = os.path.abspath(sys.argv[1])
    except IndexError:
        exit("No path")

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.split(path)[0], '.git-dropbox.cnf'))

    fetch(path)
