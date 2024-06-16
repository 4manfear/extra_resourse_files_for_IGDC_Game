#-------------------------------------------------------------------------#
#   CREATED: 26 IX 2018
#-------------------------------------------------------------------------#

from PySide2.QtCore import      Signal
from PySide2.QtCore import      Qt

from PySide2.QtGui import       QBrush
from PySide2.QtGui import       QColor
from PySide2.QtGui import       QFontMetrics
from PySide2.QtGui import       QPainter
from PySide2.QtGui import       QPen
from PySide2.QtGui import       QPixmap

from PySide2.QtWidgets import   QLabel
from PySide2.QtWidgets import   QWidget

from maya.app.flux.core import  pix

import sowsResources
import sowsUtils
import sweepUtils

#-------------------------------------------------------------------------#

class SOWSSelectionBox(QLabel):

    class SelectionFilter:
        POLY_OBJECT =   0
        POLY_VERTEX =   1
        POLY_EDGE =     2
        POLY_FACE =     3
        CURVE_OBJECT =  4

    #-------------------------------------------------------------------------#
    
    # Signals
    activated = Signal(QWidget)
    selectionFilterChanged = Signal(QWidget)
    numberOfSelectedObjectsRefreshed = Signal(QWidget)
    numberOfSelectedObjectsChanged = Signal(QWidget)

    # Other
    id = 0

    #-------------------------------------------------------------------------#

    def __init__(self, parent=None):
        super(SOWSSelectionBox, self).__init__(parent=parent)

        SOWSSelectionBox.id += 1

        self._id = SOWSSelectionBox.id
        self._active = False
        self._selectionFilter = SOWSSelectionBox.SelectionFilter.POLY_OBJECT
        self._numberOfSelectedObjects = 0

        self.setFocusPolicy(Qt.ClickFocus)
        self.setFixedHeight(pix(sowsUtils.operationControlHeight))
        self.setText(sweepUtils.getRes("kSelect"))

    #-------------------------------------------------------------------------#

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, value):
        self._active = value

    #-------------------------------------------------------------------------#

    @property
    def selectionFilter(self):
        return self._selectionFilter

    @selectionFilter.setter
    def selectionFilter(self, value):
        self._selectionFilter = value
        self.selectionFilterChanged.emit(self)

    #-------------------------------------------------------------------------#

    @property
    def numberOfSelectedObjects(self):
        return self._numberOfSelectedObjects

    @numberOfSelectedObjects.setter
    def numberOfSelectedObjects(self, value):
        if value < 0:
            value = 0

        previousValue = self._numberOfSelectedObjects
        self._numberOfSelectedObjects = value

        if self._numberOfSelectedObjects == 0:
            self.setText(sweepUtils.getRes("kSelect"))
        else:
            self.setText(str(self._numberOfSelectedObjects) + " " + sweepUtils.getRes("kSelected"))

        if previousValue != value:
            self.numberOfSelectedObjectsChanged.emit(self)

        self.numberOfSelectedObjectsRefreshed.emit(self)

    #-------------------------------------------------------------------------#

    def mousePressEvent(self, mouseEvent):
        self.activated.emit(self)
        QLabel.mousePressEvent(self, mouseEvent)

    #-------------------------------------------------------------------------#

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        paintArea = paintEvent.rect()
        x = paintArea.x()
        y = paintArea.y()
        width = paintArea.width()
        height = paintArea.height()

        # Background
        if self._active:
            painter.setPen(QPen(QColor.fromRgb(0x5aabe0)))
            painter.setBrush(QBrush(QColor.fromRgb(0x2b2b2b)))
            painter.drawRoundedRect(x + pix(3), y + pix(1), width - pix(4), height - pix(2), pix(2), pix(2))
        else:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QBrush(QColor.fromRgb(0x2b2b2b)))
            painter.drawRoundedRect(x + pix(3), y + pix(1), width - pix(4), height - pix(2), pix(2), pix(2))

        # Icon
        selectIcon = QPixmap(":/sows/select.png")
        painter.drawPixmap(pix(10), int(height / 2) - int(selectIcon.height() / 2) + 1, selectIcon)

        # Text 
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(pix(25), int(height / 2) + int(painter.fontMetrics().ascent() / 2), self.text())

    #-------------------------------------------------------------------------#

    def getID(self):
        return self._id

    #-------------------------------------------------------------------------#

    def clearSelectedObjects(self):
        self.numberOfSelectedObjects = 0
