from builtins import int
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

#from MayaToAE.client import AEClient
from MayaToAE.callbacks import AECallbacksManager
import MayaToAE.utils as AEUtils
import MayaToAE.client
from MayaToAE.client import AEClient

import maya.OpenMayaUI as omui
import maya.api.OpenMayaAnim as oma
import math
import time
import json
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from maya.internal.common.qt.doubleValidator import MayaQclocaleDoubleValidator


#import sys
#sys.stdout = sys.__stdout__
#dir(sys.stdout)

if not 'liveLinkWindow' in globals():
    liveLinkWindow = None

# ==============
# STRING RESOURCES
def getResource(name):
    return mel.eval('getPluginResource("MASH", "' + name + '")')

_SR = {
    'AE Live Link': getResource('kM2AE_Title'),
    'Pause': getResource('kM2AE_Pause'),
    'Push all': getResource('kM2AE_Push_All'),
    'Sync Timeline': getResource('kM2AE_SyncT'),
    'Import': getResource('kM2AE_Import'),
    'Export': getResource('kM2AE_Export'),
    'Advanced': getResource('kM2AE_Advanced'),
    'Set IP': getResource('kM2AE_Set_IP'),
    'Global Scale:': getResource('kM2AE_Global_Scale'),
    'Remove': getResource('kM2AE_Remove'),
    'Invalid Import File': getResource('kM2AE_Invalid_Import'),
    'Closed AE Live Link': getResource('kM2AE_Closed_AE'),
    'Preferences Mismatch': getResource('kM2AE_Preferences_Mismatch'),
    'Would you like to override the composition\'s preferences?': getResource('kM2AE_Override'),
    'Yes': getResource('kM2AE_Yes'),
    'No': getResource('kM2AE_No'),
    'Waiting for connection...': getResource('kM2AE_Waiting_Conn'),
    'Disconnected': getResource('kM2AE_Disconnected'),
    'Connected to': getResource('kM2AE_Connected_To') 
}

class AELiveLink(MayaQWidgetDockableMixin, qt.QDialog):
    callbacksManager = None
    syncPrefs = True
    samePrefs = True

    def __init__(self, parent=None):
        super(AELiveLink, self).__init__(parent)

        self.setupUI()
        self.client = AEClient()
        self.client.receiver.connect(self.linkReceiver)
        self.initCallbackManager()

        self.setupData()
        self.initLink()
        self.callbacksManager.registerCallbacks()
        self.callbacksManager.registerSceneCloseCallbacks()

