'''
Command = snapTransform(flags)

EXAMPLES:

import maya.cmds
maya.cmds.loadPlugin('snapTransform')

# Match cube1 to cube2 while reparenting to locator1
maya.cmds.snapTransform('cube1', p='locator1', m='cube2')

# Match cube1 to cube2 while reparenting to locator1, without changing the rotation
maya.cmds.snapTransform('cube1', p='locator1', m='cube2', rot=False)

# Match cube1 and cube3 to cube2
maya.cmds.snapTransform(['cube1', 'cube3'], m='cube2')

# Match cube1 to cube2 while reparenting to locator1 over the range 30-60:5
maya.cmds.snapTransform(['cube1'], p='locator1', m='cube2', fr='30-60:5.0')

# Match cube1 to cube3 while reparenting to cube2 over the range 36-50:3
maya.cmds.snapTransform(['cube1'],  p='cube2', m='cube3', fr='36-50:3')

'''

import maya.api.OpenMaya as om
import maya.cmds
import maya.internal.common.utils.transform as xfm_utils
import maya.internal.common.utils.ui as ui_utils
import maya.internal.common.utils.time as time_utils
import sys

kParentFlag = ('-p', '-parent')
kMatchFlag = ('-m', '-match')
kPreserveOffsetParentFlag = ('-pop', '-preserveOffsetParent')
kPreservePivotFlag = ('-ppv', '-preservePivot')
kFrangeFlag = ('-fr', '-frange')
kUseScaleFlag = ('-sca', '-useScale')
kUseShearFlag = ('-she', '-useShear')
kUseRotateFlag = ('-rot', '-useRotate')
kUseTranslateFlag = ('-tra', '-useTranslate')
kVerboseFlag = ('-vb', '-verbose')

#-------------------------------------------------------------------------------
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass

