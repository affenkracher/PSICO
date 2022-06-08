from ctypes.wintypes import RGB
from multiprocessing import connection
from ssl import Options
from PSICO_Admin_Watcher import AdminWatcher
import sys
import os
from PySide6.QtCore import QDate, QDateTime, QRegularExpression, QSortFilterProxyModel, QTime, Qt
from PySide6.QtGui import QStandardItemModel, QIcon
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout, QLabel, QLineEdit, QTreeView, QWidget, QTabWidget, QAbstractItemView)

CWD = os.getcwd()

class Window(QTabWidget):

    def __init__(self, parent = None):
        super(Window, self).__init__(parent)

        self.admin_controller = AdminWatcher()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()

        self.tab1State = 0
        self.citizenModel = self.updateCitizenModel()

        self.addTab(self.tab1,"Bürgeranalyse")
        self.addTab(self.tab2,"Gesamtanalyse")
        self.addTab(self.tab3,"Heatmaps")

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()

        self.setTab1Model(self.citizenModel)
        self.setTab2Model(self.updateCitizenModel())
        self.setTab3Model(self.updateCitizenModel())
        
        self.setWindowTitle("PSICO Admin-Software")
        self.setWindowIcon(QIcon('./PSICO_Logo.svg'))
        self.resize(900, 450)
        

    # this is the view definition of the first tab
    def tab1UI(self):
        self.tab1.citizenListModel = QSortFilterProxyModel()
        self.tab1.citizenListModel.setDynamicSortFilter(True)

        self.tab1.citizenListView = QTreeView()
        self.tab1.citizenListView.setRootIsDecorated(False)
        self.tab1.citizenListView.setAlternatingRowColors(True)
        self.tab1.citizenListView.setModel(self.tab1.citizenListModel)
        self.tab1.citizenListView.setSortingEnabled(True)
        self.tab1.citizenListView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.tab1.sortCaseSensitivityCheckBox = QCheckBox("Case-sensitive Sortierung")
        self.tab1.filterCaseSensitivityCheckBox = QCheckBox("Case-sensitiver Filter")

        self.tab1.filterPatternLineEdit = QLineEdit()
        self.tab1.filterPatternLineEdit.setClearButtonEnabled(True)
        self.tab1.filterPatternLabel = QLabel("Filter (RegEx):")
        self.tab1.filterPatternLabel.setBuddy(self.tab1.filterPatternLineEdit)

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

        self.tab1.filterPatternLineEdit.textChanged.connect(self.filterPatternChanged)
        self.tab1.filterColumnComboBox.currentIndexChanged.connect(self.filterColumnChanged)
        self.tab1.filterCaseSensitivityCheckBox.toggled.connect(self.filterPatternChanged)
        self.tab1.sortCaseSensitivityCheckBox.toggled.connect(self.sortCaseSensitivityChanged)
        self.tab1.citizenListView.doubleClicked.connect(self.doubleClicked)

        self.tab1.citizenListView.sortByColumn(0, Qt.AscendingOrder)
        self.tab1.filterColumnComboBox.setCurrentIndex(1)
        self.tab1.filterPatternLineEdit.setText("")
        self.tab1.filterCaseSensitivityCheckBox.setChecked(True)
        self.tab1.sortCaseSensitivityCheckBox.setChecked(True)

        layout = QGridLayout()
        layout.addWidget(self.tab1.citizenListView, 0, 0, 1, 3)
        layout.addWidget(self.tab1.filterPatternLabel, 1, 0)
        layout.addWidget(self.tab1.filterPatternLineEdit, 1, 1, 1, 2)
        layout.addWidget(self.tab1.filterColumnLabel, 2, 0)
        layout.addWidget(self.tab1.filterColumnComboBox, 2, 1, 1, 2)
        layout.addWidget(self.tab1.filterCaseSensitivityCheckBox, 3, 0, 1, 2)
        layout.addWidget(self.tab1.sortCaseSensitivityCheckBox, 3, 1)
        self.tab1.setLayout(layout)

    def doubleClicked(self,index):

        if(self.tab1State == 0):

            id = index.siblingAtColumn(0)
            name = index.siblingAtColumn(1)
            failings = index.siblingAtColumn(2)
            chars = index.siblingAtColumn(3)
            keystrokes = index.siblingAtColumn(4)
            clicks = index.siblingAtColumn(5)
            scp = index.siblingAtColumn(6)
            update = index.siblingAtColumn(7)

            self.charViewUI(id.data(), name.data(), failings.data(), chars.data(), keystrokes.data(), clicks.data(), scp.data(), update.data())
            self.tab1State = 1
            print(self.tab1State)

        else:

            self.setTab1Model(self.citizenModel)
            self.tab1State = 0
            print(self.tab1State)