######################
# Setup UI - start
######################

    def setupUI(self):
        objNamePrefix = 'MayaToAdobeAfterEffects' + str(time.time())
        #Window setup
        self.setGeometry(pix(600), pix(300), pix(305), pix(310))
        self.topLayout = qt.QHBoxLayout()
        self.topLayout.setObjectName(objNamePrefix + 'WindowLayout')
        self.topLayout.setContentsMargins(pix(0),pix(0),pix(0),pix(0))
        self.setLayout(self.topLayout)
        self.setWindowTitle(_SR['AE Live Link'])
        self.setObjectName(objNamePrefix + 'Window')

        #Scroll area
        self.scroll = qt.QScrollArea()
        self.scroll.setObjectName(objNamePrefix + 'WindowLayoutScrollArea')
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(qt.QFrame.NoFrame);
        self.topLayout.addWidget(self.scroll)

        #Scroll area widget
        self.scrollWidget = qt.QWidget()
        self.scroll.setWidget(self.scrollWidget)

        #Scroll area widget layout
        self.scrollLayout = qt.QVBoxLayout()
        self.scrollLayout.setObjectName(objNamePrefix + 'WindowLayoutScrollAreaLayout')
        self.scrollWidget.setLayout(self.scrollLayout)

        #Label notifying composition name
        self.compNameLabel = qt.QLabel('')
        self.compNameLabel.setContentsMargins(pix(6), pix(6), pix(6), pix(6))
        self.compNameLabel.setStyleSheet("background-color : rgba(75,75,75, 1); border-radius: %dpx;" % pix(3))
        self.scrollLayout.addWidget(self.compNameLabel, 0)

        #List widget
        self.listWidget = fx.DraggableListWidget()
        self.listWidget.viewport().installEventFilter(self)
        self.listWidget.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.listWidget.customContextMenuRequested.connect(self.openTreeMenu)
        self.scrollLayout.addWidget(self.listWidget)
        p = self.listWidget.sizePolicy()
        p.setVerticalStretch(1)
        self.listWidget.setSizePolicy(p)
        self.listWidget.setMinimumHeight(pix(200))

        #Buttons
        self.buttonsWidget = qt.QWidget()
        self.scrollLayout.addWidget(self.buttonsWidget)
        self.buttons = qt.QHBoxLayout()
        self.buttons.setContentsMargins(pix(6),pix(3),pix(6),pix(3))
        self.buttonsWidget.setLayout(self.buttons)

        #Refresh button
        self.pauseButton = fx.ImageButton("Maya-AE_Pause")
        self.pauseButton.clicked.connect(self.pauseClicked)
        self.pauseButton.setToolTip(_SR["Pause"])
        self.buttons.addWidget(self.pauseButton)

        #Refresh button
        self.refreshButton = fx.ImageButton("Maya-AE_Push")
        self.refreshButton.clicked.connect(self.refreshClicked)
        self.refreshButton.setToolTip(_SR["Push all"])
        self.refreshButton.bgFadeOnPress = True
        self.buttons.addWidget(self.refreshButton)

        #SyncPrefs button
        self.syncTimeline = fx.ImageButton("Maya-AE_SyncTimeline")
        self.syncTimeline.clicked.connect(self.timeSyncChanged)
        self.syncTimeline.setToolTip(_SR["Sync Timeline"])
        self.buttons.addWidget(self.syncTimeline)

        self.buttons.addStretch()

        #Import button
        self.importButton = fx.ImageButton("Maya-AE_Import")
        self.importButton.clicked.connect(self.importClicked)
        self.importButton.setToolTip(_SR["Import"])
        self.buttons.addWidget(self.importButton)

        #Export button
        self.exportButton = fx.ImageButton("Maya-AE_Export")
        self.exportButton.clicked.connect(self.export)
        self.exportButton.setToolTip(_SR["Export"])
        self.buttons.addWidget(self.exportButton)

        self.dropDownWidget = fx.FrameWidget(_SR['Advanced'])
        self.dropDownWidget.switched.connect(self.dropDownSwitched)
        self.scrollLayout.addWidget(self.dropDownWidget, 0)

        #Change ip button
        self.changeIPWidget = qt.QWidget()
        self.changeIPLayout = qt.QHBoxLayout()
        self.changeIPLayout.setContentsMargins(pix(0), pix(0), pix(0), pix(0))
        self.changeIPLayout.setSpacing(pix(5))
        self.changeIPWidget.setLayout(self.changeIPLayout)
        self.dropDownWidget.addWidget(self.changeIPWidget)

        self.changeIPField = qt.QLineEdit()
        self.changeIPField.setFrame(False)
        self.changeIPField.setText('localhost')
        self.changeIPField.setFixedHeight(pix(20))
        self.changeIPLayout.addWidget(self.changeIPField,1)
        self.changeIPButton = qt.QPushButton(_SR['Set IP'], self)
        self.changeIPButton.setFixedHeight(pix(20))
        self.changeIPButton.setFixedWidth(pix(75))
        self.changeIPButton.clicked.connect(self.ipChanged)
        self.changeIPLayout.addWidget(self.changeIPButton, 0)

        self.globalScaleWidget = qt.QWidget()
        self.globalScaleLayout = qt.QHBoxLayout()
        self.globalScaleLayout.setContentsMargins(pix(3), pix(0), pix(0), pix(0))
        self.globalScaleWidget.setLayout(self.globalScaleLayout)
        self.dropDownWidget.addWidget(self.globalScaleWidget)

        scaleLabel = qt.QLabel(_SR['Global Scale:'] + ' ')
        scaleLabel.setFixedHeight(pix(20))
        self.globalScaleLayout.addWidget(scaleLabel)

        self.globalScaleLayout.addStretch()
        scaleLabel = qt.QLabel('1:')
        scaleLabel.setFixedHeight(pix(20))
        self.globalScaleLayout.addWidget(scaleLabel)


        self.globalScaleSpinBox = qt.QLineEdit()
        self.globalScaleSpinBox.setFrame(False)
        validator = MayaQclocaleDoubleValidator()
        validator.setBottom(0.001)
        validator.setTop(100000)
        self.globalScaleSpinBox.setText('200.0')
        self.globalScaleSpinBox.setFixedHeight(pix(20))
        self.globalScaleSpinBox.setFixedWidth(pix(75))
        self.globalScaleSpinBox.setValidator(validator)
        self.globalScaleLayout.addWidget(self.globalScaleSpinBox, 0)

        self.resetUI()

    def dropDownSwitched(self):
        self.window().resize(self.window().width(), self.scrollWidget.sizeHint().height()+pix(4))

    def resetUI(self):
        self.listWidget.clear()
        self.isLinkOn = True
        self.pauseButton.setHighlighted(False)
        self.syncTimeline.setHighlighted(False)
        self.changeIPField.setText('localhost')

    def setupData(self):
        self.client.host = 'localhost'
        self.fromNodes = []
        self.compId = None
        self.isLinkOn = True
        self.timelineUpdating = False
        self.progressBar = mel.eval('$tmp = $gMainProgressBar')

    def initCallbackManager(self):
        self.callbacksManager = AECallbacksManager()
        self.callbacksManager.sceneClosing = self.sceneClosing
        self.callbacksManager.sceneOpened = self.sceneOpened
        self.callbacksManager.scrJob = self.scrJob
        self.callbacksManager.objRenamed = self.objRenamed
        self.callbacksManager.manageRename = self.manageRename
        self.callbacksManager.nodeRemovedCallback = self.nodeRemovedCallback
        self.callbacksManager.animCurveEdited = self.animCurveEdited
        self.callbacksManager.timeChanged = self.timeChangedCallback
        self.callbacksManager.prefsChanged = self.prefsChanged

