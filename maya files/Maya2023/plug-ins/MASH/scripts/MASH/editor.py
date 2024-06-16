from __future__ import division
from builtins import object
from builtins import zip
from builtins import range
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix
'''([^\w\.'"])(Q[A-Z]\w*)'''

from copy import deepcopy
import maya.OpenMayaUI as omui
import MASH.action as action
import MASH.menu as menu
import MASH.undo as undo
import MASH.deleteMashNode as dmn
from MASH.itemStyle import *
import weakref
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
import logging
import openMASH
import json
import MASH.api

# ==============
# STRING RESOURCES

def str_res(key):
    return mel.eval('getPluginResource("MASH", "%s")' % key)

kEdit = str_res('kEdit')
kForceUpdate = str_res('kForceUpdate')
kConnections = str_res('kConnections')
kUtilityNodes = str_res('kUtilityNodes')
kRed = str_res('kRed')
kBlue = str_res('kBlue')
kGrey = str_res('kGrey')
kOrange = str_res('kOrange')
kGreen = str_res('kGreen')
kYellow = str_res('kYellow')
kPurple = str_res('kPurple')
kLabelColour = str_res('kLabelColour')
kShow = str_res('kShow')
kDelete = str_res('kDelete')
kCreatePointsNode = str_res('kCreatePointsNode')
kSwitchGeometryType = str_res('kSwitchGeometryType')
kCacheThisNetwork = str_res('kCacheThisNetwork')
kCreateMeshFromPoints = str_res('kCreateMeshFromPoints')
kCreate = str_res('kCreate')
kCreateMASHNetwork = str_res('kCreateMASHNetwork')
kCreateMASHDeformer = str_res('kCreateMASHDeformer')
kCreateBlendDeformer = str_res('kCreateBlendDeformer')
kCreateJiggleDeformer = str_res('kCreateJiggleDeformer')
kMASHEditor = str_res('kMASHOutliner')
kDuplicateNetwork = str_res('kDuplicateNetwork')
kDeleteNetwork = str_res('kDeleteNetwork')
kPlacerTool = str_res('kPaintTool')

LABEL_COLOURS = [kRed, kBlue, kGrey, kOrange, kGreen, kYellow, kPurple]

# ==============
# OUTLINER USAGE:
#   import MASH.editor
#   MASH.editor.show()
# ==============

# Global look variables
ROW_HEIGHT = 30
GLOBAL_INDENTATION = 12

WAITER_CONNECTIONS_TO_IGNORE = ['MASH_Repro', 'instancer']
ATTRS_TO_CHECK = ['strengthPP', 'mColour']

# Global path variables
class MASHEditor(MayaQWidgetDockableMixin, qt.QWidget):

    def __init__(self, parent=None, name=None, title=kMASHEditor):
        MayaQWidgetDockableMixin.__init__(self, parent=parent)

        if name is None:
            name = 'MASH_Outliner_%s'%uuid.uuid4()  # make it a unique name for Maya

        self.setWindowTitle(title)
        self.resize(pix(300),pix(300))
        self.setMinimumWidth(pix(300))

        fx.setVLayout(self, pix(2), pix(2), pix(2), pix(2), pix(2))

        self.menuBar = qt.QMenuBar()
        self.createMenu = self.menuBar.addMenu(kCreate)
        self.createMenu.addAction(fx.getIconFromName('out_MASH_CreateUtility'), kCreateMASHNetwork, self.createNetwork)
        self.layout().addWidget(self.menuBar, 0)

        self.treeView = OutlinerTreeView()
        self.layout().addWidget(self.treeView, 1)
        
        self._registeredMayaCallbacks = [] # used to register/deregister Maya callbacks
        self.registerCallbacks() #register the callbacks

    def createNetwork(self):
        mel.eval('MASHnewNetwork("MASH")')

    def registerCallbacks(self):
        cb = om.MEventMessage.addEventCallback('NewSceneOpened', self.updateData, self)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('SceneOpened', self.updateData, self)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('SceneImported', self.updateData, self)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('NameChanged', self.updateData, self)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

        cb = om.MEventMessage.addEventCallback('Undo', self.updateData, self)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

        cb = om.MDGMessage.addNodeRemovedCallback(self.updateData)
        self._registeredMayaCallbacks.append(fx.MCallbackIdWrapper(cb))

    def cleanup(self):
        '''
        Cleanup environment by removing the Maya callbacks, etc.
        MCallbackWrapper items automatically clean themselves up on deletion
        '''
        self.treeView._registeredNodeCallbacks = []
        self._registeredMayaCallbacks = []

    def updateData(self, *args):
        '''
        This can be triggered from callbacks inside Maya to update the data in the outliner.
        For example, when a MASH node is added to a scene, this will refresh any open outliners.
        '''
        self.cleanup()

        if self.treeView:
            self.registerCallbacks()
            self.treeView.resetContents()

    def closeEvent(self, evt):
        self.cleanup()
        evt.accept()

    def __del__(self):
        self.cleanup()

