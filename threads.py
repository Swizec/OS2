
from threading import *
import file_changed as fc
import os
import win32file
import win32con

#---------------- Thread ----------------------------------------

class FileListener(Thread):
    
    def __init__(self,directory,dataz):
        Thread.__init__(self)
        self.directory = directory
        self.dataz = dataz
        # sets repeat flag to true
        self.r = 1
        # Set up the bits we'll need for output
        ACTIONS = {
          1 : "Created",
          2 : "Deleted",
          3 : "Updated",
          4 : "Renamed from something",
          5 : "Renamed to something"
        }
        FILE_LIST_DIRECTORY = 0x0001
        self.hDir = win32file.CreateFile (
          self.directory,
          FILE_LIST_DIRECTORY,
          win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
          None,
          win32con.OPEN_EXISTING,
          win32con.FILE_FLAG_BACKUP_SEMANTICS,
          None
        )
        
    def run(self):
        taction = 0
        tfile = ''
        while 1:
          # this ends thread when r is set to 0... i think
          if self.r == 0:
            break
          # Wait for a change to occur
          results = win32file.ReadDirectoryChangesW (
            self.hDir,
            1024,
            True,
            win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
             win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
             win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
             win32con.FILE_NOTIFY_CHANGE_SIZE |
             win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
             win32con.FILE_NOTIFY_CHANGE_SECURITY,
            None,
            None
          )

          # this ends thread when r is set to 0... i think
          if self.r == 0:
            break
          # For each change, check to see if it's updating the file we're interested in
          for action, file in results:
            if (action, file) != (taction, tfile):
                full_filename = os.path.join (self.directory, file)
                fc.file_changed(full_filename, action, self.dataz)
                taction = action
                tfile = file
            else:
                taction = 0
                tfile = ''
        #print "thread stopped!"
    
    def stop(self):
        self.r = 0
        
#---------------- Methods ---------------------------------------

class ThreadMaster():
    # starting threads
    def start(self, dataz):
        #defining empty list of threads
        self.threads = []
        #running threads for each repository
        for key in dataz.keys():
            #print dataz[key]
            dataz[key]['Repository'] = key
            thread=FileListener(dataz[key]['Location'],dataz[key])
            thread.start()
            self.threads.append(thread)
            #print "Listening to "+dataz[key]['Repository']+" located in "+dataz[key]['Location']

            
    #stoping threads
    def stop(self):
        for thread in self.threads:
            if thread.isAlive():
                #sets the loop flag in the thread to false so the thread will stop eventually.
                thread.stop()
                try:#apparently this is how youre suppolsed to kill a thread in python but it doesnt seem to work..
                    thread._Thread__stop()
                except:
                    print(str(thread.getName()) + ' could not be terminated')
                
                
    #restarts the threads.
    def restart(self, dataz):
        stop()
        start(dataz)
                    
                