from __future__ import division
from builtins import range
from builtins import zip
import maya.OpenMayaUI as mui
import MASH.api as mapi
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

class MASHsingleInputQtWidget(qt.QWidget):
    def __init__(self, node, wantedType, attr, sourceAttr, postCmd, parent=None):
        super(MASHsingleInputQtWidget, self).__init__(parent)
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
    widget = MASHsingleInputQtWidget(node, wantedType, attr, sourceAttr, postCmd)
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
            if widget.metaObject().className() == "MASHsingleInputQtWidget":
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
        if not connections:
            self.setText(kNotConnected)
            self.droppedNode = ""
            self.connected = False
            self.setBlankStyle()
        elif (len(connections) > 0):
            self.droppedNode = connections[0]
            self.setText(connections[0])
            self.connected = True
            self.setConnectedStyle()

    def disableDropZoneDropZone(self):
        self.setText(kDisabled)
        self.droppedNode = ""
        self.setDisabledStyle()

    def enterEvent(self,event):
        self.setCursor(qt.QCursor(qt.QPixmap(self.iconsPath+'rmbMenu.png'), pix(7), pix(5)))
        connections = cmds.listConnections('%s.%s' % (self.node,self.attr), sh=True)
        if not connections and not self.disableDropZone:
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
        self.droppedNode = e.mimeData().text()
        self.connectNode()

    def dragMoveEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def openMenu(self, pos):
        if self.disableDropZone:
            return
        self.checkConnections()
        self.menu.clear()

        createMapHelperAction = False
        if (self.postCmd == 'MapSwitchToUVMode' or self.postCmd == 'PosMapSwitchToUVMode' or 
            self.postCmd == 'ScaleMapSwitchToUVMode' or self.postCmd == 'RotMapSwitchToUVMode' or 
            self.postCmd == 'ConstraintMapSwitchToUVMode'):
            createMapHelperAction = True

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
            if self.desiredNodeType == 'transform' and not createMapHelperAction: #creating transforms is trivial, so lets support it.
                createLocAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_CreateUtility.png"), kCreate, self)
                createLocAction.triggered.connect(self.createLocator)
                self.menu.addAction(createLocAction)
            elif createMapHelperAction: #this means it's a map helper, we need to support creating those.
                createLocAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_CreateUtility.png"), kCreate, self)
                createLocAction.triggered.connect(self.createMapHelper)
                self.menu.addAction(createLocAction)
            elif self.postCmd == 'ConnectVoxelContainer':
                createLocAction = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_CreateUtility.png"), kCreate, self)
                createLocAction.triggered.connect(self.createVoxelContainer)
                self.menu.addAction(createLocAction)

            sel = cmds.ls( selection=True )
            if sel:
                connectAttr = qt.QAction(qt.QIcon(self.iconsPath+"out_MASH_Connect.png"), kConnect, self)
                connectAttr.triggered.connect(lambda: self.connectNode(sel[0]))
                self.menu.addAction(connectAttr)

        self.menu.exec_(qt.QCursor.pos())

    def createVoxelContainer(self):
        mel.eval('source AEMASH_DistributeTemplate.mel')
        mel.eval('distButtonCMDS %s 2' % self.node)

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
            cmds.connectAttr(  '%s.%s' % (self.droppedNode,self.sourceAttr), '%s.%s' % (self.node,self.attr), force=True )
            message = cmds.format(kConnectedTheseNodes, stringArg=(self.droppedNode, self.node))
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
        cmds.disconnectAttr(  '%s.%s' % (self.droppedNode,self.sourceAttr), '%s.%s' % (self.node,self.attr))
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

    def createMapHelper(self):
        textureAttribute = 'mColour'
        matrixAttribute = 'inMapMatrix'
        if self.postCmd == 'PosMapSwitchToUVMode':
            matrixAttribute = 'positionMapMatrix'

        elif self.postCmd == 'RotMapSwitchToUVMode':
            matrixAttribute = 'rotationMapMatrix'

        elif self.postCmd == 'ScaleMapSwitchToUVMode':
            matrixAttribute = 'scaleMapMatrix'
        elif self.postCmd == 'ConstraintMapSwitchToUVMode':
            matrixAttribute = 'connectionMapMatrix'
            textureAttribute = 'connectionColour'

        texture = cmds.listConnections(self.node + '.' + textureAttribute, d=False, s=True) or []

        bbox = self.getNetworkBoundingBox()

        scaleX, scaleY, scaleZ = [abs(x-y) for x,y in zip(*bbox)]
        centerX, centerY, centerZ = [(x+y)/2 for x,y in zip(*bbox)]

        if scaleX < 1: scaleX = 1
        if scaleY < 1: scaleY = 1
        if scaleZ < 1: scaleZ = 1

        if texture:
            plane = cmds.polyPlane(ch=True, o=True, ax=[0,1,0], w=1.0, h=1.0, sw=10, sh=10, cuv=2, name=self.node+ ' Map Helper#')
            cmds.setAttr(plane[1] + '.createUVs', True)
            cmds.select(plane[0])
            mel.eval('createAndAssignShader lambert "";')
            shader = self.getSurfaceShader(plane[0])
            cmds.connectAttr(texture[0] + '.outColor', shader + '.color', force=True)
            cmds.setKeyframe(texture[0], attribute='frameOffset', t=0)
            cmds.setKeyframe(texture[0], attribute='frameOffset', t=50, v=0.4)

            try:
                cmds.setAttr(texture[0] + '.defaultColor', 0,0,0, typ='double3')
            except:
                pass

            try:
                cmds.connectAttr(plane[0]+ '.worldMatrix[0]', self.node+ '.' +matrixAttribute, f=True)
            except:
                pass

            cmds.setAttr(plane[0] + '.' + 'scaleX', scaleX * 1.02)
            cmds.setAttr(plane[0] + '.' + 'scaleY', scaleY * 1.02)
            cmds.setAttr(plane[0] + '.' + 'scaleZ', scaleZ * 1.02)

            cmds.setAttr(plane[0] + '.' + 'translateX', centerX * 1.02)
            cmds.setAttr(plane[0] + '.' + 'translateY', centerY * 1.02)
            cmds.setAttr(plane[0] + '.' + 'translateZ', centerZ * 1.02)

            cmds.select(self.node)

            shape = cmds.listRelatives(plane[0], shapes=True)

            cmds.setAttr(shape[0] + '.primaryVisibility', 0)
            cmds.setAttr(shape[0] + '.visibleInReflections', 0)
            cmds.setAttr(shape[0] + '.visibleInRefractions', 0)
            cmds.setAttr(shape[0] + '.castsShadows', 0)

        else: #NO MAP
            plane = cmds.polyPlane(ch=True, o=True, ax=[0,1,0], w=1.0, h=1.0, sw=10, sh=10, cuv=2, name=self.node+ ' Map Helper#')
            cmds.setAttr(plane[1] + '.createUVs', True)
            cmds.select(plane[0])
            mel.eval('createAndAssignShader lambert "";')
            shader = self.getSurfaceShader(plane[0])

            fileNode = mel.eval('createRenderNodeCB -as2DTexture "" "file" ""')
            cmds.connectAttr(fileNode + '.outColor', shader + '.color', force=True)

            try:
                cmds.connectAttr(fileNode + '.outColor', self.node + '.mColor', force=True)
            except:
                pass

            cmds.setKeyframe(fileNode, attribute='frameOffset', t=0)
            cmds.setKeyframe(fileNode, attribute='frameOffset', t=50, v=0.4)

            try:
                cmds.setAttr(fileNode + '.defaultColor', 0,0,0, typ='double3')
            except:
                pass

            try:
                cmds.connectAttr(plane[0]+ '.worldMatrix[0]', self.node+ '.' +matrixAttribute, f=True)
            except:
                pass

            cmds.setAttr(plane[0] + '.' + 'scaleX', scaleX * 1.02)
            cmds.setAttr(plane[0] + '.' + 'scaleY', scaleY * 1.02)
            cmds.setAttr(plane[0] + '.' + 'scaleZ', scaleZ * 1.02)

            cmds.setAttr(plane[0] + '.' + 'translateX', centerX * 1.02)
            cmds.setAttr(plane[0] + '.' + 'translateY', centerY * 1.02)
            cmds.setAttr(plane[0] + '.' + 'translateZ', centerZ * 1.02)

            cmds.select(self.node)

            shape = cmds.listRelatives(plane[0], shapes=True)

            cmds.setAttr(shape[0] + '.primaryVisibility', 0)
            cmds.setAttr(shape[0] + '.visibleInReflections', 0)
            cmds.setAttr(shape[0] + '.visibleInRefractions', 0)
            cmds.setAttr(shape[0] + '.castsShadows', 0)

            cmds.select(plane[0])

            randomName = 'mash3dPaintCTX%d' % mel.eval('rand 10000')

            mel.eval('art3dPaintCtx %s' % randomName)
            cmds.setToolTo(randomName)
            cmds.toolPropertyWindow()

            cmds.evalDeferred('import InViewMessageWrapper; InViewMessageWrapper.MashInViewMessage("Switching to 3d paint tool.", "Info")')

        if (len(self.postCmd) > 0):
            self.runPostCommand(self.postCmd)

    def getNetworkBoundingBox(self):
        import MASH.api as mapi

        waiter = mapi.getWaiterFromNode(self.node)
            
        def getAttributePlug(name, attr):
            sel = om.MSelectionList()
            sel.add(name)
            thisNode = om.MObject()
            sel.getDependNode(0, thisNode)
            fnThisNode = om.MFnDependencyNode(thisNode)
            outAttribute = fnThisNode.attribute(attr)
            outPlug = om.MPlug(thisNode, outAttribute)
            return outPlug
            
        plug = getAttributePlug(waiter, 'outputPoints')    
        data = om.MFnArrayAttrsData(plug.asMObject())
        arr = data.getVectorData('position')

        bbox = om.MBoundingBox()
        for i in range(arr.length()):
            p = om.MPoint(arr[i])
            bbox.expand(p)
            
        pmin = bbox.min()
        pmax = bbox.max()

        pmin = [pmin.x, pmin.y, pmin.z]
        pmax = [pmax.x, pmax.y, pmax.z]

        return [pmin, pmax]

    def getSurfaceShader(self, objName):
        myShapeNode = cmds.listRelatives(objName, children=True, shapes=True)
        mySGs = cmds.listConnections(myShapeNode[0], type='shadingEngine')
        surfaceShader = cmds.listConnections(mySGs[0] + '.surfaceShader')
        return surfaceShader[0]

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
        if commandId == 'SwitchToMeshMode':
            cmds.setAttr( '%s.arrangement' % (self.node), 4 )
        elif commandId == 'ExplodeNodeConnect':
            command = 'evalDeferred \"explodeButtonCMDS(\\"'+ self.node + '\\", \\"'+ self.droppedNode + '\\",1)\"'
            mel.eval(command)
        elif commandId == 'OffsetSwitchToClosestPointMode':
            cmds.setAttr( '%s.offsetType' % (self.node), 5 )
        elif commandId == 'OrientSwitchToAimMode':
            cmds.setAttr( '%s.targetMode' % (self.node), 1 )
            cmds.setAttr( '%s.orientMode' % (self.node), 2 )
        elif commandId == 'OrientSwitchToMeshMode':
            cmds.setAttr( '%s.orientMode' % (self.node), 3 )
        elif commandId == 'DelaySwitchToFTLMode':
            cmds.setAttr( '%s.delayMode' % (self.node), 2 )
        elif commandId == 'MapSwitchToUVMode':
            cmds.setAttr( '%s.mapDirection' % (self.node), 1 )
        elif commandId == 'SwitchToVtxSetMode':
            cmds.setAttr( '%s.arrangement' % (self.node), 4 )
            cmds.setAttr( '%s.meshType' % (self.node), 7 )
        elif commandId == 'TransformNodeConnect':
            cmds.connectAttr(  '%s.rotate' % (self.droppedNode), '%s.rotationAmount' % (self.node), force=True )
            cmds.connectAttr(  '%s.scale' % (self.droppedNode), '%s.scaleAmount' % (self.node), force=True )
        elif commandId == 'CurveWarpAimCurve':
            #special command for the curveWarp node - which is not technically a MASH node.
            cmds.setAttr( '%s.aimMode' % (self.node), 3 )
        elif commandId == 'ReplicatorEnableCurve':
            cmds.setAttr( '%s.useCurve' % (self.node), 1)
        elif commandId == 'FalloffShapeIn':
            nodeType = cmds.nodeType( self.droppedNode )
            if nodeType == 'mesh':
                cmds.setAttr( '%s.falloffShape' % (self.node), 6 )
            elif nodeType == 'nParticle':
                cmds.setAttr( '%s.falloffShape' % (self.node), 5 )
            elif nodeType == 'nurbsCurve':
                cmds.setAttr( '%s.falloffShape' % (self.node), 4 )
        elif commandId == 'PosMapSwitchToUVMode':
            cmds.setAttr( '%s.posMapDirection' % (self.node), 1 )
        elif commandId == 'RotMapSwitchToUVMode':
            cmds.setAttr( '%s.rotMapDirection' % (self.node), 1 )
        elif commandId == 'ScaleMapSwitchToUVMode':
            cmds.setAttr( '%s.scaleMapDirection' % (self.node), 1 )
        elif commandId == 'WorldNodeConnectMatrix':
            transforms = cmds.listRelatives(self.droppedNode, parent=True, fullPath=True)
            cmds.connectAttr(  '%s.worldMatrix[0]' % (transforms[0]), '%s.groundMatrix' % (self.node), force=True )
        elif commandId == 'ConnectVoxelContainer':
            transforms = cmds.listRelatives(self.droppedNode, parent=True, fullPath=True)
            cmds.connectAttr(  '%s.worldMatrix[0]' % (transforms[0]), '%s.voxelObjMatrix' % (self.node), force=True )
        elif commandId == 'TrailsSwitchToPointMode':
            cmds.setAttr( '%s.trailsMode' % (self.node), 3 )
        elif commandId == 'SwitchConstraintToConnectToPoint':
            cmds.setAttr( '%s.constraintMode' % (self.node), 3 )
        elif commandId == 'SwitchConstraintToConnectToNetwork':
            cmds.setAttr( '%s.constraintMode' % (self.node), 5 )
        elif commandId == 'ConstraintMapSwitchToUVMode':
            cmds.setAttr( '%s.connectionMapDirection' % (self.node), 1 )
        elif commandId == 'OffsetSwitchToReorderByDistance':
            cmds.setAttr( '%s.reorderPoints' % (self.node), 5 )
        elif commandId == 'OffsetSwitchToReorderByMesh':
            cmds.setAttr( '%s.reorderPoints' % (self.node), 6 )

    def runPostDisconnectCommand(self, commandId):
        if commandId == 'TransformNodeConnect':
            cmds.disconnectAttr(  '%s.rotate' % (self.droppedNode), '%s.rotationAmount' % (self.node))
            cmds.disconnectAttr(  '%s.scale' % (self.droppedNode), '%s.scaleAmount' % (self.node))
            cmds.select( clear=True )
            cmds.select( self.node )
        elif commandId == 'ReplicatorEnableCurve':
            cmds.setAttr( '%s.useCurve' % (self.node), 0)
        elif commandId == 'FalloffShapeIn':
            cmds.setAttr( '%s.falloffShape' % (self.node), 1 )
        elif commandId == 'MapSwitchToUVMode':
            cmds.setAttr( '%s.mapDirection' % (self.node), 2 )
        elif commandId == 'PosMapSwitchToUVMode':
            cmds.setAttr( '%s.posMapDirection' % (self.node), 2 )
        elif commandId == 'RotMapSwitchToUVMode':
            cmds.setAttr( '%s.rotMapDirection' % (self.node), 2 )
        elif commandId == 'ScaleMapSwitchToUVMode':
            cmds.setAttr( '%s.scaleMapDirection' % (self.node), 2 )

    #pre defined pre connection commands
    def runPreCommand(self, commandId):
        createMapHelperAction = False
        if self.postCmd == 'MapSwitchToUVMode' or self.postCmd == 'PosMapSwitchToUVMode' or self.postCmd == 'ScaleMapSwitchToUVMode' or self.postCmd == 'RotMapSwitchToUVMode':
            createMapHelperAction = True

        if createMapHelperAction:
            # here we need to check if the dropped transform has a mesh underneath it
            # this prevents the user from connecting a locator for example
            error = False
            shapes = cmds.listRelatives(self.droppedNode)
            if not shapes or cmds.nodeType( shapes[0] ) != "mesh":
                error = True

            if error:
                command = 'evalDeferred \"MASHinViewMessage(\\"'+ kNoMeshFound + '\\", \\"Error\\")\"'
                mel.eval(command)
            return not error

        if commandId == 'MergeConnect':
            waiter = mapi.getWaiterFromNode(self.droppedNode)
            network = mapi.Network(waiter)
            if network.hasDynamics() == False:
                # No dynamics, so return and connect as normal
                return True
            else:
                # Dynamics found, handle the connection here
                index = network.getSolverIndex()
                solver = network.getSolver()
                attr = 'outputPoints['+str(index)+']'
                cmds.connectAttr(  '%s.%s' % (solver,attr), '%s.%s' % (self.node,self.attr), force=True )
                return False

        return True
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
