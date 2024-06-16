#-------------------------------------------------------------------------#
#   CREATED: 14 IX 2018
#-------------------------------------------------------------------------#

from PySide2.QtCore import              QEvent
from PySide2.QtCore import              QObject
from PySide2.QtCore import              Qt
from PySide2.QtGui import               QPixmap
from PySide2.QtWidgets import           QDialog
from PySide2.QtWidgets import           QFrame
from PySide2.QtWidgets import           QHBoxLayout
from PySide2.QtWidgets import           QLabel
from PySide2.QtWidgets import           QPushButton
from PySide2.QtWidgets import           QSizePolicy
from PySide2.QtWidgets import           QSpacerItem
from PySide2.QtWidgets import           QVBoxLayout
from PySide2.QtWidgets import           QWidget
from shiboken2 import                   wrapInstance

from maya.OpenMaya import               MCommandMessage
from maya.OpenMaya import               MEventMessage
from maya.OpenMaya import               MMessage
from maya.OpenMayaUI import             MQtUtil

from maya.app.flux.core import          pix

import maya.mel as                      mel

from sowsSelectionBox import            SOWSSelectionBox
from sowsWidgetHandle import            SOWSWidgetHandle
from sowsWidgetHandleEvent import       SOWSWidgetHandleEvent

import sowsResources
import sweepUtils

#-------------------------------------------------------------------------#

class SOWSBackend(object):

    def __init__(self, uuid):
        self.uuid = uuid

    @staticmethod
    def setSelectionFilterForMaya(selectionFilter):
        mel.eval("sows_setSelectionFilterForMaya"
           + " -selectionFilter " + str(selectionFilter))

    def addSelectionBox(self, selectionBoxID, selectionFilter):
        mel.eval("sows_addSelectionBox"
           + " -selectionBoxID " + str(selectionBoxID)
           + " -selectionFilter " + str(selectionFilter)
           + " -uuid \"" + self.uuid + "\"")

    def setSelectionFilterForSelectionBox(self, selectionBoxID, selectionFilter):
        mel.eval("sows_setSelectionFilterForSelectionBox"
           + " -selectionBoxID " + str(selectionBoxID)
           + " -selectionFilter " + str(selectionFilter)
           + " -uuid \"" + self.uuid + "\"")

    def updateSelectionListForSelectionBox(self, selectionBoxID):
        numSelectedObjects = mel.eval("$val = `sows_updateSelectionListForSelectionBox"
           + " -selectionBoxID " + str(selectionBoxID)
           + " -uuid \"" + self.uuid + "\"`")
        try: return int(numSelectedObjects)
        except: return 0

    def clearSelectionListForSelectionBox(self, selectionBoxID):
        mel.eval("sows_clearSelectionListForSelectionBox"
           + " -selectionBoxID " + str(selectionBoxID)
           + " -uuid \"" + self.uuid + "\"")

#-------------------------------------------------------------------------#

