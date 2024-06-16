from __future__ import division
from builtins import object
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import MASH.utils as utils
import MASH.api as mapi

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.internal.common.qt.doubleValidator import MayaQclocaleDoubleValidator

import json
import random
import collections

###############
# Window API
###############
if not 'windowInstance' in globals():
    windowInstance = None

def windowClosed (object=None):
    if windowInstance:
        windowInstance.close()
    windowDestroyed()

def windowDestroyed (object=None):
    global windowInstance
    windowInstance = None

def showWindow(worldNode):
    global windowInstance

    uuid = cmds.ls(worldNode, uuid=True)[0]

    windowType = GenotypeCreator
    args = {'uuid': uuid}
    closeScript = 'import MASH.genotypeCreator; MASH.genotypeCreator.windowClosed()'

    if windowInstance == None:
        windowInstance = windowType(parent=fx.mayaWindow(), **args)
        windowInstance.setWindowFlags(qt.Qt.Window)
        windowInstance.setProperty("saveWindowPref", True)
        windowInstance.destroyed.connect(windowDestroyed)
        windowInstance.flushScrJob = cmds.scriptJob(ct=['flushingScene', closeScript], runOnce=True)

    windowInstance.reinit(uuid)
    windowInstance.show(dockable=True, save=False, plugins='MASH', closeCallback=closeScript)

    windowInstance.window().raise_()
    windowInstance.raise_()
    windowInstance.activateWindow()
    return windowInstance

# ==============
# STRING RESOURCES
def getResource(name):
    value = name
    try:
        value = mel.eval('getPluginResource("MASH", "' + name + '")')
    except:
        pass

    return value

_SR = {
    'Age': getResource('kGeno_Age'),
    'Seed Age': getResource('kGeno_Seed_Age'),
    'Seed Count': getResource('kGeno_Seed_Count'),
    'Rate': getResource('kGeno_Rate'),
    'Id': getResource('kGeno_Id'),
    'Id Min': getResource('kGeno_Id_Min'),
    'Id Max': getResource('kGeno_Id_Max'),
    'Size': getResource('kGeno_Size'),
    'Slope': getResource('kGeno_Slope'),
    'Variance': getResource('kGeno_Variance'),
    'Id Color': getResource('kGeno_Id_Color'),
    'Temperature': getResource('kGeno_Temperature'),
    'Soil Quality': getResource('kGeno_Soil_Quality'),
    'Moisture': getResource('kGeno_Moisture'),
    'Resilience': getResource('kGeno_Resilience'),
    'Name': getResource('kGeno_Name'),
    'Defaults': getResource('kGeno_Defaults'),
    'Genotype Editor': getResource('kGeno_GEditor'),
    'Add Genotype': getResource('kGeno_Add_Geno'),
    'Update Simulation': getResource('kGeno_Update_Sim'),
    'Presets': getResource('kGeno_Presets'),
    'Copy': getResource('kGeno_Copy'),
    'Randomize': getResource('kGeno_Randomize'),
    'Rename': getResource('kGeno_Rename'),
    'Duplicate': getResource('kGeno_Duplicate'),
    'Delete': getResource('kGeno_Delete'),
    'Auto Size Model': getResource('kGeno_AutoSize'),
    'Red Maple': "Red Maple",
    'English Oak': "English Oak"
}

# key: [displayName, datatype, min, max]
kProperties = collections.OrderedDict()
kProperties['Age'] = ['Max. Age', 'int']
kProperties['Seed Age'] = ['Seed Age', 'int']
kProperties['Seed Count'] = ['Seed Count', 'int']
kProperties['Rate'] = ['Growth Rate', 'float']
kProperties['Size'] = ['Model Size', 'float']
kProperties['Slope'] = ['Slope Threshold', 'float', 0, 1]
kProperties['Variance'] = ['Rand Variance', 'float', 0, 1]
kProperties['Temperature'] = ['Temperature', 'float', 0, 1]
kProperties['Soil Quality'] = ['Soil Quality', 'float', 0, 1]
kProperties['Moisture'] = ['Moisture', 'float', 0, 1]
kProperties['Resiliance'] = ['Resiliance', 'float', 0, 1]
kProperties['Id'] = ['Object ID', 'int']
kProperties['Id Min'] = ['Min ID', 'int']
kProperties['Id Max'] = ['Max ID', 'int']
kProperties['Id Color'] = ['ID Color', 'color']