#            self.admin_controller.getAllCitizenInfo(self.admin_controller.getAllCitizen(self.admin_controller.connection))


    # this is the view definition of the second tab
    def tab2UI(self):
        self.tab2.totalsModel = QSortFilterProxyModel()
        self.tab2.totalsModel.setDynamicSortFilter(True)

        self.tab2.totalsView = QTreeView()
        self.tab2.totalsView.setRootIsDecorated(False)
        
        layout = QGridLayout()
        layout.addWidget(self.tab2.totalsView, 0, 0, 0, 0)
        self.tab2.setLayout(layout)

    # this is the view definition of the third tab
    def tab3UI(self):
        self.tab3.heatMapModel = QSortFilterProxyModel()
        self.tab3.heatMapModel.setDynamicSortFilter(True)

        self.tab3.heatmapView = QTreeView()
        self.tab3.heatmapView.setRootIsDecorated(False)
        
        layout = QGridLayout()
        layout.addWidget(self.tab3.heatmapView, 0, 0, 0, 0)
        self.tab3.setLayout(layout)

    def charViewUI(self, id, name, failings, chars, keystrokes, clicks, scp, update):
        self.tab1.charModel = QSortFilterProxyModel()
        self.tab1.charModel.setDynamicSortFilter(True)

        self.tab1.charView = QTreeView()
        self.tab1.charView.setRootIsDecorated(False)
        self.tab1.charView.setModel(self.tab1.charModel)
        self.tab1.charView.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.setTab1Model(self.createCharacteristicsModel(id, name, failings, chars, keystrokes, clicks, scp, update))

#        self.tab4.charModel.setSourceModel(self.createCharacteristicsModel(self, id, name, failings, chars, keystrokes, clicks, scp, update))

        layoutc = QGridLayout()
        layoutc.addWidget(self.tab1.charView, 0, 0, 0, 0)

        self.tab1.setLayout(layoutc)
        

    # the model is beeing connected to the tree views
    def setTab1Model(self, model):
        self.tab1.citizenListModel.setSourceModel(model)

    def setTab2Model(self, model):
        self.tab2.totalsModel.setSourceModel(model)

    def setTab3Model(self, model):
        self.tab3.heatMapModel.setSourceModel(model)

    # reaction on userchanges on the filter pattern 
    def filterPatternChanged(self):
        pattern = self.tab1.filterPatternLineEdit.text()
        reg_exp = QRegularExpression(pattern)
        if not self.tab1.filterCaseSensitivityCheckBox.isChecked():
            options = reg_exp.patternOptions()
            options |= QRegularExpression.CaseInsensitiveOption
            reg_exp.setPatternOptions(options)
        self.tab1.citizenListModel.setFilterRegularExpression(reg_exp)

    # reaction on userchanges on the filter column combo box
    def filterColumnChanged(self):
        self.tab1.citizenListModel.setFilterKeyColumn(self.tab1.filterColumnComboBox.currentIndex())

    # reaction on userchanges on the sort case sensitivity check box
    def sortCaseSensitivityChanged(self):
        if self.tab1.sortCaseSensitivityCheckBox.isChecked():
            caseSensitivity = Qt.CaseSensitive
        else:
            caseSensitivity = Qt.CaseInsensitive
        self.tab1.citizenListModel.setSortCaseSensitivity(caseSensitivity)


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


    def createCharacteristicsModel(self, id, name, failings, chars, keystrokes, clicks, scp, update):
        charModel = QStandardItemModel(8,2, self)

        charModel.setHeaderData(0, Qt.Horizontal, "Übersicht")
        charModel.setHeaderData(1, Qt.Horizontal, "Daten")

        self.buildCharacteristics(charModel, id, name, failings, chars, keystrokes, clicks, scp, update)

        return charModel


if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.show()
    sys.exit(app.exec())