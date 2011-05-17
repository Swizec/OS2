
# this file takes care of starting a new git-dropbox

import os, sys, getpass, ConfigParser
from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit, parse_timezone, ShaFile
from time import time

def start(path):
    init_the_git(write_config(path,
                              collect_data(path)))

def init_the_git(config):
    path = config.get('Local', 'path')

    repo = Repo.init(path)
    blob = Blob.from_path(os.path.join(path, '.git-dropbox.cnf'))

    tree = Tree()
    tree.add(".git-dropbox.cnf", 0100644, blob.id)

    commit = Commit()
    commit.tree = tree.id
    commit.author = config.get('Local', 'user')
    commit.committer = 'Git-dropbox'
    commit.commit_time = int(time())
    commit.author_time = os.path.getctime(os.path.join(path, '.git-dropbox.cnf'))
    commit.commit_timezone = commit.author_timezone = parse_timezone('-0200')[0]
    commit.encoding = 'UTF-8'
    commit.message = 'Initial commit'

    object_store = repo.object_store
    object_store.add_object(blob)
    object_store.add_object(tree)
    object_store.add_object(commit)

    repo.refs['refs/heads/master'] = commit.id

def write_config(path, info):
    (local, remote) = info

    config = ConfigParser.RawConfigParser()

    config.add_section('Local')
    [config.set('Local', k, local[k]) for k in local.keys()]

    config.add_section('Remote')
    [config.set('Remote', k, local[k]) for k in remote.keys()]

    with open(os.path.join(path, '.git-dropbox.cnf'), 'wb') as conf:
        config.write(conf)

    return config


def collect_data(path):
    print "Going to ask you some questions to set everything up for your git-dropboxing pleasure"

    local = {}
    local['user'] = get_input("Who are you", getpass.getuser())
    local['IP'] = get_input("What's your IP")
    local['path'] = path

    print "\nGit-dropbox needs a remote location to sync your files to."
    print "Let's configure it"

    remote = {}
    remote['user'] = get_input("Remote user", getpass.getuser())
    remote['IP'] = get_input("Remote IP", local['IP'])
    remote['path'] = get_input("Remote path", local['path'])

    print "\nThanks!\nThe two git repositories will be"
    print "local:", "%s@%s:%s" % (local['user'], local['IP'], local['path'])
    print "remote:", "%s@%s:%s" % (remote['user'], remote['IP'], remote['path'])

    print "Now just go to the other computer and run start.py there"

    return (local, remote)

def get_input(prompt, default=None):
    if default:
        value = raw_input(' '.join([prompt, '[%s]: ' % default]))
        return default if value == '' else value
    else:
        return raw_input(prompt+': ')


def lock(path):
    if os.path.exists(os.path.join(path, '.git-dropbox.cnf')):
        print "Git-dropbox is already configured for %s!\nEverything is awesome!" % path
        return False

    return True


if __name__ == '__main__':
    try:
        path = os.path.abspath(sys.argv[1])
    except IndexError:
        exit("You need to give a directory mate")


    if not os.path.exists(path):
        exit("Directory doesn't exist")

    if lock(path):
        start(path)

    try:
        if sys.argv[2] == '-ignore':
            os.remove(os.path.join(sys.argv[1], '.git-dropbox.cnf'))
    except IndexError:
        pass