DEFAULTS = {
    'Name': 'Genotype',
    'Age': 100,
    'Seed Age': 10,
    'Seed Count': 4,
    'Rate': 0.12,
    'Id': 0,
    'Id Min':0,
    'Id Max':0,
    'Size': 10.0,
    'Slope': 0.5,
    'Variance': 0.2,
    'Id Color': (0.0,0.0,0.0),
    'Temperature':0.5,
    'Soil Quality': 0.5,
    'Moisture': 0.5,
    'Resiliance': 0.2
}

ENGLISHOAK = {
    'Name': 'English Oak',
    'Age': 600,
    'Seed Age': 40,
    'Seed Count': 10,
    'Rate': 0.08,
    'Id': 0,
    'Id Min':0,
    'Id Max':0,
    'Size': 40.0,
    'Slope': 0.3,
    'Variance': 0.15,
    'Id Color': (0.0,0.0,0.0),
    'Temperature':0.4,
    'Soil Quality': 0.4,
    'Moisture': 0.6,
    'Resiliance': 0.1
}

REDMAPLE = {
    'Name': 'Red Maple',
    'Age': 200,
    'Seed Age': 6,
    'Seed Count': 6,
    'Rate': 0.16,
    'Id': 0,
    'Id Min':0,
    'Id Max':0,
    'Size': 23.0,
    'Slope': 0.3,
    'Variance': 0.15,
    'Id Color': (0.0,0.0,0.0),
    'Temperature':0.5,
    'Soil Quality': 0.5,
    'Moisture': 0.5,
    'Resiliance': 0.4
}

PRESETS = {
    'Defaults' : DEFAULTS,
    'English Oak' : ENGLISHOAK,
    'Red Maple' : REDMAPLE
}

def setWidgetBackgroundColor(widget, color):
    palette = widget.palette()
    palette.setColor(qt.QPalette.Window, color)
    widget.setAutoFillBackground(True)
    widget.setPalette(palette)

def updateWidgetPalette(widget, role, color):
    palette = widget.palette()
    palette.setColor(role, color)
    widget.setPalette(palette)

class ColorEdit(qt.QLineEdit):
    clicked = qt.Signal()

    def __init__(self):
        super(ColorEdit, self).__init__()
        self.installEventFilter(self)

    def eventFilter(self, eobj, event):
        self.clearFocus()
        if (eobj is self):
            if(event.type() == qt.QEvent.MouseButtonPress):
                self.clicked.emit()
                return True
            if(event.type() == qt.QEvent.Paint):
                return False
        return True

class GenotypeBaseProperty(qt.QWidget):
    def __init__(self,name):
        super(GenotypeBaseProperty, self).__init__()

        self.setStyleSheet("QLineEdit { border: none }"); # Removes QLineEdit border
        self.setLayout(qt.QHBoxLayout())
        self.layout().setContentsMargins(pix(15),pix(2),pix(2),pix(2))

        self.layout().addWidget(qt.QLabel(name))
        self.layout().addStretch()

        palette = self.palette()
        palette.setColor(qt.QPalette.Window, qt.QListWidget().palette().window().color())
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        self.setFixedHeight(pix(28))

