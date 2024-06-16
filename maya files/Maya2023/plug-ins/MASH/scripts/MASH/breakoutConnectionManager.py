from builtins import object
from builtins import range
from maya.app.flux.imports import *
from maya.app.flux.core import pix
import MASH.breakoutConnectionData as connectionData
import MASH.breakoutAttrColors as attrTypeColors

import maya.OpenMayaUI as omui
import maya.OpenMaya as old
from openMASH import mashGetMObjectFromNameOne
from itertools import count
import re

import MASH.action as action

from types import FunctionType
import random

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

import six

connectionManagerWindowName = "connectionManagerWindowName105"
if not 'connectionManagerWindow' in globals():
    connectionManagerWindow = None

def printf(text):
    print(text)


# ==============
# STRING RESOURCES
def getResource(name):
    return mel.eval('getPluginResource("MASH", "' + name + '")')

_SR = {
    'Breakout Connection Manager': getResource('kBCM_BCM'),
    'Name': getResource('kBCM_Name'),
    'Connections': getResource('kBCM_Connections'),
    'From Breakout': getResource('kBCM_From_Breakout'),
    'To Selection': getResource('kBCM_To_Selection'),
    'Show': getResource('kBCM_Show'),
    'Hidden': getResource('kBCM_Hidden'),
    'Utility': getResource('kBCM_Utility'),
    'Incoming connection exists on': getResource('kBCM_Incoming'),
    'Overwrite Incoming Connection?': getResource('kBCM_Overwrite'),
    'Continue?': getResource('kBCM_Continue'),
    'Yes': getResource('kBCM_Yes'),
    'No': getResource('kBCM_No'),
    'Change Connection ID': getResource('kBCM_Change_Connection'),
    'New Id (will realign current connections):': getResource('kBCM_New_Id'),
    'From:': getResource('kBCM_From'),
    'Iterate id': getResource('kBCM_Iterate'),
    'Disconnect:': getResource('kBCM_Disconnect'),
    'Disconnect All': getResource('kBCM_Disconnect_All'),
    'Remove': getResource('kBCM_Remove'),
    'New Group': getResource('kBCM_New_Group'),
    'Ungroup': getResource('kBCM_Ungroup'),
    'Connection Manager: Attribute cannot be connected to' : getResource('kBCM_Cannot_Be_Connected')
}

