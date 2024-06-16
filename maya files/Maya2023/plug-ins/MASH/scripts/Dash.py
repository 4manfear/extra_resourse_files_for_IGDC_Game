import maya.OpenMayaUI as omui
import maya.mel
import maya.cmds as cmds

import DashCommand as dc
from imp import reload
reload (dc)

# setup PySide2 version as needed
from PySide2 import QtCore, QtGui, QtWidgets
from shiboken2 import wrapInstance

global dashCommandHistory
dashCommandHistory = []


class DashUI(QtWidgets.QDialog):

    #init and expand on QDialog
    def __init__(self, parent=None):
        super(DashUI, self).__init__(parent=parent)

        self.setWindowFlags(QtCore.Qt.Popup|QtCore.Qt.FramelessWindowHint)

        pos = QtGui.QCursor.pos()
        self.setGeometry(pos.x()-250, pos.y(), 250, 25)

        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        #call layout code
        self.create_layout()

        #connect UI to commands
        self.create_connections()

        self.historyId = 0;

    #all layout code goes here
    def create_layout(self):
        #create widgets
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEdit.installEventFilter(self)

        #create layout
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(2,2,2,2) #spacing from window edges to widgets
        main_layout.setSpacing(4) #defalt spacing between iterface items

        #add widgets to layout
        main_layout.addWidget(self.lineEdit)

        #stretch will keep the window items at the top
        main_layout.addStretch()

        #set the layout
        self.setLayout(main_layout)

        #set focus to it
        self.lineEdit.setFocus()

    # Browse command history
    def eventFilter(self, widget, event):
        if (event.type() == QtCore.QEvent.KeyPress and widget is self.lineEdit):
            global dashCommandHistory
            key = event.key()
            if key == QtCore.Qt.Key_Up:
                if len(dashCommandHistory) > 0:
                    self.historyId-=1
                    if abs(self.historyId) > len(dashCommandHistory):
                        self.historyId = 0-len(dashCommandHistory)
                    self.lineEdit.setText(dashCommandHistory[self.historyId])
            if key == QtCore.Qt.Key_Down:
                if len(dashCommandHistory) > 0:
                    self.historyId+=1
                    if self.historyId > 0:
                        self.historyId == 0
                        self.lineEdit.setText("")
                    else:
                        self.lineEdit.setText(dashCommandHistory[self.historyId])

        return QtWidgets.QWidget.eventFilter(self, widget, event)

    #connect buttons to commands
    def create_connections(self):
        self.lineEdit.returnPressed.connect(self.submitCommand)

    def submitCommand(self):
        commandText =  self.lineEdit.text()

        dashCmd = dc.DashCommand(commandText)
        error = dashCmd.getCommandParts()

        global dashCommandHistory
        if error == False:
            dashCommandHistory.append(commandText)

        try:
            DashUI.close(self)
        except:
            pass

#load up window
def showDash(activatingWidget='mainChannelBox'):
     # Get a pointer to the main maya window to use as a parent
    mainWindowPtr = omui.MQtUtil.mainWindow()
    mainWindow = wrapInstance(int(mainWindowPtr), QtWidgets.QWidget)

    #which widget will we query (check dc.getAllSelectedChannels() to see which widgets are supported)
    dc.dashActivatingWidget = activatingWidget
    selectedObjs = cmds.ls(selection=True)
    selectedChannels = dc.getAllSelectedChannels()

    if not selectedChannels:
        cmds.error("No Channels Selected")
        return

    if not selectedObjs:
        cmds.error("No Objects Selected")
        return

    ui = DashUI(parent=mainWindow)
    ui.show()


# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