######################
# UI events
######################

    def sceneClosing(self, clientData=None):
        self.unlinkLink()

        self.callbacksManager.deregisterCallbacks()
        self.callbacksManager.registerSceneOpenCallbacks()

    def sceneOpened(self, clientData=None):
        self.setupData()
        self.resetUI()

        self.initLink()

        self.callbacksManager.registerCallbacks()
        self.callbacksManager.registerSceneCloseCallbacks()


    #LIST WIDGET EVENTS
    def openTreeMenu(self, position):
        if self.listWidget.currentItem() is None:
            return

        treeMenu = qt.QMenu()
        treeMenu.addAction(_SR['Remove'], self.removeObjects)
        treeMenu.exec_(self.listWidget.viewport().mapToGlobal(position))

    #On drag-drop
    def eventFilter(self, parent, event):
        if (parent is self.listWidget.viewport() and event.type() == qt.QEvent.Drop):
            mimeText = event.mimeData().text()
            if len(mimeText):
                nodes = [node.split('.')[0] for node in mimeText.splitlines()]
                nodes = [cmds.ls(name, uuid=True)[0] for name in nodes]
                if len(nodes):
                    self.insertNodes(nodes)

        return False #no interrupt

    def insertNodes(self, nodes):
        # Send preferences with first added node (existing composition)
        firstTime = len(self.fromNodes) == 0
                
        data = []

        for uuid in nodes:
            if uuid in self.fromNodes:
                continue

            name = cmds.ls(uuid, long=True)[0]
            if not AEUtils.isValidNode(name):
                continue

            self.fromNodes.append(uuid)
            qt.QListWidgetItem(name, self.listWidget)

            self.callbacksManager.registerNode(uuid)

            if self.isActive():
                AEUtils.getNodeDataForAllAttr(data, uuid)

        if self.isActive():
            self.sendNodeData(data, firstTime)

    #On menu remove
    def removeObjects(self):
        selectedObjects = self.listWidget.selectedItems()
        if not selectedObjects: return
        for obj in selectedObjects:
            name = obj.text()
            uuid = cmds.ls(name, uuid=True)[0]

            if uuid in self.fromNodes:
                self.callbacksManager.deregisterNode(uuid)
                self.fromNodes.remove(uuid)
                
                if self.isActive():
                    self.sendDelete(uuid)

            self.listWidget.takeItem(self.listWidget.row(obj))
        

    #BUTTONS EVENTS
    def pauseClicked(self):
        self.isLinkOn = not self.isLinkOn
        self.pauseButton.setHighlighted(not self.isLinkOn)
        if self.isActive()and len(self.fromNodes) > 0:
            self.sendAllNodeData(True)

    def refreshClicked(self):
        if self.client.isConnected():
            self.timelineUpdating = False
            self.sendAllNodeData()

    def timeSyncChanged(self):
        self.syncTimeline.setHighlighted(not self.syncTimeline.isHighlighted())
        if self.isActive() and self.syncTimeline.isHighlighted():
            self.sendTimeline()

    def export(self):
        self.exportData()

    def importClicked(self):
        data = AEUtils.importFromFile()
        try:
            pyData = json.loads(data)
            if 'layers' in pyData:
                self.receiveLayers(pyData['layers'])
            
        except:
            nom.MGlobal.displayInfo(_SR['Invalid Import File'])

    def ipChanged(self):
        newIP = self.changeIPField.text()
        self.unlinkLink()
        self.client.host = newIP
        self.initLink()

    def closeEvent(self, event=None):
        global liveLinkWindow
        liveLinkWindow = None
        self.unlinkLink()
        self.callbacksManager.deregisterCallbacks()
        self.callbacksManager.deregisterSceneCallbacks()

        nom.MGlobal.displayInfo(_SR['Closed AE Live Link'])