#-------------------------------------------------------------------------------
# The command class
#-------------------------------------------------------------------------------
class snapTransformCmd(om.MPxCommand):

    kPluginCmdName = 'snapTransform'
    kPluginVersion = '1.0'

    def __init__(self):
        om.MPxCommand.__init__(self)
        self._clear()

    def _clear(self):
        # setup private data members
        self._startFrame = None
        self._endFrame = None
        self._stepFrame = 1
        self._singleFrame = True

        self._preserveOffsetParent = True
        self._preservePivot = True

        self._useScale = True
        self._useShear = True
        self._useRotate = True
        self._useTranslate = True

        self._dpSrcList = list()
        self._dpTrg = om.MDagPath()
        self._dpRel = om.MDagPath()

        self._resultAttrs = list()
        self._verbose = False

    # Create an instance of the command
    @staticmethod
    def cmdCreator():
        return snapTransformCmd()

    # Make the command undoable
    def isUndoable(self):
        return True

    # Syntax creator : Builds the argument strings up for the command
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addFlag(kParentFlag[0], kParentFlag[1], om.MSyntax.kString)
        syntax.addFlag(kMatchFlag[0], kMatchFlag[1], om.MSyntax.kString)
        syntax.addFlag(kPreserveOffsetParentFlag[0], kPreserveOffsetParentFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kPreservePivotFlag[0], kPreservePivotFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kFrangeFlag[0], kFrangeFlag[1], om.MSyntax.kString)
        syntax.addFlag(kUseScaleFlag[0], kUseScaleFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kUseShearFlag[0], kUseShearFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kUseRotateFlag[0], kUseRotateFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kUseTranslateFlag[0], kUseTranslateFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kVerboseFlag[0], kVerboseFlag[1], om.MSyntax.kNoArg)

        syntax.setObjectType(syntax.kSelectionList)
        syntax.setMinObjects(0)
        syntax.useSelectionAsDefault(True)
        syntax.enableQuery = False
        syntax.enableEdit = False

        return syntax

    def _parseFlags(self, args):
        argData = om.MArgDatabase(self.syntax(), args)

        if argData.isFlagSet(kVerboseFlag[0]):
            self._verbose = True

        # Get the objects specified on the command line.
        slist = argData.getObjectList()
        for i in range(0, slist.length()):
            self._dpSrcList.append(slist.getDagPath(i))

        if argData.isFlagSet(kMatchFlag[0]):
            matchName = argData.flagArgumentString(kMatchFlag[0], 0)
            self._dpTrg = xfm_utils.getDagPathFromNodeName(matchName)
            if self._dpTrg is None:
                maya.cmds.error(u'Unable to find match object \"{}\"'.format(matchName))
                return False

        if argData.isFlagSet(kParentFlag[0]):
            parentName = argData.flagArgumentString(kParentFlag[0], 0)
            self._dpRel = xfm_utils.getDagPathFromNodeName(parentName)
            if self._dpRel is None:
                maya.cmds.error(u'Unable to find parent object \"{}\"'.format(parentName))
                return False

        if argData.isFlagSet(kFrangeFlag[0]):
            frangeSpec = argData.flagArgumentString(kFrangeFlag[0], 0)
            fr = time_utils.parseFloatRangeSpec(frangeSpec)
            if fr is None:
                maya.cmds.error(u'Invalid frame range specification \"{}\"'.format(frangeSpec))
                return False

            self._startFrame = fr[0]
            self._endFrame = fr[1]
            self._stepFrame = fr[2]

        # Use flags
        if argData.isFlagSet(kUseScaleFlag[0]):
            self._useScale = argData.flagArgumentBool(kUseScaleFlag[0], 0)
        if argData.isFlagSet(kUseShearFlag[0]):
            self._useShear = argData.flagArgumentBool(kUseShearFlag[0], 0)
        if argData.isFlagSet(kUseRotateFlag[0]):
            self._useRotate = argData.flagArgumentBool(kUseRotateFlag[0], 0)
        if argData.isFlagSet(kUseTranslateFlag[0]):
            self._useTranslate = argData.flagArgumentBool(kUseTranslateFlag[0], 0)

        # Preserve flags
        if argData.isFlagSet(kPreserveOffsetParentFlag[0]):
            self._preserveOffsetParent = argData.flagArgumentBool(kPreserveOffsetParentFlag[0], 0)
        if argData.isFlagSet(kPreservePivotFlag[0]):
            self._preservePivot = argData.flagArgumentBool(kPreservePivotFlag[0], 0)

        if self._startFrame is not None:
            self._singleFrame = False
            if self._endFrame is None:
                self._endFrame = int(maya.cmds.playbackOptions(q=True, aet=True))

        return True

    def doIt(self, args):
        # Check if all the flags can be parsed correctly
        if not self._parseFlags(args):
            maya.cmds.error('Failed to parse the arguments of the {} command: See script editor for details'.format(snapTransformCmd.kPluginCmdName))
            return

        # Check if we want to reparent to a child, because that is not allowed
        if self._dpRel != om.MDagPath():
            for dpSrc in self._dpSrcList:
                if xfm_utils.isChild(dpSrc.partialPathName(), self._dpRel.partialPathName()):
                    maya.cmds.error('Can not reparent {} to a child {}'.format(dpSrc.partialPathName(), self._dpRel.partialPathName()))
                    return

        # Check if any of the nodes we want to move is referenced or has locked attributes
        attrs = xfm_utils.getTransformAttributes(useScale=self._useScale,
                                                useShear=self._useShear,
                                                useRotate=self._useRotate,
                                                useTranslate=self._useTranslate)

        for dpSrc in self._dpSrcList:
            nodeName = dpSrc.partialPathName()
            if maya.cmds.referenceQuery(nodeName, isNodeReferenced=True):
                maya.cmds.error('Can not move references object {}'.format(nodeName))
                return

            for a in attrs:
                if not maya.cmds.getAttr('{}.{}'.format(nodeName, a), settable=True):
                    maya.cmds.error('Attribute {}.{} is not settable'.format(nodeName, a))
                    return

        # Now go do the actual work
        self.redoIt()

    def undoIt(self):
        pass

    def _collectDpSets(self):
        """
        Collect the operation sets as a list of triples that contain the dagPaths of:
            - the source object we want to move (dpSrc),
            - the target object we want to match (dpTrg),
            - the relative object we want our source to become relative to (dpRel)
        """
        self._dpSets = list()
        for dpSrc in self._dpSrcList:
            # If we did not specify a target we are our own target
            dpTrg = self._dpTrg if self._dpTrg != om.MDagPath() else dpSrc
            dpRel = self._dpRel
            self._dpSets.append( (dpSrc, dpTrg, dpRel) )

    def _captureTransforms(self):
        """
        For each operation set calculate the required transform for the source
        object to match the target object
        """
        xforms = list()
        for dpSet in self._dpSets:
            dpSrc, dpTrg, dpRel = dpSet
            xfo = om.MDagPath.matchTransform(dpSrc, dpTrg, dpRel, preserveOffsetParentMatrix=self._preserveOffsetParent, preservePivot=self._preservePivot)
            xforms.append(xfo)
        return xforms

    def _postApply(self):
        """
        After we have set all the attribute values or keyframes finish up by
        altering the parent and or initialing the offsetParentMatrix
        """
        self._resultAttrs = list()

        attrs = xfm_utils.getTransformAttributes(useScale=self._useScale,
                                                 useShear=self._useShear,
                                                 useRotate=self._useRotate,
                                                 useTranslate=self._useTranslate)

        for dpSet in self._dpSets:
            dpSrc, _dpTrg, dpRel = dpSet

            if not self._preserveOffsetParent:
                xfm_utils.initializeOffsetParentMatrix(dpSrc.partialPathName())

            if dpRel != om.MDagPath():
                curParent = xfm_utils.getParent(dpSrc.partialPathName())
                if curParent != dpRel.partialPathName():
                    maya.cmds.parent(dpSrc.partialPathName(), dpRel.partialPathName(), relative=True)

            nodeName = dpSrc.partialPathName()
            for a in attrs:
                self._resultAttrs.append(u'{}.{}'.format(nodeName, a))

    def redoIt(self):
        try:
            self.clearResult()
            self._collectDpSets()

            saveFrame = maya.cmds.currentTime(q=True)

            if self._singleFrame:
                # Doing just a single frame (the current frame)
                xforms = self._captureTransforms()

                for dpSet, xfo in zip(self._dpSets, xforms):
                    xfm_utils.setTransformAttributesOrKeyframes(dpSet[0].partialPathName(), xfo,
                                    frame=None,
                                    setScale=self._useScale,
                                    setShear=self._useShear,
                                    setRotate=self._useRotate,
                                    setTranslate=self._useTranslate,
                                    setPivot=True)

                self._postApply()

            else:
                # Loop over the specified frame range
                numFrames = ((self._endFrame+1) - self._startFrame)/self._stepFrame
                mainProgressBar = ui_utils.getMainProgressBar()

                if mainProgressBar:
                    maya.cmds.progressBar(mainProgressBar, edit=True, beginProgress=True,
                        isInterruptable=True, minValue=0, maxValue=numFrames,
                        status='Capturing transform over frame range...')

                cancelledOperation = False
                captured = dict()
                statusRange = '{}-{}:{}'.format('%g'%self._startFrame, '%g'%self._endFrame, '%g'%self._stepFrame)
                for f in time_utils.frange(self._startFrame, (self._endFrame+self._stepFrame), self._stepFrame):
                    om.MGlobal.viewFrame(f)
                    captured.update( { f : self._captureTransforms() })

                    if mainProgressBar:
                        shouldStop = maya.cmds.progressBar(mainProgressBar, query=True, isCancelled=True)
                        if shouldStop:
                            maya.cmds.warning('Cancelled {}'.format(snapTransformCmd.kPluginCmdName))
                            cancelledOperation = True
                            break

                        maya.cmds.progressBar(mainProgressBar, edit=True, status='{} : frame {} in range {}'.format(snapTransformCmd.kPluginCmdName, '%g'%f, statusRange))
                        maya.cmds.progressBar(mainProgressBar, edit=True, step=1)

                if not cancelledOperation:
                    # Get rid of all the keyframes that may be there already...
                    for dpSet in self._dpSets:
                        dpSrc, _dpTrg, _dpRel = dpSet
                        nodeName = dpSrc.partialPathName()
                        xfm_utils.cutTransformKeyframes(nodeName,
                                                        startFrame=self._startFrame,
                                                        endFrame=self._endFrame,
                                                        useScale=self._useScale,
                                                        useShear=self._useShear,
                                                        useRotate=self._useRotate,
                                                        useTranslate=self._useTranslate)

                    # Create the new keyframes
                    onFirstFrame = True
                    for f, xforms in captured.items():
                        for dpSet, xfo in zip(self._dpSets, xforms):
                            xfm_utils.setTransformKeyframes(dpSet[0].partialPathName(), xfo,
                                        frame=f,
                                        setScale=self._useScale,
                                        setShear=self._useShear,
                                        setRotate=self._useRotate,
                                        setTranslate=self._useTranslate,
                                        setPivot=onFirstFrame)
                        onFirstFrame = False

                    self._postApply()

                if mainProgressBar:
                    maya.cmds.progressBar(mainProgressBar, edit=True, endProgress=True)

        except:
            maya.cmds.error('Failed to execute {} command: See script editor for details'.format(snapTransformCmd.kPluginCmdName))
            self.setResult(-1)

        finally:
            maya.cmds.currentTime(saveFrame)
            self.setResult(self._resultAttrs)
            self._clear()

#-------------------------------------------------------------------------------
# Initialize the script plug-in
#-------------------------------------------------------------------------------
def initializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', snapTransformCmd.kPluginVersion, 'Any')

    try:
        pluginFn.registerCommand( snapTransformCmd.kPluginCmdName, snapTransformCmd.cmdCreator, snapTransformCmd.syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: {}\n'.format(snapTransformCmd.kPluginCmdName) )
        raise

#-------------------------------------------------------------------------------
# Uninitialize the script plug-in
#-------------------------------------------------------------------------------
def uninitializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', snapTransformCmd.kPluginVersion, 'Any')

    try:
        pluginFn.deregisterCommand( snapTransformCmd.kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: {}\n'.format(snapTransformCmd.kPluginCmdName) )
        raise