class ConnectionManager(MayaQWidgetDockableMixin, qt.QDialog):

    dev = False

    UTILITY_FILTER = [  "blackBox", "borderConnections", "boundingBox", "caching", "center", "containerType", "creationDate"\
                        "creator", "customTreatment", "display", "dynamics", "frozen", "geometry", "ghost", "hiddenInOutliner", "hideOnPlayback"\
                        "hyperLayout", "iconName", "identification", "inheritsTransform", "inst", "intermediateObject", "inverseMatrix", "isCollapsed"\
                        "isHistoricallyInteresting", "layerOverrideColor", "layerRenderable"\
                        "lodVisibility", "matrix", "max", "message", "min", "nodeState"\
                        "object", "outliner", "override", "parent", "published", "render", "selectionChildHighlighting", "template", "uiTreatment"\
                        "useObjectColor", "useOutlinerColor", "viewMode", "viewName", "wireColorB", "wireColorG", "wireColorR"\
                        "wireColorRGB", "worldInverseMatrix", "worldMatrix", "xformMatrix"]

    def __init__(self, parent=None, fromNodes=None, toNode=None, name=None, title=None):

        super(ConnectionManager, self).__init__(parent)

        self.fromNodes = fromNodes
        self.breakoutNode = toNode

        #self.winName = connectionManagerWindowName
        #self.setObjectName( self.winName )

        if isinstance(self.fromNodes, six.string_types):
            temp = self.fromNodes
            self.fromNodes = [self.fromNodes]

        for i in range (0, len(self.fromNodes), 1):
            self.fromNodes[i] = self.fromNodes[i].split('|')[-1]

        for node in self.fromNodes:
            # skip nodes that might be selected by accident
            nodeType = cmds.nodeType(node)
            if (nodeType == "MASH_Waiter") or (nodeType == "MASH_Breakout"):
                self.fromNodes.remove(node)

        self.setGeometry(pix(600), pix(300), pix(850), pix(500))
        self.setWindowTitle(name)

        self.menuBar = qt.QMenuBar(self)

        #DEV menu
        if self.dev:
            self.devMenu = self.menuBar.addMenu("DEV")
            self.printJSONAction =  action.Action("Print JSON", self.devMenu)
            self.printJSONAction.triggered.connect(lambda: printf(self.data.toString()))
            self.devMenu.addAction(self.printJSONAction)
            self.rebuildAction =  action.Action("Rebuild Objects", self.devMenu)
            self.rebuildAction.triggered.connect(self.rebuildObjects)
            self.devMenu.addAction(self.rebuildAction)
            self.clearDataAction =  action.Action("Clear data (destructive)", self.devMenu)
            self.clearDataAction.triggered.connect(self.clearData)
            self.devMenu.addAction(self.clearDataAction)

        #Show menu
        self.showMenu = self.menuBar.addMenu(_SR["Show"])
        self.showHiddenAction =  action.Action(_SR["Hidden"], self.showMenu, checkable=True)
        self.showHiddenAction.setChecked(False)
        self.showHiddenAction.triggered.connect(self.updateData)
        self.showMenu.addAction(self.showHiddenAction)

        self.showUtilityAction =  action.Action(_SR["Utility"], self.showMenu, checkable=True)
        self.showUtilityAction.setChecked(False)
        self.showUtilityAction.triggered.connect(self.updateData)
        self.showMenu.addAction(self.showUtilityAction)

        #Breakout selection menu
        self.breakoutMenu = qt.QComboBox()
        self.updateBreakoutMenu()
        self.breakoutMenu.currentIndexChanged.connect(self.breakoutMenuCurrentIndexChanged)
        self.breakoutMenu.setSizeAdjustPolicy(qt.QComboBox.AdjustToContents)

        self.topLayout = qt.QHBoxLayout()
        self.topLayout.addWidget(self.breakoutMenu, 0)
        self.topLayout.addWidget(self.menuBar, 1)
        self.topLayout.setAlignment(self.menuBar, qt.Qt.AlignRight)
        self.main_layout = qt.QVBoxLayout()
        self.main_layout.addLayout(self.topLayout, 0)
        self.layout = qt.QHBoxLayout()
        self.splitter = qt.QSplitter(qt.Qt.Horizontal)

        self.objectsWidget = ObjectTreeWidget()
        self.objectsWidget.clicked.connect(self.on_obj_clicked)
        self.splitter.addWidget(self.objectsWidget)

        self.objectsWidget.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.objectsWidget.customContextMenuRequested.connect(self.openTreeMenu)
        self.objectsWidget.itemChanged.connect(self.groupNameChanged)
        self.objectsWidget.itemDoubleClicked.connect(self.groupDoubleClicked)
        self.objectsWidget.viewport().installEventFilter(self)

        self.breakoutAttributesWidget = AttributeTreeWidget()
        self.breakoutAttributesWidget.clicked.connect(self.on_from_clicked)
        self.breakoutAttributesWidget.headerItem().setText(0, _SR["From Breakout"])
        self.splitter.addWidget(self.breakoutAttributesWidget)


        self.destinationAttributesWidget = AttributeTreeWidget()
        self.destinationAttributesWidget.clicked.connect(self.on_to_clicked)
        self.destinationAttributesWidget.headerItem().setText(0, _SR["To Selection"])
        self.splitter.addWidget(self.destinationAttributesWidget)

        self.layout.addWidget(self.splitter, 1)
        self.layout.addStretch(0)
        self.main_layout.addLayout(self.layout, 1)

        self.splitter.setSizes([pix(400), pix(225), pix(225)])

        self.connectedAttributes = []

        # Adding the dynamic attribute data to all breakout nodes : MAYA-93406
        for breakoutNode in cmds.ls(exactType='MASH_Breakout'):
            # skipping the node received as a parameter (toNode),
            # this should be setup for last so self.breakoutNode will be
            # the node that is supposed to be shown
            if (breakoutNode == toNode):
                continue;
            self.setupDynamicAttributeData(breakoutNode, isHidden=True)

        self.setupDynamicAttributeData(toNode, isHidden=True)

        self._registeredMayaCallbacks = []
        cb = old.MDGMessage.addConnectionCallback(self.connectionCallback, None)
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MDGMessage.addNodeRemovedCallback(self.nodeRemovedCallback, "dependNode")
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MDGMessage.addNodeAddedCallback(self.onNewMASHBreakout, "MASH_Breakout")
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MSceneMessage.addCallback(old.MSceneMessage.kBeforeOpen, self.beforeSceneExits, None)
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MSceneMessage.addCallback(old.MSceneMessage.kBeforeNew, self.beforeSceneExits, None)
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MSceneMessage.addCallback(old.MSceneMessage.kBeforeImport, self.beforeSceneExits, None)
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))
        cb = old.MSceneMessage.addCallback(old.MSceneMessage.kMayaExiting, self.beforeSceneExits, None)
        self._registeredMayaCallbacks.append(MCallbackIdWrapper(cb))

        self.attrColors = attrTypeColors.dictionary
        self.itemsToRebuildAfterDrop = []

        self.setLayout(self.main_layout)

        self.updateData(True)

        self.setAttribute(qt.Qt.WA_DeleteOnClose)

    # Sets up the dynamic attribute "data" on breakout nodes : MAYA-93406
    # This function creates the connectionData for the node passed as
    # parameter and adds the attribute data to the node if it doesn't
    # exist, or if it does, it will be initialized on the ConnectionData.
    # After this procedure, "updateAE" will be called for the breakout node.
    def setupDynamicAttributeData(self, node, isHidden=True):
        self.objectsWidget.clear()
        self.breakoutNode = node.split('|')[-1].split('.')[0]
        self.data = connectionData.ConnectionData()

        if not cmds.attributeQuery("data", node=self.breakoutNode, exists=True):
            cmds.addAttr(self.breakoutNode, longName="data", dt='string', hidden=isHidden)
        else:
            self.data.initFromString(cmds.getAttr(self.breakoutNode+ ".data"))
            self.checkConnections()
            self.rebuildObjects()
        self.saveData()

    def clearData(self):
        self.data = connectionData.ConnectionData()
        cmds.deleteAttr(self.breakoutNode, attribute="data")
        cmds.addAttr(self.breakoutNode, longName="data", dt='string', hidden=True)
        self.objectsWidget.clear()
        self.saveData()

    def reInitWindow(self, toNode):
        self.fromNodes = []
        self.setupDynamicAttributeData(toNode, isHidden=False)
        self.updateData(True)

    def breakoutMenuCurrentIndexChanged(self, index):
        allBreakouts = cmds.ls(exactType='MASH_Breakout')
        self.reInitWindow(allBreakouts[index])

    def updateBreakoutMenu(self, toNode=None):
        self.breakoutMenu.clear()
        allBreakouts = cmds.ls(exactType='MASH_Breakout')
        currentBreakout = allBreakouts.index(self.breakoutNode if toNode is None else toNode)
        self.breakoutMenu.addItems(allBreakouts)
        self.breakoutMenu.setCurrentIndex(currentBreakout)

    def onNewMASHBreakout(self, node, clientDate):
        self.updateBreakoutMenu()

    def nodeRemovedCallback(self, node, clientData):
        self.updateBreakoutMenu()
        name = old.MFnDependencyNode(node).name()
        if name == self.breakoutNode:
            allBreakouts = cmds.ls(exactType='MASH_Breakout')
            allBreakouts.remove(self.breakoutNode)
            self.breakoutMenu.clear()
            self.breakoutMenu.addItems(allBreakouts)
            if len(allBreakouts)>0:
                self.breakoutMenu.setCurrentIndex(0)
            else:
                self.close()
            return

        uuid = old.MFnDependencyNode(node).uuid().asString()
        dobj = self.data.getObjectByUUID(uuid)
        if dobj is None:
            return
        obj = self.getWidgetObject(dobj)
        if obj.parent():
            obj.parent().removeChild(obj)
        else:
            self.objectsWidget.takeTopLevelItem(self.objectsWidget.indexFromItem(obj).row())
        self.data.removeObject(dobj)
        self.saveData()

    def connectionCallback(self, source, destination, connMade, clientData):
        if not self.isActiveWindow():
            self.checkConnections()
            self.rebuildObjects()
            self.saveData()

    def beforeSceneExits(self, clientData):
        self.saveData()
        self.close()

    def handleDirectDrop(self, mimeText):
        fromNodes = [x.split('|')[-1].split('.')[0] for x in mimeText.splitlines()]
        if len(fromNodes)!=0:
            self.fromNodes = fromNodes
        self.updateData()

    def eventFilter(self, eobj, event):
        if (eobj is self.objectsWidget.viewport()):
            if(event.type() == qt.QEvent.Paint):
                for item in self.itemsToRebuildAfterDrop:
                    indexes = item["i"]
                    obj = self.objectsWidget.topLevelItem(indexes[0])
                    for i in indexes[1:]:
                        obj = obj.child(i)
                    obj.setText(1, "\n".join(item["conns"]))
                self.itemsToRebuildAfterDrop = []
            if (event.type() == qt.QEvent.Drop):

                mimeText = event.mimeData().text()
                if len(mimeText)>0:
                    self.handleDirectDrop(mimeText)
                    return False

                item = self.objectsWidget.itemAt(event.pos())
                if item is None: #if dropping at the bottom of the widget
                    index = self.objectsWidget.model().index(self.objectsWidget.topLevelItemCount()-1, 0)
                    item = self.objectsWidget.itemFromIndex(index)
                indexes = self.getItemIndexes(item)
                dobj = self.data.getObject(indexes)

                toI = list(indexes)
                dropIndicatorPosition = self.objectsWidget.dropIndicatorPosition()
                if dropIndicatorPosition == qt.QAbstractItemView.AboveItem:
                    toI = list(indexes)
                elif dropIndicatorPosition == qt.QAbstractItemView.OnItem:
                    toI = indexes + [-1]
                else:
                    toI = indexes[:-1] + [indexes[-1]+1]


                fromObjects = []

                for obj in self.objectsWidget.selectedItems():
                    fromI = self.getItemIndexes(obj)
                    dobj = self.data.getObject(fromI)
                    fromObjects.append(dobj)

                destinationObj = self.data.getObject(toI[:-1])
                destinationRequiredConnections = self.data.getConns(destinationObj)

                self.itemsToRebuildAfterDrop = []
                shouldDisconnect = []
                for conn in destinationRequiredConnections:
                    connDest = '->' + conn.split('->')[-1]
                    for dobj in fromObjects:
                        for childDataObj in self.data.getAllObjects(dobj):
                            node = cmds.ls(childDataObj["uuid"])[0]
                            conns = self.data.getConns(childDataObj)

                            otherConnsRaw = (cmds.listConnections(node, p=True, scn=True, d=False, c=True) or [])
                            otherConns = []
                            for i in range(0, len(otherConnsRaw), 2):
                                connFrom = ''

                                if otherConnsRaw[i+1].split('.')[0] != self.breakoutNode:
                                    connFrom = otherConnsRaw[i+1].split('.')[0]

                                connection = connFrom + otherConnsRaw[i+1].split('.')[-1] + '->' + otherConnsRaw[i].split('.')[-1]
                                otherConns.append( connection )

                            conns = list(set(conns + otherConns))

                            for fromObjectConn in conns:
                                if (connDest in fromObjectConn):
                                    if conn != fromObjectConn:
                                        nodeName = node + '.' + fromObjectConn.split('->')[-1]
                                        msg = (_SR['Incoming connection exists on'] + ' ' + nodeName)
                                        if not self.showYesNoPopup(msg, _SR['Overwrite Incoming Connection?']):
                                            return True
                                        else:
                                            if fromObjectConn in childDataObj["conns"]:
                                                shouldDisconnect.append([childDataObj, fromObjectConn])
                                            else:
                                                for parent in self.data.getObjGroups(childDataObj):
                                                    if fromObjectConn in parent["conns"]:
                                                        shouldDisconnect.append([parent, fromObjectConn])

                for dobj, fromObjectConn in shouldDisconnect:
                    self.disconnectDObj(dobj, fromObjectConn)
                    self.itemsToRebuildAfterDrop.append(dobj)

                for dobj in fromObjects:
                    for conn in self.data.getParentConns(dobj):
                        for dChild in self.data.getAllObjects(dobj):
                            self.disconnectDObj(dChild, conn)
                    fromI = dobj["i"]
                    if dropIndicatorPosition == qt.QAbstractItemView.OnItem:
                        toI = destinationObj['i'] + [toI[-1]]
                    self.data.moveObjFromTo(fromI,toI)
                    for conn in self.data.getParentConns(dobj):
                        for dChild in self.data.getAllObjects(dobj):
                            if not self.connectDObj(dChild, conn):
                                dChild["conns"].remove(conn)
                                self.itemsToRebuildAfterDrop.append(dChild)
                    if toI[-1]!=-1: toI[-1]+=1

                self.saveData()

        return False

    def showYesNoPopup(self, msg, msgTitle=_SR['Continue?']):
        reply = cmds.confirmDialog( title=msgTitle, message=msg, button=[_SR['Yes'],_SR['No']], defaultButton=_SR['No'], cancelButton=_SR['No'], dismissString=_SR['No'] )
        return reply == _SR['Yes']

    def saveData(self):
        if cmds.objExists(self.breakoutNode):

            if not cmds.attributeQuery("data", node=self.breakoutNode, exists=True):
                cmds.addAttr(self.breakoutNode, longName="data", dt='string', hidden=True)

            cmds.setAttr( self.breakoutNode+".data", self.data.toString(), type='string' )
            mel.eval('updateAE "'+self.breakoutNode+'";')

    def closeEvent(self, evnt):
        self.saveData()
        self._registeredMayaCallbacks = []
        connectionManagerWindowDestroyed(self.breakoutNode)

    def getCurrentIndex(self, nodeName, attributeName):
        thisNode = mashGetMObjectFromNameOne(nodeName)
        fnNode = old.MFnDependencyNode(thisNode)
        attribute = fnNode.attribute(attributeName)
        inPlug = old.MPlug( thisNode, attribute )
        count = inPlug.numElements()
        for i in range (0, count, 1):
            elPlug = inPlug.elementByPhysicalIndex(i)
            connections = old.MPlugAray()
            elPlug.connectedTo(connections, True, False)

    def getAllTreeItems(self, widget, item=None):
        if item is None:
            items = []
            for i in range(widget.topLevelItemCount()):
                citem = widget.topLevelItem(i)
                items += self.getAllTreeItems(widget, citem)
            return items
        else:
            items = [item]
            for i in range(item.childCount()):
                citem = item.child(i)
                items += self.getAllTreeItems(widget, citem)
            return items

    def getWidgetObject(self, dobj):
        indexes = dobj["i"]
        obj = self.objectsWidget.topLevelItem(indexes[0])
        for i in indexes[1:]:
            obj = obj.child(i)
        return obj

    def getSelectedObjectsRep(self):
        selectedObjects = self.objectsWidget.selectedItems()
        indexes = self.getItemIndexes(selectedObjects[0])
        obj = self.data.getObject(indexes)
        uuids = self.data.getAllObjects(obj, True)
        if len(uuids)==0:
            uuids = self.data.getAllObjects(None, True)
        objName = cmds.ls(uuids[0])[0]
        return objName

    def on_from_clicked(self, index):
        self.updateSelectionAttributes(skipColoring=True)
        if len(self.objectsWidget.selectedItems())==0:
            return
        objName = self.getSelectedObjectsRep()
        fromAttr = self.breakoutAttributesWidget.selectedItems()[0].text(0)
        attrType = cmds.attributeQuery(fromAttr, n=self.breakoutNode, at=True)
        fromCategory = attrTypeColors.attrCategories[attrType]

        for item in self.getAllTreeItems( self.destinationAttributesWidget ):
            attr = item.text(0)
            attrType = cmds.attributeQuery(attr, n=objName, at=True)
            attrCategory = attrTypeColors.attrCategories[attrType]

            if fromCategory == attrCategory:
                item.setIcon(0, self.iconForAttrType(attrType, False))
            else:
                item.setIcon(0, self.iconForAttrType(attrType, True))

    def getItemIndexes(self, item):
        parent = item.parent()
        if(parent is None):
            return [self.objectsWidget.indexFromItem(item).row()]
        else:
            return self.getItemIndexes(parent) + [parent.indexOfChild(item)]

    def deleteGroup(self):
        item = self.objectsWidget.currentItem()
        indexes = self.getItemIndexes(item)
        dobj = self.data.getObject(indexes)
        if self.data.isGroup(dobj):
            children = self.data.getAllObjects(dobj)
            conns = dobj["conns"]
            for conn in conns:
                self.disconnectItems(conn, [item])
            for dchild in children:
                self.data.elevateObject(dchild)
            self.data.deleteObject(dobj)
            self.rebuildObjects()
            self.saveData()

    def buildItem(self, dobj):
        item = qt.QTreeWidgetItem()
        item.setText(1,"\n".join(dobj["conns"]) )
        item.setFlags(qt.Qt.ItemIsDragEnabled|item.flags())
        if self.data.isGroup(dobj):
            item.setText(0, dobj["name"])
            item.setFlags(qt.Qt.ItemIsEditable|item.flags())
            for dChild in dobj["objects"]:
                item.addChild(self.buildItem(dChild))
        else:
            name = cmds.ls(dobj["uuid"])[0]
            item.setText(0,name + '['+str(dobj['outputId']) + ']')
            imgName = ":out_" + 'mesh' if cmds.nodeType(name)=='transform' else cmds.nodeType(name) + ".png"
            item.setIcon(0, qt.QIcon(imgName))
            item.setFlags(item.flags() & ~qt.Qt.ItemIsDropEnabled)
        return item

    def rebuildObjects(self):
        self.objectsWidget.clear()
        for dobj in self.data.data:
            item = self.buildItem(dobj)
            self.objectsWidget.addTopLevelItem(item)

    def checkConnectionOnObject(self, dobj):
        connsReal = list( self.getNodeConnections(dobj) )
        connsDataParent = list( self.data.getParentConns(dobj) )
        connsDataObject = list( dobj["conns"] )

        result = {'hasAdded':False, 'shouldRearange':False, 'hasRemoved':False}

        for conn in connsReal:
            shouldAdd = not(conn in (connsDataParent+connsDataObject))
            if shouldAdd:
                dobj["conns"].append(conn)
                result['hasAdded'] = True
        for conn in connsDataObject:
            shouldRemove = not(conn in connsReal)
            if shouldRemove:
                dobj["conns"].remove(conn)
                result['hasRemoved']= True
        for conn in connsDataParent:
            shouldRearange = not(conn in connsReal)
            if shouldRearange:
                result['shouldRearange'] = True
        return result

    def checkConnections(self):

        allConnected = set(cmds.listConnections(self.breakoutNode, source=False, scn=True) or [] )
        if 'MayaNodeEditorSavedTabsInfo' in allConnected:
            allConnected.remove('MayaNodeEditorSavedTabsInfo')
        shouldAdd = []
        for node in allConnected:
            uuid = cmds.ls( node, uuid=True )[0]
            if uuid not in self.data.hashedUUIDs:
                shouldAdd.append(node)
        if len(shouldAdd)>0:
            self.populateObjects(shouldAdd)

        shouldRedraw = False
        for dobj in self.data.getAllObjects():
            exists = len(cmds.ls(dobj['uuid']))>0
            if not exists:
                self.data.removeObject(dobj)
                shouldRedraw = True
                continue
            result = self.checkConnectionOnObject(dobj)

            if(result['hasAdded'] or result['shouldRearange'] or result['hasRemoved']):
                shouldRedraw = True

            while result['shouldRearange']:
                self.data.elevateObject(dobj)
                result = self.checkConnectionOnObject(dobj)
        return shouldRedraw

    def getNodeConnections(self, dobj, outputId=False):
        conns = []
        currentConnections = cmds.listConnections(self.breakoutNode, p=True, scn=True)
        if currentConnections is None:
            return conns
        node = cmds.ls(dobj["uuid"])[0]
        shortName = node.split('|')[-1]
        for s in currentConnections:
            if shortName in s:
                source = cmds.listConnections(s, p=True, scn=True)
                attributeIndex = ''
                if outputId:
                    attributeIndex = re.findall(r'\[([^]]*)\]',source[0])[-1] + '.'
                conns.append(attributeIndex + source[0].split('.')[-1] + '->' + s.split('.')[-1])
        return conns



    def printTreeItem(self):
        print(self.objectsWidget.currentItem().text(0))
        indexes = self.getItemIndexes(self.objectsWidget.currentItem())
        dobj = self.data.getObject(indexes)
        conns = self.data.getConns(dobj)
        print(conns)

    def connectDObj(self, dobj, conn, outputId=None):
        connectFrom, connectTo = conn.split("->")
        node = cmds.ls(dobj["uuid"])[0]
        destination = node + '.' + connectTo
        attributeIndex = dobj["outputId"] if outputId is None else outputId
        source = self.breakoutNode+".outputs["+str(attributeIndex)+"]."+connectFrom

        if not cmds.isConnected(source, destination, ignoreUnitConversion=True):
            cmds.connectAttr(source, destination, f=True)
            return True

        return False

    def disconnectDObj(self, dobj, conn):
        connectFrom, connectTo = conn.split("->")
        for dChildObj in self.data.getAllObjects(dobj):

            node = cmds.ls(dChildObj["uuid"])[0]
            destination = node + '.' + connectTo
            attributeIndex = self.getOutputId(destination)

            if attributeIndex is None:
                continue

            source = self.breakoutNode+".outputs["+str(attributeIndex)+"]."+connectFrom
            if cmds.isConnected(source, destination, ignoreUnitConversion=True):
                cmds.disconnectAttr(source, destination)

        if conn in dobj["conns"]:
            dobj["conns"].remove(conn)
        return False

    def getOutputId(self, destination):
        source = cmds.listConnections(destination, p=True, scn=True)
        if source:
            attributeIndex = re.findall(r'\[([^]]*)\]',source[0])[-1]
            return attributeIndex
        return None

    def disconnectItems(self, conn, items):
        currentConnections = cmds.listConnections(self.breakoutNode, p=True, scn=True)
        connectFrom, connectTo = conn.split("->")

        for myObj in items:
            dataObj = self.data.getObject(self.getItemIndexes(myObj))

            conns = {}

            for childDataObj in self.data.getAllObjects(dataObj):
                node = cmds.ls(childDataObj["uuid"])[0]
                indexFound = False
                shortName = node.split('|')[-1]
                for s in currentConnections:
                    if shortName in s:
                        source = cmds.listConnections(s, p=True, scn=True)
                        if source:
                            attributeIndex = re.findall(r'\[([^]]*)\]',source[0])[-1]
                            fromN = self.breakoutNode+".outputs["+str(attributeIndex)+"]."+connectFrom
                            toN = node+"."+connectTo
                            if cmds.isConnected(fromN, toN, ignoreUnitConversion=True):
                                cmds.disconnectAttr(fromN, toN)
                            conns[connectFrom] = connectTo
                            indexFound = True

            for key in list(conns.keys()):
                conn = key + "->" + conns[key]
                if conn in dataObj["conns"]:
                    dataObj["conns"].remove(conn)
                text = "\n".join(dataObj["conns"])
                widgetObj = self.getWidgetObject(dataObj)
                widgetObj.setText(1, text)

    def disconnectTreeItem(self, conn):
        self.disconnectItems(conn, self.objectsWidget.selectedItems())
        self.saveData()

    def createGroup(self):
        indexes = None
        if self.objectsWidget.currentItem() is None:
            indexes = [self.objectsWidget.topLevelItemCount()-1]
            parent = None
        else:
            indexes = self.getItemIndexes(self.objectsWidget.currentItem())
            parent = self.data.getObjParent(self.data.getObject(indexes))
        group = self.data.makeGroup()
        self.data.insertObject(group, parent, indexes[-1]+1 )
        pgroup = qt.QTreeWidgetItem()
        pgroup.setText(0, group["name"])
        pgroup.setFlags(qt.Qt.ItemIsDragEnabled | qt.Qt.ItemIsEditable|pgroup.flags())
        pgroup.setSelected(True)
        if parent is None:
            self.objectsWidget.insertTopLevelItem(indexes[-1] + 1, pgroup)
        else:
            parent = self.objectsWidget.currentItem().parent()
            parent.insertChild(indexes[-1] + 1, pgroup)

        self.saveData()

        return pgroup

    def getIntegerFromPrompt(self):
        dialog = qt.QDialog(self)
        form = qt.QFormLayout(dialog)
        dialog.setWindowTitle(_SR["Change Connection ID"])
        form.addRow(qt.QLabel(_SR["New Id (will realign current connections):"]))
        dialog.startId = qt.QSpinBox()
        dialog.startId.setMinimum(0)
        dialog.startId.setSingleStep(1)
        dialog.startId.setMaximum(2147000000)
        form.addRow(_SR['From:'] + ' ', dialog.startId)
        dialog.modeSelect = qt.QCheckBox(_SR['Iterate id'])
        dialog.modeSelect.setChecked(True)
        form.addRow(dialog.modeSelect)
        buttonBox = qt.QDialogButtonBox(qt.QDialogButtonBox.Ok | qt.QDialogButtonBox.Cancel, qt.Qt.Horizontal, dialog)
        form.addRow(buttonBox)
        qt.QObject.connect(buttonBox, qt.SIGNAL('accepted()'), dialog.accept)
        qt.QObject.connect(buttonBox, qt.SIGNAL('rejected()'), dialog.reject)

        ok = dialog.exec_() == qt.QDialog.Accepted
        return [ok, dialog.modeSelect.isChecked(), dialog.startId.value()]


    def changeConnectionId(self):
        ok, mode, newId = self.getIntegerFromPrompt()

        if not ok: return

        for obj in self.objectsWidget.selectedItems():
            indexes = self.getItemIndexes(obj)
            dobj = self.data.getObject(indexes)
            if self.data.isGroup(dobj):
                for childObj in self.data.getAllObjects(dobj):
                    self.changeObjectId(childObj, newId)
                    if mode: newId+=1
            else:
                self.changeObjectId(dobj, newId)
                if mode: newId+=1

    def changeObjectId(self, dobj, newId):
        conns = self.data.getConns(dobj)
        for conn in conns:
            shouldReadd = conn in dobj['conns']
            self.disconnectDObj(dobj, conn)
            self.connectDObj(dobj, conn, outputId=newId)
            if shouldReadd: dobj['conns'].append(conn)
        obj = self.getWidgetObject(dobj)
        name = cmds.ls(dobj['uuid'])[0] + '[' + str(newId) + ']'
        obj.setText(0, name)
        dobj['outputId'] = newId

    def openTreeMenu(self, position):
        treeMenu = qt.QMenu()
        currentItem = self.objectsWidget.currentItem()
        if currentItem is None:
            treeMenu.addAction(_SR['New Group'], self.createGroup)
            treeMenu.exec_(self.objectsWidget.viewport().mapToGlobal(position))
            return
        indexes = self.getItemIndexes(currentItem)
        dobj = self.data.getObject(indexes)
        conns = dobj["conns"]

        #Create right-click menu options
        for conn in conns:
            treeMenu.addAction(_SR['Disconnect:'] + ' ' + str(conn))
        treeMenu.addAction(_SR['Disconnect All'], self.disconnectAll)
        treeMenu.addAction(_SR['Remove'], self.removeObject)
        treeMenu.addAction(_SR['Change Connection ID'], self.changeConnectionId)
        treeMenu.addAction(_SR['New Group'], self.createGroup)
        if self.data.isGroup(dobj):
            treeMenu.addAction(_SR['Ungroup'], self.deleteGroup)

        action = treeMenu.exec_(self.objectsWidget.viewport().mapToGlobal(position))
        if (not action is None) and _SR['Disconnect:'] in action.text():
            conn = action.text().split(': ')[-1]
            self.disconnectTreeItem(conn)

    def removeObject(self):
        objs = self.objectsWidget.selectedItems()
        for obj in objs:
            if shiboken.isValid(obj):
                indexes = self.getItemIndexes(obj)
                dobj = self.data.getObject(indexes)

                if self.data.isGroup(dobj):
                    for childObj in self.data.getAllObjects(dobj):
                        self.disconnectAllPerNode(childObj)
                else:
                    self.disconnectAllPerNode(dobj)

                self.data.removeObject(dobj)
                if obj.parent():
                    obj.parent().removeChild(obj)
                else:
                    self.objectsWidget.takeTopLevelItem(self.objectsWidget.indexFromItem(obj).row())


    def disconnectAllPerNode(self, dobj):
        conns = self.data.getConns(dobj)
        for conn in conns:
            self.disconnectDObj(dobj, conn)

    def disconnectAll(self):
        for obj in self.objectsWidget.selectedItems():
            indexes = self.getItemIndexes(obj)
            dobj = self.data.getObject(indexes)
            if self.data.isGroup(dobj):
                for childObj in self.data.getAllObjects(dobj):
                    self.disconnectAllPerNode(childObj)
            else:
                self.disconnectAllPerNode(dobj)
        self.rebuildObjects()

    def updateConnectionData(self):
        if self.data.isEmpty():
            group = self.data.makeGroup(self.fromNodes)
            self.data.insertObject(group)

    def updateData(self, left=False):
        '''
        SETUP SHOULD DETECT EXISTING CONNECTIONS
        '''
        self.populateObjects()
        self.saveData()
        self.breakoutAttributesWidget.clear()
        self.populateFromAttributes()
        if len(self.objectsWidget.selectedItems())==0 and self.objectsWidget.topLevelItemCount()>0:
            obj = self.objectsWidget.topLevelItem(0)
            if not obj is None:
                obj.setSelected(True)
        self.updateSelectionAttributes()

        #self.updateConnectionData()

        self.destinationAttributesWidget.resizeColumnToContents(0)
        self.breakoutAttributesWidget.resizeColumnToContents(0)
        self.objectsWidget.resizeColumnToContents(0)
        self.objectsWidget.resizeColumnToContents(1)

    def on_obj_clicked(self, index):
        self.updateSelectionAttributes()
        self.destinationAttributesWidget.clearSelection()
        self.breakoutAttributesWidget.clearSelection()

    def updateSelectionAttributes(self, skipColoring=False):
        hiddenAttributes = self.showHiddenAction.isChecked()
        utilityAttributes = self.showUtilityAction.isChecked()

        self.destinationAttributesWidget.clear()
        selectedObjects = self.objectsWidget.selectedItems()
        if len(selectedObjects)==0:
            return

        dobjs = []
        for obj in selectedObjects:
            indexes = self.getItemIndexes(obj)
            dobj = self.data.getObject(indexes)
            allObj = self.data.getAllObjects(dobj)
            dobjs += allObj

        if len(dobjs)==0:
            return

        commonAttr = []
        for dobj in dobjs:
            name = cmds.ls(dobj['uuid'])[0]
            attributes = cmds.listAttr(name, c=True, se=True, w=True, v=(not hiddenAttributes))
            #attributes = cmds.attributeInfo( name, h=True, writable=True, internal=False, leaf=False)

            if len(commonAttr)==0:
                if utilityAttributes:
                    commonAttr = set(attributes)
                else:
                    commonAttr = set([x for x in attributes if x not in self.UTILITY_FILTER])

            else:
                commonAttr.intersection_update(attributes)

        commonAttr = sorted(commonAttr)


        finalAttrs = []
        if utilityAttributes:
            finalAttrs = [x for x in attributes]
        else:
            for attrs in commonAttr:
                if not any(x in attrs for x in self.UTILITY_FILTER):
                    finalAttrs.append(attrs)

        refName = cmds.ls(dobjs[0]['uuid'])[0]

        lastItem = []
        for attr in finalAttrs:
            pitems=qt.QTreeWidgetItem()
            shortName = attr.split('.')[-1]
            pitems.setText(0,shortName)
            attrType = cmds.attributeQuery(shortName, n=refName, at=True)
            if not skipColoring:
                labelIcon = self.iconForAttrType(attrType)
                pitems.setIcon(0, labelIcon)

            while len(lastItem)>0:
                if lastItem[-1].text(0) in shortName and not(shortName[-3:]=='RGB' and lastItem[-1].text(0)[-1]=='R'):
                    lastItem[-1].addChild(pitems)
                    lastItem.append(pitems)
                    break
                else:
                    lastItem.pop()
            if len(lastItem)==0:
                lastItem.append(pitems)
                self.destinationAttributesWidget.addTopLevelItem(pitems)

    def on_to_clicked(self, index):
        fromAttr = self.breakoutAttributesWidget.selectedItems()
        toAttr = self.destinationAttributesWidget.selectedItems()
        selectedObjects = self.objectsWidget.selectedItems()
        currentConnections = cmds.listConnections(self.breakoutNode, p=True)

        '''Shoud delete existing multis with removeMultiInstance "MASH_Breakout1.outputs[x]"'''
        '''Currently we connect to the wrong multi if the array is sparse on opening the scene'''
        '''We should use a technique similar to nextFreeMulti'''



        if fromAttr and toAttr:
            connectFrom = fromAttr[0].text(0)
            connectTo = toAttr[0].text(0)

            shouldDisconnect = []

            for myObj in selectedObjects:
                dataObj = self.data.getObject(self.getItemIndexes(myObj))
                for childDataObj in self.data.getAllObjects(dataObj):
                    node = cmds.ls(childDataObj["uuid"])[0]
                    conns = self.data.getConns(childDataObj)

                    otherConnsRaw = (cmds.listConnections(node, p=True, scn=True, d=False, c=True) or [])
                    otherConns = []
                    for i in range(0, len(otherConnsRaw), 2):
                        connFrom = ''

                        if otherConnsRaw[i+1].split('.')[0] != self.breakoutNode:
                            connFrom = otherConnsRaw[i+1].split('.')[0]

                        connection = connFrom + otherConnsRaw[i+1].split('.')[-1] + '->' + otherConnsRaw[i].split('.')[-1]
                        otherConns.append( connection )

                    conns = list(set(conns + otherConns))

                    for conn in conns:
                        if ('->' + connectTo) in conn:
                            if connectFrom!=conn.split('->')[0]:
                                nodeName = node + '.' + connectTo
                                msg = (_SR['Incoming connection exists on'] + ' ' + nodeName)
                                reply = self.showYesNoPopup(msg, _SR['Overwrite Incoming Connection?'])
                                if not reply:
                                    return
                                else:
                                    if conn in childDataObj["conns"]:
                                        shouldDisconnect.append([childDataObj, conn])
                                    else:
                                        for parent in self.data.getObjGroups(childDataObj):
                                            if conn in parent["conns"]:
                                                shouldDisconnect.append([parent, conn])


            for dobj, conn in shouldDisconnect:
                self.disconnectDObj(dobj, conn)
                indexes = dobj["i"]
                obj = self.objectsWidget.topLevelItem(indexes[0])
                for i in indexes[1:]:
                    obj = obj.child(i)
                obj.setText(1, "\n".join(dobj["conns"]))


            conns = {}

            for myObj in selectedObjects:
                dataObj = self.data.getObject(self.getItemIndexes(myObj))
                for childDataObj in self.data.getAllObjects(dataObj):
                    node = cmds.ls(childDataObj["uuid"])[0]
                    indexFound = False
                    shortName = node.split('|')[-1]
                    attributeIndex = childDataObj["outputId"]
                    fromN = self.breakoutNode+".outputs["+str(attributeIndex)+"]."+connectFrom
                    toN = node+"."+connectTo
                    if not cmds.isConnected(fromN, toN, ignoreUnitConversion=True):
                        try:
                            cmds.connectAttr(fromN, toN, f=True)
                            conns[connectFrom] = connectTo
                        except:
                            print(_SR['Connection Manager: Attribute cannot be connected to'] + ' ' + fromN + ' ' + toN + '.')
                    indexFound = True

                for key in list(conns.keys()):
                    conn = key + '->' + conns[key]
                    dataObj["conns"].append(conn)
                    self.removeConnInChildren(dataObj, conn)
                    widgetObj = self.getWidgetObject(dataObj)
                    widgetObj.setText(1, "\n".join(dataObj["conns"]))
            self.objectsWidget.resizeColumnToContents(1)
            self.destinationAttributesWidget.clearSelection()
            self.breakoutAttributesWidget.clearSelection()
            for item in self.getAllTreeItems( self.destinationAttributesWidget ):
                attr = item.text(0)
                objName = self.getSelectedObjectsRep()
                attrType = cmds.attributeQuery(attr, n=objName, at=True)
                item.setIcon(0, self.iconForAttrType(attrType, False))
            self.saveData()

    def removeConnInChildren(self, dobj, conn):
        if self.data.isGroup(dobj):
            for dchild in dobj['objects']:
                if conn in dchild['conns']:
                    dchild['conns'].remove(conn)
                    self.getWidgetObject(dchild).setText(1, "\n".join(dchild["conns"]))
                self.removeConnInChildren(dchild, conn)

    def populateFromAttributes(self):
        keyableDesignationAttrs = cmds.listAttr( self.breakoutNode, c=True )
        keyableDesignationAttrs = sorted(keyableDesignationAttrs)
        lastItem = []
        for attr in keyableDesignationAttrs:
            shortName = attr.split('.')[-1]
            pitems=qt.QTreeWidgetItem()
            pitems.setText(0,shortName)

            attrType = cmds.attributeQuery(shortName, n=self.breakoutNode, at=True)
            labelIcon = self.iconForAttrType(attrType)
            pitems.setIcon(0, labelIcon)

            while len(lastItem)>0:
                if lastItem[-1].text(0) in shortName and not(shortName[-3:]=='RGB' and lastItem[-1].text(0)[-1]=='R'):
                    lastItem[-1].addChild(pitems)
                    lastItem.append(pitems)
                    break
                else:
                    lastItem.pop()
            if len(lastItem)==0:
                lastItem.append(pitems)
                self.breakoutAttributesWidget.addTopLevelItem(pitems)

    def iconForAttrType(self, attrType, dim=False):
        color = None
        if attrType in self.attrColors:
            color = self.attrColors[attrType]
        else:
            color = self.attrColors['unknown']
        guiColor = qt.QColor(color[0], color[1], color[2], (0 if dim else 255))
        pixmap = qt.QPixmap (pix(100),pix(100))
        pixmap.fill(qt.QColor(0,0,0,0))
        painter = qt.QPainter(pixmap)
        painter.setBrush(guiColor)
        painter.drawEllipse(pix(25),pix(25),pix(50),pix(50))
        painter.end()
        return qt.QIcon(pixmap)

    def populateObjects(self, nodes=None):
        if nodes is None:
            nodes = self.fromNodes
        self.data.lastOutput = 0
        breakoutUUID = cmds.ls(self.breakoutNode, uuid=True)[0]
        dgroup = self.data.makeGroup()
        pgroup = qt.QTreeWidgetItem()
        pgroup.setText(0, dgroup["name"])
        pgroup.setFlags(qt.Qt.ItemIsDragEnabled | qt.Qt.ItemIsEditable|pgroup.flags())

        objects = self.data.getAllObjects(None, True)
        addedObject = False

        for obj in nodes:
            if len(cmds.ls(obj))==0:
                nodes.remove(obj)
                continue
            nodeType = cmds.nodeType(obj)
            if 'MASH' in nodeType:
                nodes.remove(obj)
                continue

        for obj in nodes:
            uuid = cmds.ls( obj, uuid=True )[0]
            if uuid in objects:
                continue

            dobj = self.data.makeObject(uuid)
            self.checkConnectionOnObject(dobj)

            #check if it already has an output index
            objConns = self.getNodeConnections(dobj, True)
            if len(objConns)>0:
                dobj['outputId'] = int(objConns[0].split('.')[0])

            pitems=qt.QTreeWidgetItem()
            pitems.setText(0,cmds.ls(uuid)[0] + '['+str(dobj['outputId']) + ']')

            pitems.setText(1,"\n".join(dobj["conns"]) )
            imgName = ":out_" + 'mesh' if cmds.nodeType(obj)=='transform' else cmds.nodeType(obj) + ".png"
            pitems.setIcon(0, qt.QIcon(imgName))
            pitems.setFlags(qt.Qt.ItemIsDragEnabled|pitems.flags())
            pitems.setFlags(pitems.flags() & ~qt.Qt.ItemIsDropEnabled)

            if len(nodes)==1:
                self.objectsWidget.addTopLevelItem(pitems)
                self.data.insertObject(dobj)
                self.objectsWidget.clearSelection()
                pitems.setSelected(True)
                return
            pgroup.addChild(pitems)
            self.data.insertObject(dobj, dgroup)
            addedObject = True

        if addedObject:
            self.objectsWidget.clearSelection()
            pgroup.setSelected(True)
            self.data.insertObject(dgroup)
            self.objectsWidget.addTopLevelItem(pgroup)


    def groupNameChanged(self, item):
        indexes = self.getItemIndexes(item)
        group = self.data.getObject(indexes)
        if(self.data.isGroup(group)):
            group["name"] = item.text(0)
            self.saveData()

    def groupDoubleClicked(self, item, column):
        self.objectsWidget.editItem(item, 0)

    def nextFreeMulti(self, nodeName, attributeName):
        thisNode = mashGetMObjectFromNameOne(nodeName)
        fnNode = old.MFnDependencyNode(thisNode)
        attribute = fnNode.attribute(attributeName)
        inPlug = old.MPlug( thisNode, attribute )
        count = inPlug.numConnectedElements()
        existingArray = old.MIntArray()
        inPlug.getExistingArrayAttributeIndices(existingArray)
        if existingArray:
            prev = existingArray[0]
            freeIndex = len(existingArray)
            #not very pythonic, sorry.
            for this in existingArray[1:]:
                if this > prev+1:
                    for item in range(prev+1, this):    # this handles gaps of 1 or more
                        freeIndex = item
                        break
                        prev = this
        else:
            return 0

        return freeIndex

