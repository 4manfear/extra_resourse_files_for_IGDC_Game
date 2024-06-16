from __future__ import division
from builtins import range
import maya.OpenMayaUI as mui
import MASH.breakoutConnectionManager as bcm
import sys
if sys.version_info[0] < 3:
    from sets import Set
import collections
import MASH.undo as undo
import MASH.dynamicsUtils as dynamicsUtils
import MASH.api as mapi
import re

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix
import six

def strRes(key):
    return mel.eval('getPluginResource("MASH", "%s")' % key)

kFields = ["vortexField","uniformField","turbulenceField","dragField","gravityField","newtonField","radialField","airField","volumeAxisField"]
#get the string resources
kDisconnectedNodes = strRes('kDisconnectedNodes')
kConnectedTheseNodes = strRes('kConnectedTheseNodes')
kIncompatibleTypes = strRes('kIncompatibleTypes')
kTypeNotSelected = strRes('kTypeNotSelected')
kDragDropType = strRes('kDragDropType')
kShowInOutliner = strRes('kShowInOutliner')
kBreakConnection = strRes('kBreakConnection')
kConnect = strRes('kConnect')
kConnected = strRes('kConnected')
kTo = strRes('kTo')
kIncompatibleNodes = strRes('kIncompatibleNodes')
kAnd = strRes('kAnd')
kDisconnected = strRes('kDisconnected')
kFrom = strRes('kFrom')
kNotConnected = strRes('kNotConnected')
kNoMeshFound = strRes('kNoMeshFound')
kDisabled = strRes('kDisabled')
kCreate = strRes('kCreate')
kClone = strRes('kClone')
kCreated = strRes('kCreated')
kNo = strRes('kNo')
kSelected = strRes('kSelected')
kFalloffNoInputs = strRes('kFalloffNoInputs')
kUnexpectedInput =  strRes('kUnexpectedInput')
kNodeNotSupportedWarning = strRes('kNodeNotSupportedWarning')
kSnapToMesh = strRes('kSnapToMesh')

def build_qt_widget(lay, node, wantedType, attr, sourceAttr, postCmd, label):
    widget = MASHlistQtWidget(node, wantedType, attr, sourceAttr, postCmd, label)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def update_qt_widget(layout, node, wantedType, attr, sourceAttr, postCmd, label):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "MASHlistQtWidget":
                widget.set_node(node, wantedType, attr, sourceAttr, postCmd, label)
                break
            #isinstance DOES NOT always detect the correct class type unfortunatly
            #if isinstance(widget, MASHlistQtWidget):
            #    widget.set_node(node, wantedType, attr, sourceAttr, postCmd)


class MASHListWidget(fx.ListButtonWidget):
    def __init__(self, *args, **wargs):
        fx.ListButtonWidget.__init__(self)
        self.setAutoFillBackground(True)
        self.setProperty('bgColor', self.palette().color(qt.QPalette.Window))


    def onBackgroundPropertyChange(self):
        p = self.palette()
        p.setColor(qt.QPalette.Window, self.property('bgColor'))
        self.setPalette(p)

    def event(self, e):
        if e.type() == qt.QEvent.Type.DynamicPropertyChange:
            self.onBackgroundPropertyChange()

        return fx.ListButtonWidget.event(self, e)


