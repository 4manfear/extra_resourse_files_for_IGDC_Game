from __future__ import division
from builtins import object
from builtins import range
import maya.OpenMayaUI as mui
from types import *

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix
from maya.internal.common.qt.doubleValidator import MayaQclocaleDoubleValidator

import logging

# ==============
# LOGGING
#   Use the python standard logging module to control logging info, warning, and
#   debug statements for the editor.  By default, only warnings and errors are displayed
#   After is module is loaded, the logging level can be specified.
#   This is useful for debugging,
# Usage:
#     MASHthreeFloatSpinner.logger.setLevel(logging.DEBUG)
# ==============

logger = logging.getLogger('MASHThreeFloatSpinner')
#logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
if len(logger.handlers) == 0:
    formatter = logging.Formatter('[%(name)s] %(levelname)s: %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.propagate=0   # do not propagate to the standard Maya logger or it will double-represent it in the logs


def mashGetMObjectFromNameOne(nodeName):
    sel = om.MSelectionList()
    sel.add(nodeName)
    thisNode = om.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode

class MASHthreeFloatParentWidget(qt.QWidget):
    def __init__(self, node, minimumValue, maximumValue, sourceAttrs, command, parent=None):
        super(MASHthreeFloatParentWidget, self).__init__(parent)
        self.node = node
        mashPath = mel.eval('getenv("MASH_LOCATION")')
        self.iconsPath = mashPath+'icons/'
        attributeList = sourceAttrs.split(',')

        self.xVirtualSlider = ButtonLineEdit(self.iconsPath+"ae_MASH_Slider.png", node, attributeList[0], self)
        self.yVirtualSlider = ButtonLineEdit(self.iconsPath+"ae_MASH_Slider.png", node, attributeList[1], self)
        self.zVirtualSlider = ButtonLineEdit(self.iconsPath+"ae_MASH_Slider.png", node, attributeList[2], self)

        self.xVirtualSlider.attribute = node+'.'+attributeList[0]
        self.yVirtualSlider.attribute = node+'.'+attributeList[1]
        self.zVirtualSlider.attribute = node+'.'+attributeList[2]

        self.xVirtualSlider.setInitialValue()
        self.yVirtualSlider.setInitialValue()
        self.zVirtualSlider.setInitialValue()

        self.layout = qt.QBoxLayout(qt.QBoxLayout.LeftToRight, self)
        self.layout.setContentsMargins(pix(0),pix(0),pix(0),pix(0))
        self.layout.setSpacing(pix(2))
        self.setAttribute(qt.Qt.WA_MacShowFocusRect, 0)

        self.layout.addWidget(self.xVirtualSlider)
        self.layout.addWidget(self.yVirtualSlider)
        self.layout.addWidget(self.zVirtualSlider)

        self.nodeObj = mashGetMObjectFromNameOne(node)

        # Track MCallbacks added by this class so they can be cleaned up when the widget closes
        self._registeredMayaCallbacks = []        # used to register/deregister Maya callbacks
        self._registeredMayaCallbacksPerNode = {}  # key=<MObjectHandle<node>> value=[callbacks] -- used to register/deregister Maya callbacks per creaseSet node

        self.playbackState = 0


    #update connections
    def set_node(self, node, minimumValue, maximumValue, sourceAttrs, command):
        self.node = node
        '''
        self.xVirtualSlider.node = node
        self.xVirtualSlider.desiredNodeType = minimumValue
        self.xVirtualSlider.maximumValue = maximumValue
        self.xVirtualSlider.sourceAttrs = sourceAttrs
        #self.xSpinner.checkConnections()
        self.xVirtualSlider.command = command
        '''
    def addPerNodeMayaCallbacks(self, nodeObj):
        '''Add the Maya per-node callbacks for the specified item
        and register them with the widget (so they can be cleaned up).

        :Parameters:
            nodeObj (MObject)
                MObject depend node to add per-node callbacks to

        :Return: None
        '''

        # = Attr Changed (Connect Controls)
        # Do a 'connectControl' style operation
        cb = om.MNodeMessage.addAttributeChangedCallback(nodeObj, self.objectSetAttrChangedCB, None)
        self._registeredMayaCallbacks.append( MCallbackIdWrapper(cb) )

        cb = om.MConditionMessage.addConditionCallback("playingBack", self.playbackStateChanged)
        self._registeredMayaCallbacks.append( MCallbackIdWrapper(cb) )
        #MCallbackId callbackId = MEventMessage::addEventCallback("timeChanged",  (MMessage::MBasicFunction) MySampleCmd::userCB);

        # = Name changed callback
        cb = om.MNodeMessage.addNameChangedCallback(nodeObj, self.objectSetNodeNameChangedCB, None)
        self._registeredMayaCallbacks.append( MCallbackIdWrapper(cb) )

    def removePerNodeMayaCallbacks(self, nodeObj):
        '''Remove per-node Maya callbacks.

        :Parameters:
            nodeObjs ([MObject])
                List of MObject dependency nodes on which to remove the Maya per-node callbacks
        '''
        logger.debug('CreaseSetEditor::removePerNodeMayaCallbacks(%s)'%nodeObj)
        # Remove existing per-set callbacks
        nodeObjHandle = HashableMObjectHandle(nodeObj) # Determine MObjectHandles for the nodeObjs as that is used for the keys
        if nodeObjHandle in self._registeredMayaCallbacksPerNode:
            callbacks = self._registeredMayaCallbacksPerNode[nodeObjHandle]
            logger.debug('Removing %i per-node callbacks for \"%s\"'%(len(callbacks), om.MFnDependencyNode(nodeObjHandle.object()).name()))
            del self._registeredMayaCallbacksPerNode[nodeObjHandle]
        else:
            logger.debug('No registered per-node callbacks to remove for %s.'%nodeObjHandle)

    def beforeSceneUpdatedCB(self, clientData):
        '''Freeze the callbacks before the entire scene is being reloaded or cleared.
        Unfreezing the callbacks is handled in the sceneUpdatedCB below.

        :Parameters:
            clientData
                container of the Maya client data for the event

        :Return: None
        '''
        logger.debug('beforeSceneUpdatedCB(%s)'%clientData)
        self.cleanup()

    def showEvent(self, *args):

        self.addPerNodeMayaCallbacks(self.nodeObj)
        self.forceUpdateChildren()

    def hideEvent(self, *args):
        '''When widget is hidden, remove the Maya callbacks and clean up.
        '''
        self.cleanup()

        # NOTE: Not using super() as hideEvent could be called after it seems that self is deleted with __del__ and super does not work then
        return qt.QWidget.hideEvent(self, *args)

    def cleanup(self):
        '''Cleanup environment by removing the Maya callbacks, etc.
        '''
        logger.debug('CreaseSetEditor::cleanup()')
        # MCallbackWrapper items automatically clean themselves up on deletion
        self._registeredMayaCallbacks = []
        self._registeredMayaCallbacksPerNode= {}

    def objectSetAttrChangedCB(self, msg, plg, otherPlg, clientData):
        """Selectively update the widget tree for the specified item when
        the attributes of a creaseSet are modified

        :Parameters:
            msg (maya.OpenMaya.MNodeMessage)
                om.MNodeMessage enum for the action upon the attr.  Use '&' to check the value.
                Example use: msg&om.MNodeMessage.kAttributeSet
            plug (MPlug)
                MPlug for the attribute
            otherPlg (MPlug)
                MPlug for other connected attribute that may be contributing to this action
            clientData
                container of the Maya client data for the event

        :Return: None
        """

        if not (msg&om.MNodeMessage.kAttributeEval or msg&om.MNodeMessage.kAttributeSet):
            logger.debug('Skipping. Attr message does is not kAttributeEval or kAttributeSet')
            return

        (nodename, attrName) = plg.name().split('.',1)
        if attrName in ('amplitudeX', 'amplitudeY', 'amplitudeZ', 'outputPoints'):
            self.forceUpdateChildren()

    def playbackStateChanged(self, state, clientData):
        if (state==0):
            self.forceUpdateChildren()
        self.playbackState = state

    def forceUpdateChildren(self):
        if (self.xVirtualSlider.interaction == False):
            self.xVirtualSlider.setInitialValue()
        if (self.yVirtualSlider.interaction == False):
            self.yVirtualSlider.setInitialValue()
        if (self.zVirtualSlider.interaction == False):
            self.zVirtualSlider.setInitialValue()

    def objectSetNodeNameChangedCB(self, nodeObj, prevName, clientData):
        '''Selectively update the widget items when a Maya CreaseSet node name changes

        :Parameters:
            nodeObj (MObject)
                MObject depend node for the node added
            prevName (string)
                previous name of the node
            clientData
                container of the Maya client data for the event

        :Return: None
        '''
        logger.debug('In objectSetNodeNameChangedCB')

def build_qt_widget(lay, node, minimumValue, maximumValue, sourceAttrs, command):
    widget = MASHthreeFloatParentWidget(node, minimumValue, maximumValue, sourceAttrs, command)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def update_qt_widget(layout, node, minimumValue, maximumValue, sourceAttrs, command):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "MASHthreeFloatParentWidget":
                widget.set_node(node, minimumValue, maximumValue, sourceAttrs, command)
                break

class MashSpinner(qt.QToolButton):
    def __init__(self, parent=None):
        super(MashSpinner, self).__init__(parent)

        self.mouseDown = False

    def mousePressEvent(self, event):
        self.offset = event.x()
        self.mouseDown = True
        qt.QEvent.ignore(event)

    def mouseReleaseEvent(self, event):
        self.mouseDown = False
        qt.QEvent.ignore(event)

    def mouseMoveEvent(self, event):
        qt.QEvent.ignore(event)


class ButtonLineEdit(qt.QLineEdit):
    buttonClicked = qt.Signal()

    def __init__(self, icon_file, node, attribute, parent=None):
        super(ButtonLineEdit, self).__init__(parent)
        self.button = MashSpinner(self)
        self.interaction = False
        mashPath = mel.eval('getenv("MASH_LOCATION")')
        self.iconsPath = mashPath+'icons/'
        self.iconFile = icon_file
        self.iconOff = self.iconsPath+"ae_MASH_Slider.png"
        self.iconRight = self.iconsPath+"ae_MASH_SliderRight.png"
        self.iconLeft = self.iconsPath+"ae_MASH_SliderLeft.png"
        self.node = node
        self.button.setIcon(qt.QIcon(self.iconOff))
        self.button.setStyleSheet('border: 0px; padding: 0px;')
        self.button.setCursor(qt.Qt.ArrowCursor)
        self.button.clicked.connect(self.buttonClicked.emit)
        validator = MayaQclocaleDoubleValidator()
        self.value = 0.0
        self.offset = 0.0
        self.setValidator(validator)
        self.setMouseTracking(True)
        frameWidth = self.style().pixelMetric(qt.QStyle.PM_DefaultFrameWidth)
        buttonSize = self.button.sizeHint()
        self.mouseDown = False
        #self.setStyleSheet('QLineEdit {padding-right: %dpx; }' % (buttonSize.width() + frameWidth + 1))
        self.setMinimumSize(max(self.minimumSizeHint().width(), buttonSize.width() + frameWidth*2 + pix(2)),
                            max(self.minimumSizeHint().height(), buttonSize.height() + frameWidth*2 + pix(2)))
        #self.setStyleSheet("outline: none;")
        self.mousePosition = (0.0,0.0)
        self.attribute = ""
        self.mimimumValue = 0.0
        self.isKeyed = False
        self.isConnected = False
        self.setAttribute(qt.Qt.WA_MacShowFocusRect, 0)

        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.menu = qt.QMenu();
        #

    def openMenu(self, pos):
        self.menu.clear()

        menuItem = qt.QAction("Blah", self)
        menuItem.triggered.connect(self.setInitialValue)
        self.menu.addAction(menuItem)

        self.menu.exec_(qt.QCursor.pos())

    def setInitialValue(self):
        self.value = cmds.getAttr(self.attribute);
        self.setValue(self.value)

        # bg colour
        keyframes = cmds.keyframe(self.attribute,query=True)
        if keyframes and self.isKeyed == False:
            self.isKeyed = True
            self.setStyleSheet('color: black; background-color: #dd727a;')
        elif not keyframes and self.isKeyed == True:
            self.setStyleSheet('')

        if self.isKeyed == False:
            connections = cmds.listConnections(self.attribute, d=False, s=True)
            if keyframes and self.isConnected == False:
                self.isConnected = True
                self.setStyleSheet('color: black; background-color: #f1f1a5;')
            elif not connections and self.isConnected == True:
                self.setStyleSheet('')

    def setAttributeCmd(self):
        currentValue = float(self.text())
        cmds.setAttr(self.attribute,currentValue)

    def setValue(self, value):
        interfaceValue = round(value,3)
        self.setText(str(interfaceValue))

    def resizeEvent(self, event):
        buttonSize = self.button.sizeHint()
        frameWidth = self.style().pixelMetric(qt.QStyle.PM_DefaultFrameWidth)
        self.button.move(self.rect().right() - frameWidth - buttonSize.width(),(self.rect().bottom() - buttonSize.height() + pix(1))/2)
        super(ButtonLineEdit, self).resizeEvent(event)

    def mousePressEvent(self, event):
        self.offset = event.x()
        self.mouseDown = True
        cursor =qt.QCursor()
        self.mousePosition = cursor.pos()
        qt.QLineEdit.mousePressEvent(self,event)

    def mouseReleaseEvent(self, event):
        self.mouseDown = False
        self.interaction = False
        self.value = float(self.text())
        self.setAttributeCmd()
        self.button.setIcon(qt.QIcon(self.iconOff))
        qt.QLineEdit.mouseReleaseEvent(self,event)

    def mouseMoveEvent(self, event):
        modifiers = qt.QApplication.keyboardModifiers()
        if (self.button.mouseDown == True) or ((modifiers == qt.Qt.ControlModifier) and (self.mouseDown == True)):
            self.interaction = True
            relPos = float(event.x()-self.offset)*0.01
            newValue = relPos+self.value
            if (newValue >= self.mimimumValue):
                self.setValue(newValue)
                self.setAttributeCmd()
            else:
                self.setValue(self.mimimumValue)

            if (newValue > self.value):
                self.button.setIcon(qt.QIcon(self.iconRight))
            else:
                self.button.setIcon(qt.QIcon(self.iconLeft))

            #cursor.setPos(self.mousePosition.x()-self.offset, self.mousePosition.y())
            qt.QWidget.mouseMoveEvent(self, event)
        else:
            qt.QLineEdit.mouseMoveEvent(self,event)


class HashableMObjectHandle(om.MObjectHandle):
    '''Hashable MObjectHandle referring to an MObject that can be used as a key in a dict.

    :See: MObjectHandle documentation for more information.
    '''
    def __hash__(self):
        '''Use the proper unique hash value unique to the MObject that the MObjectHandle points to so this class can be used as a key in a dict.

        :Return:
            MObjectHandle.hasCode() unique memory address for the MObject that is hashable

        :See: MObjectHandle.hashCode() documentation for more information.
        '''
        return self.hashCode()


class MCallbackIdWrapper(object):
    '''Wrapper class to handle cleaning up of MCallbackIds from registered MMessage
    '''
    def __init__(self, callbackId):
        super(MCallbackIdWrapper, self).__init__()
        self.callbackId = callbackId
        logger.debug("Adding callback %s"%self.callbackId)

    def __del__(self):
        om.MMessage.removeCallback(self.callbackId)
        logger.debug("Removing callback %s"%self.callbackId)

    def __repr__(self):
        return 'MCallbackIdWrapper(%r)'%self.callbackId
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
