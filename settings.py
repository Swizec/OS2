import pickle

def get_replist():
    try:
        f = open(".\\repositories.dataz",'rb')
    except (IOError):
        f = open(".\\repositories.dataz",'wb')
    try:
        replist = pickle.load(f)
    except Exception:
        replist = {}
    f.close()
    return replist
    
def put_replist(replist):
    f = open(".\\repositories.dataz",'wb')
    pickle.dump(replist, f)
    f.close()

def append_rep(rep):
    replist = get_replist()
    replist[rep[0]] = {'Username': rep[1], 'Password': rep[2], 'Location': rep[3]}
    put_replist(replist)
    