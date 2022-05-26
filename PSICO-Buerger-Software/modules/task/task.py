import psutil
# import pandas as pd

def getTasks():
    # the list the contain all process dictionaries
    processes = []
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

    return processes

# def construct_dataframe(processes):
#     # convert to pandas dataframe
#     df = pd.DataFrame(processes)
#     # set the process id as index of a process
#     df.set_index('pid', inplace=True)
#     return df

# def printTasks():
#     processes = getTasks()
#     df = construct_dataframe(processes)
#     print(df.to_string())
        
#test
#print(getTasks())
#printTasks()