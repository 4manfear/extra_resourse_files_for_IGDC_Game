from maya.app.flux.ae.Template import Template
from maya.app.flux.ae.Custom import Custom

from MASHsingleInputQtWidget import MASHsingleInputQtWidget
from MASHlistQtWidget import MASHlistQtWidget
import InViewMessageWrapper
import MASH.nodeHeaders

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

class AETemplate(Template):
    def buildUI(self, nodeName):
        #hide legacy, experimental controls
        self.suppress("forwardVector")
        self.suppress("voxelObjMatrix")
        self.suppress("initialStateMatrix")
        self.suppress("selectionSetMessage")
        self.suppress("waiterMessage")
        self.suppress("biasRampX")
        self.suppress("biasRampY")
        self.suppress("biasRampZ")
        self.suppress("inPositionPP")
        self.suppress("translateInPP")
        self.suppress("translateOutPP")
        self.suppress("inputMesh")
        self.suppress("scatterEvenly")
        self.suppress("strengthPP")
        self.suppress("stringOn")
        self.suppress("stringOff")
        self.suppress("radialOffset")
        self.suppress("inIterations")
        self.suppress("time")
        self.suppress("randomVertexPos")

        MASH.nodeHeaders.addHeader(nodeName, 'kDistribute')
        self.addCustom(MyCustom(nodeName))

         #TODO: replace with cmds.gradientControl(at="%s.biasRamp" % self.name)
        cmds.editorTemplate(beginLayout=mel.eval('getPluginResource("MASH", "kRamps")'))
        mel.eval('AEaddRampControl("%s.biasRamp");' % self.name)
        mel.eval('AEaddRampControl("%s.rotationRamp");' % self.name)
        mel.eval('AEaddRampControl("%s.scaleRamp");' % self.name)
        cmds.editorTemplate(endLayout=True)

        self.addCustom(EndCustom(nodeName))

class EndCustom(Custom):
    def buildUI(self, nodeName):
        self.pluginName = 'MASH'

        with self.frameLayout('kAdvanced'):
            self.addControl('batchRenderMultiplier', ann=self.getRes('kBatchMultAnn'))

    def getRes(self, name):
        return mel.eval('getPluginResource("MASH", "%s")' % name)