######################
# Callback Events
######################

    def nodeRemovedCallback(self, node, clientData):
        fnThisNode = nom.MFnDependencyNode ( node )
        uuid = fnThisNode.uuid().asString()
        name = cmds.ls(uuid, long=True)[0]
        if uuid in self.fromNodes:
            self.callbacksManager.deregisterNode(uuid)
            self.fromNodes.remove(uuid)
            self.refreshListWidget()

            if self.isActive():
                self.sendDelete(uuid)

    #API callback on any animCurve change
    def animCurveEdited(self, curves, clientData):
        if not self.isActive(): return
        data = []
        nodesToUpdate = []

        for curveObj in curves:
            curveNodes = self.getValidCurveNodes(curveObj)
            if curveNodes:
                nodesToUpdate.append(curveNodes)
            
        for nodes, attr in nodesToUpdate:
            for name in nodes:
                AEUtils.getNodeDataForAttr(data, name, attr)

        self.sendNodeData(data)

    #Scriptjob for valid attr of selected objects
    def scrJob(self, uuid, attr):
        if not self.isActive(): return
        
        data = []
        if self.timelineUpdating: return
        name = cmds.ls(uuid, long=True)[0]
        AEUtils.getNodeDataForAttr(data, name, attr)
        self.sendNodeData(data)

    def objRenamed(self, node, oldName, clientData):
        uuid = nom.MFnDependencyNode(node).uuid().asString()
        self.manageRename(uuid)

    def manageRename(self, uuid):
        if uuid not in self.fromNodes:
            return
        
        self.refreshListWidget()
        self.callbacksManager.renameNode(uuid)

        if self.isActive():
            self.sendRename(uuid)

    def timeChangedCallback(self, mtime, clientData):
        self.timelineUpdating = True
        cmds.evalDeferred(self.afterTimeChangeCallback, lp=True)
        if self.syncTimeline.isHighlighted() and self.isActive():
            self.sendTimeline()

    def afterTimeChangeCallback(self):
        self.timelineUpdating = False

    def prefsChanged(self, clientData=None):
        if self.isActive() and self.syncPrefs:
            self.sendPrefs()