class OutlinerTreeView(qt.QTreeWidget):
    '''
    The main view, used to show the MASH networks.
    '''

    # Not all MASH nodes are supported here, so name them explicitly.
    MASH_NODE_TYPES = [
        'Audio', 'Curve', 'Color', 'Delay', 'Explode', 'Flight', 'ID', 'Strength',\
        'Influence', 'Offset', 'Orient', 'Python', 'Random', 'Replicator', 'Signal',\
        'Spring', 'Symmetry', 'Time', 'Trails', 'Transform', 'Visibility', 'Points',\
        'Breakout', 'World', 'Placer', 'Merge', 'Dynamics'
    ]

    # [Label, Command(), icon]
    MASH_UTILITIES = [
        [kSwitchGeometryType, 'MASHswitchGeometryType()'], 
        [kCacheThisNetwork, 'MASHcacheRedirection()', 'out_MASH_Cache'],\
        [kCreateMeshFromPoints, 'MASHcreateMeshFromPointsEntry()', 'out_MASH_MeshFromPoints']
    ]

    REPRO_IMAGE = fx.getPixmap('out_MASH_Repro')
    INSTANCER_IMAGE = fx.getPixmap('out_MASH_Instancer')
    EXPAND_WIDTH = pix(60)

    def __init__(self, parent=None):
        qt.QTreeWidget.__init__(self, parent)
        self.actionButtonPressed = False
        # used to store self destructing Maya callbacks
        self._registeredNodeCallbacks = []
        self.setHeaderHidden(True)
        self.setIndentation(GLOBAL_INDENTATION)
        self.setMouseTracking(True)
        self.setSelectionMode(qt.QAbstractItemView.SingleSelection)

        self.lastHitAction = None
        self.selectionParent = None
        self.selectionNode = None

        self.populateItems()

        self.header().setCascadingSectionResizes(False)
        self.setColumnWidth(0,pix(250))
        self.header().resizeSection(0, pix(250));
        self.resizeColumnToContents(0)
        delegate = TreeViewDelegate(self)
        self.setItemDelegate(delegate)
        self.setStyle(ItemStyle())
        self.setRootIsDecorated(False)
        self.expandAll()
        self.buttonPressed = None
        self.setExpandsOnDoubleClick(False)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(qt.Qt.MoveAction)

        self.contextMenu = menu.Menu(self)
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._showContextMenu)

        self.utilitiesMenu = menu.Menu(self)
        self.utilitiesMenuAction = action.Action('Utilities Menu', self.utilitiesMenu, triggered=self._popupUtilitiesMenu)
        self.addNodeMenu = menu.Menu(self)
        self.addNodeMenuAction = action.Action('Add Node Menu', self.addNodeMenu, triggered=self._showAddNodeMenu)
        self.connectionsMenu = menu.Menu(self)
        self.connectionsMenuAction = action.Action('Connections Menu', self.connectionsMenu, triggered=self._showConnectionsMenu)
        self.MASH_NODE_TYPES = sorted(self.MASH_NODE_TYPES)
        self.LABEL_COLOURS = sorted(LABEL_COLOURS)

        self.updateWaiterExpansions()

    def _showContextMenu(self, point):
        ''' Rebuild the context menu from scratch '''
        selectedIndexes = self.selectedIndexes()
        numIndexes = len(selectedIndexes)
        self.contextMenu.clear()
        item = self._getCurrentItem()
        if item is None:
            return
        if item.isWaiter():
            # Only show the context menu if we have selected items
            if numIndexes > 0:
                pixmap = qt.QPixmap (pix(100),pix(100))
                pixmap.fill(self._getLabelColour())
                labelIcon = qt.QIcon(pixmap)
                prevMenu = self.contextMenu.addMenu(labelIcon,kLabelColour)
                for item in self.LABEL_COLOURS:
                    pixmap = qt.QPixmap (pix(100),pix(100))
                    pixmap.fill(self._getColourFromLabel(item))
                    labelIcon = qt.QIcon(pixmap)
                    prevMenu.addAction(labelIcon, item, lambda item=item: self._setLabelColour(item))

            self.contextMenu.addAction(fx.getIconFromName('out_MASH_Duplicate'), kDuplicateNetwork, self._duplicateNetwork)
            self.contextMenu.addAction(fx.getIconFromName('out_MASH_Delete'), kDeleteNetwork, self._deleteNode)

        # Distribute nodes do not get a delete option, you must remove the network via the Waiter to delete them
        elif item.nodeType() != 'MASH_Distribute':
            self.contextMenu.addAction(fx.getIconFromName('out_MASH_Delete'), kDelete, self._deleteNode)

        self.contextMenu.popup(qt.QCursor.pos())
        self.contextMenu.exec_(self.mapToGlobal(point))

    def _showAddNodeMenu(self):
        ''' Rebuild the Add node menu from scratch  '''
        self.addNodeMenu.clear()
        for item in self.MASH_NODE_TYPES:
            # workaround for display name and node name not matching.

            name = item
            if item == 'Merge': 
                name == 'Blend'

            menu_action = self.addNodeMenu.addAction(fx.getIconFromName('out_MASH_%s' % name), name, lambda item=item: self._addNodeToWaiter(item))

            if item in ['Color', 'Time']:
                waiter = self._getCurrentItem().mashNode.nodeName
                allNodes = MASH.api.getAllNodesInNetwork(waiter)
                hasRepro = False
                for node in allNodes:
                    if cmds.nodeType(node) == 'MASH_Repro':
                        hasRepro = True
                        break
                menu_action.setEnabled(hasRepro)

        self.addNodeMenu.popup(qt.QCursor.pos())

    def _showConnectionsMenu(self):
        ''' Rebuild the Connections node menu from scratch  '''
        self.connectionsMenu.clear()
        treeItem = self.currentItem()

        if treeItem.connectedNodes:
            for connectedNode in treeItem.connectedNodes:
                shapes = cmds.listRelatives(connectedNode, shapes=True)
                menu_action = None
                if shapes: # Falloff (in future perhaps also locator)
                    wantedNode = shapes[0]
                    nodeType = cmds.nodeType(wantedNode)
                    icon = fx.getIconFromName('out_' + nodeType)
                    self.connectionsMenu.addAction(icon, wantedNode, lambda item=wantedNode: showAETempalateOf(item))
                else: # Shader
                    nodeType = cmds.nodeType(connectedNode)
                    icon = fx.getIconFromName('out_' + nodeType)
                    self.connectionsMenu.addAction(icon, connectedNode, lambda item=connectedNode: showAETempalateOf(item))

        self.connectionsMenu.popup(qt.QCursor.pos())

    def _popupUtilitiesMenu(self):
        ''' Rebuild the utilities node menu from scratch  '''
        self.utilitiesMenu.clear()

        def callback_factory(script):
            return lambda : self._runUtilityScript(script)

        for index, item in enumerate(self.MASH_UTILITIES):
            scriptName = item[0]
            script = item[1]

            if (len(item) > 2):
                icon = fx.getIconFromName(item[2])
                menu_action = self.utilitiesMenu.addAction(icon, scriptName)
            else:
                if scriptName == kSwitchGeometryType:
                    waiter = self._getNodeName()

                    instancerConns = cmds.listConnections(waiter + ".instancerMessage", d=True, s=False)
                    if not instancerConns:
                        continue

                    geometryNode = None
                    if cmds.objExists(waiter+'.instancerMessage'):
                        geometryNode = cmds.listConnections(waiter+'.instancerMessage', d=True, s=False )

                    if geometryNode and (cmds.nodeType(geometryNode[0]) == 'MASH_Repro'):
                        pixmap = self.INSTANCER_IMAGE # get the opposite of this node, because we're showing what you'd change to
                    else:
                        pixmap = self.REPRO_IMAGE

                    menu_action = self.utilitiesMenu.addAction(qt.QIcon(pixmap), scriptName)
                else:
                    menu_action = self.utilitiesMenu.addAction(scriptName)

            menu_action.triggered[()].connect(callback_factory(script))

        self.utilitiesMenu.popup(qt.QCursor.pos())

    def _toggleExpandCollapse(self):
        ''' expand and collaps the Waiters, this infomation is stored in the scene and restored on file load '''

        item = self.currentItem()

        if item.isExpanded():
            self.collapseItem(item)
        else:
            self.expandItem(item)

        waiterJSON = cmds.getAttr(item.mashNode.nodeName+'.outlinerJSON')
        parsedJSON = json.loads(waiterJSON)
        parsedJSON['expanded'] = item.isExpanded()
        cmds.setAttr(item.mashNode.nodeName+'.outlinerJSON', json.dumps(parsedJSON), type='string')

    def handle(self, item, column):
        pass

    def cleanup(self):
        ''' delete and deregister callbacks '''
        self._registeredNodeCallbacks = []

    def _getCurrentAction(self, point, item):
        ''' find out which button the mouse is over '''
        if item:
            # If the row has children, check to see if the user clicked before the row entry name. 
            # If so, then expand/collapse the row
            if item.childCount() > 0 and point.x() < self.EXPAND_WIDTH:
                return 'ExpandCollapse'

            return self.lastHitAction
        return None

    def mouseMoveEvent(self, event):
        if not self.actionButtonPressed:
            qt.QTreeWidget.mouseMoveEvent(self, event)

        modifiers = qt.QGuiApplication.keyboardModifiers()
        # are we copying a node
        if modifiers == qt.Qt.AltModifier:
            qt.QWidget.setCursor(self,(qt.QCursor(qt.Qt.DragCopyCursor)))
        else:
            qt.QWidget.unsetCursor(self)
        # dirty the treeview so it will repaint when the mouse moves over it
        # this is needed to change the icon rollover state
        self.lastHitAction = None
        region = self.childrenRegion()
        self.setDirtyRegion(region)

    def mousePressEvent(self, event):
        ''' trigger actions based on mouse presses '''
        self.buttonPressed = event.button()
        #deselect when the user clicks in a blank space
        if event.button() == qt.Qt.LeftButton:
            index = self.indexAt(event.pos())

            if index.row()==-1:
                self.actionButtonPressed = False
                qt.QTreeWidget.mousePressEvent(self, event)
                self.clearSelection()
                forceRepaint(self)
                return

            item = self._getCorrespondingItem(index)
            action = self._getCurrentAction(event.pos(), item)
            
            self.setCurrentItem(item)
            # set up variables for node duplication / reordering between networks
            if item.mashNode.nodeType != 'MASH_Waiter': # waiters can't move
                self.selectionParent = item.parent().getName()
                self.selectionNode = item.getName()
            #select the cell without updating the display

            self.selectionModel().setCurrentIndex(index, qt.QItemSelectionModel.NoUpdate)

            if action != None:
                self.actionButtonPressed = True
                # set the currently clicked on element active without selecting it
                # trigger the action to be executed
                if (action == 'Enabled'):
                    item.setEnabled()
                if (action == 'Repro'):
                    waiter = item
                    if item.parent():
                        waiter = item.parent()

                    goToRepro(waiter.getName())
                if (action == 'Scripts'):
                    self.utilitiesMenuAction.trigger()
                if (action == 'Add'):
                    self.addNodeMenuAction.trigger()
                if (action == 'ExpandCollapse'):
                    if item.mashNode.nodeType == 'MASH_Waiter':
                        self._toggleExpandCollapse()
                if (action == 'Connections'):
                    self.connectionsMenuAction.trigger()
            else:
                #clicking anywhere on a node shows it in the AE
                self._showAETempalate()
            event.accept()
        elif event.button() == qt.Qt.MiddleButton:
            qt.QTreeWidget.mousePressEvent(self, event)

        self.clearSelection()
        qt.QTreeWidget.mousePressEvent(self, event)
        forceRepaint(self)

    def mouseReleaseEvent(self, event):
        qt.QGuiApplication.restoreOverrideCursor()
        if not self.actionButtonPressed:
            qt.QTreeWidget.mouseReleaseEvent(self, event)
        else:
            self.actionButtonPressed = False
        forceRepaint(self)

    def leaveEvent(self, *args, **kwargs):
        ''' clear the action tracking '''
        self.lastHitAction = None
        forceRepaint(self)

    def getIndent(self, index):
        indent = 0
        while(index and index.parent().isValid()):
            index = index.parent()
            indent += self.indentation()
        return indent

    def _getCorrespondingItem(self, index):
        if index.isValid():
            return self.itemFromIndex(index)
        return None

    def _getCurrentItem(self):
        return self.currentItem()

    def _duplicateUtility(self, node, name, origin):
        nodeCopy = cmds.duplicate(node, n=name)[0]
        if cmds.attributeQuery('outputMesh', node=nodeCopy, exists=True):
            mesh = cmds.listConnections(nodeCopy + '.outputMesh', d=True, s=False, shapes=True)
            if mesh:
                cmds.rename(mesh[0], nodeCopy + '_Mesh')

        multiIndex = ''
        if cmds.attributeQuery('outputPoints', node=origin, multi=True):
            multiIndex = '[0]'
        cmds.connectAttr(origin + '.outputPoints' + multiIndex, nodeCopy + '.inputPoints')

    def _duplicateUtilities(self, waiter, newWaiter):
        def getOrigins(waiterNode):
            outPoints = cmds.listConnections(waiterNode + '.outputPoints', d=True, s=False, shapes=True)
            return [waiterNode] + [x for x in outPoints if cmds.nodeType(x) == 'MASH_BulletSolver']

        origins = getOrigins(waiter)
        newOrigins = getOrigins(newWaiter)
        utilityTypes = ['MASH_Breakout', 'MASH_Explode', 'MASH_Points', 'MASH_Trails']

        for origin, newOrigin in zip(origins, newOrigins):
            nodes = cmds.listConnections(origin + '.outputPoints', d=True, s=False, shapes=True) or []
            for node in nodes:
                nodeType = cmds.nodeType(node)
                if nodeType in utilityTypes:
                    suffix = nodeType[4:]
                    self._duplicateUtility(node, newWaiter + suffix, newOrigin)
            
    @undo.chunk('Duplicate Network')
    def _duplicateNetwork(self):
        waiter = self._getNodeName()
        if cmds.objExists(waiter+'.instancerMessage'):
            outConnections = cmds.listConnections(waiter+'.instancerMessage', d=True, s=False)
            if outConnections:
                newNodes = cmds.duplicate(outConnections[0], un=True)
                newWaiter = [x for x in newNodes if cmds.nodeType(x) == 'MASH_Waiter']
                if newWaiter:
                    self._duplicateUtilities(waiter, newWaiter[0])
            else: #shellDynamics
                conns = cmds.listConnections(waiter + '.outputPoints', d=True, s=False, shapes=True)
                if conns:
                    solver = conns[0]
                    conns = cmds.listConnections(solver + '.outputPoints', d=True, s=False, shapes=True)
                    if conns:
                        shellDeformer = conns[0]
                        conns = cmds.listConnections(shellDeformer + '.outputGeometry[0]', d=True, s=False, shapes=True)
                        if conns:
                            mesh = conns[0]
                            cmds.duplicate(mesh, un=True)

    @undo.chunk('Delete Node')
    def _deleteNode(self):
        item = self._getCurrentItem()
        responce = cmds.confirmDialog( title='Confirm', message='Confirm Deletion', 
            button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        if (item is not None) and responce == 'Yes':
            cmds.select(clear=True)
            item.deleteNode()
        else:
            print(responce)

    def _showAETempalate(self):
        item = self._getCurrentItem()
        if item is not None:
            item.showAETemplate()

    def dragEnterEvent(self, event):
        qt.QTreeWidget.dragEnterEvent(self, event)

    @undo.chunk('Run Utility Script')
    def _runUtilityScript(self, script):
        item = self._getCurrentItem()
        if script != 'MASHplacePoints()':
            waiter = item.getName()
            cmds.select(clear=True)
            cmds.select(waiter, ne=True)
        else:
            # find the Paint node and select it, if there isn't one, create one.
            placerNode = None
            for x in range(item.childCount()):
                child = item.child(x)
                if child.mashNode.nodeType == 'MASH_Placer':
                    placerNode = child
                    cmds.select(placerNode.mashNode.nodeName)
            if not placerNode:
                placerNode = self._addNodeToWaiter('Placer')
                cmds.select(placerNode)
        mel.eval(script)

    def _getColourFromLabel(self, label):
        colors = {
            'yellow': [191,178,58],
            'blue': [88,165,204],
            'grey': [189,189,189],
            'orange': [219,148,86],
            'green': [85,171,100],
            'purple': [174,156,219],
            'default': [241,90,91]
        }

        label = label.lower()

        color = colors['default']
        if label in colors:
            color = colors[label]

        return qt.QColor(*color)

    @undo.chunk('Set Label Colour')
    def _setLabelColour(self, label):
        color = self._getColourFromLabel(label)
        self._getCurrentItem().setLabelColour(color)

    def _getLabelColour(self):
        item = self._getCurrentItem()
        return item.mashNode.labelColour

    def _getNodeName(self):
        return self._getCurrentItem().getName()

    @undo.chunk('Add Node')
    def _addNodeToWaiter(self, nodeType):
        if nodeType == 'Merge': nodetype = 'Blend'
        item = self._getCurrentItem()
        newNode = item.addNode('MASH_'+nodeType)
        self.resetContents()
        return newNode

    def resetContents(self, resetCallbacks=True):
        '''
        Repopulates the tree widget
        TODO: It would be good if we have time to replace this with something more elegent
        '''

        self.selectionParent = None
        self.selectionNode = None

        self.clearItems()
        self.populateItems(resetCallbacks)
        self.updateWaiterExpansions()

    def clearItems(self):
        #self.clear() This crashes Maya (bug in PySide?)
        # This doesn't:
        count = self.topLevelItemCount()
        for i in range(count):
            self.takeTopLevelItem(0)

    def updateWaiterExpansions(self):
        for i in range(self.topLevelItemCount()):
            waiter = self.topLevelItem(i)
            waiterJSON = cmds.getAttr(waiter.mashNode.nodeName+'.outlinerJSON')
            parsedJSON = json.loads(waiterJSON)
            isExpanded = bool(parsedJSON['expanded'])
            if isExpanded:
                self.expandItem(waiter)
            else:
                self.collapseItem(waiter)

    @undo.chunk('Reorder Network')
    def dropEvent(self, event):
        index = self.indexAt(event.pos())
        item = self.itemFromIndex(index)

        # Check if this is a suported scene item
        dropIndicatorPosition = self.dropIndicatorPosition()

        isInvalidPosition = (not index.isValid() or item.childCount()==-1 or 
            (item.parent().indexOfChild(item) == (item.childCount()-1) and dropIndicatorPosition == qt.QAbstractItemView.BelowItem))

        if isInvalidPosition:
            event.ignore()
            return
        else:
            self.dropMimeData(self.currentIndex().row(), self.indexAt(event.pos()).row(), self.indexFromItem(item.parent()))
            #qt.QTreeWidget.dropEvent(self, event)
        # hacky update of data model
        self.resetContents()

    def makeWaiterItem(self, waiter):
        # Creates a top-level waiter item

        distributeNode = cmds.listConnections(waiter+'.waiterMessage', d=False, s=True)

        showEnabled = False
        networkEnabled = True
        if distributeNode and len(distributeNode) > 0 and cmds.objExists(distributeNode[0]+'.enable'):
            networkEnabled = cmds.getAttr(distributeNode[0]+'.enable')
            showEnabled = True

        nodeIcon = fx.getPixmap('out_MASH_Waiter')
        color = cmds.getAttr(waiter+'.labelColor')[0]

        mashNode = mash_node_class(waiter, 'MASH_Waiter', True, nodeIcon, networkEnabled, networkEnabled)
        mashNode.labelColour = qt.QColor(*[x * 255.0 for x in color])

        item = TreeItem(mashNode, waiter, showEnabled, None)
        item.connectedNodes = getUtilityConnections(waiter)

        return item

    def addNetworkItem(self, node, waiterItem):
        # Adds a network item under the waiter

        showEnabled = True
        enabled = None

        if cmds.objExists(node+'.enable'):
            enabled = cmds.getAttr(node+'.enable')
        else:
            showEnabled = False

        inConnections = getNodeConnections(node)
        nodeType = cmds.nodeType(node)
        nodeIcon = fx.getPixmap('out_' + nodeType)

        mashNode = mash_node_class(node, nodeType, False, nodeIcon, enabled, waiterItem.mashNode.networkEnabled)
        mashNode.labelColour = waiterItem.labelColor()

        item = TreeItem(mashNode, '', showEnabled, waiterItem)
        item.connectedNodes = inConnections
        return item

    def registerNetworkItemCallbacks(self, node):
        # Adds an attribute changed callback

        nodeObj = openMASH.mashGetMObjectFromNameOne(node)
        
        cb = om.MNodeMessage.addAttributeChangedCallback(nodeObj, self._attributeChanged, None)
        self._registeredNodeCallbacks.append(fx.MCallbackIdWrapper(cb))
        
    def populateItems(self, addCallbacks=True):
        # Populates the model with all the mash networks in the scene

        if addCallbacks:
            self.cleanup()

        allWaiters = cmds.ls(type='MASH_Waiter') or []

        for waiter in allWaiters:
            if not cmds.objExists(waiter+'.instancerMessage'):
                continue
            
            waiterItem = self.makeWaiterItem(waiter)
            waiterItem.setFlags(waiterItem.flags() | qt.Qt.ItemIsEditable | qt.Qt.ItemIsDropEnabled)
            waiterItem.setFlags(waiterItem.flags() & ~qt.Qt.ItemIsDragEnabled)
            self.addTopLevelItem(waiterItem)
            nodesInNetwork = getMASHNodesInNetwork(waiter)

            for node in nodesInNetwork:
                child = self.addNetworkItem(node, waiterItem)
                if child.nodeType() == 'MASH_Distribute':
                    child.setFlags(child.flags() | qt.Qt.ItemIsEditable)
                    child.setFlags(child.flags() & ~qt.Qt.ItemIsDragEnabled)
                    child.setFlags(child.flags() & ~qt.Qt.ItemIsDropEnabled)
                else:
                    child.setFlags(child.flags() | qt.Qt.ItemIsEditable | qt.Qt.ItemIsDropEnabled)
                
                waiterItem.addChild(child)

                if addCallbacks:
                    self.registerNetworkItemCallbacks(node)

    def _attributeChanged(self, message, plug, otherPlug, clientData):
        name = plug.partialName(False, False, False, False, False, True)

        if name == 'enable' or name in ATTRS_TO_CHECK:
            #update the tree, but don't clear and add the callbacks again as there's no need
            self.resetContents(False)

    def dropMimeData(self, oldRow, row, parentIndex):
        ''' Handles the data supplied by a drag and drop operation that ended with the given action. '''

        parent = self.itemFromIndex(parentIndex)
        # If the user drops the node on the parent waiter (-1), simply send it to the front of the chain (0)
        destRow = row if row != -1 else 0
        numPlacedBeforeDestination = 0

        # are we copying a node
        modifiers = qt.QGuiApplication.keyboardModifiers()
        if modifiers == qt.Qt.AltModifier:
            # node being moved to a different network, this duplicates the node and adds it to the new network
            # args: node being moved, old network, new network, destination row in new network
            success = insertNode(self.selectionNode, self.selectionParent, parent, destRow)
            if success:
                self.resetContents(False)

            return False

        child = parent.child(oldRow)
        oldParent = child.parent()
            
        oldParent.removeChild(child)
        if oldParent is parent and oldRow < row:
            numPlacedBeforeDestination += 1

        parent.insertChild(destRow - numPlacedBeforeDestination, child)
        waiter = parent.getName()
        #reorder the network
        reorderNetwork(waiter, oldRow, destRow - numPlacedBeforeDestination)

        return True

    def supportedDropActions(self):
        ''' Returns the drop actions supported by this model. '''
        return qt.Qt.MoveAction

class TreeViewDelegate(qt.QItemDelegate):
    '''
    Custom display delegate for the tree items
    '''
    def __init__(self, treeView):
        qt.QItemDelegate.__init__(self)
        self.treeView = weakref.ref(treeView)

    # Item

    def initStyleOption(self, option, index):
        # let the base class initStyleOption fill option with the default values
        qt.QAbstractItemModel.initStyleOption(self, option, index)
        # override what you need to change in option
        if option.state & qt.QStyle.State_Selected:
            option.state &= ~ qt.QStyle.State_Selected
            option.backgroundBrush = qt.QBrush(qt.Qt.red)

    def _getItem(self, index):
        return self.treeView().itemFromIndex(index)

    def paint(self, painter, option, index):
        ''' Main entry point of drawing the cell '''
        if not index.isValid():
            return

        item = self._getItem(index)
        rowPainter = RowPainter(painter, option, item, self.treeView())
        rowPainter.paintRow()

    def sizeHint(self, option, index):
        hint = qt.QItemDelegate.sizeHint(self, option, index)
        hint.setHeight(pix(ROW_HEIGHT))
        return hint

    # Editor

    def createEditor(self, parent, option, index):
        ''' Creates the double-click editor for renaming render setup entries. The override entry is left aligned. '''
        editor = qt.QLineEdit(parent)
        editor.setAlignment(qt.Qt.AlignLeft | qt.Qt.AlignVCenter)
        return editor

    def updateEditorGeometry(self, editor, option, index):
        ''' Defines the rectangle of the qt.QLineEdit used to edit the name of the node. '''
        indent = self.treeView().getIndent(index)
        rect = deepcopy(option.rect)
        rect.setLeft(indent + pix(46.5))
        rect.setBottom(rect.bottom() - pix(4))
        rect.setRight(rect.right() - pix(50))
        editor.setGeometry(rect)

    def setEditorData (self, editor, index):
        item = self._getItem(index)
        editor.setText(item.getName())

    def setModelData(self, editor, model, index):
        ''' Sets the model data which will trigger the node renaming script to run in Maya '''
        oldValue = index.data()
        newValue = editor.text()
        if newValue != oldValue:
            name = self.treeView().itemFromIndex(index).getName()
            if name:
                # renaming the Waiter will automatically rename all nodes in the network.
                cmds.rename(name, newValue)

class RowPainter(object):

    kTooltips = {
        'Add' : kEdit,
        'Enable' : kEdit,
        'Scripts' : kEdit
    }

    DISABLED_BACKGROUND_IMAGE = fx.getPixmap('out_MASH_ChevronBG')
    DISABLED_HIGHLIGHT_IMAGE = fx.getPixmap('out_MASH_ChevronBGSelected')
    EXPANDED_ARROW = (pix(qt.QPointF(9.0, 11.0)), pix(qt.QPointF(19.0, 11.0)), pix(qt.QPointF(14.0, 16.0)))
    COLLAPSED_ARROW = (pix(qt.QPointF(12.0, 8.0)), pix(qt.QPointF(17.0, 13.0)), pix(qt.QPointF(12.0, 18.0)))
    ARROW_COLOR = qt.QColor(189, 189, 189)
    ICON_PADDING = pix(10.0)
    ACTION_BORDER = pix(0)
    ACTION_WIDTH = pix(20)
    ENABLED_IMAGE = fx.getPixmap('out_MASH_Enable')
    DISABLED_IMAGE = fx.getPixmap('out_MASH_Disable')
    ENABLED_SELECTED_IMAGE = fx.getPixmap('out_MASH_Enable_Selected')
    INACTIVE_ENABLED_IMAGE = fx.getPixmap('out_MASH_Inactive')
    REPRO_IMAGE = fx.getPixmap('out_MASH_Repro')
    INSTANCER_IMAGE = fx.getPixmap('out_MASH_Instancer')
    SCRIPTS_IMAGE = fx.getPixmap('out_MASH_Utilities')
    CONNECTIONS_IMAGE = fx.getPixmap('out_MASH_Connections')
    ADD_IMAGE = fx.getPixmap('out_MASH_AddNode')
    DRAG_HANDLE_IMAGE = fx.getPixmap('out_MASH_OutlinerDrag')
    LOCK_IMAGE = fx.getPixmap('out_MASH_OutlinerNoDrag')
    ICON_WIDTH = pix(20)
    ICON_WIDTH_NO_DPI = pix(20)
    ICON_TOP_OFFSET = pix(4)
    COLOR_BAR_WIDTH = pix(6)

    def __init__(self, painter, option, item, parent):
        self.parent = weakref.ref(parent)
        self.painter = painter
        self.item = item
        self.rect = deepcopy(option.rect)
        self.isHighlighted = option.showDecorationSelected and option.state & qt.QStyle.State_Selected
        self.highlightColor = option.palette.color(qt.QPalette.Highlight)

    def paintRow(self):
        self._drawBackground()
        self._drawColorBar()
        self._drawFill()
        self._drawArrowDragLock()
        textRect = self._drawText()
        self._drawIcon(textRect)
        self._addActionIcons()

    def _drawBackground(self):
        ''' Draws the cell bacground colour / image '''

        if self.item.isWaiter() or self.item.networkEnabled():
            color = self.highlightColor if self.isHighlighted else self.item.getBackgroundColor()
            self.painter.fillRect(self.rect, color)
        else:
            pixmap = self.DISABLED_HIGHLIGHT_IMAGE if self.isHighlighted else self.DISABLED_BACKGROUND_IMAGE
            self.painter.drawTiledPixmap(self.rect, pixmap, qt.QPoint(self.rect.left(), 0))

    def _drawIcon(self, textRect):
        ''' Draws the node icon '''

        rect2 = deepcopy(textRect)
        oldPen = self.painter.pen()
        icon = None

        icon = self.item.getIcon()

        if icon:
            newRect = qt.QRect()
            newRect.setRight(rect2.left() - pix(4))
            newRect.setLeft(newRect.right() - self.ICON_WIDTH_NO_DPI)
            newRect.setBottom(rect2.top() - self.ICON_WIDTH + pix(6))
            newRect.setTop(newRect.bottom() + self.ICON_WIDTH)
            drawEnabled = True
            if not self.item.mashNode.isWaiter and not self.item.networkEnabled():
                drawEnabled = False
            if not self.item.mashNode.enabled or not drawEnabled:
                self.painter.setOpacity(0.5)
            self.painter.drawPixmap(newRect, icon)
            oldPen = self.painter.pen()

    def _drawText(self):
        ''' Draws the node name '''

        oldPen = self.painter.pen()
        #if the item is disabed, draw a lighter text colour
        drawEnabled = True
        if not self.item.mashNode.isWaiter and not self.item.networkEnabled():
            drawEnabled = False
        if self.item.mashNode.enabled and drawEnabled:
            self.painter.setPen(qt.QPen(self.parent().palette().text().color(), pix(1)))
        else:
            self.painter.setPen(qt.QPen(self.item.getInactiveColor(), pix(1)))
        #draw the text for the node
        textRect = deepcopy(self.rect)
        textRect.setBottom(textRect.bottom() + pix(2))
        textRect.setLeft(textRect.left() + pix(40) + self.ICON_PADDING)
        textRect.setRight(textRect.right() - pix(11))
        self.painter.drawText(textRect, qt.Qt.AlignLeft | qt.Qt.AlignVCenter, self.item.getName())
        self.painter.setPen(oldPen)
        oldPen = self.painter.pen()

        return textRect

    def _drawColorBar(self):
        ''' Draws the label colour bar '''

        colour = self.item.labelColor()
        rect2 = deepcopy(self.rect)
        rect2.setRight(rect2.left() + self.COLOR_BAR_WIDTH)
        self.painter.fillRect(rect2, colour)

    def _drawArrowDragLock(self):
        ''' Draws the expansion arrow on the nodes that want it '''

        self.painter.save()
        arrow = None
        if self.item.isWaiter():
            padding = pix(3)
            self.painter.translate(self.rect.left()+padding, self.rect.top()+pix(2))
            arrow = self.COLLAPSED_ARROW
            if self.item.isExpanded():
                arrow = self.EXPANDED_ARROW

            oldBrush = self.painter.brush()
            self.painter.setBrush(self.ARROW_COLOR)
            self.painter.setPen(qt.Qt.NoPen)
            self.painter.drawPolygon(arrow)
            self.painter.setBrush(oldBrush)
            self.painter.restore()
        else:
            oldBrush = self.painter.brush()
            rect2 = deepcopy(self.rect)
            padding = pix(26)
            newRect = qt.QRect()

            newRect.setRight(rect2.left() + padding)
            newRect.setLeft(newRect.right() - self.ICON_WIDTH_NO_DPI)
            newRect.setBottom(rect2.top() - self.ICON_WIDTH + pix(6))
            newRect.setTop(newRect.bottom() + self.ICON_WIDTH)
            icon = self.DRAG_HANDLE_IMAGE
            if self.item.nodeType() == 'MASH_Distribute':
                icon = self.LOCK_IMAGE
            self.painter.drawPixmap(newRect, icon)
            self.painter.setBrush(oldBrush)
            self.painter.restore()

    def _drawFill(self):
        ''' Draws the border of the cell '''

        rect2 = deepcopy(self.rect)
        oldPen = self.painter.pen()

        # draw a 2 pixel border around the box
        self.painter.setPen(qt.QPen(self.item.getWindowBackgroundColor(), pix(2)))
        rect2.setLeft(rect2.left())
        rect2.setRight(rect2.right()-pix(2))
        rect2.setTop(rect2.top() )
        rect2.setBottom(rect2.bottom() )
        self.painter.drawRect(rect2)

        self.painter.setPen(oldPen)

    def _addActionIcons(self):
        ''' Draws the icons, buttons and tags on the right hand side of the cell '''

        top = self.rect.top() + (self.ICON_TOP_OFFSET)

        start = self.ACTION_BORDER
        count = self.item.getActionButtonCount()
        toolbarCount = 1 #count

        for iconIndex in range(0, count):
            extraPadding = 0
            checked = False
            pixmap = None
            actionName = self.item.getActionButton(iconIndex)

            if (actionName == 'Enabled') :
                showEnabledButton = self.item.hasEnableToggle()
                if not showEnabledButton:
                    start += self.ACTION_WIDTH + extraPadding
                    continue
                extraPadding = pix(10)
                pixmap = self.ENABLED_IMAGE
                if not self.item.isWaiter() and not self.item.networkEnabled():
                    pixmap = self.INACTIVE_ENABLED_IMAGE
                checked = self.item.isEnabled()
                if not checked:
                    pixmap = self.DISABLED_IMAGE

                if self.isHighlighted and checked:
                    pixmap = self.ENABLED_SELECTED_IMAGE
            elif (actionName == 'Add'):
                pixmap = self.ADD_IMAGE
            elif (actionName == 'Repro'):
                waiter = self.item.getName()
                geometryNode = None
                if cmds.objExists(waiter+'.instancerMessage'):
                    geometryNode = cmds.listConnections(waiter+'.instancerMessage', d=True, s=False )
                if geometryNode and (cmds.nodeType(geometryNode[0]) == 'MASH_Repro'):
                    pixmap = self.REPRO_IMAGE
                else:
                    pixmap = self.INSTANCER_IMAGE
            elif (actionName == 'Scripts'):
                pixmap = self.SCRIPTS_IMAGE
            elif (actionName == 'Connections') and self.item.hasConnections():
                pixmap = self.CONNECTIONS_IMAGE

            start += self.ACTION_WIDTH + extraPadding
            self._drawAction(actionName, pixmap, self.rect.right() - start, top)


    def _drawAction(self, actionName, pixmap, left, top):
        ''' Paints the icons requested by _addActionIcons along with their opacity change on mouse over '''
        ''' Crucially, self.lastHitAction is set here, which allows us to process clicks on the icons '''

        if (pixmap != None):
            iconRect = qt.QRect(left, top, self.ICON_WIDTH, self.ICON_WIDTH)

            # draw the icon.  Its brightness depends on mouse over.
            p = self.parent().mapFromGlobal(qt.QCursor.pos())
            if not iconRect.contains(p):
                self.painter.setOpacity(1.0)
            else:
                self.parent().lastHitAction = actionName
                pixmap = self.rolloverIcon_(pixmap)
            self.painter.drawPixmap(iconRect, pixmap)
            self.painter.setOpacity(1.0)

    def rolloverIcon_(self, pixmap):
        img = qt.QImage(pixmap.toImage().convertToFormat(qt.QImage.Format_ARGB32))
        imgh = img.height()
        imgw = img.width()

        for y in range (0, imgh, 1):
            for x in range (0, imgw, 1):
                pixel = img.pixel(x, y);
                highLimit = 205 # value above this limit will just max up to 255
                lowLimit = 30 # value below this limit will not be adjusted
                adjustment = 255 - highLimit;
                color = qt.QColor(pixel);
                v = color.value()
                s = color.saturation()
                h = color.hue()
                if(v > lowLimit):
                    if (v < highLimit):
                        v = v + adjustment
                    else:
                        v = 255
                v = color.setHsv(h, s, v)
                img.setPixel(x, y, qt.qRgba(color.red(), color.green(), color.blue(), qt.qAlpha(pixel)));

        return qt.QPixmap(img)

class mash_node_class(object):
    '''
    a trivial custom data object
    '''
    def __init__(self, nodeName, nodeType, isWaiter, icon, enabled, networkEnabled):
        self.nodeName = nodeName
        self.nodeType = nodeType
        self.isWaiter = isWaiter
        self.networkEnabled = networkEnabled
        self.icon = icon
        self.labelColour = qt.QColor(241,90,91)
        color = qt.QColor(0, 0, 0)
        color.setNamedColor('#444444')
        self.backgroundColour = color
        if (self.isWaiter):
            color.setNamedColor('#5d5d5d')
            self.backgroundColour = color

        self.enabled = enabled
        self.tooltip = None

    def __repr__(self):
        return 'NODE - %s %s'% (self.nodeName)

class TreeItem(qt.QTreeWidgetItem):

    def __init__(self, mashNode, header, showEnabled, parent=None):
        #self._model = model
        qt.QTreeWidgetItem.__init__(self)
        self.mashNode = mashNode
        self.header = header
        self.connectedNodes = []
        self.showEnable = showEnabled # show the enable button

        self.setParent(parent)

    # Override parent mechanism to avoid deleted C++ objects
    def parent(self):
        return self._parent

    def setParent(self, parent):
        self._parent = parent

    def getName(self):
        return self.mashNode.nodeName

    def setName(self, name, useNodeType = False):
        newName = name
        if (not self.mashNode.isWaiter) and useNodeType:
            newName = name+self.mashNode.nodeType[4:]

        returnedName = cmds.rename(self.getName(), name)
        self.mashNode.nodeName = returnedName

    def setEnabled(self):
        self.mashNode.enabled = not self.isEnabled()
        if not self.isWaiter():
            cmds.setAttr(self.getName() + '.enable', self.isEnabled())
            if (self.nodeType() == 'MASH_Distribute'):
                waiterNode = cmds.listConnections(self.getName() + '.waiterMessage', d=True, s=False)
                parent = self.parent()
                if waiterNode and (parent.getName() == waiterNode[0]):
                    parent.mashNode.networkEnabled = self.mashNode.enabled
        else:
            distributeNode = cmds.listConnections(self.getName() + '.waiterMessage', d=False, s=True )
            self.mashNode.networkEnabled = self.isEnabled()
            if distributeNode:
                cmds.setAttr(distributeNode[0] + '.enable', self.isEnabled())
                for x in range(self.childCount()):
                    child = self.child(x)
                    child.mashNode.networkEnabled = self.isEnabled()

    def showAETemplate(self):
        if (self.mashNode.nodeName is not None):
            mel.eval ( ' evalDeferred \"showEditorExact(\\"' + self.mashNode.nodeName + '\\")\" -lp' )

    def getMashNetworkObjects(self, name=None, foundNames=None, dest=True):
        if foundNames is None or name is None:
            name = self.mashNode.nodeName
            foundNames = set([name])
        objs = cmds.listConnections(name, destination=dest) or []
        for obj in objs:
            if obj in foundNames: continue
            if 'MASH' in cmds.nodeType(obj):
                foundNames.add(obj)
                shouldDest = 'MASH_Breakout' != cmds.nodeType(obj)
                if 'MASH_Repro' == cmds.nodeType(obj):
                    foundNames = foundNames.union(cmds.listConnections(obj, source=False, type='mesh'))
                mObjs = self.getMashNetworkObjects(obj, foundNames, shouldDest)
                foundNames = foundNames.union(mObjs)
                relatives = cmds.listRelatives(obj)
                if relatives:
                    foundNames = foundNames.union(relatives)
            else:
                relatives = cmds.listRelatives(obj)
                if relatives:
                    for rel in relatives:
                        if 'MASH' in cmds.nodeType(rel):
                            foundNames.add(obj)
                            mObjs = self.getMashNetworkObjects(obj, foundNames)
                            foundNames = foundNames.union(mObjs)
        return foundNames

    def deleteNode(self):
        if self.mashNode.isWaiter:
            for obj in self.getMashNetworkObjects():
                if cmds.objExists(obj):
                    cmds.delete(obj, s=True)
        elif cmds.nodeType(self.mashNode.nodeName) == 'MASH_Dynamics':
            dmn.deleteMashNode(self.mashNode.nodeName)
        else:
            mel.eval('source "MASHdeleteNodeButton.mel"; deleteButtonCMDS("'+self.mashNode.nodeName+'",1,0)')

    def addNode(self, nodeType):
        melCmd = 'source "AEMASH_WaiterTemplate.mel";'
        mel.eval(melCmd)
        melCmd = 'MASHaddNode("'+nodeType+'","'+self.mashNode.nodeName+'");'
        newNode = mel.eval(melCmd)
        return newNode

    def getName(self):
        if self.mashNode:
            return self.mashNode.nodeName
        return self.header

    def getIcon(self):
        return self.mashNode.icon

    def getBackgroundColor(self):
        return self.mashNode.backgroundColour

    def isEnabled(self):
        return self.mashNode.enabled

    def isWaiter(self):
        return self.mashNode.isWaiter

    def labelColor(self):
        return self.mashNode.labelColour

    def nodeType(self):
        return self.mashNode.nodeType

    def networkEnabled(self):
        return self.parent().mashNode.networkEnabled

    def hasConnections(self):
        return bool(self.connectedNodes and len(self.connectedNodes))

    def getActionButtonCount(self):
        return 7 if self.mashNode.isWaiter else 3

    def hasEnableToggle(self):
        return self.showEnable

    def getInactiveColor(self):
        return qt.QColor(150, 150, 150)

    def getWindowBackgroundColor(self):
        return qt.QColor(43, 43, 43)

    def getActionButton(self, index):
        '''
        Return the button type / layout for Waiters and nodes
        '''
        if self.mashNode.isWaiter:
            if index >= 0 and index <= 6:
                return ['Enabled', None, 'Repro', 'Scripts', 'Add', None, 'Connections'][index]
        else:
            if index >= 0 and index <= 2:
                return ['Enabled', None, 'Connections'][index]
        return None

    def setLabelColour(self, color):
        self.mashNode.labelColour = color
        value = [color.red()/255.0, color.green()/255.0, color.blue()/255.0]
        cmds.setAttr(self.mashNode.nodeName + '.labelColor', *value, type='double3')
        for x in range(self.childCount()):
            child = self.child(x)
            child.mashNode.labelColour = color

# ==============
# LAUNCH THE INTERFACE - WITH WORKSPACE COMPATIBILITY
# ==============

if not 'mashEditorWindow' in globals():
    mashEditorWindow = None

def mashEditorWindowClosed(object=None):
    global mashEditorWindow
    if mashEditorWindow is not None:
        mashEditorWindow.cleanup()
        mashEditorWindow.parent().setParent(None)
        mashEditorWindow.parent().deleteLater()
    mashEditorWindow = None

def mashEditorWindowDestroyed(object=None):
    global mashEditorWindow
    mashEditorWindow = None

def show(restore=False):
    global mashEditorWindow

    if mashEditorWindow:
        mashEditorWindow.updateData()

    if restore == True:
        if mashEditorWindow is not None:
            mashEditorWindow.close()
            mashEditorWindowClosed()

        parent = omui.MQtUtil.getCurrentParent()
        mashEditorWindow = MASHEditor(name='MASHOutliner')
        mashEditorWindow.destroyed.connect(mashEditorWindowDestroyed)
        mashEditorWindow.setProperty('saveWindowPref', True )
        
        widget = wrapInstance(int(parent), qt.QWidget)
        layout = widget.layout()
        layout.addWidget(mashEditorWindow)
        forceRepaint(mashEditorWindow)
        return mashEditorWindow

    elif mashEditorWindow is None:
        # Create Window
        #   Do not parent the widget under the Maya mainWindow (so it does not auto-destroy itself when the variable that references
        #   it goes out of scope), because it does not work since Qt 5.12.
        mashEditorWindow = MASHEditor(name='MASHOutliner', parent=None)

        mashEditorWindow.destroyed.connect(mashEditorWindowDestroyed)
        mashEditorWindow.setProperty('saveWindowPref', True ) # identify a Maya-managed floating window, which handles the z order properly and saves its positions

    # Show window, setting save = True so that this Widget is saved for Workspaces
    restoreScript = 'import MASH.editor; MASH.editor.show(restore=True)'
    mashEditorWindow.show(dockable=True, save=True, plugins='MASH', uiScript=restoreScript)

    forceRepaint(mashEditorWindow)
    return mashEditorWindow

# ==============
# UTILITIES
# ==============

def getMASHNodesInNetwork(waiter):
    inConnections = cmds.listConnections( waiter+'.inputPoints', d=False, s=True, sh=True )
    nodesInNetwork = []

    if inConnections:
        while (len(inConnections)) > 0:
            mashNode = inConnections[0]
            mashNodeType = cmds.nodeType(mashNode)
            if mashNodeType and mashNodeType.startswith('MASH_'):
                nodesInNetwork.append(mashNode)

            if cmds.objExists(inConnections[0]+'.inputPoints'):
                inConnections = cmds.listConnections( inConnections[0]+'.inputPoints', d=False, s=True, sh=True )
                if not inConnections:
                    break
            else:
                break
    return nodesInNetwork

def getNodeFalloffs(node):
    falloffs = set()
    conns = cmds.listConnections(node, destination=False) or []
    for conn in conns:
        relatives = cmds.listRelatives(conn, type='MASH_Falloff') or set()
        falloffs = falloffs.union(relatives)
    return falloffs

def reorderNetwork(waiter, startIndex, endIndex):
    nodesInNetwork = getMASHNodesInNetwork(waiter)
    # 1. Disconnect the node that's moving, and reconnect the surrounding nodes
    inConnections = cmds.listConnections(nodesInNetwork[startIndex]+'.inputPoints', d=False, s=True, p=True) or []
    outConnections = cmds.listConnections(nodesInNetwork[startIndex]+'.outputPoints', d=True, s=False, p=True) or []

    #we're moving away from the Waiter, adjust the end index accordingly
    if (startIndex < endIndex):
        endIndex=endIndex+1

    if startIndex == endIndex:
        return

    for connection in outConnections:
        try:
            cmds.disconnectAttr(connection, nodesInNetwork[startIndex]+'.outputPoints')
        except:
            pass
        try:
            cmds.connectAttr(inConnections[0], connection, force=True)
        except:
            pass

    # 2. Hook up the output of the previous node at the desired location to the input of the node being reorderer
    cmds.connectAttr(nodesInNetwork[endIndex]+'.outputPoints', nodesInNetwork[startIndex]+'.inputPoints', force=True)

    # 2.1 Check if there are falloffs connected to this node, and adjust them as well
    source = nodesInNetwork[endIndex]+'.outputPoints'
    for falloff in getNodeFalloffs(nodesInNetwork[startIndex]):
        if not cmds.isConnected(source, falloff+'.falloffIn', ignoreUnitConversion=True):
            cmds.connectAttr(source, falloff+'.falloffIn', force=True)


    # 3. Now hook up the output to the next node along's input (check to see if we're becoming the first node, if so, connect to the Waiter)
    destinationPlug = ''

    if (startIndex > endIndex and endIndex > 0) or (startIndex <= endIndex and endIndex < len(nodesInNetwork)):
        destinationPlug = nodesInNetwork[endIndex-1]+'.inputPoints'
    elif startIndex > endIndex:
        destinationPlug = waiter+'.inputPoints'

    cmds.connectAttr(nodesInNetwork[startIndex]+'.outputPoints', destinationPlug, force=True)

def getUtilityConnections(node):
    # get connections to the Waiter's outputPoints exclusing Repro/ Instancer
    # eg. Trails and Explode

    outConnections = cmds.listConnections(node+'.outputPoints', d=True, s=False) or []
    nodesFound = [node for node in outConnections if cmds.nodeType(node) not in WAITER_CONNECTIONS_TO_IGNORE]
    for found in nodesFound:
        if cmds.nodeType(found) == "transform":
            child = cmds.listRelatives(found)[0]
            try:
                outConnections = cmds.listConnections(child+'.outputPoints', d=True, s=False) or []
                extras = [node for node in outConnections if cmds.nodeType(node) not in WAITER_CONNECTIONS_TO_IGNORE]
                nodesFound.extend(extras)
            except: pass
    return nodesFound

def getNodeConnections(node):
    # get input connections to strengthPP (like falloff nodes)
    attrs = list(ATTRS_TO_CHECK)

    if cmds.nodeType(node) == 'MASH_Dynamics':
        attrs += ['dynamicsPP', 'constraintsPP']

    nodesFound = []
    for attr in attrs:
        if cmds.objExists(node+'.'+attr):
            nodesFound += (cmds.listConnections(node+'.'+attr, d=False, s=True) or [])

    return nodesFound

def insertNode(nodeBeingDuplicated, oldWaiter, newWaiter, destinationIndex):
    nodesInNetwork = getMASHNodesInNetwork(newWaiter.getName())
    outConnections = cmds.listConnections( nodesInNetwork[destinationIndex]+'.outputPoints', d=True, s=False, p=True )
    newNode = cmds.duplicate(nodeBeingDuplicated)[0]

    if cmds.nodeType(newNode) == 'transform':
        newNode = cmds.listRelatives(newNode, shapes=True)
        if not newNode:
            return False
        else:
            newNode = newNode[0]

    if 'MASH' in cmds.nodeType(newNode):
        cmds.connectAttr(nodesInNetwork[destinationIndex]+'.outputPoints', newNode+'.inputPoints', force=True)
        cmds.connectAttr(newNode+'.outputPoints', outConnections[0], force=True)
        return True

    return False

def showAETempalateOf(nodeName):
    mel.eval('showEditorExact("' + nodeName + '")')

def goToRepro(waiter):
    outConnections = None
    if cmds.objExists(waiter+'.instancerMessage'):
        outConnections = cmds.listConnections(waiter+'.instancerMessage', d=True, s=False)
    if outConnections:
        showAETempalateOf(outConnections[0])

def get_maya_window():
    ptr = omui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), qt.QMainWindow)

def updateMASHEditor():
    ''' Refresh all the MASH Outliners in a Scene'''
    widgets = get_maya_window().findChildren(MASHEditor) or []
    for widget in widgets:
        widget.updateData()
        forceRepaint(widget)
    if mashEditorWindow:
        mashEditorWindow.updateData()
        forceRepaint(mashEditorWindow)

def forceRepaint(widget):
    widget.window().repaint()

# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