class AttributeTreeWidget(qt.QTreeWidget):
    def __init__(self, parent=None):
        super(AttributeTreeWidget, self).__init__()

        self.setColumnCount(1)
        self.headerItem().setText(0, "Name")

class ObjectTreeWidget(qt.QTreeWidget):
    def __init__(self, parent=None):
        super(ObjectTreeWidget, self).__init__()

        font = qt.QFont()
        font.setPointSize(13)
        self.setFont(font)

        self.setColumnCount(2)
        self.headerItem().setText(0, _SR["Name"] + " "*30)
        self.headerItem().setText(1, _SR["Connections"]+ " "*30)
        self.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(qt.QAbstractItemView.InternalMove)

        mime = qt.QMimeData()
        mime.setData('application/x-item', qt.QByteArray(b'???'))

        drag = qt.QDrag(self)
        drag.setMimeData(mime)

        self.setAcceptDrops(True)
        self.setAlternatingRowColors(True)

    #def supportedDropActions(self):
    #    return qt.Qt.MoveAction
    def dragEnterEvent(self, event):
        event.acceptProposedAction()
        event.accept()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()
        event.accept()


class MCallbackIdWrapper(object):
    '''Wrapper class to handle cleaning up of MCallbackIds from registered MMessage
    '''
    def __init__(self, callbackId):
        super(MCallbackIdWrapper, self).__init__()
        self.callbackId = callbackId

    def __del__(self):
        old.MMessage.removeCallback(self.callbackId)

    def __repr__(self):
        return 'MCallbackIdWrapper(%r)'%self.callbackId