class MASHlistQtWidget(qt.QWidget):
    def __init__(self, node, wantedType, attr, sourceAttr, postCmd, label, parent=None):
        qt.QWidget.__init__(self, parent)

        mashPath = mel.eval('getenv("MASH_LOCATION")')
        self.iconsPath = mashPath+'icons/'

        self.setMinimumWidth(pix(380))
        self.setMinimumHeight(pix(103))
        self.setMouseTracking(True)

        self.setLayout(qt.QVBoxLayout())
        self.layout().setContentsMargins(pix(5),pix(3),pix(11),pix(3))
        self.layout().setSpacing(pix(5))

        self.headerLayout = qt.QHBoxLayout()
        self.headerTitle = qt.QLabel()
        self.headerTitle.setContentsMargins(pix(2),pix(0),pix(0),pix(0))
        self.headerLayout.addWidget(self.headerTitle)

        if cmds.nodeType(node) == 'MASH_Placer':
            self.helperButton = qt.QPushButton(kSnapToMesh)
            self.helperButton.setIcon(fx.getIconFromName('out_MASH_Utilities'))
            self.helperButton.clicked.connect(self.snapToMeshes)
            self.headerLayout.addStretch()
            self.headerLayout.addWidget(self.helperButton)

        self.listWidget = MASHListWidget()
        self.listWidget.objectName = "MASH_ListWidget"
        self.listWidget.dataDelegate = self
        self.listWidget.showToggleButton = False
        self.listWidget.setFixedHeight(pix(130))
        self.listWidget.setDefaultDropAction(qt.Qt.MoveAction)
        self.listWidget.setDropIndicatorShown(True)
        self.listWidget.showDropIndicator = True
        self.layout().addLayout(self.headerLayout)
        self.layout().addWidget(self.listWidget)

        self.set_node(node, wantedType, attr, sourceAttr, postCmd, label)

    # Delegates
    def dropEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            self.droppedNode = e.mimeData().text()
            success = self.connectNode()
            if not success:
                self.flashRedIndicator()

    def flashRedIndicator(self):
        p = self.listWidget.property('bgColor')
        p2 = qt.QColor(255, 72, 82)
        self.paAnimation = qt.QPropertyAnimation(self.listWidget, qt.QByteArray(b'bgColor'))
        self.paAnimation.setEasingCurve(qt.QEasingCurve.InOutQuint)
        self.paAnimation.setStartValue(p)
        self.paAnimation.setKeyValueAt(0.5, p2)
        self.paAnimation.setEndValue(p)
        self.paAnimation.setDuration(500)
        self.paAnimation.start()
        cmds.evalDeferred('import maya.cmds as cmds; cmds.warning("{}")'.format(kNodeNotSupportedWarning))


    def buttonPressed(self, index, buttonName):
        if buttonName == 'invertFalloffBtn':
            item = self.listWidget.itemFromIndex( index )
            attr = item.text() + '.invertFalloff'
            current = cmds.getAttr(attr)
            item.getButton('invertFalloffBtn').state = abs(current-1)
            self.listWidget.viewport().update()
            cmds.setAttr(attr, not current)

        elif buttonName == 'enableFalloffBtn':
            item = self.listWidget.itemFromIndex( index )
            attr = item.text() + '.enable'
            current = cmds.getAttr(attr)
            item.getButton('enableFalloffBtn').state = abs(current-1)
            self.listWidget.viewport().update()
            cmds.setAttr(attr, not current)


    def doubleClick(self, index, buttonName):
        self.listWidget.setCurrentRow(index.row())
        self.showInOutliner(False)

    def setupTreeMenu(self, treeMenu, position):
        item = self.listWidget.itemAt( position )
        if item:
            showInOutliner = qt.QAction(fx.getIconFromName('out_MASH_ShowInOutliner'), kShowInOutliner, self)
            showInOutliner.triggered.connect(lambda: self.showInOutliner(True))
            treeMenu.addAction(showInOutliner)
            disconnectAttr = qt.QAction(fx.getIconFromName('out_MASH_BreakConnection'), kBreakConnection, self)
            disconnectAttr.triggered.connect(self.disconnectNode)
            treeMenu.addAction(disconnectAttr)
            if self.desiredNodeType == 'MASH_Falloff':
                createLocAction = qt.QAction(fx.getIconFromName('ae_MASH_Falloff'), kClone, self)
                createLocAction.triggered.connect(lambda: self.cloneFalloff(position))
                treeMenu.addAction(createLocAction)

                color = item.color
                labelIcon = fx.createColorIcon(qcolor=color)
                colorMenu = treeMenu.addMenu(labelIcon, fx.colorLabel('kLabelColour'))
                for colorName in fx.allColorLabels():
                    labelIcon = fx.createColorIcon(colorName)
                    colorMenu.addAction(labelIcon, colorName, lambda prm=fx.getColourFromLabel(colorName): self.setFalloffColor(prm))

        else:
            self.listWidget.clearSelection()
            sel = cmds.ls( selection=True )
            if cmds.nodeType(self.node) != "MASH_Breakout":
                createLocAction = qt.QAction(fx.getIconFromName('out_MASH_CreateUtility'), kCreate, self)
                if self.desiredNodeType == 'MASH_Falloff':
                    createLocAction.triggered.connect(self.createFalloff)
                    treeMenu.addAction(createLocAction)
                if self.desiredNodeType == 'transform':
                    createLocAction.triggered.connect(self.createLocator)
                    treeMenu.addAction(createLocAction)
                if self.desiredNodeType == 'MASH_ChannelRandom':
                    createLocAction.triggered.connect(self.createChannelRandom)
                    treeMenu.addAction(createLocAction)
                if self.desiredNodeType == 'MASH_Constraint':
                    createLocAction.triggered.connect(self.createConstraint)
                    treeMenu.addAction(createLocAction)

            if sel:
                self.droppedNode = sel
                connectAttr = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_Connect.png"),kConnect, self)
                connectAttr.triggered.connect(self.connectNode)
                treeMenu.addAction(connectAttr)

    def setFalloffColor(self, color):
        for item in self.listWidget.selectedItems() or []:
            item.color = color
            cmds.setAttr(item.text() + '.colour', color.red()/255.0, color.green()/255.0, color.blue()/255.0, typ='double3')
        self.listWidget.viewport().update()

    def selectionChanged(self):
        pass

    #update connections
    def set_node(self, node, wantedType, attr, sourceAttr, postCmd, label):
        self.droppedNode = ""
        self.node = node
        self.desiredNodeType = wantedType
        self.attr = attr
        self.sourceAttr = sourceAttr
        self.sourceAttrRaw = sourceAttr
        self.postCmd = postCmd

        cmd = 'getPluginResource("MASH",' + '"' + label + '")'
        self.label = mel.eval(cmd)
        self.headerTitle.setText(self.label)

        self.checkConnections()


    def enterEvent(self,event):
        self.headerTitle.setText("%s %s" % (kDragDropType, self.desiredNodeType))
        self.listWidget.setCursor(qt.QCursor(qt.QPixmap(self.iconsPath+'rmbMenu.png'), pix(7), pix(5)))

    def leaveEvent(self,event):
        self.listWidget.setCursor(qt.Qt.ArrowCursor)
        self.headerTitle.setText(self.label)

    def checkConnections(self):
        self.listWidget.clear()
        connections = cmds.listConnections('%s.%s' % (self.node,self.attr), sh=True)

        if not connections:
            return

        connections = list(OrderedSet(connections))

        for curve in connections:
            item = fx.ListButtonItem(curve, self.listWidget)

            iconPath = ''

            if self.desiredNodeType == "MASH_Falloff":
                iconPath = "ae_MASH_Falloff"

                flipIcon = fx.getPixmap("MASH_InvertOff")
                flipIcon2 = fx.getPixmap("MASH_InvertOn")
                item.addButton([flipIcon, flipIcon2], 'invertFalloffBtn', alignRight=True)

                attr = item.text() + '.invertFalloff'
                current = cmds.getAttr(attr)
                item.getButton('invertFalloffBtn').state = current

                enableIcon = fx.getPixmap("out_MASH_Disable")
                enableIcon2 = fx.getPixmap("out_MASH_Enable")
                item.addButton([enableIcon, enableIcon2], 'enableFalloffBtn', alignRight=True)

                attr = item.text() + '.enable'
                current = cmds.getAttr(attr)
                item.getButton('enableFalloffBtn').state = current

                item.color = qt.QColor(*[x*255 for x in cmds.getAttr(curve + '.colour')[0]])

            elif self.desiredNodeType == "transform":
                iconPath = "locator"

            elif "nurbsCurve" in self.desiredNodeType:
                iconPath = "curveEP"

            elif self.desiredNodeType == "stroke":
                iconPath = "out_stroke"

            elif self.desiredNodeType == "MASH_Waiter":
                iconPath = "ae_MASH_Waiter"

            elif self.desiredNodeType == "MASH_ChannelRandom":
                iconPath = "ae_MASH_ChannelRandom"

            elif self.desiredNodeType == "MASH_Constraint":
                iconPath = "out_MASH_Constraint"

            elif self.desiredNodeType == "mesh":
                iconPath = "out_mesh"

            elif any(cmds.nodeType(curve) in s for s in kFields):
                iconPath = "out_"+cmds.nodeType(curve)

            if len(iconPath) > 0:
                icon = fx.getPixmap(iconPath)
                item.addButton([icon], 'nodeTypeIcon', highlightable=False)

            self.listWidget.addItem(item)

    def showInOutliner(self, checkShapes = False):
        selectedItems = self.listWidget.selectedItems()
        if selectedItems is not None:
            allOutliners = cmds.getPanel(typ='outlinerPanel') #get the names of all the outliners
            outliner = str(allOutliners[0]) #assume we want the first one (lazy, should be more discriminating)
            allPannels = cmds.getPanel(vis=1) #get all the pannels
            cmds.select( clear=True )
            for sel in selectedItems:
                selectedNode = sel.text()
                if not any('outliner' in s for s in allPannels): #is there an outliner in the house?
                    cmds.OutlinerWindow() #bring up an outliner
                cmds.select( selectedNode,  add=True  )
                cmds.evalDeferred("import maya.cmds as cmds; import maya.mel as mel; cmds.outlinerEditor('%s', e=1, sc=1); mel.eval('showEditorExact(\"%s\")')" % (outliner, selectedNode)) # show in the outliner
        #check if the user has requested a shape be shown in the outliner, if so, we'll need to enable shape display for them
        if checkShapes and self.checkInheritsShape(selectedItems):
            cmds.evalDeferred("import maya.cmds as cmds; cmds.outlinerEditor('%s', e=1, showShapes=1)" % outliner) # enable show shapes

    """
    Check if any of the selected objects inherit from the Shape base node type
    """
    def checkInheritsShape(self, selectedItems):
        enableShapeDisplay = False
        for sel in selectedItems:
            nodeType = cmds.nodeType( sel.text(), i=True )
            if "shape" in nodeType:
                enableShapeDisplay = True
        return enableShapeDisplay

    #checks to see if we actually want the node that was dropped onto the dropzone
    #node types can be single, like "mesh", or comma seperated like "mesh, nurbsCurve" any MASH node can be specified by using "MASH_" as a node type.
    def isDesiredNode(self, nodeType):
        wantedNodeTypes = self.desiredNodeType.split(',')
        destinationAttr = self.sourceAttrRaw.split(',')
        for i in range (0, len(wantedNodeTypes), 1):
            if wantedNodeTypes[i] == nodeType:
                if len(destinationAttr) > i:
                    self.sourceAttr = destinationAttr[i]
                else:
                    self.sourceAttr = destinationAttr[0]
                return True
            elif wantedNodeTypes[i] == "MASH_" and wantedNodeTypes[i] == nodeType[:5]:
                self.sourceAttr = destinationAttr[i]
                return True
        return False


    def connectNode(self):
        if isinstance(self.droppedNode, six.string_types):
            temp = self.droppedNode
            #splitlines here as Maya now splits multiple selected objects by newlines.
            self.droppedNode = temp.splitlines()

        connectedNode = False

        if (len(self.postCmd) > 0):
            connectedNode = self.runPreCommand(self.postCmd)

        # skip if we don't manage the connection
        if len(self.sourceAttr) == 0:
            return connectedNode

        toHighlight = []

        for droppedNodes in self.droppedNode:
            nodeType = cmds.nodeType( droppedNodes )
            if self.desiredNodeType == "MASH_Falloff" and nodeType == "MASH_Audio":
                self.desiredNodeType = "MASH_Audio"

            # Check if it is already connected
            try:
                alreadyConnected = cmds.listConnections('%s.%s' % (self.node, self.attr)) or []
                alreadyConnected = [cmds.ls(x, long=True)[0] for x in alreadyConnected]

                if droppedNodes in alreadyConnected:
                    connectedNode = True
                    shapeName = cmds.listRelatives(droppedNodes, shapes=True)[0]
                    toHighlight.append(shapeName)
                    continue

            except Exception as e:
                print(str(e))
                pass

            index = mel.eval('getNextFreeMultiIndex( (\"'+self.node+'\"+"."+\"'+self.attr+'\"), 0 )')
            if (nodeType == "transform" and self.desiredNodeType != "transform"):
                shapes = cmds.listRelatives(droppedNodes)
                droppedNodes = shapes[0] #get the first found shape
                nodeType = cmds.nodeType( droppedNodes )

            isWanted = self.isDesiredNode(nodeType)
            if isWanted:

                 #check the falloff object has incoming connections
                if self.desiredNodeType == "MASH_Falloff" and nodeType == "MASH_Falloff":
                    standardConnect = self.checkFalloffConnections(droppedNodes)
                    if not standardConnect:
                        return connectedNode
                cmds.connectAttr(  '%s.%s' % (droppedNodes,self.sourceAttr), '%s.%s[%s]' % (self.node,self.attr, index), force=True )
                message = cmds.format(kConnectedTheseNodes, stringArg=(droppedNodes, self.node))
                command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
                mel.eval(command)
                hasMASHFlag = cmds.objExists('%s.mashOutFilter' % (droppedNodes))
                if not hasMASHFlag:
                    cmds.addAttr( droppedNodes, longName='mashOutFilter', attributeType='bool' )
                connectedNode = True
                #run the post connection command if there is one
                if (len(self.postCmd) > 0):
                    self.runPostCommand(self.postCmd)
            #if not a MASH node (which may be selected to get at the interface), error.
            elif nodeType[:5] != "MASH_":
                message = cmds.format(kIncompatibleTypes, stringArg=(nodeType, self.desiredNodeType))
                command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Error\\")\"'
                mel.eval(command)
        self.checkConnections() #repopulate list

        for i in range(self.listWidget.count()):
            name = self.listWidget.item(i).text()
            if name in toHighlight:
                self.listWidget.item(i).setSelected(True)

        if not connectedNode:
            message = cmds.format(kTypeNotSelected, stringArg=self.desiredNodeType)
            command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Error\\")\"'
            mel.eval(command)

        return connectedNode

    def disconnectNode(self):
        if self.postCmd == 'ConnectColliderObject':
            stat = self.runCustomDisconnectCommand(self.postCmd)
            return
        selectedItems = self.listWidget.selectedItems()
        for sel in selectedItems:
            nodeType = cmds.nodeType( sel.text() )
            self.isDesiredNode(nodeType) #sets the correct attributes to disconnect from
            selectedNode = sel.text()
            if cmds.nodeType(self.node) != "MASH_Breakout":
                connections = cmds.listConnections( '%s.%s' % (selectedNode,self.sourceAttr), p=True)
                if not connections:
                    continue
                for conn in connections:
                    if self.node in conn:
                        cmds.disconnectAttr(  '%s.%s' % (selectedNode,self.sourceAttr), conn)

                        message = cmds.format(kDisconnectedNodes, stringArg=(selectedNode, self.node))
                        command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
                        mel.eval(command)
                        hasMASHFlag = cmds.objExists('%s.mashOutFilter' % (selectedNode))
                        if hasMASHFlag:
                            cmds.deleteAttr( selectedNode, at='mashOutFilter' )
            else:
                connections = cmds.listConnections(self.node, plugs=True, skipConversionNodes=True) or []
                connections = [x for x in connections if x.startswith(selectedNode + '.')]
                for conn in connections:
                    source = cmds.listConnections(conn, plugs=True, skipConversionNodes=True) or []
                    if source:
                        source = source[0]
                        cmds.disconnectAttr(source, conn)
            

        self.checkConnections() #repopulate list

    #pre defined post commands used to set attributes on nodes specific to MASH
    def runPostCommand(self, commandId):
        if commandId == 'SwitchToInitialState':
            cmds.setAttr( '%s.arrangement' % (self.node), 7 )
        if commandId == 'SwitchToPfxMode':
            cmds.setAttr( '%s.arrangement' % (self.node), 8 )

    #pre defined pre connection commands
    def runPreCommand(self, commandId):
        if commandId == 'BreakoutNodeConnect':
            bcm.CreateUI(self.droppedNode, self.node)
            return True

        if commandId == 'ConnectTrailsToWaiter':
            for droppedNodes in self.droppedNode:
                cmds.connectAttr( '%s.outputPoints' % (self.node), '%s.inputPoints' % (droppedNodes), force=True )
                message = '%s %s.%s %s %s.%s' % (kConnected, self.droppedNode,self.sourceAttr,kTo,self.node,self.attr)
                command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
                mel.eval(command)
            self.checkConnections() #repopulate list
            return True

        if commandId == 'ConnectColliderObject':
            success = False

            allItemsInListWidget = [self.listWidget.item(x).text() for x in range(self.listWidget.count())]
            toHighlight = []

            for droppedNodes in self.droppedNode:
                nodeType = cmds.nodeType( droppedNodes )
                if (nodeType == "transform" and self.desiredNodeType != "transform"):
                    shapes = cmds.listRelatives(droppedNodes)
                    droppedNodes = shapes[0] #get the first found shape
                    nodeType = cmds.nodeType( droppedNodes )
                    isWanted = self.isDesiredNode(nodeType)
                    if isWanted:
                        success = True
                        if droppedNodes in allItemsInListWidget:
                            toHighlight.append(droppedNodes)
                            continue
                        dynamicsUtils.connectColliderObject(self.node, droppedNodes)

            for i in range(self.listWidget.count()):
                name = self.listWidget.item(i).text()
                if name in toHighlight:
                    self.listWidget.item(i).setSelected(True)

            return success

    #pre defined pre connection commands
    def runCustomDisconnectCommand(self, commandId):
        selectedItems = self.listWidget.selectedItems()
        for sel in selectedItems:
            nodeType = cmds.nodeType( sel.text() )
            self.isDesiredNode(nodeType) #sets the correct attributes to disconnect from

            outputPlugs = cmds.listConnections( sel.text()+".collisionShape", s=False, d=True, p=True)
            solverConnection = None
            for conn in outputPlugs:
                node = conn.split('.')[0]
                if cmds.nodeType(node) == "MASH_BulletSolver":
                    solverConnection = conn
                    break

            if solverConnection == None:
                cmds.error("Disconnect MASH Node: Solver not found")

            index = solverConnection[solverConnection.find("[")+1:solverConnection.find("]")]
            cmds.removeMultiInstance(self.node+'.collisionObjects['+index+']', b=True)

            selectedNode = sel.text()
            message = cmds.format(kDisconnectedNodes, stringArg=(selectedNode, self.node))
            command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
            mel.eval(command)


    def createLocator(self):
        newTransform = cmds.createNode('transform', n='%s_loc'% (self.node), skipSelect=True)
        digit = re.match(r'[^\d]*(\d*)', newTransform).group(1)
        newShape = cmds.createNode('locator', p=newTransform, n='%s_locShape%s'% (self.node, digit), skipSelect=True)
        cmds.setAttr( '%s.overrideColor' % (newTransform), 9 )
        cmds.setAttr( '%s.overrideEnabled' % (newTransform), 1 )
        self.droppedNode = newTransform
        self.connectNode()

    def createFalloff(self):
        falloffNode = mel.eval('MASH_FalloffButtonCmds("'+self.node+'", 1)')

        message = '%s %s' % (kCreated, self.desiredNodeType)
        command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
        mel.eval(command)
        if (len(self.postCmd) > 0):
            self.runPostDisconnectCommand(self.postCmd)

        parent = cmds.listRelatives( falloffNode, parent=True )[0]
        cmds.select(parent)

    def createChannelRandom(self):
        newNode = cmds.createNode('MASH_ChannelRandom', skipSelect=True)
        message = '%s %s' % (kCreated, self.desiredNodeType)
        command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
        mel.eval(command)
        index = mel.eval('getNextFreeMultiIndex( (\"'+self.node+'\"+"."+\"'+self.attr+'\"), 0 )')
        inConns = cmds.listConnections('%s.inputPoints' % (self.node), p=True)
        cmds.connectAttr( inConns[0], newNode+'.inputPoints')
        cmds.connectAttr(newNode+'.outputPoints', self.node+"."+self.attr+"["+str(index)+"]")
        if self.postCmd == 'ConstraintChannelRandom':
            cmds.setAttr( '%s.dynamicsChannelName' % (newNode), 0 )

    def createConstraint(self):
        newNode = cmds.createNode('MASH_Constraint', skipSelect=True)
        message = '%s %s' % (kCreated, self.desiredNodeType)
        command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Info\\")\"'
        mel.eval(command)
        index = mel.eval('getNextFreeMultiIndex( (\"'+self.node+'\"+"."+\"'+self.attr+'\"), 0 )')
        inConns = cmds.listConnections('%s.inputPoints' % (self.node), p=True)
        cmds.connectAttr( inConns[0], newNode+'.inputPoints')
        cmds.connectAttr(newNode+'.outputPoints', self.node+"."+self.attr+"["+str(index)+"]")

    def cloneFalloff(self, pos=-1):
        cmds.select(clear=True)
        if pos != -1:
            item = self.listWidget.itemAt( pos )
            cmds.select(item.text(), add=True)
        else:
            cmds.select(self.droppedNode[0], add=True)

        mel.eval('MASH_FalloffButtonCmds("'+self.node+'", 2)')
        if (len(self.postCmd) > 0):
            self.runPostDisconnectCommand(self.postCmd)

    def checkFalloffConnections(self, falloffObject):
        connections = cmds.listConnections('%s.falloffIn' % (falloffObject))
        nodeInConnectionsPlug = cmds.listConnections('%s.inputPoints' % (self.node), p=True)

        #Falloff node has no input connection (user has duplicated it in the outliner), so connect one.
        if not connections:
            if nodeInConnectionsPlug:
                cmds.connectAttr( nodeInConnectionsPlug[0], '%s.falloffIn' % (falloffObject), force=True )

        #Varify the incoming connection is what we expect.
        else:
            falloffInConnectionsPLug = cmds.listConnections('%s.falloffIn' % (falloffObject), p=True)
            if nodeInConnectionsPlug and nodeInConnectionsPlug[0] != falloffInConnectionsPLug[0]:
                modifiers = qt.QGuiApplication.keyboardModifiers()
                if modifiers == qt.Qt.AltModifier:
                    self.cloneFalloff()
                    return False
                else:
                    message = '%s: %s' % (kUnexpectedInput, falloffInConnectionsPLug[0])
                    command = 'evalDeferred \"MASHinViewMessage(\\"'+ message + '\\", \\"Warning\\")\"'
                    mel.eval(command)
        return True

    def snapToMeshes(self):
        placerNode = mapi.Node(self.node)
        placerNode.snapPlacerPointsToPaintMeshes()

class OrderedSet(collections.MutableSet):

    def __init__(self, iterable=None):
        self.end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.map = {}                   # key --> [key, prev, next]
        if iterable is not None:
            self |= iterable

    def __len__(self):
        return len(self.map)

    def __contains__(self, key):
        return key in self.map

    def add(self, key):
        if key not in self.map:
            end = self.end
            curr = end[1]
            curr[2] = end[1] = self.map[key] = [key, curr, end]

    def discard(self, key):
        if key in self.map:
            key, prev, next = self.map.pop(key)
            prev[2] = next
            next[1] = prev

    def __iter__(self):
        end = self.end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def pop(self, last=True):
        if not self:
            raise KeyError('set is empty')
        key = self.end[1][0] if last else self.end[2][0]
        self.discard(key)
        return key

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, list(self))

    def __eq__(self, other):
        if isinstance(other, OrderedSet):
            return len(self) == len(other) and list(self) == list(other)
        return set(self) == set(other)




# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
