
# this file takes care of starting a new git-dropbox

import os, sys, getpass, ConfigParser

def start(path):
    write_config(path,
                 collect_data(path))
    init_the_git(path)

def init_the_git(path):
    pass

def write_config(path, info):
    (local, remote) = info

    config = ConfigParser.RawConfigParser()

    config.add_section('Local')
    [config.set('Local', k, local[k]) for k in local.keys()]

    config.add_section('Remote')
    [config.set('Remote', k, local[k]) for k in remote.keys()]

    with open(os.path.join(path, '.git-dropbox'), 'wb') as conf:
        config.write(conf)


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

    return (local, remote)

def get_input(prompt, default=None):
    if default:
        value = raw_input(' '.join([prompt, '[%s]: ' % default]))
        return default if value == '' else value
    else:
        return raw_input(prompt+': ')


def lock(path):
    if os.path.exists(os.path.join(path, '.git-dropbox')):
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
            os.remove(os.path.join(sys.argv[1], '.git-dropbox'))
    except IndexError:
        pass
