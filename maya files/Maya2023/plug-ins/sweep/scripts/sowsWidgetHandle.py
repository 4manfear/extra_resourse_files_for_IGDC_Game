#-------------------------------------------------------------------------#
#   CREATED: 15 IX 2018
#   NOTES:
#       SOWSWidgetHandle widget allows user to grab SOWS floating dialog
#       and reposition it. It was made because SOWS dialogs are frameless.
#-------------------------------------------------------------------------#

from PySide2.QtCore import          QCoreApplication
from PySide2.QtCore import          QEvent
from PySide2.QtCore import          Qt
from PySide2.QtWidgets import       QWidget

from sowsWidgetHandleEvent import   SOWSWidgetHandleEvent

#-------------------------------------------------------------------------#

class SOWSWidgetHandle(QWidget):

    def __init__(self, parent=None):
        super(SOWSWidgetHandle, self).__init__(parent=parent)

        self.isLeftMouseButtonPressed = False
        self.mousePosX = 0
        self.mousePosY = 0

    #-------------------------------------------------------------------------#

    def mousePressEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            self.isLeftMouseButtonPressed = True
            self.mousePosX = mouseEvent.globalX()
            self.mousePosY = mouseEvent.globalY()
        else:
            super(SOWSWidgetHandle, self).mousePressEvent(mouseEvent)

    #-------------------------------------------------------------------------#

    def mouseReleaseEvent(self, mouseEvent):
        if mouseEvent.button() == Qt.MouseButton.LeftButton:
            self.isLeftMouseButtonPressed = False
        else:
            super(SOWSWidgetHandle, self).mouseReleaseEvent(mouseEvent)

    #-------------------------------------------------------------------------#

    def mouseMoveEvent(self, mouseEvent):
        if self.isLeftMouseButtonPressed:
            widgetHandleEvent = SOWSWidgetHandleEvent()
            widgetHandleEvent.deltaPosX = mouseEvent.globalX() - self.mousePosX
            widgetHandleEvent.deltaPosY = mouseEvent.globalY() - self.mousePosY

            self.mousePosX = mouseEvent.globalX()
            self.mousePosY = mouseEvent.globalY()

            QCoreApplication.sendEvent(self.parent(), widgetHandleEvent)

        else:
            super(SOWSWidgetHandle, self).mouseMoveEvent(mouseEvent)

