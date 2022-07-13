from PSICO_Admin_Watcher import AdminWatcher
import sys
import os
from PySide6.QtCore import QRegularExpression, QSortFilterProxyModel, Qt
from PySide6.QtGui import QStandardItemModel, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, QLineEdit, QTreeView, QWidget, QTabWidget, QAbstractItemView, QMainWindow, QPushButton)

"""
AUTHOR: ROBERT SEDELMEIER, MATIEU STENZEL, DANIEL HILLMANN
"""

# class for all GUI related operations and functions (except the authentication)
class Window(QTabWidget):

    # creating a window via constructor method
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        # window contains its own model data handler
        self.adminController = AdminWatcher()

        # window gets some tabwidgets as tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        # simple way of checking which view is currently present in tab1 via state variable
        self.tab1State = 0

        # initially setting the database model to view all citizen
        self.citizenModel = self.createCitizenModel()
        self.addEntryList(self.adminController.allCitizenData)

        self.totalsModel = self.buildTotals(self.adminController.numOfCitizen, self.adminController.numOfKeystrokes, self.adminController.numOfClicks, self.adminController.avgNumOfKeystrokesPerMinute, self.adminController.avgNumOfClicksPerMinute, self.adminController.sumNumOfCitizenFailings, self.adminController.avgNumOfFailings, self.adminController.avgSocialCreditScore)

        # add tabs to the window
        self.addTab(self.tab1,"Bürgeranalyse")
        self.addTab(self.tab2,"Gesamtanalyse")
        self.addTab(self.tab3,"Heatmaps")

        # initialize all tabs for presentation
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        # set datamodels for the different tabs
        self.setTab1Model(self.citizenModel)
        self.setTab2Model(self.totalsModel)
        # self.setTab3Model(self.createCitizenModel())

        # adjust window settings
        self.setWindowTitle("PSICO Admin-Software")
        self.setWindowIcon(QIcon(getCWD() + '\PSICO-Admin-Software\PSICO_Logo.svg'))
        self.setFixedSize(800, 450)
        

    # building tab1's foundation
    def tab1UI(self):
        
        self.tab1.lastCitizenId = " "

        # creating a basic datamodel
        self.tab1.citizenListModel = QSortFilterProxyModel()
        self.tab1.citizenListModel.setDynamicSortFilter(True)

        # creating a viewing model
        self.tab1.citizenListView = QTreeView()
        self.tab1.citizenListView.setRootIsDecorated(False)
        self.tab1.citizenListView.setAlternatingRowColors(True)
        self.tab1.citizenListView.setModel(self.tab1.citizenListModel)
        self.tab1.citizenListView.setSortingEnabled(True)
        self.tab1.citizenListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # creating checkboxes for the filter functions
        self.tab1.sortCaseSensitivityCheckBox = QCheckBox("Case-sensitive Sortierung")
        self.tab1.filterCaseSensitivityCheckBox = QCheckBox("Case-sensitiver Filter")

        # create filter input field including a clear input button and connect a label
        self.tab1.filterPatternLineEdit = QLineEdit()
        self.tab1.filterPatternLineEdit.setClearButtonEnabled(True)
        self.tab1.filterPatternLabel = QLabel("Filter (RegEx):")
        self.tab1.filterPatternLabel.setBuddy(self.tab1.filterPatternLineEdit)

        # return button to get back to general citizen view
        self.tab1.backButton = QPushButton()
        self.tab1.backButton.setText('X')
        self.tab1.backButton.setFixedSize(20, 20)
        self.tab1.backButton.hide()
        self.tab1.backButton.clicked.connect(self.backToCitizenView)
        
        # button to generate the citizen mouse heatmap
        self.tab1.heatmapButton = QPushButton()
        self.tab1.heatmapButton.setText('Generiere eine Maus-Heatmap!')
        self.tab1.heatmapButton.setFixedSize(180, 25)
        self.tab1.heatmapButton.hide()

        # create a dropdown menu to filter on different columns and connect a label
        self.tab1.filterColumnComboBox = QComboBox()
        self.tab1.filterColumnComboBox.addItem("ID")
        self.tab1.filterColumnComboBox.addItem("Name")
        self.tab1.filterColumnComboBox.addItem("Verbrechen")
        self.tab1.filterColumnComboBox.addItem("Tastenanschläge / min")
        self.tab1.filterColumnComboBox.addItem("Klicks / min")
        self.tab1.filterColumnComboBox.addItem("Social-Credit-Punkte")
        self.tab1.filterColumnLabel = QLabel("Filter-Spalte:")
        self.tab1.filterColumnLabel.setBuddy(self.tab1.filterColumnComboBox)

        # connect functions to the different control elements
        self.tab1.filterPatternLineEdit.textChanged.connect(self.filterPatternChanged)
        self.tab1.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.tab1.filterCaseSensitivityCheckBox.toggled.connect(self.filterPatternChanged)
        self.tab1.sortCaseSensitivityCheckBox.toggled.connect(self.sortCaseSensitivityChanged)
        self.tab1.citizenListView.doubleClicked.connect(self.createCitizenView)
        self.tab1.heatmapButton.clicked.connect(self.generateCitizenMouseDataHeatmap)

        # default settings for the control elements
        self.tab1.citizenListView.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filterColumnComboBox.setCurrentIndex(1)
        self.tab1.filterPatternLineEdit.setText("")
        self.tab1.filterCaseSensitivityCheckBox.setChecked(True)
        self.tab1.sortCaseSensitivityCheckBox.setChecked(True)

        # define a layout, add created widgets and assign it to the tab
        layout = QGridLayout()
        layout.addWidget(self.tab1.backButton, 0, 2)
        layout.addWidget(self.tab1.heatmapButton, 2, 1)
        layout.addWidget(self.tab1.citizenListView, 1, 0, 1, 3)
        layout.addWidget(self.tab1.filterPatternLabel, 2, 0)
        layout.addWidget(self.tab1.filterPatternLineEdit, 2, 1, 1, 2)
        layout.addWidget(self.tab1.filterColumnLabel, 3, 0)
        layout.addWidget(self.tab1.filterColumnComboBox, 3, 1, 1, 2)
        layout.addWidget(self.tab1.filterCaseSensitivityCheckBox, 4, 0, 1, 2)
        layout.addWidget(self.tab1.sortCaseSensitivityCheckBox, 4, 1)
        self.layoutAll = layout
        self.tab1.setLayout(layout)

    
    def generateCitizenMouseDataHeatmap(self):
        self.adminController.generateHeatmap(self.adminController.getCitizenMouseData(self.tab1.lastCitizenId))
        
    def generateComulatedMouseDataHeatmap(self):
        self.adminController.generateHeatmap(self.adminController.getComulatedMouseData())

        
    # creates a detailed view of a specific citizen entry
    def createCitizenView(self, index):

        if self.tab1State == 0:

            # fetching data from the double clicked entry
            id = index.siblingAtColumn(0)
            name = index.siblingAtColumn(1)
            numOfFailings = index.siblingAtColumn(2)
            keystrokesPerMinute = index.siblingAtColumn(3)
            clicksPerMinute = index.siblingAtColumn(4)
            scs = index.siblingAtColumn(5)
            listOfFilings = index.siblingAtColumn(6)
            
            self.tab1.lastCitizenId = id.data()

            # build a characteristics page for the selected entry and set tab1State to 1 for characteristics view
            self.tab1State = 1
            
            self.tab1.filterColumnComboBox.hide()
            self.tab1.filterPatternLineEdit.hide()
            self.tab1.filterCaseSensitivityCheckBox.hide()
            self.tab1.sortCaseSensitivityCheckBox.hide()
            self.tab1.filterColumnLabel.hide()
            self.tab1.filterPatternLabel.hide()
            
            self.tab1.backButton.show()
            self.tab1.heatmapButton.show()
            
            self.charViewUI(id.data(), name.data(), numOfFailings.data(), keystrokesPerMinute.data(), clicksPerMinute.data(), scs.data(), listOfFilings.data())
            

    # return to all view mode if in characteristics view #subject to change
    def backToCitizenView(self):
        if self.tab1State == 1:
            self.addEntryList(self.adminController.getAllCitizenInfo())
            self.setTab1Model(self.citizenModel)
            self.tab1State = 0
            self.tab1.backButton.hide()
            self.tab1.heatmapButton.hide()
            
            self.tab1.filterColumnComboBox.show()
            self.tab1.filterPatternLineEdit.show()
            self.tab1.filterCaseSensitivityCheckBox.show()
            self.tab1.sortCaseSensitivityCheckBox.show()
            self.tab1.filterColumnLabel.show()
            self.tab1.filterPatternLabel.show()


    # building tab2's foundation
    def tab2UI(self):

        # create a datamodel
        self.tab2.totalsModel = QSortFilterProxyModel()
        self.tab2.totalsModel.setDynamicSortFilter(True)

        # create a view model
        self.tab2.totalsView = QTreeView()
        self.tab2.totalsView.setRootIsDecorated(False)
        self.tab2.totalsView.setModel(self.tab2.totalsModel)
        self.tab2.totalsView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTab2Model(self.totalsModel)

        # set the layout and add created widgets   
        layout = QGridLayout()
        layout.addWidget(self.tab2.totalsView, 0, 0, 0, 0)
        self.tab2.setLayout(layout)


    def buildTotals(self, numOfCitizen, numOfKeysPressed, numOfClicks, avgNumOfKeystrokesPerMinute, avgNumOfClicksPerMinute, numOfCitizenFailings, avgNumOfFailings, avgSocialCreditScore):

        totalsModel = QStandardItemModel(8,2, self)

        totalsModel.setHeaderData(0, Qt.Horizontal, "Beschreibung")
        totalsModel.setHeaderData(1, Qt.Horizontal, "Daten")

        totalsModel.setData(totalsModel.index(0, 0), "Bürger gesamt:")
        totalsModel.setData(totalsModel.index(1, 0), "Tastendücke gesamt:")
        totalsModel.setData(totalsModel.index(2, 0), "Klicks gesamt:")
        totalsModel.setData(totalsModel.index(3, 0), "Tasten pro Minute:")
        totalsModel.setData(totalsModel.index(4, 0), "Klicks pro Minute:")
        totalsModel.setData(totalsModel.index(5, 0), "Verstöße:")
        totalsModel.setData(totalsModel.index(6, 0), "Verstöße pro Kopf:")
        totalsModel.setData(totalsModel.index(7, 0), "Social-Credit-Score Durchschnitt:")

        totalsModel.setData(totalsModel.index(0, 1), numOfCitizen)
        totalsModel.setData(totalsModel.index(1, 1), numOfKeysPressed)
        totalsModel.setData(totalsModel.index(2, 1), numOfClicks)
        totalsModel.setData(totalsModel.index(3, 1), avgNumOfKeystrokesPerMinute)
        totalsModel.setData(totalsModel.index(4, 1), avgNumOfClicksPerMinute)
        totalsModel.setData(totalsModel.index(5, 1), numOfCitizenFailings)
        totalsModel.setData(totalsModel.index(6, 1), avgNumOfFailings)
        totalsModel.setData(totalsModel.index(7, 1), avgSocialCreditScore)

        return totalsModel


    # build tab3's foundation
    def tab3UI(self):
        
        # button to generate the comulated mouse heatmap
        self.tab3.mouseHeatmapButton = QPushButton()
        self.tab3.mouseHeatmapButton.setText('Generiere eine Maus-Heatmap!')
        self.tab3.mouseHeatmapButton.setFixedSize(200, 25)
        self.tab3.mouseHeatmapButton.clicked.connect(self.generateComulatedMouseDataHeatmap)
        
        # button to generate the comulated keyboard heatmap
        self.tab3.keyboardHeatmapButton = QPushButton()
        self.tab3.keyboardHeatmapButton.setText('Generiere eine Tastatur-Heatmap!')
        self.tab3.keyboardHeatmapButton.setFixedSize(200, 25)
        self.tab3.keyboardHeatmapButton.clicked.connect(self.adminController.generateKeyboardHeatmap)
        
        # set layout and add created widgets
        layout = QGridLayout()
        layout.addWidget(self.tab3.mouseHeatmapButton, 0, 0, 2, 0)
        layout.addWidget(self.tab3.keyboardHeatmapButton, 1, 0, 2, 0)
        self.tab3.setLayout(layout)


    # create a one time use characteristics model and view from data passed from the view
    def charViewUI(self, id, name, numOfFailings, keystrokesPerMinute, clicksPerMinute, scs, failings):
        self.tab1.charModel = QSortFilterProxyModel()
        self.tab1.charModel.setDynamicSortFilter(True)

        self.tab1.charView = QTreeView()
        self.tab1.charView.setRootIsDecorated(False)
        self.tab1.charView.setModel(self.tab1.charModel)
        self.tab1.charView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTab1Model(self.createCharacteristicsModel(id, name, numOfFailings, keystrokesPerMinute, clicksPerMinute, scs, failings))


    # methods to quickly set models in the tabs
    def setTab1Model(self, model):
        self.tab1.citizenListModel.setSourceModel(model)
        for i in range(0,5):
            self.tab1.citizenListView.resizeColumnToContents(i)
        self.tab1.citizenListModel.sort(1, Qt.AscendingOrder)
        self.tab1.citizenListModel.sort(0, Qt.AscendingOrder)


    def setTab2Model(self, model):
        self.tab2.totalsModel.setSourceModel(model)
        self.tab2.totalsView.resizeColumnToContents(0)

    # reaction on changes in the filter input field
    def filterPatternChanged(self):
        pattern = self.tab1.filterPatternLineEdit.text()
        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filterCaseSensitivityCheckBox.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizenListModel.setFilterRegularExpression(reg_exp)


    # reaction on the filter column dropdown menu
    def filterColumnChanged(self):
        self.tab1.citizenListModel.setFilterKeyColumn(self.tab1.filterColumnComboBox.currentIndex())


    # reaction on the case sensitivity checkboxes
    def sortCaseSensitivityChanged(self):
        if self.tab1.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive
        self.tab1.citizenListModel.setSortCaseSensitivity(caseSensitivity)


    # method for adding entries in the current datamodel
    def addEntry(self, citizenModel, id, name, cntFailings, keysPerMinute, clicksPerMinute, scs, failings):
        citizenModel.insertRow(0)
        citizenModel.setData(citizenModel.index(0, 0), id)
        citizenModel.setData(citizenModel.index(0, 1), name)
        citizenModel.setData(citizenModel.index(0, 2), cntFailings)
        citizenModel.setData(citizenModel.index(0, 3), keysPerMinute)
        citizenModel.setData(citizenModel.index(0, 4), clicksPerMinute)
        citizenModel.setData(citizenModel.index(0, 5), scs)
        citizenModel.setData(citizenModel.index(0, 6), failings)


    # method for adding a list of entries in the current datamodel
    def addEntryList(self, citizenData):
        for citizen in citizenData:
             id = 0 if citizen['ID'] == -1 else citizen['ID']
             if len(self.citizenModel.findItems(id)) < 1:
                name = citizen['Name']
                cntFailings = len([*citizen['Failings']])
                failings = citizen['Failings']
                kpm = citizen['KPM']
                cpm = citizen['CPM']
                scs = citizen['SCS']
                self.addEntry(self.citizenModel, id, name, cntFailings, kpm, cpm, scs, failings)


    # method for building the characteristics view
    def buildCharacteristics(self, characteristicsModel, id, name, numOfFailings, keystrokesPerMinute, clicksPerMinute, scs, failings):

        execution = "Möglich"

        if(numOfFailings > 20):
            execution = "Exekution Empfohlen"
            if(numOfFailings > 100):
                execution = "Exekution erforderlich"
                if(numOfFailings > 200):
                    execution += " mitsamt Familie"
                    if(numOfFailings > 300):
                        execution += " und Freunden"
                        if(numOfFailings > 500):
                            execution += "...und den Hund am besten auchnoch, zur Sicherheit!"
        
        for i in range(0,7):
            characteristicsModel.setData(characteristicsModel.index(i, 0), i + 1)

        characteristicsModel.setData(characteristicsModel.index(0, 1), "ID:")
        characteristicsModel.setData(characteristicsModel.index(1, 1), "Name:")
        characteristicsModel.setData(characteristicsModel.index(2, 1), "Anzahl der Verbrechen:")
        characteristicsModel.setData(characteristicsModel.index(3, 1), "Tasten pro Minute:")
        characteristicsModel.setData(characteristicsModel.index(4, 1), "Klicks pro Minute:")
        characteristicsModel.setData(characteristicsModel.index(5, 1), "Social-Credit-Score:")
        characteristicsModel.setData(characteristicsModel.index(6, 1), "Exekution:")

        characteristicsModel.setData(characteristicsModel.index(0, 2), id)
        characteristicsModel.setData(characteristicsModel.index(1, 2), name)
        characteristicsModel.setData(characteristicsModel.index(2, 2), numOfFailings)
        characteristicsModel.setData(characteristicsModel.index(3, 2), keystrokesPerMinute)
        characteristicsModel.setData(characteristicsModel.index(4, 2), clicksPerMinute)
        characteristicsModel.setData(characteristicsModel.index(5, 2), scs)
        characteristicsModel.setData(characteristicsModel.index(6, 2), execution)

        i = 1
        for key, crime in failings.items():
            if i < 10:
                x = '0'
            else:
                x = ''
                
            if(crime != -1 and key != "Initial"):
                characteristicsModel.insertRow(0)
                characteristicsModel.setData(characteristicsModel.index(0, 0), '8.' + x + str(i))
                characteristicsModel.setData(characteristicsModel.index(0, 1), 'Verbrechen:')
                characteristicsModel.setData(characteristicsModel.index(0, 2), crime)
                i += 1


    # method for building the citizen datamodel
    def createCitizenModel(self):

        self.citizenModel = QStandardItemModel(0, 7, self)

        self.citizenModel.setHeaderData(0, Qt.Horizontal, "ID")
        self.citizenModel.setHeaderData(1, Qt.Horizontal, "Name")
        self.citizenModel.setHeaderData(2, Qt.Horizontal, "Anzahl Verbrechen")
        self.citizenModel.setHeaderData(3, Qt.Horizontal, "Tastenanschläge / min")
        self.citizenModel.setHeaderData(4, Qt.Horizontal, "Klicks / min")
        self.citizenModel.setHeaderData(5, Qt.Horizontal, "Social-Credit-Punkte")
        self.citizenModel.setHeaderData(6, Qt.Horizontal, "")

        return self.citizenModel


    # method for building characteristics data model  
    def createCharacteristicsModel(self, id, name, numOfFailings, keystrokesPerMinute, clicksPerMinute, scs, failings):
        charModel = QStandardItemModel(8,3, self)

        charModel.setHeaderData(0, Qt.Horizontal, "")
        charModel.setHeaderData(1, Qt.Horizontal, "Übersicht")
        charModel.setHeaderData(2, Qt.Horizontal, "Daten")

        self.buildCharacteristics(charModel, id, name, numOfFailings, keystrokesPerMinute, clicksPerMinute, scs, failings)

        return charModel
    



# class for the authentication
class PasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon(getCWD() + '\\PSICO-Admin-Software\\PSICO_Logo.svg'))
        self.setFixedSize(170, 30)

        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.setCentralWidget(self.password)
        self.password.editingFinished.connect(self.validatePassword)


    # method to validate the passwort entry and to start the main program
    def validatePassword(self):
        if self.password.text() == 'admin':
            self.window = Window()
            self.window.show()
            self.close()
            
def getCWD():
    CWD = os.getcwd()
    if CWD.find("\PSICO-Admin-Software") >= 0:
        cut = len("\PSICO-Admin-Software")
        CWD = CWD[0:-cut]
    return CWD


# main method for running the application
if __name__ == '__main__':
    app = QApplication()
    startWindow = PasswordWindow()
    startWindow.show()
    sys.exit(app.exec())