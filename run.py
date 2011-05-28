
import wx
import os
import sys_tray_icon as sti
import folder_select as fs
import settings as st
import threads as thr
from input import TextFrame as tf

try:
    import winxpgui as win32gui
except ImportError:
    import win32gui

#---------------- Random ----------------------------------------



#----------------  Main class  ----------------------------------------

class Run():
    
    def __init__(self):
        self.r = 0
        self.d = 'Snake.ico'
        self.hover_text = "Git Dropbox"
    #random testing function that i will remove later. most likely.
    def test(self): 
        #print st.get_replist()
        print 'trol'
    #opens the windows explorer browser in a directory defined by 'dir'
    def open_folder(self,sysTrayIcon,dir):
        os.startfile(dir)
    #shamelessly kills and then necros a new clone of our system tray thingy.
    #kind of a refresh
    def restart(self,sysTrayIcon,dir):
        self.r = 1
        self.tray.execute_menu_option('quit')
    #just catches the data from another object
    def insert(self,data):
        self.data = data
    #gatherz data for new repository
    def new(self,sysTrayIcon,a):
        #get repository name, username and password
        app = wx.PySimpleApp()
        frame = tf()
        frame.callback = self.insert
        frame.Show()
        app.MainLoop()
        #get directory
        dir = fs.get_folder()
        #put both together
        self.data.append(dir)
        #add the data to the config file
        st.append_rep(self.data)
        self.restart(None,None)
    #deletes a repository
    def delete_rep(self,sysTrayIcon,delkey):
        dataz = st.get_replist()
        app = wx.PySimpleApp()
        retCode = wx.MessageBox("Are you sure you want to delete the repository?", "Delete",wx.YES_NO | wx.ICON_QUESTION)
        if retCode == 2:
            del dataz[delkey]
            st.put_replist(dataz)
            self.restart(None,None)
    #gets the repository dataz :D
    def get_dataz(self):
        #read the Repository dataz
        self.dataz = st.get_replist()
        #setup the system icon menu
        #submenu with repositories list
        repositories = ()
        for key in self.dataz.keys():
            repositories = repositories + ((key+" - "+self.dataz[key]['Location'], None, self.dataz[key]['Location'], self.open_folder),)
        #submenu with delete repositories list
        #gottamake new one to define a delete function to each
        delrep = ()
        for key in self.dataz.keys():
            delrep = delrep + ((key, None, key, self.delete_rep),)
        #the right-click menu
        menu_options = (('Repositories', None, None, repositories),
                        ('Delete', None, None, delrep),
                        ('New', None, None, self.new),
                        ('Restart', None, None, self.restart)
                        )
        return menu_options
    #... gets the party started?
    def start(self):
        
        def bye(sysTrayIcon): pass
        
        #starts the system tray icon thingy and runs it again if the 'r' flag is set,
        #to allow for tray resets, to refresh new content
        while True:
            #reads the file for which threads to run, and generates the menu contents
            menu_options = self.get_dataz()
            
            #starting the repository change listening threads
            threadz = thr.ThreadMaster()
            threadz.start(self.dataz)
            
            self.r = 0
            self.tray = sti.SysTrayIcon()
            self.tray.start(self.d, self.hover_text, menu_options, on_quit=bye, default_menu_index=1)
            
            #stopping the repository change listening threads
            threadz.stop()
            if self.r == 0:
                break
        
        
        
#----------------  MAIN  ----------------------------------------

if __name__ == '__main__':
    r = Run()
    r.start()

