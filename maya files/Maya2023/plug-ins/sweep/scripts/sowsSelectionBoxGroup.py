#-------------------------------------------------------------------------#
#   CREATED: 26 IX 2018
#-------------------------------------------------------------------------#

from PySide2.QtGui import           QIcon

from PySide2.QtWidgets import       QHBoxLayout
from PySide2.QtWidgets import       QPushButton
from PySide2.QtWidgets import       QWidget
from PySide2.QtWidgets import       QSizePolicy

from maya.app.flux.core import      pix

from sowsSelectionBox import        SOWSSelectionBox

import sowsResources

#-------------------------------------------------------------------------#

class SOWSSelectionBoxGroup(QWidget):

    def __init__(self, parent=None):
        super(SOWSSelectionBoxGroup, self).__init__(parent=parent)

        self._setupUI()
        self._setupConnections()

    #-------------------------------------------------------------------------#

    def _setupUI(self):
        #-------------------------------------------------------------------------#
        #   UI NESTING
        #
        #   H BOX LAYOUT                                (mainLayout)
        #   ... SOWS SELECTION BOX                      (selectionBox)
        #   ... PUSH BUTTON                             (clearSelectionPushButton)
        #-------------------------------------------------------------------------#

        mainLayout = QHBoxLayout()
        mainLayout.setContentsMargins(0, 0, 0, 0)
        mainLayout.setSpacing(pix(4))
        self.setLayout(mainLayout)

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        self.selectionBox = SOWSSelectionBox()
        mainLayout.addWidget(self.selectionBox)

        self.clearSelectionPushButton = QPushButton(QIcon(":/sows/clearSelection.png"), "")
        self.clearSelectionPushButton.setObjectName("operationControlClearSelectionPushButton")
        self.clearSelectionPushButton.setFixedSize(pix(20), pix(21))
        self.clearSelectionPushButton.setVisible(False)
        mainLayout.addWidget(self.clearSelectionPushButton)

    #-------------------------------------------------------------------------#

    def _setupConnections(self):
        self.selectionBox.numberOfSelectedObjectsChanged.connect(self._displayClearSelectionPushButton)
        self.clearSelectionPushButton.clicked.connect(self.selectionBox.clearSelectedObjects)

    #-------------------------------------------------------------------------#

    def _displayClearSelectionPushButton(self, selectionBox):
        if selectionBox.numberOfSelectedObjects > 0:
            self.clearSelectionPushButton.setVisible(True)
        else:
            self.clearSelectionPushButton.setVisible(False)

