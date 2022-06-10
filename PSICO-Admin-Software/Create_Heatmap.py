import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#TO DO import in pip install

class CreateHeatmap():
    
    def __init__(self):
        super().__init__()

    def unstack(self, dictionary):
        ser = pd.Series(list(dictionary.values()), index=pd.MultiIndex.from_tuples(dictionary.keys()))
        df = ser.unstack().fillna(0)
        return df

    def generateHeatmap(self, dataframe):
        sns.heatmap(dataframe, xticklabels=False, yticklabels=False, cbar=False)
        # plt.savefig('output.png')
        plt.show()
    
    def getData(self):
        keys = [self.querryConnection.get()][:-1]
        mouseData = {}
        for key in keys:
            CITIZEN_REF = self.querryConnection.child(key)
            MOUSE_LOGS_REF = CITIZEN_REF.child("MouseLogs")
            mousePositions = [MOUSE_LOGS_REF.get()].remove("-1")
            for pos in mousePositions:
                freq = MOUSE_LOGS_REF.get()[pos]
                temp1 = pos.split(",")
                x = int(temp1[1:])
                y = int(temp1[:-1])
                mouseData[(x,y)] = freq
        return mouseData

if __name__ == '__main__':
    pixlist= {(1083,228):4,(1087,381):7,(1119,984):3,(1128,503):3,(1130,360):4,(1137,358):4,(1145,357):4,(1156,354):4,(1163,352):4,(1170,350):4,(1179,348):4}

    crhm = CreateHeatmap()
    crhm.generateHeatmap(crhm.unstack(pixlist))