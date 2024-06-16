from builtins import range
import maya.OpenMayaUI as mui

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import InViewMessageWrapper

# ==============
# STRING RESOURCES
# ==============
kPoints = mel.eval('getPluginResource("MASH", "kPoints")')
kDelete = mel.eval('getPluginResource("MASH", "kDelete")')
kId = mel.eval('getPluginResource("MASH", "kId")')
kRotate = mel.eval('getPluginResource("MASH", "kRotate")')
kScale = mel.eval('getPluginResource("MASH", "kScale")')
kCollide = mel.eval('getPluginResource("MASH", "kCollide")')
kMove = mel.eval('getPluginResource("MASH", "kMove")')
kSelectPointsManip = mel.eval('getPluginResource("MASH", "kSelectPointsManip")')
kDragOver = mel.eval('getPluginResource("MASH", "kDragOver")')
kNudge = mel.eval('getPluginResource("MASH", "kNudge")')

class PlacerToolButtons(qt.QWidget):
    def __init__(self, node, parent=None):
        super(PlacerToolButtons, self).__init__(parent)

        #
        #   The node the widget is attached to, it's vital to keep this current.
        #
        self.node = node

        #
        #   Create the layout
        #
        self.layout = qt.QHBoxLayout(self)
        self.layout.addStretch()
        self.layout.setContentsMargins(pix(5),pix(3),pix(11),pix(3))
        self.layout.setSpacing(pix(5))
        self.toolButtons = []

        #
        #   Create the buttons
        #
        self.paintButton = ImageButtonExtend('out_MASH_PlacerAdd', kPoints)
        self.paintButton.clicked.connect(lambda: self.toolClicked(self.paintButton))
        self.paintButton.id = 1
        self.toolButtons.append(self.paintButton)

        self.deleteButton = ImageButtonExtend('out_MASH_PlacerDelete', kDelete)
        self.deleteButton.clicked.connect(lambda: self.toolClicked(self.deleteButton))
        self.deleteButton.id = 3
        self.toolButtons.append(self.deleteButton)

        self.collideButton = ImageButtonExtend('out_MASH_PlacerCollide', kCollide)
        self.collideButton.clicked.connect(lambda: self.toolClicked(self.collideButton))
        self.collideButton.id = 2
        self.toolButtons.append(self.collideButton)

        self.idButton = ImageButtonExtend('out_MASH_PlacerID', kId)
        self.idButton.clicked.connect(lambda: self.toolClicked(self.idButton))
        self.idButton.id = 4
        self.toolButtons.append(self.idButton)

        self.nudgeButton = ImageButtonExtend('out_MASH_PlacerNudge', kNudge)
        self.nudgeButton.clicked.connect(lambda: self.toolClicked(self.nudgeButton))
        self.nudgeButton.id = 8
        self.toolButtons.append(self.nudgeButton)

        self.moveButton = ImageButtonExtend('out_MASH_PlacerMove', kMove)
        self.moveButton.clicked.connect(lambda: self.toolClicked(self.moveButton))
        self.moveButton.id = 5
        self.toolButtons.append(self.moveButton)

        self.rotateButton = ImageButtonExtend('out_MASH_PlacerRotate', kRotate)
        self.rotateButton.clicked.connect(lambda: self.toolClicked(self.rotateButton))
        self.rotateButton.id = 6
        self.toolButtons.append(self.rotateButton)

        self.scaleButton = ImageButtonExtend('out_MASH_PlacerScale', kScale)
        self.scaleButton.clicked.connect(lambda: self.toolClicked(self.scaleButton))
        self.scaleButton.id = 7
        self.toolButtons.append(self.scaleButton)

        #
        #   Add buttons to layout (with stretch)
        #
        self.layout.addWidget(self.paintButton)
        self.layout.addWidget(self.deleteButton)
        self.layout.addWidget(self.collideButton)
        self.layout.addWidget(self.idButton)
        self.layout.addWidget(self.nudgeButton)
        self.layout.addStretch()
        self.layout.addWidget(self.moveButton)
        self.layout.addWidget(self.rotateButton)
        self.layout.addWidget(self.scaleButton)
        self.layout.addStretch()

        #   None callback Id for safety
        self.idx = None

    def disableAllButtons(self):
        for button in self.toolButtons:
            button.setHighlighted(False)

    def toolClicked(self, clickedButton):
        # brute force unhighlighting
        self.disableAllButtons()

        # set the clicked button as highlighted
        clickedButton.setHighlighted(True)

        # set the brush type
        cmds.setAttr(self.node+".brushType", clickedButton.id)

        # update the AE template control dimming
        mel.eval('MASHplacerModeType("'+self.node+'");')

        # select the Placer node (otherwise painting will not work
        currentSelection = cmds.ls(sl=True) or []
        if self.node not in currentSelection:
            cmds.select(self.node, add=True)
            mel.eval('showEditorExact("'+self.node+'")')

        # activate the tool context
        mel.eval("MASHplacePoints()")

        if clickedButton.id == 5 or clickedButton.id == 6 or clickedButton.id == 7:
            InViewMessageWrapper.MashInViewMessage(kSelectPointsManip,"Info")
        else:
            InViewMessageWrapper.MashInViewMessage(kDragOver,"Info")

    def hideEvent(self, *args):
        '''
        When widget is hidden, disable the buttons.
        '''
        self.disableAllButtons()

        # change to the select tool
        mel.eval("SelectTool()")

        # remove the tool changed callback
        if self.idx:
            om.MMessage.removeCallback(self.idx)

    def showEvent(self, *args):
        '''
        Add a callback to turn off the tool when the tool/context is changed.
        '''
        self.idx = om.MEventMessage.addEventCallback("PostToolChanged", lambda _: placer_context_check(self.toolButtons))

    def nodeChanged(self):
        '''
        Change to the select tool
        '''
        self.disableAllButtons()
        mel.eval("SelectTool()")

    def setNode(self, node):
        '''
        Update the name of the node that the widget is attached to
        '''
        self.node = node
        self.nodeChanged()

def placer_context_check(toolButtons):
    '''
    If we're no longer in the points tool, disable the buttons.
    '''
    ctx = cmds.currentCtx()
    if "paintPointsContext" not in ctx and len(ctx):
        for button in toolButtons:
            button.setHighlighted(False)

def build_qt_widget(lay, node):
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        mayaWidget = wrapInstance(int(ptr), qt.QWidget)
        widget = PlacerToolButtons(node, mayaWidget)
        mayaLayout = mayaWidget.layout()
        mayaLayout.addWidget(widget)

def update_qt_widget(layout, node):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "PlacerToolButtons":
                widget.setNode(node)
                break

class ImageButtonExtend(fx.ImageButton):
    '''
    Subclass adding id to identify each button in the collection, this is used to set the brush mode.
    '''
    def __init__(self, imageName, text='', textPos='bottom', highlighted=False, parent=None):
        fx.ImageButton.__init__(self, imageName, text, textPos, highlighted, parent)
        self.id = 0
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
