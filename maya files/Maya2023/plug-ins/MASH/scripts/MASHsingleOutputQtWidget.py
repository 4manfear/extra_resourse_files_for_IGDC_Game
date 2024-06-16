from builtins import range
import maya.OpenMayaUI as mui

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

#get the string resources
kDisconnectedNodes = mel.eval('getPluginResource("MASH", "kDisconnectedNodes")')
kConnectedTheseNodes = mel.eval('getPluginResource("MASH", "kConnectedTheseNodes")')
kIncompatibleTypes = mel.eval('getPluginResource("MASH", "kIncompatibleTypes")')
kTypeNotSelected = mel.eval('getPluginResource("MASH", "kTypeNotSelected")')
kDragDropType = mel.eval('getPluginResource("MASH", "kDragDropType")')
kShowInOutliner = mel.eval('getPluginResource("MASH", "kShowInOutliner")')
kBreakConnection = mel.eval('getPluginResource("MASH", "kBreakConnection")')
kConnect = mel.eval('getPluginResource("MASH", "kConnect")')
kConnected = mel.eval('getPluginResource("MASH", "kConnected")')
kTo = mel.eval('getPluginResource("MASH", "kTo")')
kIncompatibleNodes = mel.eval('getPluginResource("MASH", "kIncompatibleNodes")')
kAnd = mel.eval('getPluginResource("MASH", "kAnd")')
kDisconnected = mel.eval('getPluginResource("MASH", "kDisconnected")')
kFrom = mel.eval('getPluginResource("MASH", "kFrom")')
kNotConnected = mel.eval('getPluginResource("MASH", "kNotConnected")')
kNoMeshFound = mel.eval('getPluginResource("MASH", "kNoMeshFound")')
kDisabled = mel.eval('getPluginResource("MASH", "kDisabled")')
kClone = mel.eval('getPluginResource("MASH", "kClone")')
kCreate = mel.eval('getPluginResource("MASH", "kCreate")')
kCreated = mel.eval('getPluginResource("MASH", "kCreated")')
kNo = mel.eval('getPluginResource("MASH", "kNo")')
kSelected = mel.eval('getPluginResource("MASH", "kSelected")')
kFalloffNoInputs = mel.eval('getPluginResource("MASH", "kFalloffNoInputs")')
kDisplayAsWireframe = mel.eval('getPluginResource("MASH", "kDisplayAsWireframe")')

class MASHsingleOutputQtWidget(qt.QWidget):
    def __init__(self, node, wantedType, attr, sourceAttr, postCmd, parent=None):
        super(MASHsingleOutputQtWidget, self).__init__(parent)
        self.node = node
        self.dropZone = MASH_QLineEditExtend(wantedType, node, attr, sourceAttr, postCmd)
        self.layout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom, self)
        self.layout.setContentsMargins(pix(0),pix(3),pix(0),pix(3))
        self.layout.setSpacing(pix(5))
        self.layout.addWidget(self.dropZone)

    #update connections
    def set_node(self, node, wantedType, attr, sourceAttr, postCmd):
        self.node = node
        self.dropZone.node = node
        self.dropZone.desiredNodeType = wantedType
        self.dropZone.attr = attr
        self.dropZone.sourceAttr = sourceAttr
        self.dropZone.checkConnections()
        self.dropZone.postCmd = postCmd

def build_qt_widget(lay, node, wantedType, attr, sourceAttr, postCmd):
    widget = MASHsingleOutputQtWidget(node, wantedType, attr, sourceAttr, postCmd)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def update_qt_widget(layout, node, wantedType, attr, sourceAttr, postCmd):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "MASHsingleOutputQtWidget":
                widget.set_node(node, wantedType, attr, sourceAttr, postCmd)
                break


