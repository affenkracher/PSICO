from ctypes.wintypes import RGB
from multiprocessing import connection
from ssl import Options
from PSICO_Admin_Watcher import AdminWatcher
import sys
import os
from PySide6.QtCore import QDate, QDateTime, QRegularExpression, QSortFilterProxyModel, QTime, Qt
from PySide6.QtGui import QStandardItemModel, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, QLineEdit, QTreeView, QWidget, QTabWidget, QAbstractItemView, QMainWindow)

# Constant for current working directory
CWD = os.getcwd()

# Class for all GUI related operations and functions aka Model-View-Controller
class Window(QTabWidget):

#   creating a window via constructor method
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

#   window contains its own model data handler
        self.admin_controller = AdminWatcher()

#   window gets some tabwidgets as tabs
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

#   simple way of checking which view is currently present in tab1 via state variable
        self.tab1State = 0

#   initially setting the database model to view all citizen
        self.citizenModel = self.updateCitizenModel()

#   add tabs to the window
        self.addTab(self.tab1,"Bürgeranalyse")
        self.addTab(self.tab2,"Gesamtanalyse")
        self.addTab(self.tab3,"Heatmaps")

#   initialize all tabs for presentation
        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

#   set datamodels for the different tabs
        self.setTab1Model(self.citizenModel)
        self.setTab2Model(self.updateCitizenModel())
        self.setTab3Model(self.updateCitizenModel())
        
#   adjust window settings
        self.setWindowTitle("PSICO Admin-Software")
        self.setWindowIcon(QIcon('./PSICO_Logo.svg'))
        self.resize(900, 450)
        

#   building tab1's foundation
    def tab1UI(self):

#   creating a basic datamodel
        self.tab1.citizenListModel = QSortFilterProxyModel()
        self.tab1.citizenListModel.setDynamicSortFilter(True)

#   creating a viewing model
        self.tab1.citizenListView = QTreeView()
        self.tab1.citizenListView.setRootIsDecorated(False)
        self.tab1.citizenListView.setAlternatingRowColors(True)
        self.tab1.citizenListView.setModel(self.tab1.citizenListModel)
        self.tab1.citizenListView.setSortingEnabled(True)
        self.tab1.citizenListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

#   creating checkboxes for the filter functions
        self.tab1.sortCaseSensitivityCheckBox = QCheckBox("Case-sensitive Sortierung")
        self.tab1.filterCaseSensitivityCheckBox = QCheckBox("Case-sensitiver Filter")

#   create filter input field including a clear input button and connect a label
        self.tab1.filterPatternLineEdit = QLineEdit()
        self.tab1.filterPatternLineEdit.setClearButtonEnabled(True)
        self.tab1.filterPatternLabel = QLabel("Filter (RegEx):")
        self.tab1.filterPatternLabel.setBuddy(self.tab1.filterPatternLineEdit)

#   create a dropdown menu to filter on different columns and connect a label
        self.tab1.filterColumnComboBox = QComboBox()
        self.tab1.filterColumnComboBox.addItem("ID")
        self.tab1.filterColumnComboBox.addItem("Name")
        self.tab1.filterColumnComboBox.addItem("Anzahl Verstöße")
        self.tab1.filterColumnComboBox.addItem("Eingegebene Buchstaben")
        self.tab1.filterColumnComboBox.addItem("Tastenanschläge / min")
        self.tab1.filterColumnComboBox.addItem("Klicks / min")
        self.tab1.filterColumnComboBox.addItem("Social-Credit-Punkte")
        self.tab1.filterColumnComboBox.addItem("letzte Aktualisierung")
        self.tab1.filterColumnLabel = QLabel("Filter-Spalte:")
        self.tab1.filterColumnLabel.setBuddy(self.tab1.filterColumnComboBox)

#   connect functions to the different control elements
        self.tab1.filterPatternLineEdit.textChanged.connect(self.filterPatternChanged)
        self.tab1.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.tab1.filterCaseSensitivityCheckBox.toggled.connect(self.filterPatternChanged)
        self.tab1.sortCaseSensitivityCheckBox.toggled.connect(self.sortCaseSensitivityChanged)
        self.tab1.citizenListView.doubleClicked.connect(self.doubleClicked)

#   default settings for the control elements
        self.tab1.citizenListView.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filterColumnComboBox.setCurrentIndex(1)
        self.tab1.filterPatternLineEdit.setText("")
        self.tab1.filterCaseSensitivityCheckBox.setChecked(True)
        self.tab1.sortCaseSensitivityCheckBox.setChecked(True)

