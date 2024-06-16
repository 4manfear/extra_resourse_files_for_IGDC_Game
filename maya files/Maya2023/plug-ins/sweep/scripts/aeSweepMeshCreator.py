#-------------------------------------------------------------------------#
#   CREATED: 04 V 2020
#-------------------------------------------------------------------------#

from functools import partial

from maya.app.flux.ae.Custom import Custom
from maya.app.flux.ae.Template import Template

import maya.cmds as cmds
import maya.mel as mel


import sowsGUIManager
from sowsCustomSweepProfile import SOWSCustomSweepProfile
import sweepUtils as utils

#-------------------------------------------------------------------------#

class SweepProfileType:
    REGULAR_POLYGON = 0
    ROUNDED_RECTANGLE = 1
    LINE = 2
    ARC = 3
    WAVE = 4
    CUSTOM = 5

#-------------------------------------------------------------------------#

class AETemplate(Template):
    def buildUI(self, nodeName):
        self.addCustom(CustomAETemplate(nodeName))

#-------------------------------------------------------------------------#

class CustomAETemplate(Custom):
    imageBackgroundColorActive = (82.0/255.0, 82.0/255.0, 82.0/255.0)
    textBackgroundColorActive = (235.0/255.0, 154.0/255.0, 94.0/255.0)
    textBackgroundColorInactive = (56.0/255.0, 56.0/255.0, 56.0/255.0)

    #-------------------------------------------------------------------------#

    def buildUI(self, nodeName):
        self.pluginName = utils.pluginName

        with self.frameLayout("kSweepProfiles", expanded=True):
            self.sweepProfileTypeControlsLayoutMap = {}
            self._addSweepProfileTypeLayout()
            
            with self.verticalLayout():
                cmds.separator(vis=True, height=10, st="single", horizontal=True)

            with self.stackedLayout(ref="sweepProfileTypeControlsLayout"):
                i = -1

                with self.page():
                    i += 1
                    self.sweepProfileTypeControlsLayoutMap[SweepProfileType.REGULAR_POLYGON] = i

                    with self.verticalLayout():
                        self.profilePolyTypeControlID = cmds.radioButtonGrp(
                            label = utils.getRes("kType"),
                            numberOfRadioButtons = 2,
                            label1 = utils.getRes("kCircle"),
                            data1 = 0,
                            label2 = utils.getRes("kStar"),
                            data2 = 1
                        )
                        self.addControl("profilePolySides", label=utils.getRes("kSides"))

                        with self.verticalLayout(ref="profilePolyInnerRadiusLayout"):
                            self.addControl("profilePolyInnerRadius", label=utils.getRes("kInnerRadius"))

                        self.addControl("capsEnable", label=utils.getRes("kCap"))

                with self.page():
                    i += 1
                    self.sweepProfileTypeControlsLayoutMap[SweepProfileType.ROUNDED_RECTANGLE] = i

                    with self.verticalLayout():
                        self.addControl("profileRectWidth", label=utils.getRes("kWidth"))
                        self.addControl("profileRectHeight", label=utils.getRes("kHeight"))
                        self.addControl("profileRectCornerRadius", label=utils.getRes("kCornerRadius"))
                        self.addControl("profileRectCornerSegments", label=utils.getRes("kCornerSegments"))
                        self.addControl("profileRectCornerDepth", label=utils.getRes("kCornerDepth"))

                        self.addControl("capsEnable", label=utils.getRes("kCap"))

                with self.page():
                    i += 1
                    self.sweepProfileTypeControlsLayoutMap[SweepProfileType.ARC] = i

                    with self.verticalLayout():
                        self.addControl("profileArcAngle", label=utils.getRes("kAngle"))
                        self.addControl("profileArcSegments", label=utils.getRes("kSegments"))

                with self.page():
                    i += 1
                    self.sweepProfileTypeControlsLayoutMap[SweepProfileType.WAVE] = i

                    with self.verticalLayout():
                        self.addControl("profileWaveAmplitude", label=utils.getRes("kAmplitude"))
                        self.addControl("profileWaveCycles", label=utils.getRes("kCycles"))
                        self.addControl("profileWaveOffset", label=utils.getRes("kOffset"))
                        self.addControl("profileWaveSegments", label=utils.getRes("kSegments"))
                
                with self.page():
                    i += 1
                    self.sweepProfileTypeControlsLayoutMap[SweepProfileType.CUSTOM] = i

                    self.addControl("capsEnable", label=utils.getRes("kCap"))

            with self.frameLayout("kDistribution", expanded=False):
                self.addControl("patternEnable", label=utils.getRes("kDistribute"))

                with self.verticalLayout(ref="patternControlsLayout"):
                    self.addControl("patternDistribution", label=utils.getRes("kDistribution"))
                    self.addControl("patternNumberOfElements", label=utils.getRes("kNumberOfInstances"))

                    with self.stackedLayout(ref="patternScaleElementsControlsLayout"):
                        with self.page():
                            self.addControl("patternScaleElementsX", label=utils.getRes("kScaleInstancesX"))
                            self.addControl("patternScaleElementsY", label=utils.getRes("kScaleInstancesY"))

                        with self.page():
                            self.addControl("patternScaleElementsX", label=utils.getRes("kScaleInstances"))

                    self.addControl("patternRotateElements", label=utils.getRes("kRotateInstances"))
                    self.addControl("patternCoverage", label=utils.getRes("kCoverage"))

            with self.frameLayout("kAlignment", expanded=False):
                self.addControl("alignProfileEnable", label=utils.getRes("kAlign"))

                with self.verticalLayout(ref="alignmentControlsLayout"):
                    self.addControl("alignProfileHorizontal", label=utils.getRes("kHorizontal"))
                    self.addControl("alignProfileVertical", label=utils.getRes("kVertical"))
                    self.addControl("translateProfileX", label=utils.getRes("kHorizontalOffset"))
                    self.addControl("translateProfileY", label=utils.getRes("kVerticalOffset"))

        with self.frameLayout("kTransformation", expanded=True):
            with self.stackedLayout(ref="scaleProfileControlsLayout"):
                with self.page():
                    self.addControl("scaleProfileX", label=utils.getRes("kScaleProfileX"))
                    self.addControl("scaleProfileY", label=utils.getRes("kScaleProfileY"))

                with self.page():
                    self.addControl("scaleProfileX", label=utils.getRes("kScaleProfile"))

            self.addControl("rotateProfile")
            self.addControl("twist")
            self.addControl("taper")
            self._addTaperCurveLayout()

        with self.frameLayout("kInterpolation", expanded=True):
            self.addControl("interpolationMode", label=utils.getRes("kMode"))

            with self.stackedLayout(ref="interpolationControlsLayout"):
                with self.page(): # precision
                    self.addControl("interpolationPrecision", label=utils.getRes("kPrecision"))
                with self.page(): # start to end
                    self.addControl("interpolationSteps", label=utils.getRes("kSteps"))
                with self.page(): # ep to ep
                    self.addControl("interpolationSteps", label=utils.getRes("kSteps"))
                with self.page(): # distance
                    self.addControl("interpolationDistance", label=utils.getRes("kDistance"))

            self.addControl("interpolationOptimize", label=utils.getRes("kOptimize"))

        with self.frameLayout("kNormals", expanded=False):
            self.addControl("normalsSmoothing", label=utils.getRes("kSmoothing"))
            self.addControl("normalsReverse", label=utils.getRes("kReverse"))

        with self.frameLayout("kUV", expanded=False):
            self.addControl("createUVs")

        with self.frameLayout("kSettings", expanded=False):
            self.addControl("automaticRoll", label=utils.getRes("kAutomaticRoll"))
            self.addControl("scaleProfileUniform", label=utils.getRes("kProfileUniformScale"))
            self.addControl("patternScaleElementsUniform", label=utils.getRes("kPatternElementsUniformScale"))
            self.addControl("patternAutomaticOrientation", label=utils.getRes("kPatternElementsAutomaticOrientation"))

        self.createAttributeListener("sweepProfileType", self._updateSweepProfileTypeControls)
        self.createAttributeListener("profilePolyType", self._updateProfilePolyControls)
        self.createAttributeListener("patternEnable", self._updatePatternControls)
        self.createAttributeListener("alignProfileEnable", self._updateAlignmentControls)
        self.createAttributeListener("interpolationMode", self._updateInterpolationControls)
        self.createAttributeListener("scaleProfileUniform", self._updateTransformationsControls)
        self.createAttributeListener("patternScaleElementsUniform", self._updatePatternControls)

        self.connectControls()
        self.updateControls()

    #-------------------------------------------------------------------------#

    def nodeChanged(self):
        self.connectControls()
        self.updateControls()

    #-------------------------------------------------------------------------#

    def connectControls(self):
        for (key, value) in self.sweepProfileTypeButtonsMap.items():
            cmds.symbolButton(
                value[0], 
                edit = True,
                command = partial(self._setSweepProfileType, key)
            )

        cmds.connectControl(self.profilePolyTypeControlID, self.name + ".profilePolyType")

        cmds.gradientControl(
            self.taperCurveControlID,
            edit = True,
            attribute = "{0}.taperCurve".format(self.name),
            selectedColorControl = self.taperCurveValueControlID,
            selectedPositionControl = self.taperCurvePositionControlID,
            selectedInterpControl = self.taperCurveInterpolationControlID
        )

    #-------------------------------------------------------------------------#

    def updateControls(self):
        self._updateSweepProfileTypeControls()
        self._updateProfilePolyControls()
        self._updatePatternControls()
        self._updateAlignmentControls()
        self._updateTransformationsControls()
        self._updateInterpolationControls()
    
    #-------------------------------------------------------------------------#

    def _addSweepProfileTypeLayout(self):
        self.sweepProfileTypeButtonsMap = {}

        imageSize = 58
        textRowHeight = 20

        flowLayoutID = cmds.flowLayout(height=75, wrap=True)

        modes = [
            { 'label':'kPoly',     'image':'ae_polySweepProfile.png',  'id':SweepProfileType.REGULAR_POLYGON },
            { 'label':'kRectangle','image':'ae_rectSweepProfile.png',  'id':SweepProfileType.ROUNDED_RECTANGLE },
            { 'label':'kLine',     'image':'ae_lineSweepProfile.png',  'id':SweepProfileType.LINE },
            { 'label':'kArc',      'image':'ae_arcSweepProfile.png',   'id':SweepProfileType.ARC },
            { 'label':'kWave',     'image':'ae_waveSweepProfile.png',  'id':SweepProfileType.WAVE },
            { 'label':'kCustom',   'image':'ae_customSweepProfile.png','id':SweepProfileType.CUSTOM }
        ]

        for m in modes:
            cmds.setParent(flowLayoutID)
            cmds.rowColumnLayout(
                numberOfRows = 2,
                rowHeight = [(1, imageSize), (2, textRowHeight)]
            )
            buttonID = cmds.symbolButton(
                width = imageSize,
                height = imageSize,
                image = m['image']
            )
            textID = cmds.text(
                label = utils.getRes(m['label']),
                font = "tinyBoldLabelFont",
                backgroundColor = self.textBackgroundColorInactive,
                height = textRowHeight
            )
            self.sweepProfileTypeButtonsMap[m['id']] = (buttonID, textID)

    #-------------------------------------------------------------------------#

    def _addTaperCurveLayout(self):
        with self.frameLayout("kTaperCurve", expanded=False):       
            cmds.rowColumnLayout(
                numberOfColumns = 2,
                adjustableColumn = 1
            )
            self.taperCurveControlID = cmds.gradientControl()
            self.taperCurveButtonControlID = cmds.button(
                label = ">",
                width = 23,
                command = lambda i : mel.eval("editRampAttribute " + self.name + ".taperCurve")
            )
            cmds.setParent("..")

            self.taperCurveValueControlID = cmds.attrFieldSliderGrp(label=utils.getRes("kValue"), minValue=0.0, maxValue=1.0)
            self.taperCurvePositionControlID = cmds.attrFieldSliderGrp(label=utils.getRes("kPosition"), minValue=0.0, maxValue=1.0)
            self.taperCurveInterpolationControlID = cmds.attrEnumOptionMenuGrp(label=utils.getRes("kInterpolation"))
    
    #-------------------------------------------------------------------------#

    def _updateSweepProfileTypeControls(self, *args):
        sweepProfileType = cmds.getAttr(self.name + ".sweepProfileType")
        
        # reset sweep profile types buttons
        for (key, value) in self.sweepProfileTypeButtonsMap.items():
            cmds.symbolButton(
                value[0], 
                edit = True,
                enableBackground = False
            )
            cmds.text(
                value[1],
                edit = True,
                backgroundColor = self.textBackgroundColorInactive,
                highlightColor = (255.0/255.0, 255.0/255.0, 255.0/255.0)
            )

        # highlight active sweep profile type button
        (buttonID, textID) = self.sweepProfileTypeButtonsMap[sweepProfileType]
        cmds.symbolButton(
            buttonID,
            edit = True,
            enableBackground = True,
            backgroundColor = self.imageBackgroundColorActive
        )
        cmds.text(
            textID,
            edit = True,
            backgroundColor = self.textBackgroundColorActive,
            highlightColor = (255.0/255.0, 56.0/255.0, 56.0/255.0)  
        )

        # update sweep profile type controls stacked layout
        if sweepProfileType in self.sweepProfileTypeControlsLayoutMap:
            self.setLayoutHidden("sweepProfileTypeControlsLayout", False)
            self.setIndex("sweepProfileTypeControlsLayout", self.sweepProfileTypeControlsLayoutMap[sweepProfileType])
        else:
            self.setLayoutHidden("sweepProfileTypeControlsLayout", True)

    #-------------------------------------------------------------------------#

    def _updateProfilePolyControls(self, *args):
        polyType = cmds.getAttr(self.name + ".profilePolyType")
        if polyType == 0:
            self.setLayoutHidden('profilePolyInnerRadiusLayout', True)
        else:
            self.setLayoutHidden('profilePolyInnerRadiusLayout', False)

    #-------------------------------------------------------------------------#

    def _updatePatternControls(self, *args):
        isPatternEnabled = cmds.getAttr(self.name + ".patternEnable")
        self.setLayoutHidden('patternControlsLayout', not isPatternEnabled)

        patternScaleElementsUniform = cmds.getAttr(self.name + ".patternScaleElementsUniform")
        self.setIndex("patternScaleElementsControlsLayout", patternScaleElementsUniform)

    #-------------------------------------------------------------------------#

    def _updateAlignmentControls(self, *args):
        isAlignProfileEnabled = cmds.getAttr(self.name + ".alignProfileEnable")
        self.setLayoutHidden('alignmentControlsLayout', not isAlignProfileEnabled)

    #-------------------------------------------------------------------------#

    def _updateTransformationsControls(self, *args):
        scaleProfileUniform = cmds.getAttr(self.name + ".scaleProfileUniform")
        self.setIndex("scaleProfileControlsLayout", scaleProfileUniform)

    #-------------------------------------------------------------------------#

    def _updateInterpolationControls(self, *args):
        interpolationMode = cmds.getAttr(self.name + ".interpolationMode")
        self.setIndex("interpolationControlsLayout", interpolationMode)

    #-------------------------------------------------------------------------#

    def _setSweepProfileType(self, sweepProfileType, *args):
        attributePath = self.name + ".sweepProfileType"
        previousSweepProfileType = cmds.getAttr(attributePath)

        # execute when SOWSCustomSweepProfile is not instantiated
        sows = sowsGUIManager.getSOWS()
        if not isinstance(sows, SOWSCustomSweepProfile):
            cmds.setAttr(attributePath, sweepProfileType)
            self._updateSweepProfileTypeControls()

        # create SOWSCustomSweepProfile
        if sweepProfileType == SweepProfileType.CUSTOM:
            if sows is None:
                mel.eval("createSOWS"
                    + " -type \"" + SOWSCustomSweepProfile.TYPE + "\""
                    + " -a \"" + self.name + "\""
                    + " -a " + str(previousSweepProfileType)
                )
            else:
                if not isinstance(sows, SOWSCustomSweepProfile):
                    mel.eval("rejectSOWS -uuid \"" + sows.uuid + "\"")
                    mel.eval("createSOWS"
                        + " -type \"" + SOWSCustomSweepProfile.TYPE + "\""
                        + " -a \"" + self.name + "\""
                        + " -a " + str(previousSweepProfileType)
                    )

