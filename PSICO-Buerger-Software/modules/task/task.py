import psutil
#import pandas as pd

class Task():
    def __init__(self, queryController):
        self.processes = []
    
    def getTasks(self):
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
                
            self.processes.append({
                'pid': pid, 'name': name,  
            })

        return self.processes

    # def construct_dataframe(processes):
    #     # convert to pandas dataframe
    #     df = pd.DataFrame(processes)
    #     # set the process id as index of a process
    #     df.set_index('pid', inplace=True)
    #     return df

    # def printTasks(self):
    #     self.getTasks()
    #     df = self.construct_dataframe(self.processes)
    #     print(df.to_string())

    def killTask(self):
        for process in psutil.process_iter():
            if any(procstr in process.name() for procstr in\
                ['Spotify', 'Firefox', 'Google Chrome', 'Netflix']): #liste zu vervollständigen
                    #print(f'Killing {process.name()}')
                    process.kill()