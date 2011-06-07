
import os, sys, ConfigParser

from dulwich import client
from dulwich.repo import Repo
from dulwich.diff_tree import tree_changes
from dulwich.objects import Tree

def fetch(root):
    repo = Repo(root)

    (remote, path) = client.get_transport_and_path('git@github.com:Swizec/OS2.git')

    def progress(arg):
        print ".", arg

    remotes = remote.fetch(path, repo, progress=progress)
    #print remote.fetch_pack(path, progress=progress)

    print remotes

    #local_tree = repo.open_index().commit(repo.object_store)
    remote_tree = repo.commit(remotes['HEAD']).tree
    #print Tree(remotes['refs/heads/master'])

    #for change in tree_changes(repo.object_store, local_tree, remote_tree):
    #    print change

    repo.do_commit("a merge",
                   committer="Git-dropbox",
                   tree=remote_tree)

if __name__ == '__main__':
    remote = client.get_transport_and_path('git@github.com:Swizec/OS2.git')

    try:
        path = os.path.abspath(sys.argv[1])
    except IndexError:
        exit("No path")

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.split(path)[0], '.git-dropbox.cnf'))

    fetch(path)
