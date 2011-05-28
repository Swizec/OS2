
from threading import Thread
import file_changed as fc


#---------------- Thread ----------------------------------------

class FileListener(Thread):
    
    def __init__(self,directory,dataz):
        Thread.__init__(self)
        self.directory = directory
        self.dataz = dataz
    
    def run(self):
        fc.run_listener(self.directory,self.dataz)

        
#---------------- Methods ---------------------------------------

class ThreadMaster():
    #defining empty list of threads
    def start(self, dataz):
        self.threads = []
        #running threads for each repository
        for key in dataz.keys():
            #print dataz[key]
            dataz[key]['Repository'] = key
            thread=FileListener(dataz[key]['Location'],dataz[key])
            thread.start()
            self.threads.append(thread)
            print "Listening to "+dataz[key]['Repository']+" located in "+dataz[key]['Location']

            
    #stoping threads
    def stop(self):
        for thread in self.threads:
            if thread.isAlive():
                try:
                    #magical unicorns murder the thread with sugary goodness
                    thread._Thread__stop()
                    #print "stopping threads"
                except:
                    print(str(thread.getName()) + ' could not be terminated')


    def restart(self, dataz):
        stop()
        start(dataz)
                    
                