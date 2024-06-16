from builtins import range
import maya.OpenMayaUI as mui
import MASH.api as mapi
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import InViewMessageWrapper

# Node type specific callbacks to tell us if the generated Ids are fixed
def placerFixedModeCheck(node):
    return True if cmds.getAttr(node+".idMode") == 1 else False

def getResource(name):
    return mel.eval('getPluginResource("MASH", "' + name + '")')

# Node type, method
modeCallbackDictionary = {'MASH_Placer':placerFixedModeCheck}

class IdFeedbackWidget(qt.QWidget):
    def __init__(self, node, attrs, modeAttr=None, parent=None):
        super(IdFeedbackWidget, self).__init__(parent)

        # Id feedback can either be based on multiple attributes
        self.attrs = attrs
        self.modeAttr = modeAttr

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
        #   Create the label
        #
        self.label = qt.QLabel()
        self.label.setText(getResource('kPossibleObjects'))
        self.label.setFixedWidth(pix(137))
        self.label.setFixedHeight(pix(14))
        self.label.setAlignment(qt.Qt.AlignRight)

        #
        #   Create the text field
        #
        self.textBox = qt.QLineEdit()
        sp = self.textBox.sizePolicy()
        sp.setHorizontalStretch(1)
        self.textBox.setSizePolicy(sp)
        self.textBox.setReadOnly(True)
        colour = self.palette().color(qt.QPalette.Midlight)
        self.textBox.setStyleSheet('background-color: rgb('+str(colour.red())+', '+str(colour.green())+', '+str(colour.blue())+');');

        #
        #   Add widgets to layout 
        #
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.textBox)

        #   Callback Ids
        self.callbackIds = []

    def getId(self):
        fixedMode = True
        nt = cmds.nodeType(self.node)
        if nt in list(modeCallbackDictionary.keys()):
            fixedMode = modeCallbackDictionary[nt](self.node)

        instancerObjects = self.getInstancerObjects()

        if fixedMode and self.attrs:
            attrId = cmds.getAttr(self.node+"."+self.attrs[0])

            if len(instancerObjects) > attrId:
                self.setFeedback(str(attrId)+": " + instancerObjects[attrId])
            else:
                self.setFeedback(getResource('kNoObjectWithId'))
        elif self.attrs and len(self.attrs) == 3:
            minId = cmds.getAttr(self.node+"."+self.attrs[1])
            maxId = cmds.getAttr(self.node+"."+self.attrs[2])
            feedbackString = ''
            for x in range(minId, maxId+1):
                if len(instancerObjects) > x:
                    feedbackString+=str(x)+': '+instancerObjects[x]+', '
            feedbackString = feedbackString[:-2]

            self.setFeedback(feedbackString)

    def getInstancerObjects(self):
        waiter = mapi.getWaiterFromNode(self.node)
        network = mapi.Network(waiter)
        instancerObjects = []
        if cmds.nodeType(network.instancer) == 'instancer':
            instancerObjects = cmds.listConnections(network.instancer+'.inputHierarchy')
        elif cmds.nodeType(network.instancer) == 'MASH_Repro':
            instancerObjects = cmds.reproInstancer(network.instancer, q=True, obs=True)
        return instancerObjects

    def setFeedback(self, text):
        self.textBox.setText(text)

    def hideEvent(self, *args):
        # remove the attr changed callback
        for cbId in self.callbackIds:
            cmds.scriptJob( kill=cbId, force=True)
        self.callbackIds = []

    def showEvent(self, *args):
        self.getId()
        for attr in self.attrs:
            self.callbackIds.append(cmds.scriptJob( attributeChange=[self.node+'.'+attr, self.getId] ))
        # Monitor for mode changes if needed
        if self.modeAttr:
            self.callbackIds.append(cmds.scriptJob( attributeChange=[self.node+'.'+self.modeAttr, self.getId] ))

    
    def setNode(self, node, attrs, modeAttr):
        '''
        Update the name of the node and the attributes that the widget is attached to
        '''
        self.node = node
        self.attrs = attrs
        self.modeAttr = modeAttr

def buildQtWidget(lay, node, attrs, modeAttr=None):
    widget = IdFeedbackWidget(node, attrs, modeAttr)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def updateQtWidget(layout, node, attrs, modeAttr=None):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "IdFeedbackWidget":
                widget.setNode(node, attrs, modeAttr)
                break
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