#   define a layout, add created widgets and assign it to the tab
        layout = QGridLayout()
        layout.addWidget(self.tab1.citizenListView, 0, 0, 1, 3)
        layout.addWidget(self.tab1.filterPatternLabel, 1, 0)
        layout.addWidget(self.tab1.filterPatternLineEdit, 1, 1, 1, 2)
        layout.addWidget(self.tab1.filterColumnLabel, 2, 0)
        layout.addWidget(self.tab1.filterColumnComboBox, 2, 1, 1, 2)
        layout.addWidget(self.tab1.filterCaseSensitivityCheckBox, 3, 0, 1, 2)
        layout.addWidget(self.tab1.sortCaseSensitivityCheckBox, 3, 1)
        self.tab1.setLayout(layout)

        
#   defines what happens if a citizen entry is double clicked
    def doubleClicked(self,index):

#   checking if in all citizen view mode
        if(self.tab1State == 0):

#   fetching data from the double clicked entry
            id = index.siblingAtColumn(0)
            name = index.siblingAtColumn(1)
            failings = index.siblingAtColumn(2)
            chars = index.siblingAtColumn(3)
            keystrokes = index.siblingAtColumn(4)
            clicks = index.siblingAtColumn(5)
            scp = index.siblingAtColumn(6)
            update = index.siblingAtColumn(7)

#   build a characteristics page for the selected entry and set tab1State to 1 for characteristics view
            self.charViewUI(id.data(), name.data(), failings.data(), chars.data(), keystrokes.data(), clicks.data(), scp.data(), update.data())
            self.tab1State = 1

        else:

#   return to all view mode if in characteristics view #subject to change
            self.setTab1Model(self.citizenModel)
            self.tab1State = 0
#            self.admin_controller.getAllCitizenInfo(self.admin_controller.getAllCitizen(self.admin_controller.connection))


#   building tab2's foundation
    def tab2UI(self):

#   create a datamodel
        self.tab2.totalsModel = QSortFilterProxyModel()
        self.tab2.totalsModel.setDynamicSortFilter(True)

#   create a view model
        self.tab2.totalsView = QTreeView()
        self.tab2.totalsView.setRootIsDecorated(False)

#   set the layout and add created widgets   
        layout = QGridLayout()
        layout.addWidget(self.tab2.totalsView, 0, 0, 0, 0)
        self.tab2.setLayout(layout)

#   build tab3's foundation
    def tab3UI(self):
#   create a datamodel
        self.tab3.heatMapModel = QSortFilterProxyModel()
        self.tab3.heatMapModel.setDynamicSortFilter(True)

#   create a view model
        self.tab3.heatmapView = QTreeView()
        self.tab3.heatmapView.setRootIsDecorated(False)
        
#   set layout and add created widgets
        layout = QGridLayout()
        layout.addWidget(self.tab3.heatmapView, 0, 0, 0, 0)
        self.tab3.setLayout(layout)

#   create a one time use characteristics model and view from data passed from the view
    def charViewUI(self, id, name, failings, chars, keystrokes, clicks, scp, update):
        self.tab1.charModel = QSortFilterProxyModel()
        self.tab1.charModel.setDynamicSortFilter(True)

        self.tab1.charView = QTreeView()
        self.tab1.charView.setRootIsDecorated(False)
        self.tab1.charView.setModel(self.tab1.charModel)
        self.tab1.charView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTab1Model(self.createCharacteristicsModel(id, name, failings, chars, keystrokes, clicks, scp, update))

        layoutc = QGridLayout()
        layoutc.addWidget(self.tab1.charView, 0, 0, 0, 0)

        self.tab1.setLayout(layoutc)
        

#   methods to quickly set models in the tabs
    def setTab1Model(self, model):
        self.tab1.citizenListModel.setSourceModel(model)

    def setTab2Model(self, model):
        self.tab2.totalsModel.setSourceModel(model)

    def setTab3Model(self, model):
        self.tab3.heatMapModel.setSourceModel(model)

#   reaction on changes in the filter input field
    def filterPatternChanged(self):
        pattern = self.tab1.filterPatternLineEdit.text()
        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filterCaseSensitivityCheckBox.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizenListModel.setFilterRegularExpression(reg_exp)

#   reaction on the filter column dropdown menu
    def filterColumnChanged(self):
        self.tab1.citizenListModel.setFilterKeyColumn(self.tab1.filterColumnComboBox.currentIndex())

#   reaction on the case sensitivity checkboxes
    def sortCaseSensitivityChanged(self):
        if self.tab1.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive
        self.tab1.citizenListModel.setSortCaseSensitivity(caseSensitivity)