class GenotypeProperty(GenotypeBaseProperty):
    changed = qt.Signal()

    def __init__(self,name,info):
        super(GenotypeProperty, self).__init__(name)
        self.lineEdit = qt.QLineEdit()
        self.lineEdit.setFixedHeight(pix(24))
        self.lineEdit.setMaximumWidth(pix(122))
        self.lineEdit.editingFinished.connect(self.textEdited)
        self.info = info
        self.setupValidator()
        self.layout().addWidget(self.lineEdit)

    def setupValidator(self):
        validator = None
        if self.info[1] == 'int':
            validator = qt.QIntValidator()
        elif self.info[1] == 'float':
            validator = MayaQclocaleDoubleValidator()
        if len(self.info) > 2: validator.setBottom(self.info[2])
        if len(self.info) > 3: validator.setTop(self.info[3])
        self.lineEdit.setValidator(validator)

    def value(self):
        if self.info[1] == 'int':
            return int(self.lineEdit.text())
        elif self.info[1] == 'float':
            return float(self.lineEdit.text())

    def setValue(self, value):
        self.lineEdit.setText(str(value))

    def textEdited(self):
        self.changed.emit()
        self.lineEdit.clearFocus()

class GenotypeColorProperty(GenotypeBaseProperty):
    changed = qt.Signal()

    def __init__(self,name):
        super(GenotypeColorProperty, self).__init__(name)
        self.colorPicker = ColorEdit()
        self.colorPicker.setFixedHeight(pix(24))
        self.colorPicker.setMaximumWidth(pix(122))
        self.colorPicker.setAutoFillBackground(True)
        self.setColor([0,0,0])
        self.colorPicker.clicked.connect(self.colorPickerClicked)
        self.layout().addWidget(self.colorPicker)

    def colorPickerClicked(self):
        cmds.colorEditor()

        if not cmds.colorEditor(query=True, result=True):
            return

        values = cmds.colorEditor(query=True, rgb=True)
        self.setColor([int(x * 255) for x in values])

        self.changed.emit()

    def updateButtonColor(self):
        #color = qt.QColor(*self._color)
        #role = qt.QPalette.Window
        #updateWidgetPalette(self.colorPicker, role, color)
        self.colorPicker.setStyleSheet("QLineEdit { background-color: rgba(%d,%d,%d,255); }" % (self._color[0], self._color[1], self._color[2]));

    def setColor(self, color):
        self._color = color
        self.updateButtonColor()

    def color(self):
        return self._color

    def value(self):
        return self.color()

    def setValue(self, value):
        self.setColor(value)

