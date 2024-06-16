#-------------------------------------------------------------------------#
#   CREATED: 16 IX 2018
#-------------------------------------------------------------------------#

from PySide2.QtCore import QEvent

#-------------------------------------------------------------------------#

class SOWSWidgetHandleEvent(QEvent):

    eventType = QEvent.Type(QEvent.registerEventType())

    #-------------------------------------------------------------------------#

    def __init__(self):
        super(SOWSWidgetHandleEvent, self).__init__(SOWSWidgetHandleEvent.eventType)

        self.deltaPosX = 0
        self.deltaPosY = 0
