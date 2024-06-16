from builtins import chr
from builtins import range
from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import json

import maya
import maya.OpenMayaUI as mui


class MASHTextFieldWidget(qt.QWidget):
    def __init__(self, node, parent=None):
        super(MASHTextFieldWidget, self).__init__(parent)
        self.node = node
        self.listWidget = TextEditExtend(node)
        self.setMinimumWidth(pix(360))
        self.setMinimumHeight(pix(100))
        self.layout = qt.QBoxLayout(qt.QBoxLayout.TopToBottom, self)

        self.layout.setContentsMargins(pix(5),pix(3),pix(11),pix(3))
        self.layout.setSpacing(pix(5))
        self.layout.addWidget(self.listWidget)
        self.listWidget.updateContent()

    #update connections
    def set_node(self, node):
        self.node = node
        self.listWidget.node = node
        self.listWidget.updateContent()

def build_qt_widget(lay, node):
    widget = MASHTextFieldWidget(node)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def update_qt_widget(layout, node):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "MASHTextFieldWidget":
                widget.set_node(node)
                break

class TextEditExtend(qt.QTextEdit):

    def __init__(self, node, parent=None):
        super(TextEditExtend, self).__init__()
        self.node = node
        self.textChanged.connect(self.saveContent)

    def updateContent(self):
        inputText = cmds.getAttr(self.node+".inputText")
        self.setText(HexToUni(inputText))

    def saveContent(self):
        plainText = self.toPlainText()
        hexText = ByteToHex(plainText)
        cmds.setAttr(self.node+".inputText", hexText, type="string")

def ByteToHex( byteStr ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """

    # Uses list comprehension which is a fractionally faster implementation than
    # the alternative, more readable, implementation below
    #
    #    hex = []
    #    for aChar in byteStr:
    #        hex.append( "%02X " % ord( aChar ) )
    #
    #    return ''.join( hex ).strip()

    return ''.join( [ "%02X " % ord( x ) for x in byteStr ] ).strip()

def HexToUni( hexStr ):
    bytes = []

    if len(hexStr) == 0:
        return ""

    hexStr = hexStr.split(" ")

    for hexChar in hexStr:
        ordNum = int(hexChar, 16)
        bytes.append(chr(ordNum))

    return ''.join( bytes )# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
