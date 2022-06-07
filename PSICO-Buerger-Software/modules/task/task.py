import psutil
import time
#import pandas as pd

class Task():
    def __init__(self, queryConnector, blackListTasks):
        self.alive = 1
        self.queryConnector = queryConnector
        self.blackListTasks = blackListTasks
    
    def getTasks(self):
        while 1:
            processes = []
            # the list the contain all process dictionaries
            for process in psutil.process_iter():
                # get all process info in one shot
                with process.oneshot():
                    # get the process id
                    pid = process.pid
                    if pid == 0:
                        # System Idle Process for Windows NT, useless to see anyways
                        continue
                    # get the name of the file executed
                    name = process.name()
                    try:
                        username = process.username()
                        if username == "NT AUTHORITY\SYSTEM":
                            continue
                    except psutil.AccessDenied:
                        continue
                    
                processes.append({
                    'pid': pid, 'name': name,  
                })
            yield processes
            time.sleep(5 * 60)

    def killTask(self):
        for process in psutil.process_iter():
            if any(procstr in process.name() for procstr in\
                self.blackListTasks): #liste zu vervollständigen
                    #print(f'Killing {process.name()}')
                    process.kill()

    def main(self):
        tasksGenerator = self.getTasks()
        for tasks in tasksGenerator:
            self.queryConnector.addToTaskLog(tasks)
            time.sleep(2)
            self.killTask()