class MyCustom(Custom):
    def buildUI(self, nodeName):
        self.pluginName = 'MASH'

        self.createMASHControls()

        self.distButton = qt.QPushButton(self.getRes('kCreateContainer'))
        self.distButton.clicked.connect(self.distClicked)

        self.addControl('pointCount')
        self.addControl('arrangement')
        
        self.addSpacing(pix(5))

        with self.stackedLayout(ref='stacked'):

            with self.page():
                self.addControl('centerLinearDistribution')
                self.addControl('amplitudeX')
                self.addControl('amplitudeY')
                self.addControl('amplitudeZ')
                self.addControl('rotateX')
                self.addControl('rotateY')
                self.addControl('rotateZ')
                self.addControl('scaleX')
                self.addControl('scaleY')
                self.addControl('scaleZ')
                self.addControl('offset')

            with self.page():
                self.addControl('radialRadius')
                self.addControl('radialAngle')
                self.addControl('amplitudeZ')
                self.addControl('modelAxis')
                self.addControl('calcRotation')
                self.addControl('ignoreRamps')

            with self.page():
                self.addControl('sphericalAngleX')
                self.addControl('sphericalAngleY')
                self.addControl('radialRadius')
                self.addControl('noiseFrequency')
                self.addControl('animationTime')
                self.addControl('ignoreRamps')

            with self.page():
                self.addControl('meshType')
                self.addControl('distanceAlongNormal')
                self.addControl('useUpVector')
                self.addControl('upVector')

                with self.indentLayout('kInputMesh', autoStretch=False):
                    self.addWidget(self.distSingleInput1)

                with self.indentLayout('kSelectionSet', autoStretch=False):
                    self.addWidget(self.distSingleInput2)

                self.addControl('calcRotation')
                self.addControl('floodMesh')
                self.addControl('ignoreRamps')
                self.addControl('areaBasedScatter')

                with self.frameLayout('kFaceEdgeSettings'):
                    self.addControl('useFaceScale')
                    self.addControl('faceScaleMultiplier')
                    self.addControl('edgeAlignment')

                with self.frameLayout('kVoxelSettings'):
                    self.addControl('voxelDensity')
                    self.addControl('maxVoxels')
                    self.addControl('voxelMode')

                    with self.indentLayout('kVoxelContainer', autoStretch=False):
                        self.addWidget(self.voxelInputContainer)

                    with self.indentLayout(''):
                        self.addWidget(self.distButton)

            with self.page():
                self.addControl('centerLinearDistribution')
                self.addControl('gridAmplitudeX')
                self.addControl('gridAmplitudeY')
                self.addControl('gridAmplitudeZ')
                self.addControl('gridx')
                self.addControl('gridy')
                self.addControl('gridz')

            with self.page():
                self.addWidget(self.matrixList)

            with self.page():
                self.addControl('enableMain')
                self.addControl('enableLeaf')
                self.addControl('enableFlowers')
                self.addControl('floodMesh', controlKey='floodMesh2')
                self.addWidget(self.distributePfxList)
                self.addControl('useFaceScale', controlKey='useFaceScale2')
                self.addControl('enablePfxRotation')
                self.addControl('pfxMode')
            with self.page():
                self.addControl('volumeShape')
                self.addControl('volumeSize')
                self.addControl('sphericalBias')

        with self.frameLayout('kStrength'):
            self.addControl('strengthPosition')
            self.addControl('strengthRotation')
            self.addControl('strengthScale')
            self.addControl('zeroScale', ann=self.getRes('kZeroScaleAnn'))
            self.addControl('Envelope')
            self.addControl('randEnvelope')
            self.addControl('StepEnvelope')
            self.addControl('mColour')
            self.addControl('mapDirection')

            with self.indentLayout('kMapHelper', autoStretch=False):
                self.addWidget(self.mapHelper)

        self.addControl('seed')

        self.createAttributeListener('arrangement', self.arrangementChanged)
        self.createAttributeListener('meshType', self.meshTypeChanged)
        self.createAttributeListener('useUpVector', self.useUpVectorChanged)
        self.createAttributeListener('floodMesh', self.floodMeshChanged)
        self.createAttributeListener('volumeShape', self.volumeShapeChanged)

        self.runUIUpdates()

    def runUIUpdates(self):
        self.arrangementChanged()
        self.meshTypeChanged()
        self.useUpVectorChanged()
        self.floodMeshChanged()
        self.volumeShapeChanged()

    def volumeShapeChanged(self):
        value = cmds.getAttr(self.name + '.volumeShape')
        self.controlHandle('volumeSize').setEnabled(value in [2,3])
        self.controlHandle('sphericalBias').setEnabled(value == 3)

    def shouldEnablePointCount(self):
        arr = cmds.getAttr(self.name + '.arrangement')
        floodMesh = cmds.getAttr(self.name + '.floodMesh')
        meshType = cmds.getAttr(self.name + '.meshType')

        if arr not in (4,5,6):
            return True
        elif arr == 4:
            if not floodMesh and not meshType == 6:
                return True

        return False

    def floodMeshChanged(self):
        arr = cmds.getAttr(self.name + '.arrangement')
        floodMesh = cmds.getAttr(self.name + '.floodMesh')

        self.controlHandle('pointCount').setEnabled(self.shouldEnablePointCount())

    def useUpVectorChanged(self):
        useUpVector = cmds.getAttr(self.name + '.useUpVector')
        self.controlHandle('upVector').setEnabled(useUpVector)

    def meshTypeChanged(self):
        if cmds.getAttr(self.name + '.meshType') == 10:
            InViewMessageWrapper.MashInViewMessage(fx.res('kUVSpaceMode'),"Info")

        meshType = cmds.getAttr(self.name + '.meshType')
        #turn off flood mesh when not in vertex or face modes
        self.controlHandle('floodMesh').setEnabled(meshType not in (1,6))
        self.controlHandle('areaBasedScatter').setEnabled(meshType in (1, 10))
        self.controlHandle('useFaceScale').setEnabled(meshType in (4,5,8,9,7))
        self.controlHandle('faceScaleMultiplier').setEnabled(meshType in (4,5,8,9,7))

        #voxel specific settings
        self.controlHandle('voxelDensity').setEnabled(meshType == 6)

        #disabled specifically for voxel
        self.controlHandle('pointCount').setEnabled(self.shouldEnablePointCount())
        self.controlHandle('distanceAlongNormal').setEnabled(meshType != 6)
        self.controlHandle('calcRotation').setEnabled(meshType != 6)
        self.controlHandle('distanceAlongNormal').setEnabled(meshType not in (6,8,9))
        self.controlHandle('edgeAlignment').setEnabled(meshType in (8,9))

    def getRes(self, name):
        return mel.eval('getPluginResource("MASH", "%s")' % name)

    def arrangementChanged(self):
        arr = cmds.getAttr(self.name + '.arrangement')

        self.floodMeshChanged()

        if arr == 5:
            self.setLayoutHidden('stacked', True)
        else:
            #point count slider disabled for grid || flood mesh || inPostionsPP modes
            self.controlHandle('useFaceScale').setEnabled(arr == 4)
            self.controlHandle('useFaceScale2').setEnabled(arr == 8)
            self.controlHandle('floodMesh2').setEnabled(arr == 8)

            if arr == 4: # mesh
                self.meshTypeChanged()
                                
            if arr > 5:
                arr -= 1
            self.setLayoutHidden('stacked', False)
            self.setIndex('stacked', arr-1)

    def distClicked(self):
        mel.eval('source AEMASH_DistributeTemplate.mel')
        mel.eval('distButtonCMDS %s 2' % self.name)

    def createMASHControls(self):
        self.voxelInputContainer = MASHsingleInputQtWidget(self.name, 'mesh', 'voxelBoundingBox', 'worldMesh[0]', 'ConnectVoxelContainer')
        self.mapHelper = MASHsingleInputQtWidget(self.name, 'transform', 'inMapMatrix', 'worldMatrix[0]', 'MapSwitchToUVMode')
        self.distSingleInput1 = MASHsingleInputQtWidget(self.name, 'mesh', 'inputMesh', 'worldMesh', 'SwitchToMeshMode')
        self.distSingleInput2 = MASHsingleInputQtWidget(self.name, 'objectSet', 'selectionSetMessage', 'message', 'SwitchToVtxSetMode')
        self.matrixList = MASHlistQtWidget(self.name, 'transform', 'initialStateMatrix', 'worldMatrix[0]', 'SwitchToInitialState', 'kInitialTransforms')
        self.distributePfxList = MASHlistQtWidget(self.name, 'stroke', 'inPaintEffects', 'worldMainMesh[0]', 'SwitchToPfxMode', 'kPaintEffectsStrokes')

    def updateMASHControls(self):
        self.voxelInputContainer.set_node(self.name, 'mesh', 'voxelBoundingBox', 'worldMesh[0]', 'ConnectVoxelContainer')
        self.mapHelper.set_node(self.name, 'transform', 'inMapMatrix', 'worldMatrix[0]', 'MapSwitchToUVMode')
        self.distSingleInput1.set_node(self.name, 'mesh', 'inputMesh', 'worldMesh', 'SwitchToMeshMode')
        self.distSingleInput2.set_node(self.name, 'objectSet', 'selectionSetMessage', 'message', 'SwitchToVtxSetMode')
        self.matrixList.set_node(self.name, 'transform', 'initialStateMatrix', 'worldMatrix[0]', 'SwitchToInitialState', 'kInitialTransforms')
        self.distributePfxList.set_node(self.name, 'stroke', 'inPaintEffects', 'worldMainMesh[0]', 'SwitchToPfxMode', 'kPaintEffectsStrokes')

    def nodeChanged(self):
        self.updateMASHControls()
        self.runUIUpdates()
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