class SOWSEventFilter(QObject):

    def __init__(self, sows, parent=None):
        super(SOWSEventFilter, self).__init__(parent=parent)
        self.sows = sows

    #-------------------------------------------------------------------------#

    def eventFilter(self, qobj, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.sows.accept()
                return True

            elif event.key() == Qt.Key_Escape:
                self.sows.reject()
                return True

        return super(SOWSEventFilter, self).eventFilter(qobj, event)

#-------------------------------------------------------------------------#

class SOWS(QDialog):

    TYPE = "sows"

    #-------------------------------------------------------------------------#

    def __init__(self, uuid, parent=None):
        super(SOWS, self).__init__(parent=parent)
        
        self.setObjectName(SOWS.TYPE)
        
        self.uuid = uuid
        self.isPendingDelete = False
        self._selectionBoxList = []

        # Parent to maya main window
        self._mayaWindow = wrapInstance(int(MQtUtil.mainWindow()), QWidget)
        self.setParent(self._mayaWindow)

        # Identify a Maya-managed floating window, which handles the z order properly
        self.setProperty("saveWindowPref", True)

        # Install event filter
        self._eventFilter = SOWSEventFilter(self)
        self._mayaWindow.installEventFilter(self._eventFilter)

        # Setup
        self._setupBackendConnection()
        self._setupUI()
        self._setupConnections()

    #-------------------------------------------------------------------------#

    def event(self, event):
        if event.type() == SOWSWidgetHandleEvent.eventType:
            self.move(self.pos().x() + event.deltaPosX, self.pos().y() + event.deltaPosY)
            return True

        elif event.type() == QEvent.WindowActivate:
            self.windowTitle.setStyleSheet("color: #eeeeee")
            return super(SOWS, self).event(event)

        elif event.type() == QEvent.WindowDeactivate:
            self.windowTitle.setStyleSheet("color: #aaaaaa")
            return super(SOWS, self).event(event)

        else:
            return super(SOWS, self).event(event)

    #-------------------------------------------------------------------------#

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.accept()
            return True

        elif event.key() == Qt.Key_Escape:
            self.reject()
            return True

        else:
            return super(SOWS, self).keyPressEvent(event)

    #-------------------------------------------------------------------------#

    def accept(self):
        if not self.isPendingDelete:
            mel.eval("acceptSOWS \"" + self.uuid + "\"")
        else:
            self.done(QDialog.Accepted)

    #-------------------------------------------------------------------------#

    def reject(self):
        if not self.isPendingDelete:
            mel.eval("rejectSOWS \"" + self.uuid + "\"")
        else:
            self.done(QDialog.Rejected)

    #-------------------------------------------------------------------------#

    def done(self, resultCode):
        super(SOWS, self).done(resultCode)
        MMessage.removeCallback(self.selectionChangedCallbackID)
        self._mayaWindow.removeEventFilter(self._eventFilter)

    #-------------------------------------------------------------------------#

    def deleteUI(self):
        self.done(QDialog.Rejected)
        self.deleteLater()

    #-------------------------------------------------------------------------#

    def setWindowTitle(self, title):
        super(SOWS, self).setWindowTitle(title)
        self.windowTitle.setText(title)

    #-------------------------------------------------------------------------#

    def addSelectionBox(self, selectionBox):
        if selectionBox not in self._selectionBoxList:
            self._selectionBoxList.append(selectionBox)
            self.sowsBackend.addSelectionBox(selectionBox.id, selectionBox.selectionFilter)

            selectionBox.activated.connect(self.setActiveSelectionBox)
            selectionBox.selectionFilterChanged.connect(self.setSelectionFilterForMaya)
            selectionBox.selectionFilterChanged.connect(self._setSelectionFilterForSelectionBox)
            selectionBox.numberOfSelectedObjectsChanged.connect(self._selectionBoxClearSelectedObjects)

            if len(self._selectionBoxList) == 1:
                self.setActiveSelectionBox(selectionBox)

    #-------------------------------------------------------------------------#

    def setActiveSelectionBox(self, selectionBox):
        if selectionBox not in self._selectionBoxList:
            self.addSelectionBox(selectionBox)

        if selectionBox.active:
            return

        # Deactivate previous selection boxes
        for selectionBox in self._selectionBoxList:
            selectionBox.active = False

        # Set active selection box
        selectionBox.active = True
        self.setSelectionFilterForMaya(selectionBox)

    #-------------------------------------------------------------------------#

    def setSelectionFilterForMaya(self, selectionBox):
        SOWSBackend.setSelectionFilterForMaya(selectionBox.selectionFilter)

    #-------------------------------------------------------------------------#

    def _setupBackendConnection(self):
        self.sowsBackend = SOWSBackend(self.uuid)

    #-------------------------------------------------------------------------#

    def _setupUI(self):
        borderWidth = 2
        borderColor = "#373737"

        self.setWindowFlags(Qt.Dialog | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint)
        self.setStyleSheet("""
            QDialog {{
                border: {0}px solid {1};
            }}

            .QFrame {{ 
                border: 1px solid {1};
            }}

            #operationControlLabel {{
                margin-right: 3px;
                qproperty-alignment: "AlignVCenter | AlignRight";
            }}

            #operationControlComboBox {{
                background-color: #2b2b2b;
            }}

            #operationControlClearSelectionPushButton {{ 
                border: 0;
                background-color: transparent;
            }}

            #operationControlClearSelectionPushButton:hover {{
                border-radius: 2px;
                background-color: #383838;
            }}

            #operationControlClearSelectionPushButton:pressed {{
                border-radius: 2px;
                background-color: #1d1d1d;
            }}
            """.format(borderWidth, borderColor)
        )

        #-------------------------------------------------------------------------#
        #   UI NESTING
        #
        #   V BOX LAYOUT                                (mainLayout)
        #   ... SOWS WIDGET HANDLE                      (widgetHandle)
        #   ....... H BOX LAYOUT                        (widgetHandleLayout)
        #   ........... LABEL                           (visualHandle)
        #   ........... LABEL                           (windowTitle)
        #   ... FRAME                                   (separator1)
        #   ... WIDGET                                  (operationControlsWidget)
        #       ...
        #   ... SPACER ITEM                             (spacerItem1)
        #   ... FRAME                                   (separator2)
        #   ... H BOX LAYOUT                            (buttonsLayout)
        #   ....... PUSH BUTTON                         (acceptButton)
        #   ....... PUSH BUTTON                         (rejectButton)
        #-------------------------------------------------------------------------#

        mainLayout = QVBoxLayout()
        mainLayout.setContentsMargins(borderWidth, borderWidth, borderWidth, borderWidth)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

        widgetHandle = SOWSWidgetHandle()
        widgetHandle.setFixedHeight(pix(24))
        mainLayout.addWidget(widgetHandle)

        widgetHandleLayout = QHBoxLayout()
        widgetHandleLayout.setContentsMargins(0, 0, 0, 0)
        widgetHandleLayout.setSpacing(0)
        widgetHandle.setLayout(widgetHandleLayout)

        visualHandle = QLabel()
        visualHandle.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        visualHandle.setContentsMargins(pix(2), 0, pix(7), 0)
        visualHandle.setPixmap(QPixmap(":/sows/sowsHandle.png"))
        widgetHandleLayout.addWidget(visualHandle)

        self.windowTitle = QLabel(sweepUtils.getRes("kSmallOperationWidgetSystem"))
        self.windowTitle.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.windowTitle.setContentsMargins(0, 0, 0, 0)
        widgetHandleLayout.addWidget(self.windowTitle)

        separator1 = QFrame()
        separator1.setFixedHeight(pix(1))
        mainLayout.addWidget(separator1)

        self.operationControlsWidget = QWidget()
        self.operationControlsWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        mainLayout.addWidget(self.operationControlsWidget, 100)

        spacerItem1 = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Fixed)
        mainLayout.addSpacerItem(spacerItem1)

        separator2 = QFrame()
        separator2.setFixedHeight(pix(1))
        mainLayout.addWidget(separator2)

        buttonsLayout = QHBoxLayout()
        buttonsLayout.setContentsMargins(pix(9), pix(8), pix(9), pix(8))
        buttonsLayout.setAlignment(Qt.AlignRight)
        buttonsLayout.setSpacing(5)
        mainLayout.addLayout(buttonsLayout)

        self.acceptButton = QPushButton(sweepUtils.getRes("kOK"))
        buttonsLayout.addWidget(self.acceptButton)

        self.rejectButton = QPushButton(sweepUtils.getRes("kCancel"))
        buttonsLayout.addWidget(self.rejectButton)

    #-------------------------------------------------------------------------#

    def _setupConnections(self):
        self.selectionChangedCallbackID = MEventMessage.addEventCallback(
            "SelectionChanged", self._mayaSelectionChanged)
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton.clicked.connect(self.reject)

    #-------------------------------------------------------------------------#

    def _mayaSelectionChanged(self, *args):
        for selectionBox in self._selectionBoxList:
            if selectionBox.active:
                selectionBox.numberOfSelectedObjects = self.sowsBackend.updateSelectionListForSelectionBox(selectionBox.getID())

    #-------------------------------------------------------------------------#

    def _setSelectionFilterForSelectionBox(self, selectionBox):
        self.sowsBackend.setSelectionFilterForSelectionBox(selectionBox.getID(), selectionBox.selectionFilter)

    #-------------------------------------------------------------------------#

    def _selectionBoxClearSelectedObjects(self, selectionBox):
        if selectionBox.numberOfSelectedObjects <= 0:
            self.sowsBackend.clearSelectionListForSelectionBox(selectionBox.getID())
