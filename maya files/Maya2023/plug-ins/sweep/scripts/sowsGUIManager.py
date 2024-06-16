#-------------------------------------------------------------------------#
#   CREATED: 18 V 2019
#-------------------------------------------------------------------------#

from PySide2.QtGui import               QGuiApplication
from PySide2.QtWidgets import           QWidget
from shiboken2 import                   wrapInstance

from maya.OpenMayaUI import             MQtUtil
import maya.cmds as                     cmds

from sows import                        SOWS
from sowsCustomSweepProfile  import     SOWSCustomSweepProfile

#-------------------------------------------------------------------------#

g_sows = None

#-------------------------------------------------------------------------#

def getSOWS():
    global g_sows
    return g_sows

#-------------------------------------------------------------------------#

def cleanupSOWS(uuid=""):
    def deleteSOWS(sows):
        sows.isPendingDelete = True
        cmds.deleteUI(sows.objectName())
    
    global g_sows
    if g_sows is not None:
        # Delete specific
        if uuid:
            if uuid == g_sows.uuid:
                deleteSOWS(g_sows)
                g_sows = None

        # Delete general
        else:
            deleteSOWS(g_sows)
            g_sows = None

#-------------------------------------------------------------------------#

def createSOWS(uuid):
    cleanupSOWS()
    global g_sows
    g_sows = SOWS(uuid)
    showsSOWS()

#-------------------------------------------------------------------------#

def createCustomSweepProfile(uuid):
    cleanupSOWS()
    global g_sows
    g_sows = SOWSCustomSweepProfile(uuid)
    showsSOWS()

#-------------------------------------------------------------------------#

def showsSOWS():
    global g_sows
    if g_sows is not None:
        g_sows.show()
        adjustSOWSSize()
        adjustSOWSPosition()

#-------------------------------------------------------------------------#

def adjustSOWSSize():
    global g_sows
    if g_sows is not None:
        g_sows.resize(g_sows.minimumSizeHint())

#-------------------------------------------------------------------------#

def adjustSOWSPosition():
    global g_sows
    if g_sows is not None:
        isInScreens = False
        screens = QGuiApplication.screens()

        for screen in screens:
            if screen.geometry().intersects(g_sows.geometry()):
                isInScreens = True
                break

        if not isInScreens:
            mayaWindowPtr = MQtUtil.mainWindow()
            mayaWindow = wrapInstance(int(mayaWindowPtr), QWidget)
            mayaWindowCenter = mayaWindow.geometry().center()
            sowsGeometry = g_sows.geometry()

            x = mayaWindowCenter.x() - (sowsGeometry.width() / 2)
            y = mayaWindowCenter.y() - (sowsGeometry.height() / 2)
            g_sows.move(x, y)