class GenotypeCreator(MayaQWidgetDockableMixin, qt.QDialog):

    def __init__(self, parent=None, uuid=None):
        super(GenotypeCreator, self).__init__(parent)
        self.genotypeData = GenotypeInstance(uuid)
        self.lastSelection = None
        self.setupUI()

    def closeEvent(self, event):
        windowClosed()

    def reinit(self, uuid):
        self.genotypeData = GenotypeInstance(uuid)
        self.refreshGenotypes()
        self.refreshProperties()

        self.listWidget.item(0).setSelected(True)
        self.lastSelection = self.getSelectedRows()

    def refreshGenotypes(self):
        selection = self.getSelectedRows()
        self.listWidget.clear()
        genotypeNames = self.genotypeData.getGenotypeNames()
        row = 0
        for name in genotypeNames:
            item = self.createGenotypeItem(name)
            item.color = qt.QColor(*self.genotypeData.getColorBar(row))
            row += 1
        self.lastSelection = selection
        for row in self.lastSelection:
            if row < self.listWidget.count():
                self.listWidget.item(row).setSelected(True)

    def refreshProperties(self):
        row = self.getCurrentRow()
        for key in list(self.propertyWidgets.keys()):
            prop = self.propertyWidgets[key]
            prop.setValue(self.genotypeData.getValue(row, key))

    def setupUI(self):
        #Window setup
        self.setGeometry(pix(600), pix(300), pix(600), pix(600))
        self.setWindowTitle(_SR['Genotype Editor'])
        self.setLayout(qt.QVBoxLayout())
        self.layout().setContentsMargins(pix(2),pix(2),pix(2),pix(2))
        self.layout().setSpacing(pix(1))

        # Top Bar
        topWidget = qt.QWidget()
        topWidget.setLayout(qt.QHBoxLayout())
        self.layout().addWidget(topWidget, 0)
        self.topBar = topWidget.layout()
        self.topBar.setContentsMargins(pix(10),pix(10),pix(10),pix(10))

        self.createButton = fx.ImageButton("out_MASH_AddLayer", '')
        self.createButton.clicked.connect(self.createGenotype)
        self.createButton.setToolTip(_SR['Add Genotype'])

        self.updateButton = fx.ImageButton("out_MASH_Refresh", '')
        self.updateButton.clicked.connect(self.updateSimulation)
        self.updateButton.setToolTip(_SR['Update Simulation'])

        self.topBar.addWidget(self.createButton)
        self.topBar.addWidget(self.updateButton)
        self.topBar.addStretch()

        # Split Widget
        self.splitter = qt.QSplitter(qt.Qt.Horizontal)
        self.layout().addWidget(self.splitter, 1)

        self.listWidget = fx.ListButtonWidget()
        self.listWidget.dataDelegate = self
        self.listWidget.showToggleButton = False

        # Properties
        propertiesScroll = qt.QScrollArea()
        propertiesScroll.setWidgetResizable(True)

        properties = qt.QWidget()
        propertiesScroll.setWidget(properties)

        properties.setLayout(qt.QVBoxLayout())
        listWidgetBaseColor = self.listWidget.palette().color(qt.QPalette.Base)
        updateWidgetPalette(properties, qt.QPalette.Window, listWidgetBaseColor)
        properties.layout().setContentsMargins(pix(2),pix(2),pix(2),pix(2))

        self.propertyWidgets = {}
        for key in list(kProperties.keys()):
            info = kProperties[key]

            widget = None
            if info[1] == 'float' or info[1] == 'int':
                widget = GenotypeProperty(info[0], info)
            elif info[1] == 'color':
                widget = GenotypeColorProperty(info[0])

            widget.changed.connect(lambda pkey=key: self.propertyChanged(pkey))
            self.propertyWidgets[key] = widget
            properties.layout().addWidget(widget)

        properties.layout().addStretch()
        properties.layout().setSpacing(pix(2))

        self.splitter.addWidget(self.listWidget)
        self.splitter.addWidget(propertiesScroll)

    # Delegates
    def dropEvent(self, event):
        pass
    def buttonPressed(self, index, buttonName):
        pass
    def doubleClick(self, index, buttonName):
        if buttonName=='textField':
            self.listWidget.edit(index)
    def setupTreeMenu(self, treeMenu, position):
        index = self.listWidget.indexAt(position)

        rows = self.getSelectedRows()

        labelIcon = qt.QIcon(fx.fluxIcons['Create'])
        treeMenu.addAction(labelIcon, _SR['Add Genotype'], self.createGenotype)

        if len(rows)>0 and index.row()>=0:
            # Color Bar
            currentItem = self.listWidget.item(rows[-1])
            labelIcon = fx.createColorIcon(qcolor=currentItem.color)
            colorMenu = treeMenu.addMenu(labelIcon, fx.colorLabel('kLabelColour'))
            for color in fx.allColorLabels():
                labelIcon = fx.createColorIcon(color)
                colorMenu.addAction(labelIcon, color, lambda prm=color: self.setLabelColor(prm))

            # Presets
            presetsIcon = fx.getIconFromName('out_MASH_Utilities')
            presetsMenu = treeMenu.addMenu(presetsIcon, _SR['Presets'])
            for key in list(PRESETS.keys()):
                presetsMenu.addAction(presetsIcon, _SR[key], lambda preset=PRESETS[key]: self.loadPresetIntoGenotype(preset))

            treeMenu.addAction(fx.getIconFromName('out_MASH_ChannelRandom'), _SR['Randomize'], self.randomizeGenotype)
            treeMenu.addAction(fx.getIconFromName('out_MASH_SetModelSize'), _SR['Auto Size Model'], self.setModelSize)
            treeMenu.addAction(fx.getIconFromName('out_MASH_Options'), _SR['Rename'], self.renameGenotype)
            treeMenu.addAction(fx.getIconFromName('out_MASH_Duplicate'), _SR['Duplicate'], self.duplicateGenotype)
            treeMenu.addAction(fx.getIconFromName('out_MASH_Delete'), _SR['Delete'], self.deleteGenotype)
    def selectionChanged(self):
        if len(self.getSelectedRows()) == 0:
            for row in self.lastSelection:
                self.listWidget.item(row).setSelected(True)
        self.lastSelection = self.getSelectedRows()
        self.refreshProperties()

    # Utilities
    def getSelectedRows(self):
        selectedIndexes = self.listWidget.selectionModel().selectedRows()
        return [i.row() for i in selectedIndexes]

    def getCurrentRow(self):
        selectedRows = self.getSelectedRows()
        if len(selectedRows) > 0:
            return selectedRows[-1]
        return 0

    # Events
    def propertyChanged(self, key):
        rows = self.getSelectedRows()
        value = self.propertyWidgets[key].value()
        for row in rows:
            self.genotypeData.setValue(row, key, value)

    def itemTextChangedAtIndex(self, index, oldValue, newValue):
        if len(newValue)==0:
            return oldValue
        else:
            self.genotypeData.setValue(index.row(), 'Name', newValue)
            return newValue

    def createGenotypeItem(self, name):
        item = fx.ListButtonItem(name, self.listWidget)
        self.listWidget.addItem(item)
        return item

    def createGenotype(self):
        name = self.genotypeData.addGenotype()
        self.createGenotypeItem(name)

    def updateSimulation(self):
        self.genotypeData.updateSimulation()

    def renameGenotype(self):
        item = self.listWidget.currentItem()
        if item:
            self.listWidget.editItem(item)

    def loadPresetIntoGenotype(self, preset):
        rows = self.getSelectedRows()
        for row in rows:
            self.genotypeData.loadPresetIntoRow(row, preset)
        self.refreshGenotypes()
        self.refreshProperties()

    def duplicateGenotype(self):
        selectedRows = self.getSelectedRows()
        for row in selectedRows:
            item = self.listWidget.item(row)
            newName = item.text() + ' ' + _SR['Copy']
            self.createGenotypeItem(newName)
            self.genotypeData.duplicateRow(row)

    def deleteGenotype(self):
        rows = self.getSelectedRows()
        if len(rows) == self.genotypeData.getCount():
            del rows[-1]

        for i in sorted(rows, reverse=True):
            self.listWidget.takeItem(i)
        self.genotypeData.removeGenotypes(rows)
        self.refreshProperties()

    def randomizeGenotype(self):
        selectedRows = self.getSelectedRows()
        self.genotypeData.randomizeGenotypes(selectedRows)
        self.refreshProperties()

    def setModelSize(self):
        selectedRows = self.getSelectedRows()
        self.genotypeData.setModelSizes(selectedRows)
        self.refreshProperties()

    def setLabelColor(self, color):
        rows = self.getSelectedRows()
        for row in rows:
            item = self.listWidget.item(row)
            item.color = fx.getColourFromLabel(color)
            self.genotypeData.setColorBar(row, [item.color.red(), item.color.green(), item.color.blue()])
        self.listWidget.viewport().update()

