import DashCommand as dc
from imp import reload
reload (dc)

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

global dashCommandHistory
dashCommandHistory = []

class DashUI(qt.QDialog):

    #init and expand on QDialog
    def __init__(self, parent=None):
        super(DashUI, self).__init__(parent=parent)

        self.setWindowFlags(qt.Qt.Popup|qt.Qt.FramelessWindowHint)

        pos = qt.QCursor.pos()
        self.setGeometry(pos.x()-pix(250), pos.y(), pix(250), pix(25))

        self.setAttribute(qt.Qt.WA_DeleteOnClose)

        #call layout code
        self.create_layout()

        #connect UI to commands
        self.create_connections()

        self.historyId = 0;

    #all layout code goes here
    def create_layout(self):
        #create widgets
        self.lineEdit = qt.QLineEdit()
        self.lineEdit.installEventFilter(self)

        #create layout
        main_layout = qt.QVBoxLayout()
        main_layout.setContentsMargins(pix(2),pix(2),pix(2),pix(2)) #spacing from window edges to widgets
        main_layout.setSpacing(pix(4)) #defalt spacing between iterface items

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
        if (event.type() == qt.QEvent.KeyPress and widget is self.lineEdit):
            global dashCommandHistory
            key = event.key()
            if key == qt.Qt.Key_Up:
                if len(dashCommandHistory) > 0:
                    self.historyId-=1
                    if abs(self.historyId) > len(dashCommandHistory):
                        self.historyId = 0-len(dashCommandHistory)
                    self.lineEdit.setText(dashCommandHistory[self.historyId])
            if key == qt.Qt.Key_Down:
                if len(dashCommandHistory) > 0:
                    self.historyId+=1
                    if self.historyId > 0:
                        self.historyId == 0
                        self.lineEdit.setText("")
                    else:
                        self.lineEdit.setText(dashCommandHistory[self.historyId])

        return qt.QWidget.eventFilter(self, widget, event)

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

    ui = DashUI(parent=fx.mayaWindow())
    ui.show()


# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
