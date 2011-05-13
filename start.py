
# this file takes care of starting a new git-dropbox

import os, sys, getpass

def start(path):
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

    settings = {'local': local,
                'remote': [remote]}

    print "\nThanks!\nThe two git repositories will be"
    print "local:", "%s@%s:%s" % (local['user'], local['IP'], local['path'])
    print "remote:", "%s@%s:%s" % (remote['user'], remote['IP'], remote['path'])


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

    open(os.path.join(path, '.git-dropbox'), 'w').close()
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