class GenotypeInstance(object):
    def __init__(self, uuid):
        self.uuid = uuid

        self.genotypeDict = DEFAULTS

        self.jsonData = self.getData()

    def addGenotype(self):
        self.jsonData.append(self.genotypeDict.copy())
        self.saveData()
        return self.jsonData[-1]['Name']

    def removeGenotypes(self, indexes):
        for i in sorted(indexes, reverse=True):
            del self.jsonData[i]
        self.saveData()

    def randomizeGenotypes(self, indexes):
        for i in indexes:
            genotype = self.jsonData[i]
            genotype['Age'] = random.randrange(30, 200)
            genotype['Seed Age'] = random.randrange(1, int(genotype['Age']*0.2))
            genotype['Seed Count'] = random.randrange(1, 6)
            idealRate = (1.0/genotype['Age'])*2
            rate = round(idealRate*random.uniform(0.7, 1.3),3)
            genotype['Rate'] = rate
            genotype['Slope'] = round(random.uniform(0.3, 0.9),3)
            genotype['Variance'] = round(random.uniform(0.0, 0.3),3)
            genotype['Temperature'] = round(random.uniform(0.3, 0.7),3)
            genotype['Soil Quality'] = round(random.uniform(0.3, 0.7),3)
            genotype['Moisture'] = round(random.uniform(0.3, 0.7),3)
            genotype['Resiliance'] = round(random.uniform(0.0, 0.2),3)
        self.saveData()

    def setModelSizes(self, indexes):
        nodeName = self.getName()
        networkNodes = utils.getNetworkFromNode(nodeName)
        instancer = None
        for node in networkNodes:
            if cmds.nodeType(node) == "MASH_Waiter":
                instancer = cmds.listConnections(node+".instancerMessage")[0] or None

        if not instancer:
            return

        for i in indexes:
            genotype = self.jsonData[i]

            idToGet = genotype['Id Max']
            if idToGet == 0:
                idToGet = genotype['Id']

            size = self.getModelSizeFromInstancer(idToGet, instancer)
            genotype['Size'] = size

        self.saveData()

    def getModelSizeFromInstancer(self, index, instancer):
        inputNode = None
        if cmds.nodeType(instancer) == "instancer":
            conns = cmds.listConnections(instancer+".inputHierarchy")
            if len(conns) > index:
                inputNode = conns[index]
        elif cmds.nodeType(instancer) == "MASH_Repro":
            conns = cmds.listConnections('MASH1_Repro.instancedGroup['+str(index)+'].groupMessage')
            if conns:
                inputNode = conns[0]

        bbox = cmds.exactWorldBoundingBox(inputNode)
        xAxis = bbox[3]-bbox[0]
        zAxis = bbox[5]-bbox[2]
        return round((xAxis+zAxis)*.5, 3)


    def loadPresetIntoRow(self, row, preset):
        for key in list(preset.keys()):
            self.jsonData[row][key] = preset[key]
        self.saveData()

    def duplicateRow(self, row):
        data = self.jsonData[row].copy()
        self.jsonData.append(data)
        self.saveData()

    def getCount(self):
        return len(self.jsonData)

    def getGenotypeNames(self):
        return [g['Name'] for g in self.jsonData]

    def getValue(self, row, key):
        return self.jsonData[row][key]

    def setValue(self, row, key, value):
        self.jsonData[row][key] = value
        self.saveData()

    def getColorBar(self, row):
        if 'colorBar' not in self.jsonData[row]:
            self.setColorBar(row, [255,255,255])
        return self.jsonData[row]['colorBar']

    def setColorBar(self, row, color):
        self.jsonData[row]['colorBar'] = color
        self.saveData()

    def updateSimulation(self):
        cmds.dgdirty(self.getName())

    def saveData(self):
        cmds.setAttr(self.getName() + '.genotypeJSON', json.dumps(self.jsonData), type='string')

    def getData(self):
        jsonRaw = cmds.getAttr(self.getName() + '.genotypeJSON')
        if len(jsonRaw):
            return json.loads(jsonRaw)
        return []

    def getName(self):
        return cmds.ls(self.uuid, long=True)[0]# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
