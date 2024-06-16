from maya.app.flux.ae.Template import Template
from maya.app.flux.ae.Custom import Custom

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import MASH.nodeHeaders
import mash_repro_aetemplate

class AETemplate(Template):
    def buildUI(self, nodeName):
        myCustom = MyCustom(nodeName)
        reproName = myCustom.getRes('kRepro')
        MASH.nodeHeaders.addHeader(nodeName, reproName, False)
        self.addCustom(myCustom)

class MyCustom(Custom):
    def buildUI(self, nodeName):
        self.pluginName = 'MASH'

        self.addControl('useGPU', label='kUseGPU', ann=self.getRes('kUseGPUAnnotation'))
        self.addControl('lod', label='kLod', ann=self.getRes('kLodAnnotation'))
        self.addControl('rotationOrder', label='kRotationOrder', ann=self.getRes('kRotationOrderAnnotation'))

        AEMASH_ReproCameraWidget(self.name)

        self.addSpacing(pix(2))
        self.reproWidget = mash_repro_aetemplate.AEMASH_ReproTemplate(self.name)
        self.addWidget(self.reproWidget)
        self.addSpacing(pix(2))

        self.addControl('motionBlurInstanceMode', label='kMotionBlurInstanceMode', ann=self.getRes('kMotionBlurInstanceModeAnnotation'))

        with self.frameLayout('kOutputAttributes'):
            self.addControl('setUVs', label='kUVs', ann=self.getRes('kUVsAnnotation'))
            self.addControl('setColors', label='kCPV', ann=self.getRes('kCPVAnnotation'))
            self.addControl('normalMode', label='kNormals', ann=self.getRes('kNormalsAnnotation'))

        with self.frameLayout('kRemapAttributes', False):
            self.addControl('positionAttributeName')
            self.addControl('rotationAttributeName')
            self.addControl('scaleAttributeName')
            self.addControl('objectIndexAttributeName')
            self.addControl('visibilityAttributeName')
            self.addControl('colorAttributeName')
            self.addControl('uvTileAttributeName')
            self.addControl('animatedAttributeName')
            self.addControl('frameAttributeName')

        self.addSpacing(pix(1))

    def nodeChanged(self):
        AEMASH_ReproCameraWidgetUpdate(self.name)
        self.reproWidget.update_data(self.name)

    def getRes(self, name):
        return res(name)

def res(name):
    return mel.eval('getPluginResource("MASH", "%s")' % name)

def AEMASH_ReproGetCameras(nodeName):
    cameras = []
    cameras.append('None')
    existCamera = cmds.ls(typ='camera') or []
    cameras += existCamera

    connections = cmds.listConnections(nodeName + '.cameraMatrix', s=True, p=True)
    if connections:
        newCameras = []
        cameraName = connections[0].split('.')[0]
        newCameras.append(cameraName)
        for i in cameras:
            if i != cameraName:
                newCameras.append(i)
        return newCameras
    else:
        return cameras

def AEMASH_ReproUpdateCamerasMenu(nodeName):
    menuItems = cmds.optionMenuGrp('reproCameraMenu', q=True, itemListLong=True)
    if menuItems:
        cmds.deleteUI(menuItems)
    cameras = AEMASH_ReproGetCameras(nodeName)
    for i in cameras:
        cmds.menuItem(label=i, p='reproCameraMenu|OptionMenu')

def AEMASH_ReproCameraChanged(nodeName):
    cameraName = cmds.optionMenu("reproCameraMenu|OptionMenu", q=True, v=True)
    if cmds.objExists(cameraName) and cmds.objectType(cameraName, i='camera'):
        cmds.connectAttr(cameraName + '.worldMatrix[0]', nodeName + '.cameraMatrix', f=True)
        mash_repro_aetemplate.refresh_camera_aetemplates(nodeName, cameraName)
    else:
        connections = cmds.listConnections(nodeName + '.cameraMatrix', s=True, p=True)
        if connections:
            cmds.disconnectAttr(connections[0], nodeName + '.cameraMatrix')
            mash_repro_aetemplate.refresh_camera_aetemplates(nodeName, '')

def AEMASH_ReproCameraWidget(attr):
    nodeName = attr.split('.')[0]
    parent = cmds.setParent(q=True)

    reproCameraMenu = cmds.optionMenuGrp("reproCameraMenu", label=res("kLODCamera"), annotation=res("kLODCameraAnnotation"));
    AEMASH_ReproCameraWidgetUpdate(attr)

def AEMASH_ReproCameraWidgetUpdate(attr):
    nodeName = attr.split('.')[0]

    cmds.optionMenu("reproCameraMenu|OptionMenu", e=True, beforeShowPopup=(lambda a, name=nodeName: AEMASH_ReproUpdateCamerasMenu(name)))
    cmds.optionMenu("reproCameraMenu|OptionMenu", e=True, cc=(lambda a, name=nodeName: AEMASH_ReproCameraChanged(name)))
    AEMASH_ReproUpdateCamerasMenu(nodeName)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
