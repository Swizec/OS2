
import os

import win32file
import win32con

#path_to_watch = "." look at the current directory
def run_listener(path_to_watch,dataz):
    # Set up the bits we'll need for output
    ACTIONS = {
      1 : "Created",
      2 : "Deleted",
      3 : "Updated",
      4 : "Renamed from something",
      5 : "Renamed to something"
    }
    FILE_LIST_DIRECTORY = 0x0001
    hDir = win32file.CreateFile (
      path_to_watch,
      FILE_LIST_DIRECTORY,
      win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
      None,
      win32con.OPEN_EXISTING,
      win32con.FILE_FLAG_BACKUP_SEMANTICS,
      None
    )

    while 1:
      # Wait for a change to occur
      results = win32file.ReadDirectoryChangesW(hDir, 1024, True, win32con.FILE_NOTIFY_CHANGE_LAST_WRITE, None, None)
      #print results
      # For each change, check to see if it's updating the file we're interested in
      for action, file in results:
        full_filename = os.path.join (path_to_watch, file)
        #what to do when a file is changed
        print "File changed: %s"%full_filename
        
        # @ SWIZC
        #to se laufa ko se spremeni fajl, mas pa dictionary "dataz" z naslednjo vsebino:
        #{'Username': u'user', 'Password': u'pass', 'Location': u'D:\\Games', 'Repository': u'rep_name'}
        
        
if __name__ == '__main__':
    run_listener(".\\test")
        
        
        
        
        
        
        
        