class MASH_QLineEditExtend(qt.QLineEdit):
    def __init__(self, desiredNodeType, node, attr, sourceAttr, postCmd, parent=None):
        super(MASH_QLineEditExtend, self).__init__()
        self.setAcceptDrops(True)
        self.setMaximumHeight(pix(22))
        self.setReadOnly(True)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.setMouseTracking(True)
        self.desiredNodeType = desiredNodeType
        self.droppedNode = ""
        self.node = node
        self.attr = attr
        self.disableDropZone = False
        self.connected = False
        self.menu = qt.QMenu();
        self.sourceAttrRaw = sourceAttr
        self.sourceAttr = None
        self.postCmd = postCmd
        self.checkConnections()
        self.objectName = "MASH_DropZone"
        mashPath = mel.eval('getenv("MASH_LOCATION")')
        self.iconsPath = mashPath+'icons/'
        #checkable action for contextual menu
        self.wireframeAction = qt.QAction(kDisplayAsWireframe, self, checkable=True)
        self.wireframeAction.triggered.connect(self.setMeshToWireframe,)

    def setConnectedStyle(self):
        self.setStyleSheet("background-color:#F1F1A5; color: black;")

    def setBlankStyle(self):
        self.setStyleSheet("")

    def setDisabledStyle(self):
        self.setStyleSheet("background-color:#5C6874; color: black;")

    def checkConnections(self):
        connections = cmds.listConnections('%s.%s' % (self.node,self.attr), sh=True)
        if connections and (len(connections) > 0):
            for connect in connections:
                nodeType = cmds.nodeType(connect)
                if self.isDesiredNode(nodeType):
                    self.droppedNode = connect
                    self.setText(connect)
                    self.connected = True
                    self.setConnectedStyle()
                    return
        self.droppedNode = ""
        self.setBlankStyle()
        self.connected = False
        self.setText(kNotConnected)

    def disableDropZoneDropZone(self):
        self.setText(kDisabled)
        self.droppedNode = ""
        self.setDisabledStyle()

    def enterEvent(self,event):
        self.setCursor(qt.QCursor(qt.QPixmap(self.iconsPath+'rmbMenu.png'), pix(7), pix(5)))
        connections = cmds.listConnections('%s.%s' % (self.node,self.attr), sh=True)
        foundNode = False
        # there can be more then one connection to an output, make sure the type of node we want isn't connected before displaying the hint text
        if connections:
            for connect in connections:
                nodeType = cmds.nodeType(connect)
                if self.isDesiredNode(nodeType):
                    foundNode = True
        if not foundNode and not self.disableDropZone:
            self.setText("%s %s" % (kDragDropType, self.desiredNodeType))

    def leaveEvent(self,event):
        self.setCursor(qt.Qt.ArrowCursor)
        connections = cmds.listConnections('%s.%s' % (self.node,self.attr), sh=True)
        self.checkConnections()

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            qt.QLineEdit.dropEvent(self, e)
            self.droppedNode = e.mimeData().text()
            self.connectNode()

    def openMenu(self, pos):
        if self.disableDropZone:
            return
        self.checkConnections()
        self.menu.clear()
        if (self.connected == True):
            showInOutliner = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_ShowInOutliner.png"), kShowInOutliner, self)
            showInOutliner.triggered.connect(self.showInOutliner)
            self.menu.addAction(showInOutliner)
            disconnectAttr = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_BreakConnection.png"), kBreakConnection, self)
            disconnectAttr.triggered.connect(self.disconnectNode)
            self.menu.addAction(disconnectAttr)
            if self.desiredNodeType == 'mesh':
                self.menu.addAction(self.wireframeAction)
        else:
            if self.desiredNodeType == 'transform' and self.postCmd != 'MapSwitchToUVMode': #creating transforms is trivial, so lets support it.
                createLocAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_CreateUtility.png"), kCreate, self)
                createLocAction.triggered.connect(self.createLocator)
                self.menu.addAction(createLocAction)
            elif self.postCmd == 'MapSwitchToUVMode': #this means it's a map helper, we need to support creating those.
                createLocAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_CreateUtility.png"), kCreate, self)
                createLocAction.triggered.connect(self.createMapHelper)
                self.menu.addAction(createLocAction)
            if self.postCmd == 'AddAudioEq': #creating a points node as an audio equaliser
                createAudioEqAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_Points.png"), kCreate, self)
                createAudioEqAction.triggered.connect(self.createAudioEq)
                self.menu.addAction(createAudioEqAction)

            sel = cmds.ls( selection=True )
            if sel:
                connectAttr = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_Connect.png"), kConnect, self)
                connectAttr.triggered.connect(lambda: self.connectNode(sel[0]))
                self.menu.addAction(connectAttr)
        self.menu.exec_(qt.QCursor.pos())

    def showInOutliner(self):
        if (self.droppedNode != ""):
            allOutliners = cmds.getPanel(typ='outlinerPanel') #get the names of all the outliners
            outliner = str(allOutliners[0]) #assume we want the first one
            allPannels = cmds.getPanel(vis=1) #get all the pannels
            if any('outliner' in s for s in allPannels): #is there an outliner in the house?
                cmds.select( clear=True )
                cmds.select( self.droppedNode )
                cmds.evalDeferred("import maya.cmds as cmds; cmds.outlinerEditor('%s', e=1, sc=1)" % outliner) # show in the outliner
            else:
                cmds.OutlinerWindow() #bring up an outliner
                cmds.select( clear=True )
                cmds.select( self.droppedNode )
                cmds.evalDeferred("import maya.cmds as cmds; cmds.outlinerEditor('%s', e=1, sc=1)" % outliner) # show in the outliner

    def goToNode(self):
        if (self.droppedNode != ""):
            command = 'evalDeferred \"showEditorExact(\\"'+ self.droppedNode + '\\")\"'
            mel.eval(command)

    #checks to see if we actually want the node that was dropped onto the dropzone
    #node types can be single, like "mesh", or comma seperated like "mesh, nurbsCurve" any MASH node can be specified by using "MASH_" as a node type.
    def isDesiredNode(self, nodeType):
        wantedNodeTypes = self.desiredNodeType.split(',')
        destinationAttr = self.sourceAttrRaw.split(',')
        for i in range (0, len(wantedNodeTypes), 1):
            if wantedNodeTypes[i] == nodeType:
                self.sourceAttr = destinationAttr[i]
                return True
            elif wantedNodeTypes[i] == "MASH_" and wantedNodeTypes[i] == nodeType[:5]:
                self.sourceAttr = destinationAttr[i]
                return True
        return False

    def connectNode(self, selNode=""):
        #check if a node has been specified in the function call
        if len(selNode) > 0:
            self.droppedNode = selNode

        #to check if the pre connection command passes
        stat = True
        if (len(self.postCmd) > 0):
            stat = self.runPreCommand(self.postCmd)
        #if the pre connection command failed, return here
        if not stat:
            return
        nodeType = cmds.nodeType( self.droppedNode )

        #if the user selected a transform (and that isn't what we want) then get it's shape node
        if (nodeType == "transform" and self.desiredNodeType != "transform"):
            shapes = cmds.listRelatives(self.droppedNode)
            self.droppedNode = shapes[0] #get the first found shape
            nodeType = cmds.nodeType( self.droppedNode )

        isWanted = self.isDesiredNode(nodeType)

        if isWanted:
            self.setText(self.droppedNode)
            self.setConnectedStyle()
            cmds.connectAttr(  '%s.%s' % (self.node,self.attr), '%s.%s' % (self.droppedNode,self.sourceAttr), force=True )
            message = cmds.format(kConnectedTheseNodes, stringArg=(self.node, self.droppedNode))
            command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
            mel.eval(command)
            hasMASHFlag = cmds.objExists('%s.mashOutFilter' % (self.droppedNode))
            if not hasMASHFlag:
                cmds.addAttr( self.droppedNode, longName='mashOutFilter', attributeType='bool' )
            #run the post connection command if there is one
            if (len(self.postCmd) > 0):
                self.runPostCommand(self.postCmd)
        else:
            message = cmds.format(kIncompatibleTypes, stringArg=(nodeType, self.desiredNodeType))
            command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Error\\")\"'
            mel.eval(command)
        self.menu.clear()

    def disconnectNode(self):
        nodeType = cmds.nodeType( self.droppedNode )
        self.isDesiredNode(nodeType) #sets the correct attributes to disconnect from
        cmds.disconnectAttr(  '%s.%s' % (self.node,self.attr), '%s.%s' % (self.droppedNode,self.sourceAttr))
        self.menu.clear()
        self.setText(kNotConnected)
        self.setBlankStyle()
        message = cmds.format(kDisconnectedNodes, stringArg=(self.droppedNode, self.node))
        command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
        mel.eval(command)
        if (len(self.postCmd) > 0):
            self.runPostDisconnectCommand(self.postCmd)
        hasMASHFlag = cmds.objExists('%s.mashOutFilter' % (self.droppedNode))
        if hasMASHFlag:
            cmds.deleteAttr( self.droppedNode, at='mashOutFilter' )

    def createLocator(self):
        newTransform = cmds.spaceLocator( p=(0, 0, 0), n='%s_loc'% (self.node)  )
        cmds.setAttr( '%s.overrideColor' % (newTransform[0]), 9 )
        cmds.setAttr( '%s.overrideEnabled' % (newTransform[0]), 1 )
        self.droppedNode = newTransform[0]
        self.connectNode()
        self.setConnectedStyle()

    def createAudioEq(self):
        newTransform = cmds.createNode("transform", name="AudioEq#")
        self.droppedNode = cmds.createNode("MASH_Points", name="AudioEqShape#", parent=newTransform)
        cmds.setAttr( '%s.useCustomChannel' % (self.droppedNode), 1 )
        self.connectNode()
        self.setConnectedStyle()

    def setMeshToWireframe(self):
        if self.wireframeAction.isChecked():
            cmds.setAttr( '%s.overrideEnabled' % (self.droppedNode), 1 )
            cmds.setAttr( '%s.overrideShading' % (self.droppedNode), 0 )
            cmds.setAttr( '%s.overrideColor' % (self.droppedNode), 9 )
        else:
            cmds.setAttr( '%s.overrideEnabled' % (self.droppedNode), 0 )
            cmds.setAttr( '%s.overrideShading' % (self.droppedNode), 1 )
            cmds.setAttr( '%s.overrideColor' % (self.droppedNode), 0 )

    #pre defined post commands used to set attributes on nodes specific to MASH
    def runPostCommand(self, commandId):
        if commandId == "AddAudioEq":
            cmds.select(self.node)

    def runPostDisconnectCommand(self, commandId):
        return True

    #pre defined pre connection commands
    def runPreCommand(self, commandId):
        return True
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
