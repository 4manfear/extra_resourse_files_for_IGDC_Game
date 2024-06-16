#-------------------------------------------------------------------------#
#   CREATED: 01 X 2018
#-------------------------------------------------------------------------#

from PySide2.QtCore import              Qt
from PySide2.QtGui import               QIcon
from PySide2.QtWidgets import           QComboBox
from PySide2.QtWidgets import           QDialog
from PySide2.QtWidgets import           QGridLayout
from PySide2.QtWidgets import           QLabel
from PySide2.QtWidgets import           QSizePolicy

import maya.mel as                      mel

from maya.app.flux.core import          pix

from sows import                        SOWS
from sows import                        SOWSBackend
from sowsSelectionBox import            SOWSSelectionBox
from sowsSelectionBoxGroup import       SOWSSelectionBoxGroup

import sowsResources
import sowsUtils
import sweepUtils

#-------------------------------------------------------------------------#

class SOWSCustomSweepProfileBackend(SOWSBackend):

    def __init__(self, uuid):
        super(SOWSCustomSweepProfileBackend, self).__init__(uuid)

    def getType(self):
        type = mel.eval("$val = `sowsCustomSweepProfile_getType"
           + " -uuid \"" + self.uuid + "\"`")
        return type

    def performSelection(self):
        mel.eval("sowsCustomSweepProfile_performSelection"
           + " -uuid \"" + self.uuid + "\"")

    def buildSweepMesh(self, selectionBoxID):
        mel.eval("sowsCustomSweepProfile_buildSweepMesh"
           + " -selectionBoxID " + str(selectionBoxID)
           + " -uuid \"" + self.uuid + "\"")

#-------------------------------------------------------------------------#

class SOWSCustomSweepProfile(SOWS):

    TYPE = "sowsCustomSweepProfile"

    #-------------------------------------------------------------------------#

    def __init__(self, uuid, parent=None):
        super(SOWSCustomSweepProfile, self).__init__(uuid, parent=parent)
        self.setObjectName(SOWSCustomSweepProfile.TYPE)

        # Setup
        self._buildSweepMeshLock = True
        self.typeComboBox.setCurrentText(self.sowsBackend.getType())
        self._buildSweepMeshLock = False

        self.sowsBackend.performSelection()

    #-------------------------------------------------------------------------#

    def _setupBackendConnection(self):
        # Invoked from a base class
        self.sowsBackend = SOWSCustomSweepProfileBackend(self.uuid)

    #-------------------------------------------------------------------------#

    def _setupUI(self):
        # Invoked from a base class
        super(SOWSCustomSweepProfile, self)._setupUI()
        self.setWindowTitle(sweepUtils.getRes("kCustomSweepProfile"))

        #-------------------------------------------------------------------------#
        #   UI NESTING
        #
        #   GRID LAYOUT                                 (mainLayout)
        #   ... LABEL                                   (typeLabel)
        #   ... COMBO BOX                               (typeComboBox)
        #   ... LABEL                                   (profileLabel)
        #   ... SOWS SELECTION BOX GROUP                (selectionBoxGroup)
        #-------------------------------------------------------------------------#

        mainLayout = QGridLayout()
        mainLayout.setContentsMargins(pix(9), pix(8), pix(9), pix(8))
        mainLayout.setColumnMinimumWidth(0, pix(60))
        mainLayout.setColumnStretch(0, 0)
        mainLayout.setColumnStretch(pix(1), pix(1))
        mainLayout.setHorizontalSpacing(pix(2))
        mainLayout.setVerticalSpacing(pix(3))
        self.operationControlsWidget.setLayout(mainLayout)

        typeLabel = QLabel(sweepUtils.getRes("kType"))
        typeLabel.setObjectName("operationControlLabel")
        mainLayout.addWidget(typeLabel, 0, 0)

        self.typeComboBox = QComboBox()
        self.typeComboBox.setObjectName("operationControlComboBox")
        self.typeComboBox.setFixedHeight(pix(sowsUtils.operationControlHeight))
        self.typeComboBox.addItem(QIcon(":/sows/curveObject.png"), sweepUtils.getRes("kCurveObject"))
        self.typeComboBox.addItem(QIcon(":/sows/polyObject.png"), sweepUtils.getRes("kPolyObject"))
        self.typeComboBox.addItem(QIcon(":/sows/polyFace.png"), sweepUtils.getRes("kPolyFace"))
        self.typeComboBox.addItem(QIcon(":/sows/polyEdge.png"), sweepUtils.getRes("kPolyEdge"))
        self.typeComboBox.setFocusPolicy(Qt.ClickFocus) # otherwise global keyboard shortcuts are blocked
        mainLayout.addWidget(self.typeComboBox, 0, 1)

        profileLabel = QLabel(sweepUtils.getRes("kProfile"))
        profileLabel.setObjectName("operationControlLabel")
        mainLayout.addWidget(profileLabel, 1, 0)

        self.selectionBoxGroup = SOWSSelectionBoxGroup()
        self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.CURVE_OBJECT
        self.addSelectionBox(self.selectionBoxGroup.selectionBox)
        self.setActiveSelectionBox(self.selectionBoxGroup.selectionBox)
        mainLayout.addWidget(self.selectionBoxGroup, 1, 1)

    #-------------------------------------------------------------------------#

    def _setupConnections(self):
        # Invoked from a base class
        super(SOWSCustomSweepProfile, self)._setupConnections()

        self.typeComboBox.currentIndexChanged.connect(self._setSelectionBoxSelectionFilter)
        self.selectionBoxGroup.selectionBox.numberOfSelectedObjectsRefreshed.connect(self._buildSweepMesh)

    #-------------------------------------------------------------------------#

    def _setSelectionBoxSelectionFilter(self, index):
        self.selectionBoxGroup.selectionBox.clearSelectedObjects()

        if index == 0: self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.CURVE_OBJECT
        elif index == 1: self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.POLY_OBJECT
        elif index == 2: self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.POLY_FACE
        elif index == 3: self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.POLY_EDGE
        else: self.selectionBoxGroup.selectionBox.selectionFilter = SOWSSelectionBox.SelectionFilter.CURVE_OBJECT

    #-------------------------------------------------------------------------#

    def _buildSweepMesh(self, selectionBox):
        if self._buildSweepMeshLock:
            return

        self.sowsBackend.buildSweepMesh(selectionBox.id)

