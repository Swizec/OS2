
import os, sys, ConfigParser

from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit, parse_timezone, ShaFile
from time import time

def commit(root, path, author):
    repo = Repo(root)

    repo.stage([path])

    return repo.do_commit('Automated commit',
                          committer='Git-dropbox',
                          author=author,
                          commit_timestamp=int(time()),
                          commit_timezone=parse_timezone('-0200')[0],
                          author_timestamp=os.path.getctime(os.path.join(root, path)),
                          encoding='UTF-8')

if __name__ == '__main__':
    try:
        path = os.path.abspath(sys.argv[1])
    except IndexError:
        exit("No path")

    config = ConfigParser.RawConfigParser()
    config.read(os.path.join(os.path.split(path)[0], '.git-dropbox.cnf'))

    commit(os.path.split(path)[0],
           os.path.split(path)[1],
           config.get('Local', 'user'))
