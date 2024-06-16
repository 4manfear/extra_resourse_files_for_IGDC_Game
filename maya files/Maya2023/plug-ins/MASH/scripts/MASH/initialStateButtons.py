import InViewMessageWrapper as ivm

from maya.app.flux.ae.Custom import Custom

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

def add(node):
    import maya.app.flux.ae.api as aeAPI
    aeAPI.addCustom(InitialStateButtons(node))

class MyEventFilter(qt.QObject):
    def __init__(self, obj):
        qt.QObject.__init__(self)
        self.obj = obj

    def eventFilter(self, widget, event):
        if event.type() == qt.QEvent.Resize:
            self.obj.move(widget.width() - pix(22), pix(1))
        return False


class InitialStateButtons(Custom):
    def buildUI(self, nodeName):

        self.registerExternalNode('initialStateNode', self.getInitialStateNode)

        self.addSpacing(pix(5))

        title = mel.eval('getPluginResource("MASH", "kInitStateNode")')
        with self.indentLayout(title, autoStretch=False):
            self.lineEdit = qt.QLineEdit()
            self.lineEdit.setReadOnly(True)
            self.lineEdit.setStyleSheet('QLineEdit(border: 0px; border-radius:2px;)')
            self.lineEdit.setTextMargins(pix(18), pix(0), pix(22), pix(0))
            self.lineEdit.setFixedHeight(pix(22))

            self.setButton = fx.ImageButton('out_MASH_CreateUtility', parent=self.lineEdit)
            self.setButton.move(pix(1), pix(1))
            self.setButton.clicked.connect(self.setBtnClicked)
            self.switchButton = fx.ImageButton('out_MASH_Enable', parent=self.lineEdit)
            self.switchButton.clicked.connect(self.switchBtnClicked)
            self.switchEventFilter = MyEventFilter(self.switchButton)
            self.lineEdit.installEventFilter(self.switchEventFilter)

            self.addWidget(self.lineEdit)

        self.addSpacing(pix(5))

        self.createAttributeListener('enable', self.enableChanged, node='initialStateNode')
        self.createAttributeListener('initialStateMessage', self.initialStateMessageChanged)

        self.initialStateMessageChanged()
        self.enableChanged()

    def initialStateMessageChanged(self):
        node = self.getInitialStateNode()
        if node:
            self.lineEdit.setText(node)
            self.switchButton.show()
            self.setButton.setImage('out_MASH_Refresh')
        else:
            self.lineEdit.setText(fx.res('kNotConnected'))
            self.switchButton.hide()
            self.setButton.setImage('out_MASH_CreateUtility')


    def getInitialStateNode(self):
        if 'initialStateMessage' in cmds.listAttr(self.name):
            conns = cmds.listConnections(self.name+'.initialStateMessage')
            if conns:
                return conns[0]

        return None

    def enableChanged(self):
        node = self.getInitialStateNode()
        if node:
            enabled = cmds.getAttr(node + '.enable')
            self.switchButton.setImage('out_MASH_Enable' if enabled else 'out_MASH_Disable')

    def setBtnClicked(self):
        node = self.getInitialStateNode()
            
        if node:
            if cmds.nodeType(node) == "MASH_DynamicsInitialState":
                self.set_initial_state()
                cmds.setAttr(node+".enable", 1)
            else:
                self.create_initial_state()
        else:
            self.create_initial_state()

        self.initialStateMessageChanged()
        self.enableChanged()

    def switchBtnClicked(self):
        node = self.getInitialStateNode()
        if node and cmds.nodeType(node) == 'MASH_DynamicsInitialState':
            value = cmds.getAttr(node + '.enable')

            if value == 1:
                cmds.setDynamicsInitialState(clearState=True, name=self.name)
                cmds.setAttr(node + '.enable', 0)
            else:
                self.set_initial_state()
                cmds.setAttr(node+".enable", 1)

            self.enableChanged()

    def create_initial_state(self):
        if 'initialStateMessage' not in cmds.listAttr(self.name):
            cmds.addAttr(self.name, longName='initialStateMessage', at='message')
        initialStateNode = cmds.createNode("MASH_DynamicsInitialState", skipSelect=True)
        cmds.addAttr(initialStateNode, longName='initialStateMessage', at='message')
        cmds.connectAttr(initialStateNode+'.initialStateMessage', self.name+'.initialStateMessage', f=True)
        inputPointsConnection = cmds.listConnections(self.name+'.inputPoints', p=True)[0]
        self.set_initial_state()
        cmds.connectAttr(inputPointsConnection, initialStateNode+'.inputPoints', f=True)
        cmds.connectAttr(initialStateNode+'.outputPoints', self.name+'.inputPoints', f=True)
        cmds.setAttr(initialStateNode+".enable", 1)

        self._refreshAttributeListeners()

    def set_initial_state(self):
        cmds.setDynamicsInitialState(setState=True, name=self.name)
        message = mel.eval('getPluginResource("MASH", "kInitStateSet")')
        ivm.MashInViewMessage(message, "Info")

    def nodeChanged(self):
        self.initialStateMessageChanged()
        self.enableChanged()
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
