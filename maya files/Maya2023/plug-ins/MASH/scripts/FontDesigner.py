from builtins import chr
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import json
import re

class FontDesigner(MayaQWidgetDockableMixin, qt.QWidget):

    #init and expand on QDialog
    def __init__(self, parent=None):
        from os import path as os_path
        super(FontDesigner, self).__init__(parent=parent)

        self.setWindowTitle("Font Designer")
        self.resize(pix(900),pix(600))

        mashPath = mel.eval('getenv("MASH_LOCATION")')
        self.fontsPath = os_path.join(mashPath, '3d Fonts')
        self.jsonData = None

        self.menuBar = qt.QMenuBar(self)

        self.horizontalLayoutWidget = qt.QWidget()
        self.horizontalLayoutWidget.setGeometry(qt.QRect(pix(0), pix(10), pix(801), pix(41)))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = qt.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(pix(0), pix(0), pix(0), pix(0))
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.fontNamesComboBox = qt.QComboBox(self.horizontalLayoutWidget)
        self.fontNamesComboBox.setObjectName("comboBox")
        self.fontNamesComboBox.setEditable(True)
        self.fontNamesComboBox.currentIndexChanged[str].connect(self.previewThisFont)
        self.horizontalLayout.addWidget(self.fontNamesComboBox)
        self.pushButton = qt.QPushButton(self.horizontalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.importFont)
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem = qt.QSpacerItem(pix(40), pix(20), qt.QSizePolicy.Expanding, qt.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        #self.pushButton_2 = qt.QPushButton(self.horizontalLayoutWidget)
        #self.pushButton_2.setObjectName("pushButton_2")
        #self.horizontalLayout.addWidget(self.pushButton_2)
        self.splitter = qt.QSplitter()
        self.splitter.setGeometry(qt.QRect(pix(0), pix(50), pix(801), pix(561)))
        self.splitter.setOrientation(qt.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.gridLayoutWidget = qt.QWidget(self.splitter)
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.thumbnailHorizontalLayout = qt.QHBoxLayout(self.gridLayoutWidget)
        self.gridLayout = QdIconView()
        self.thumbnailHorizontalLayout.addWidget(self.gridLayout)
        self.gridLayout.itemSelectionChanged.connect(self.updateGlyphInfo)

        self.gridLayout.setObjectName("gridLayout")

        self.rightSplitter = qt.QSplitter(self.splitter)
        self.rightSplitter.setGeometry(qt.QRect(pix(0), pix(0), pix(256), pix(384)))
        self.rightSplitter.setOrientation(qt.Qt.Vertical)
        self.rightSplitter.setObjectName("rightSplitter")

        self.verticalLayoutWidget = qt.QWidget(self.rightSplitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = qt.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(pix(0), pix(0), pix(0), pix(0))
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = qt.QTabWidget(self.verticalLayoutWidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = qt.QWidget()
        self.tab.setObjectName("tab")
        self.fontTabHorizontalLayout = qt.QHBoxLayout(self.tab)
        self.tableWidget = qt.QTableWidget()

        self.fontTabHorizontalLayout.addWidget(self.tableWidget, 1)
        tableHeader = self.tableWidget.horizontalHeader()
        tableHeader.setSectionResizeMode(qt.QHeaderView.Stretch)
        tableHeader.hide()

        self.infoWidget = qt.QTextEdit(self.rightSplitter)
        self.infoWidget.setObjectName("attributeListWidget")
        self.infoWidget.setReadOnly(True)

        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(1)
        self.tableWidget.setRowCount(6)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = qt.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = qt.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.glyphTabHorizontalLayout = qt.QHBoxLayout(self.tab_2)
        self.glyphTableWidget = qt.QTableWidget()

        self.glyphTabHorizontalLayout.addWidget(self.glyphTableWidget, 1)
        tableHeader = self.glyphTableWidget.horizontalHeader()
        tableHeader.setSectionResizeMode(qt.QHeaderView.Stretch);
        tableHeader.hide();
        self.glyphTableWidget.setColumnCount(1)
        self.glyphTableWidget.setRowCount(3)
        item = qt.QTableWidgetItem()
        self.glyphTableWidget.setVerticalHeaderItem(0, item)
        item = qt.QTableWidgetItem()
        self.glyphTableWidget.setVerticalHeaderItem(1, item)
        item = qt.QTableWidgetItem()
        self.glyphTableWidget.setVerticalHeaderItem(2, item)
        item = qt.QTableWidgetItem()
        self.glyphTableWidget.setHorizontalHeaderItem(0, item)
        self.verticalLayout.addWidget(self.tabWidget)

        self.createMenu = self.menuBar.addMenu("File")
        #self.createNetworkAction =  qt.QAction("Test", self.createMenu)
        #self.createMenu.addAction(self.createNetworkAction)

        self.tableWidget.verticalHeaderItem(0).setText("Font Name")
        self.tableWidget.verticalHeaderItem(1).setText("Font Creator")
        self.tableWidget.verticalHeaderItem(2).setText("Model Prefix")
        self.tableWidget.verticalHeaderItem(3).setText("Space Width")
        self.tableWidget.verticalHeaderItem(4).setText("Leading")
        self.tableWidget.verticalHeaderItem(5).setText("About")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), "Font")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2),"Glyph")
        self.pushButton.setText(qt.QApplication.translate("Widget", "Use Font", None, -1))
        #self.pushButton_2.setText(qt.QApplication.translate("Widget", "Add Glyph", None, -1))

        self.glyphTableWidget.verticalHeaderItem(0).setText("Glyph")
        self.glyphTableWidget.verticalHeaderItem(1).setText("Kerning")
        self.glyphTableWidget.verticalHeaderItem(2).setText("Id")

        self.splitter.setStretchFactor(1, 0)
        self.splitter.setSizes([pix(630),pix(270)])

        main_layout = qt.QVBoxLayout()
        main_layout.setContentsMargins(pix(2), pix(2), pix(2), pix(2))
        main_layout.setSpacing(pix(2))
        main_layout.addWidget(self.menuBar, 0)
        main_layout.addWidget(self.horizontalLayoutWidget,0)
        main_layout.addWidget(self.splitter,1)

        self.setLayout(main_layout)
        self.setMinimumWidth(pix(300))

        self.loadFonts()

    def loadFonts(self):
        from os import listdir as os_listdir
        foundFonts = []
        files = os_listdir(self.fontsPath)
        for possibleFont in files:
            if possibleFont.lower().endswith(('.3df')):
                self.fontNamesComboBox.addItem(possibleFont)

        self.previewThisFont()

    def previewThisFont(self):
        from os import path as os_path
        self.gridLayout.clear()

        thisFont = self.fontNamesComboBox.currentText()
        jsonPath = self.fontsPath+thisFont+"/Resources/data.json"
        if os_path.isfile(jsonPath):
            with open(jsonPath) as fontData:
                self.jsonData = json.load(fontData)
                self.setUpFontInUI()
        else:
            print("JSON not found: " + jsonPath)

    def setUpFontInUI(self):
        thisFont = self.fontNamesComboBox.currentText()
        fontMetaData = self.jsonData["metadata"]
        if "fontName" in fontMetaData:
            self.tableWidget.setItem(0,0, qt.QTableWidgetItem(self.jsonData["metadata"]["fontName"]))
        if "designer" in fontMetaData:
            self.tableWidget.setItem(1,0, qt.QTableWidgetItem(self.jsonData["metadata"]["designer"]))
        if "modelPrefix" in fontMetaData:
            self.tableWidget.setItem(2,0, qt.QTableWidgetItem(self.jsonData["metadata"]["modelPrefix"]))
        else:
            self.tableWidget.setItem(2,0, qt.QTableWidgetItem(""))
        if "spaceWidth" in fontMetaData:
            self.tableWidget.setItem(3,0, qt.QTableWidgetItem(str(self.jsonData["metadata"]["spaceWidth"])))
        else:
            self.tableWidget.setItem(3,0, qt.QTableWidgetItem(""))
        if "leadingHeight" in fontMetaData:
            self.tableWidget.setItem(4,0, qt.QTableWidgetItem(str(self.jsonData["metadata"]["leadingHeight"])))
        else:
            self.tableWidget.setItem(4,0, qt.QTableWidgetItem(""))

        self.infoWidget.clear()
        if "notes" in fontMetaData:
            self.infoWidget.setText(self.jsonData["metadata"]["notes"])

        for glyph in self.jsonData["glyphs"]:
            if "preview" in glyph:
                imagePath = self.fontsPath+thisFont+"/Resources/Images/"+glyph["preview"]
                itm = ListItem( HexToUni(str(glyph["unicode"])) )
                itm.setIcon(qt.QPixmap(imagePath));
                if "id" in glyph:
                    itm.id = glyph["id"]
                itm.unicode = glyph["unicode"]
                itm.kerning = glyph["kerning"]

                self.gridLayout.addItem(itm);

    def importFont(self):
        from os import listdir as os_listdir
        thisFont = self.fontNamesComboBox.currentText()
        modelsPath = self.fontsPath+thisFont+"/Resources/3d/"
        files = os_listdir(modelsPath)
        modelsToLoad = []
        for model in files:
            if model.lower().endswith(('.fbx')):
                modelsToLoad.append(model)

        namespace = re.sub('[^A-Za-z]+', '', thisFont)
        addedNodes = []
        for model in modelsToLoad:
            modelPath = modelsPath+model
            nodes = cmds.file( modelPath, r=True, type='FBX', namespace=namespace, returnNewNodes=True )
            addedNodes.extend(nodes)

        instancer = cmds.createNode('instancer')
        fontNode = cmds.createNode('MASH_Font')
        cmds.addAttr (instancer, longName='instancerMessage', at='message')
        cmds.addAttr (fontNode, longName='instancerMessage', at='message')

        # Add the models to the instancer
        # Todo: Base this on the ID (add the ID to the JSON array ourselves, and set this to the MASH_Font node). Remove ID from the JSON.
        if len(self.jsonData["glyphs"]):
            objId = 0
            for glyph in self.jsonData["glyphs"]:
                modelName = namespace+":"+glyph['model']
                cmds.instancer( instancer, e=True, a=True, object=modelName )
                cmds.hide(modelName)
                glyph["id"] = objId
                objId += 1

        cmds.connectAttr ((fontNode+".outputPoints"),(instancer+".inputPoints"), force=True)

        cmds.setAttr((fontNode+".fontJSON"), json.dumps(self.jsonData), type='string')

        cmds.connectAttr ((fontNode+".instancerMessage"),(instancer+".instancerMessage"), force=True)

        if len(self.jsonData["glyphs"]):
            firstGlyphUnicode = str(self.jsonData["glyphs"][0]['unicode'])
            #set default text, which is the first glyph in the font
            cmds.setAttr((fontNode+".inputText"), firstGlyphUnicode, type='string')

    def updateGlyphInfo(self):
        # get the current gylph
        item = self.gridLayout.selectedItems()
        if len(item) == 1:
            item = self.gridLayout.selectedItems()
            self.glyphTableWidget.setItem(0, 0, qt.QTableWidgetItem(str(item[0].unicode)))
            self.glyphTableWidget.setItem(1, 0, qt.QTableWidgetItem(str(item[0].kerning)))
            self.glyphTableWidget.setItem(2, 0, qt.QTableWidgetItem(str(item[0].id)))
        else:
            self.glyphTableWidget.setItem(0,0, qt.QTableWidgetItem(""))
            self.glyphTableWidget.setItem(1,0, qt.QTableWidgetItem(""))
            self.glyphTableWidget.setItem(2,0, qt.QTableWidgetItem(""))