#   method for adding entries in the current datamodel
    def addEntry(self, citizenModel, id, name, anzahlVerstöße, eingegebeneBuchstaben, tastenanschlägeProMin, klicksProMin, socialCredit, letzteAktualisierung):
        citizenModel.insertRow(0)
        citizenModel.setData(citizenModel.index(0, 0), id)
        citizenModel.setData(citizenModel.index(0, 1), name)
        citizenModel.setData(citizenModel.index(0, 2), anzahlVerstöße)
        citizenModel.setData(citizenModel.index(0, 3), eingegebeneBuchstaben)
        citizenModel.setData(citizenModel.index(0, 4), tastenanschlägeProMin)
        citizenModel.setData(citizenModel.index(0, 5), klicksProMin)
        citizenModel.setData(citizenModel.index(0, 6), socialCredit)
        citizenModel.setData(citizenModel.index(0, 7), letzteAktualisierung)

#   method for building the characteristics view
    def buildCharacteristics(self, characteristicsModel, id, name, failings, chars, keystrokes, clicks, scp, update):
        characteristicsModel.setData(characteristicsModel.index(0, 0), "ID:")
        characteristicsModel.setData(characteristicsModel.index(1, 0), "Name:")
        characteristicsModel.setData(characteristicsModel.index(2, 0), "Verstöße:")
        characteristicsModel.setData(characteristicsModel.index(3, 0), "zuletzt geschrieben:")
        characteristicsModel.setData(characteristicsModel.index(4, 0), "Tasten pro Minute:")
        characteristicsModel.setData(characteristicsModel.index(5, 0), "Klicks pro Minute:")
        characteristicsModel.setData(characteristicsModel.index(6, 0), "Social-Credit-Score:")
        characteristicsModel.setData(characteristicsModel.index(7, 0), "zuletzt aktualisiert:")
        characteristicsModel.setData(characteristicsModel.index(0, 1), id)
        characteristicsModel.setData(characteristicsModel.index(1, 1), name)
        characteristicsModel.setData(characteristicsModel.index(2, 1), failings)
        characteristicsModel.setData(characteristicsModel.index(3, 1), chars)
        characteristicsModel.setData(characteristicsModel.index(4, 1), keystrokes)
        characteristicsModel.setData(characteristicsModel.index(5, 1), clicks)
        characteristicsModel.setData(characteristicsModel.index(6, 1), scp)
        characteristicsModel.setData(characteristicsModel.index(7, 1), update)

#   method for building the citizen datamodel
    def updateCitizenModel(self):

        self.citizenModel = QStandardItemModel(0, 8, self)

        self.citizenModel.setHeaderData(0, Qt.Horizontal, "ID")
        self.citizenModel.setHeaderData(1, Qt.Horizontal, "Name")
        self.citizenModel.setHeaderData(2, Qt.Horizontal, "Anzahl Verstöße")
        self.citizenModel.setHeaderData(3, Qt.Horizontal, "Verbrechen")
        self.citizenModel.setHeaderData(4, Qt.Horizontal, "Tastenanschläge / min")
        self.citizenModel.setHeaderData(5, Qt.Horizontal, "Klicks / min")
        self.citizenModel.setHeaderData(6, Qt.Horizontal, "Social-Credit-Punkte")
        self.citizenModel.setHeaderData(7, Qt.Horizontal, "letzte Aktualisierung")

        self.addEntry(self.citizenModel, 1, "Bürger9", 23, ''.join(["I","v","E","J","Z"]), 89, 67, 193, QDateTime(QDate(2020, 12, 31), QTime(17, 3)))
        
        return self.citizenModel

#   method for building characteristics data model  
    def createCharacteristicsModel(self, id, name, failings, chars, keystrokes, clicks, scp, update):
        charModel = QStandardItemModel(8,2, self)

        charModel.setHeaderData(0, Qt.Horizontal, "Übersicht")
        charModel.setHeaderData(1, Qt.Horizontal, "Daten")

        self.buildCharacteristics(charModel, id, name, failings, chars, keystrokes, clicks, scp, update)

        return charModel


class PasswordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle(" ")
        self.setWindowIcon(QIcon('./PSICO_Logo.svg'))
        self.resize(170, 30)
        
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        self.setCentralWidget(self.password)
        self.password.editingFinished.connect(self.validatePassword)

    def validatePassword(self):
        if self.password.text() == 'admin':
            self.window = Window()
            self.window.show()
            self.close()
            
#   main method for running the application
if __name__ == '__main__':
    app = QApplication()
    startWindow = PasswordWindow()
    startWindow.show()
    sys.exit(app.exec())