######################
# Helper Functions
######################

    def refreshListWidget(self):
        self.listWidget.clear()
        for i, uuid in enumerate(self.fromNodes):
            name = cmds.ls(uuid, long=True)[0]
            qt.QListWidgetItem(name, self.listWidget)

    def getDataForAllNodes(self):
        data = []
        for uuid in self.fromNodes:
            AEUtils.getNodeDataForAllAttr(data, uuid)

        return data

    def getValidCurveNodes(self, curveObj):
        validNodes = []
        curve = oma.MFnAnimCurve(curveObj).name()
        name, attr = curve.split('_')
        uuid = cmds.ls(name, uuid=True)[0]

        apiAttr = None
        for a in (AEUtils.allSpecificAttributes + AEUtils.commonAttr):
            if a in attr:
                apiAttr = a
                break

        if not apiAttr: return []

        # Check if shape and get transform
        if apiAttr in AEUtils.allSpecificAttributes:
            name = cmds.listRelatives(name, parent=True, f=True)[0]
        
        validNodes.append(name)

        #Check if animCurve is not of our objects
        if (not AEUtils.isValidNode(name)) or (uuid not in self.fromNodes):
            validNodes = []

        #Check if animCurve is of a parent of our objects
        if self.callbacksManager.isObservableParent(uuid):
            validNodes += self.callbacksManager.getAffectedNodeNamesByParent(uuid)

        return [validNodes, apiAttr]


    def askSyncPrefs(self):
        if self.syncPrefs:
            return True

        elif not self.samePrefs:
            result = cmds.confirmDialog( title=_SR['Preferences Mismatch'], 
                message=_SR['Would you like to override the composition\'s preferences?'], 
                button=[_SR['Yes'],_SR['No']], defaultButton=_SR['Yes'], 
                cancelButton=_SR['No'], dismissString=_SR['No'])

            self.syncPrefs = (result == _SR['Yes'])

            if self.syncPrefs:
                return True
                
        return False
        

