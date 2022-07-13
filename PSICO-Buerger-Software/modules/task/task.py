import psutil
import time
#import pandas as pd

"""
AUTHOR: MAHMOUD ALMASRI, PHILIPP WENDEL
"""

class Task():
    def __init__(self, queryConnector, blackListTasks):
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

    def killTask(self):
        for process in psutil.process_iter():
            if any(procstr in process.name() for procstr in\
                self.blackListTasks):
                    self.queryConnector.updateSCS(-5)
                    self.queryConnector.saveBadHabits(f'Unerwuenschtes Programm erkannt: {process.name()} ')
                    try:    
                        process.kill()
                    except psutil.NoSuchProcess:
                        pass

    def killEverything(self):
        while 1:
            time.sleep(3)
            self.killTask()

    def main(self):
        tasksGenerator = self.getTasks()
        for tasks in tasksGenerator:
            self.queryConnector.addToTaskLog(tasks)
            time.sleep(1)
            self.killTask()
            time.sleep(5 * 60)