def HexToUni( hexStr ):
    bytes = []

    hexStr = hexStr.split(" ")

    for hexChar in hexStr:
        ordNum = int(hexChar, 16)
        bytes.append(chr(ordNum))

    return ''.join( bytes )

#load up window
def showFontDesigner():
    ui = FontDesigner(parent=fx.mayaWindow())
    ui.setWindowFlags(qt.Qt.Window) # Make this widget a standalone window even though it is parented
    ui.setProperty("saveWindowPref", True ) # identify a Maya-managed floating window, which handles the z order properly and saves its positions

    ui.show(dockable=True)

class QdIconView(qt.QListWidget):
    def __init__(self, parent=None):
        qt.QListWidget.__init__(self, parent)

        self.setIconSize(qt.QSize(pix(160), pix(90))) # or setGridSize
        self.setViewMode(qt.QListView.IconMode)
        self.setMovement(qt.QListView.Static)
        self.setResizeMode(qt.QListView.Adjust) # re-lays out the items on resize
        self.setLayoutMode(qt.QListView.Batched) # does the layout with a timer for better performance
        self.setWrapping(True) # wraps the items to the next line so theres no horiz scrollbar
        self.setDragEnabled(True) # in case you want drag and drop
        self.setSpacing(pix(1)) # spacing between each item, buggy in Qt < 4.7 but works with small #'s

class ListItem(qt.QListWidgetItem):
    def __init__(self, text):
        qt.QListWidgetItem.__init__(self, text)
        self.string = text
        self.unicode = 0
        self.kerning = 0
        self.id = 0

# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