def connectionManagerWindowDestroyed (toNode=None):
    global connectionManagerWindow

    if connectionManagerWindow:
        connectionManagerWindow.saveData()
        connectionManagerWindow._registeredMayaCallbacks = []
        toNode = connectionManagerWindow.breakoutNode

    if toNode is None:
        return

    connectionManagerWindow = None

def CreateUI(fromNodes, toNode):
    # Create Window
    #   Parent the widget under the Maya mainWindow so it does not auto-destroy itself when the variable that references
    #   it goes out of scope

    toNode = toNode.split('.')[0]

    global connectionManagerWindow

    if connectionManagerWindow is None:
        # Get a pointer to the main maya window to use as a parent
        mainWindowPtr = omui.MQtUtil.mainWindow()
        mainWindow = wrapInstance(int(mainWindowPtr), qt.QWidget)
        connectionManagerWindow = ConnectionManager(name=_SR['Breakout Connection Manager'], fromNodes=fromNodes, toNode=toNode, parent=mainWindow)
        connectionManagerWindow.setProperty("saveWindowPref", True ) # identify a Maya-managed floating window, which handles the z order properly and saves its positions
    else:
        if toNode != connectionManagerWindow.breakoutNode:
            connectionManagerWindow.updateBreakoutMenu(toNode)

        connectionManagerWindow.fromNodes = fromNodes
        connectionManagerWindow.updateData()

    closeScriptStr = 'import MASH.breakoutConnectionManager\nMASH.breakoutConnectionManager.connectionManagerWindowDestroyed()'

    connectionManagerWindow.show(dockable=True, plugins='MASH', closeCallback=closeScriptStr)
    connectionManagerWindow.window().raise_()
    connectionManagerWindow.raise_()
    connectionManagerWindow.activateWindow()

    return connectionManagerWindow
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
