import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import operator
import re
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame

"""
<<<<<<< HEAD
AUTHOR: ROBERT SEDELMEIER, MATHIEU STENZEL, PHILIPP WENDEL, WLADIMIR URBAN
=======
AUTHOR: ROBERT SEDELMEIER, MATHIEU STENZEL, PHILIPP WENDEL, DANIEL HILLMANN
>>>>>>> 488aa4add42b040594ba61d1a68c61e76f79d214
"""


# class AdminWatcher for calculating data and sending to the View
class AdminWatcher():

    # connect to database
    def queryConnect(self):
        CERTIFICATE_FILE_PATH = self.getCWD() + '\\PSICO-Admin-Software\\res\\firebaseCertificate.json'
        CRED = credentials.Certificate(CERTIFICATE_FILE_PATH)
        APP = firebase_admin.initialize_app(CRED, options = {'databaseURL':'https://psico-software-default-rtdb.europe-west1.firebasedatabase.app/'})
        ref = db.reference('Citizen')
        return ref

    # initialize the AdminWatcher 
    def __init__(self) -> None:

        # create variables for calculations and data handling
        self.numOfCitizen = 0
        self.numOfKeystrokesPerMinute = 0
        self.numOfClicksPerMinute = 0
        self.numOfKeystrokes = 0
        self.avgNumOfKeystrokesPerMinute = 0
        self.numOfClicks = 0
        self.avgNumOfClicksPerMinute = 0
        self.sumSocialCreditScore = 0
        self.avgSocialCreditScore = 0
        self.sumNumOfCitizenFailings = 0
        self.avgNumOfFailings = 0
        self.keyLogs = []
        self.keyLogSting = ''
        self.connection = self.queryConnect()
        self.allCitizenData = []
        self.allCitizenData = self.getAllCitizenInfo()

    # query function for database access
    def query(self):
        query = []
        for doc in self.connection.get():
            citizen_ref = self.connection.child(f'{doc}')
            data = citizen_ref.get()
            citizen_id = doc
            query.append((citizen_id, data))
        return query

    # fetching all citizen data
    def getAllCitizenInfo(self):

        # resetting the variables before calculation
        self.numOfCitizen = 0
        self.numOfKeystrokesPerMinute = 0
        self.numOfClicksPerMinute = 0
        self.sumSocialCreditScore = 0
        self.sumNumOfCitizenFailings = 0
        self.keyLogs = []
        citizenList = []

        # iterate through all citizen and extract data into a dictionary
        for i,q in self.query():
            if(isinstance(q, dict)):
                if(i != 'Citizen1'):
                    del q['Failings']['-1']
                    del q['KeyLogs']['-1']
                    info = {'Name':q['Name'],'SCS':q['SCS'],'ID':i, 'KPM':q['KPM'], 'CPM':q['CPM'], 'Failings':q['Failings'], 'KeyLogs':q['KeyLogs']}
                    citizenList.append(info)

                    # counting all sums and incrementing counter for number of citizens
                    self.numOfCitizen += 1
                    self.numOfKeystrokes += q['KOA']
                    self.numOfKeystrokesPerMinute += q['KPM']
                    self.numOfClicks += q['COA']
                    self.numOfClicksPerMinute += q['CPM']
                    self.sumSocialCreditScore += q['SCS']
                    self.sumNumOfCitizenFailings += len(q['Failings'])
                    self.keyLogs += q['KeyLogs']
                    for log in q['KeyLogs'].values():
                        self.keyLogSting += log
                    
        # calculate averages on the basis of cumulated sums and the count of citizen
        self.avgNumOfKeystrokesPerMinute = self.numOfKeystrokesPerMinute / self.numOfCitizen
        self.avgNumOfClicksPerMinute = self.numOfClicksPerMinute / self.numOfCitizen
        self.avgNumOfFailings = self.sumNumOfCitizenFailings / self.numOfCitizen
        self.avgSocialCreditScore = self.sumSocialCreditScore / self.numOfCitizen
        
        return citizenList

    # function for heatmap generation
    def generateHeatmap(self, dictionary):
        ser = pd.Series(list(dictionary.values()), index=pd.MultiIndex.from_tuples(dictionary.keys()))
        dataframe = ser.unstack().fillna(0)
        sns.set(rc = {'figure.figsize':(12.8,7.2)})
        sns.heatmap(dataframe, xticklabels=False, yticklabels=False, cbar=False, vmin=0, vmax=200, cmap="rocket")
        plt.show()
    
    # function for mousedata cumulation
    def getComulatedMouseData(self):
        keys = [*self.connection.get()][:-1]
        mouseData = {}

        # iterate through citizen and getting mouse data
        for key in keys:
            CITIZEN_REF = self.connection.child(key)
            MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
            mousePositions = [*MOUSE_LOGS_REF.get()]
            data = MOUSE_LOGS_REF.get()

            # collect positions and build sum
            for pos in mousePositions: 
                if pos == '-1':
                    continue
                freq = data[pos]
                temp1 = pos[1:-1].split(',')
                x = int(temp1[0])
                y = int(temp1[1])
                if (x,y) in mouseData:
                    mouseData[(x,y)] = mouseData[(x,y)] + freq
                else:
                    mouseData[(x,y)] = freq
        return mouseData
    
    # function to fetch all citizen mouse data from the database
    def getCitizenMouseData(self, citizenId):
        mouseData = {}
        CITIZEN_REF = self.connection.child(citizenId)
        MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
        mousePositions = [*MOUSE_LOGS_REF.get()]
        data = MOUSE_LOGS_REF.get()

        # collect mouse positions
        for pos in mousePositions: 
            if pos == '-1':
                continue
            freq = data[pos]
            temp1 = pos[1:-1].split(',')
            x = int(temp1[0])
            y = int(temp1[1])
            if (x,y) in mouseData:
                mouseData[(x,y)] = mouseData[(x,y)] + freq
            else:
                mouseData[(x,y)] = freq
        return mouseData
    
    # function for analyzing strings
    def analyzeString(self):
        
        # key whitelist
        allowedkeys = ("esc","~","`","1","2","3","4","5","6","7","8","9","0","!","@","#","$","%","^","&","*","(",")","-","=","_","+","del","tab","q","w","e","r","t","y","u","i","o","p","[","{","]","}","\\","|","a","s","d","f","g","h","j","k","l",":",";","'","\"","\n","shift","z","x","c","v","b","n","m",",",".","<",">","/","?","fn","ctrl","opt","cmd"," ","up","left","down","right","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z")

        fstr = self.keyLogSting
        keyCount = {}
        
        #convert special comands
        cmd = [m.start() for m in re.finditer('\<cmd\>', fstr)]
        keyCount['cmd'] = len(cmd)
        fstr = fstr.replace('<cmd>', '')

        cmd = [m.start() for m in re.finditer('\<del\>', fstr)]
        keyCount['del'] = len(cmd)
        fstr = fstr.replace('<del>', '')

        cmd = [m.start() for m in re.finditer('\<shift\>', fstr)]
        keyCount['shift'] = len(cmd)
        fstr = fstr.replace('<shift>', '')

        cmd = [m.start() for m in re.finditer('\<cntrl\>', fstr)]
        keyCount['ctrl'] = len(cmd)
        fstr = fstr.replace('<cntrl>', '')
        cmd = [m.start() for m in re.finditer('\<ctrl\>', fstr)]
        keyCount['ctrl'] = keyCount['ctrl'] + len(cmd)
        fstr = fstr.replace('<ctrl>', '')

        cmd = [m.start() for m in re.finditer('\<opt\>', fstr)]
        keyCount['opt'] = len(cmd)
        fstr = fstr.replace('<opt>', '')

        cmd = [m.start() for m in re.finditer('\<esc\>', fstr)]
        keyCount['esc'] = len(cmd)
        fstr = fstr.replace('<esc>', '')

        cmd = [m.start() for m in re.finditer('\<fn\>', fstr)]
        keyCount['fn'] = len(cmd)
        fstr = fstr.replace('<fn>', '')

        cmd = [m.start() for m in re.finditer('\<tab\>', fstr)]
        keyCount['tab'] = len(cmd)
        fstr = fstr.replace('<tab>', '')

        cmd = [m.start() for m in re.finditer('\<left\>', fstr)]
        cmd2 = [m.start() for m in re.finditer('\<eft\>', fstr)]
        keyCount['left'] = len(cmd) + len(cmd2)
        fstr = fstr.replace('<left>', '')
        fstr = fstr.replace('<eft>', '')

        cmd = [m.start() for m in re.finditer('\<up\>', fstr)]
        keyCount['up'] = len(cmd)
        fstr = fstr.replace('<up>', '')

        cmd = [m.start() for m in re.finditer('\<down\>', fstr)]
        keyCount['down'] = len(cmd)
        fstr = fstr.replace('<down>', '')

        cmd = [m.start() for m in re.finditer('\<right\>', fstr)]
        keyCount['right'] = len(cmd)
        fstr = fstr.replace('<right>', '')

        # check wether keys are allowed
        for key in fstr:
            if key not in allowedkeys:
                fstr = fstr.replace(key, '')
        
        #count keys
        for char in fstr:
            if char.istitle():
                keyCount['shift'] +=1
                char = char.lower()
            if char in "\":{}|!@#$%^&*()_+":
                keyCount['shift'] +=1
            if char in keyCount:
                keyCount[char] +=1
            else:
                keyCount[char] = 1
            
        #sort counted keys
        sortedCount = sorted(keyCount.items(), key=operator.itemgetter(1))
        return sortedCount

    # function to re-map keys
    def mapStringOnKeyboard(self, dt, screen):

        sizeMappings = {1:(44,44),2:(65, 47),3:(90, 47),4:(116, 47),5:(49, 28),6:(260,54),8:(50, 54),7:(49,54)}

        keyMappings = {"esc":(40,73,5),"~":(40, 118,1),"`":(40,118,1),"1":(93 ,118,1),"2":(146, 118,1),"3":(199, 118,1),"4":(255, 118,1),"5":(308, 118,1),"6":(362, 118,1),"7":(417, 118,1),"8":(470, 118,1),"9":(525, 118,1),"0":(579, 118,1),"!":(93 ,118,1),"@":(146, 118,1),"#":(199, 118,1),"$":(255, 118,1),"%":(308, 118,1),"^":(362, 118,1),"&":(417, 118,1),"*":(470, 118,1),"(":(525, 118,1),")":(579, 118,1),"-":(633, 118,1),"=":(686, 118,1),"_":(633, 118,1),"+":(686, 118,1),"del":(755, 118,2),"tab":(50 ,171,2),"q":(118, 171,1),"w":(172, 171,1),"e":(226, 171,1),"r":(280, 171,1),"t":(334, 171,1),"y":(388, 171,1),"u":(442, 171,1),"i":(496, 171,1),"o":(550, 171,1),"p":(604, 171,1),"[":(658, 171,1),"{":(658, 171,1),"]":(712, 171,1),"}":(712, 171,1),"\\":(766, 171,1),"|":(766, 171,1),"a":(133, 222,1),"s":(187, 222,1),"d":(241, 222,1),"f":(295, 222,1),"g":(349, 222,1),"h":(403, 222,1),"j":(457, 222,1),"k":(511, 222,1),"l":(565, 222,1),":":(619, 222,1),";":(619, 222,1),"'":(673, 222,1),"\"":(673, 222,1),"\n":(752, 222,3),"shift":(76 ,275,4),"z":(160, 275,1),"x":(214, 275,1),"c":(268, 275,1),"v":(322, 275,1),"b":(376, 275,1),"n":(430, 275,1),"m":(484, 275,1),",":(538, 275,1),".":(592, 275,1),"<":(538, 275,1),">":(592, 275,1),"/":(646, 275,1),"?":(646, 275,1),"fn":(39 ,331,7),"ctrl":(92 ,331,7),"opt":(147, 331,7),"cmd":(207, 331,8)," ":(378, 331, 6),"up":(714, 318,5),"left":(660, 343,5),"down":(714, 343,5),"right":(767, 343,5)}

        # sum of all keys
        allkeys = 0
        for key, count in dt:
            allkeys += count
        #check wether keys were pressed
        if allkeys != 0:
            for key, count in dt:
                #calculate percentage and adjust
                countfactor = (count/allkeys)*100
                #prepare drawing
                centX = keyMappings[key][0]
                centY = keyMappings[key][1]
                width = sizeMappings[keyMappings[key][2]][0]
                height = sizeMappings[keyMappings[key][2]][1]
                s = pygame.Surface((width, height))
                
                s.set_alpha(155)
                if 0 == countfactor:
                    s.set_alpha(0)
                elif countfactor < 1:
                    s.fill((125,0,255))
                elif countfactor < 2:
                    s.fill((0,0,255))
                elif countfactor < 3:
                    s.fill((0,125,255))
                elif countfactor < 4:
                    s.fill((0,255,255))
                elif countfactor < 5:
                    s.fill((0,255,125))
                elif countfactor < 6:
                    s.fill((0,255,0))
                elif countfactor < 7:
                    s.fill((125,255,0))
                elif countfactor < 8:
                    s.fill((255,255,0))
                elif countfactor < 9:
                    s.fill((255,125,0))
                else:
                    s.fill((255,0,0))
                #draw
                screen.blit(s, (centX - width/2, centY - height/2))
    
    # function for generating a keyboard heatmap
    def generateKeyboardHeatmap(self):
        pygame.init()
        keyboard = pygame.image.load(self.getCWD() + '\\PSICO-Admin-Software\\res\\keyboard.png')
        keyRect = keyboard.get_rect()
        size = (width, height) = keyboard.get_size()
        pygame.display.set_caption('Tastatur-Heatmap')
        icon = pygame.image.load(self.getCWD() + '\\PSICO-Admin-Software\\PSICO_Logo.svg')
        pygame.display.set_icon(icon)
        screen = pygame.display.set_mode(size)
        screen.blit(keyboard, keyRect)
        count = self.analyzeString()
        self.mapStringOnKeyboard(count, screen)
        pygame.display.update()
        running  = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    running = False
    
    # function for getting the current working directory
    def getCWD(self):
        CWD = os.getcwd()
        if CWD.find("\PSICO-Admin-Software") >= 0:
            cut = len("\PSICO-Admin-Software")
            CWD = CWD[0:-cut]
        return CWD