######################
# Connection Utilities
######################

    def isActive(self):
        return self.client.isConnected() and self.isLinkOn

    def initLink(self):
        self.compNameLabel.setText(_SR['Waiting for connection...']) #<font color=\"#9E8E29\"></font>
        self.client.run()

    def unlinkLink(self):
        self.compNameLabel.setText(_SR['Disconnected'])#<font color=\"#9E2929\"></font>
        self.client.closeConnection()

    def sendHandshake(self):
        data = {'prefs' : AEUtils.getPrefs(), 'handshake':True}
        self.sendDataAsJSON(data)

    def linkReceiver(self, data):
        try:
            pyData = json.loads(data)
            if 'compName' in pyData:
                self.receiveCompName(pyData['compName'])
                self.samePrefs = pyData['samePrefs']
                self.syncPrefs = pyData['samePrefs']
                if len(self.fromNodes) > 0 and self.isActive():
                    self.sendAllNodeData(True)

            if 'layers' in pyData:
                self.receiveLayers(pyData['layers'])
            
        except:
            if 'Connection established' == data:
                self.sendHandshake()

            if 'Connection closed' == data:
                self.unlinkLink()
                if liveLinkWindow is not None:
                    self.initLink()

            if 'Request handshake' == data:
                self.sendHandshake()


    def receiveCompName(self, data):
        name = str(data)
        self.compNameLabel.setText('<font color=\"#3A9E29\">' + _SR['Connected to'] + '</font> ' + name)

    def receiveLayers(self, data):
        globalScale = float(self.globalScaleSpinBox.text())
        AEUtils.registerLayers(data, globalScale)

    def scaleData(self, data):
        if 'data' in data:
            globalScale = float(self.globalScaleSpinBox.text())
            for i, row in enumerate(data['data']):
                if row['attr'] in ['translate', 'scale']:
                    for j, v in enumerate(data['data'][i]['values']):
                        data['data'][i]['values'][j] = [x * globalScale for x in v]
                if row['type'].lower() == 'directionalLight'.lower():
                    if 'poiValues' in data['data'][i]:
                        for j, v in enumerate(data['data'][i]['poiValues']):
                            data['data'][i]['poiValues'][j] = [x * globalScale for x in v]

    def scaleDataDown(self, data):
        #TODO
        pass

    def sendDataAsJSON(self, data):
        self.scaleData(data)

        jsonStr = json.dumps(data)
        self.client.sendMsg(jsonStr)

    def sendPrefs(self):
        data = {'prefs' : AEUtils.getPrefs()}
        self.sendDataAsJSON(data)

    def sendNodeData(self, data, firstTime=False):
        dataToSend = {'data' : data}

        if firstTime and self.askSyncPrefs():
            dataToSend['prefs'] = AEUtils.getPrefs()

        self.sendDataAsJSON(dataToSend)

    def sendAllNodeData(self, firstTime=False):
        dataToSend = {'data' : self.getDataForAllNodes()}

        if firstTime and self.askSyncPrefs():
            dataToSend['prefs'] = AEUtils.getPrefs()

        self.sendDataAsJSON(dataToSend)

    def sendTimeline(self):
        time = cmds.currentTime(query=True)
        fps = mel.eval("currentTimeUnitToFPS;")
        time /= fps
        data = {'timeline': time}
        self.sendDataAsJSON(data)

    def sendRename(self, uuid):
        name = cmds.ls(uuid, long=True)[0]
        data = {'rename': [uuid, name]}
        self.sendDataAsJSON(data)

    def sendDelete(self, uuid):
        data = {'delete': uuid}
        self.sendDataAsJSON(data)

    def sendSceneName(self):
        data = {'mayaName' : AEUtils.getName()}
        self.sendDataAsJSON(data)

    def exportData(self):
        data = {'data' : self.getDataForAllNodes()}
        data['mayaName'] = AEUtils.getName()
        data['prefs'] = AEUtils.getPrefs()
        myJson = json.dumps(data) 
        AEUtils.exportToFile(myJson)

######################
# Window Setup
######################

def openAELiveLink(restore=False):
    global liveLinkWindow
    if liveLinkWindow is None:
        liveLinkWindow = AELiveLink(parent=fx.mayaWindow())
        liveLinkWindow.setProperty("saveWindowPref", True )

    if restore == True:
        parent = omui.MQtUtil.getCurrentParent()
        mixinPtr = omui.MQtUtil.findControl(liveLinkWindow.objectName())
        omui.MQtUtil.addWidgetToMayaLayout(int(mixinPtr), int(parent))
       
    else:
        closeScriptStr = 'import MayaToAE.livelink\nMayaToAE.livelink.liveLinkWindowDestroyed()'
        uiScriptStr = 'import MayaToAE.livelink\nMayaToAE.livelink.openAELiveLink(restore=True)'
        liveLinkWindow.show(dockable=True, save=True, plugins='MASH', closeCallback=closeScriptStr, uiScript=uiScriptStr)
    liveLinkWindow.window().raise_()
    liveLinkWindow.raise_()
    liveLinkWindow.activateWindow()

def liveLinkWindowDestroyed():
    global liveLinkWindow
    if liveLinkWindow:
        liveLinkWindow.closeEvent()
    liveLinkWindow = None

#openAELiveLink()
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
