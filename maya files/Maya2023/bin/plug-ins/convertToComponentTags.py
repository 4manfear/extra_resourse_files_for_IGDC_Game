import maya.api.OpenMaya as OpenMaya
import maya.cmds

import maya.internal.common.utils.deform as dfm_utils
import maya.internal.common.utils.geometry as geo_utils
import maya.internal.common.utils.material as mtl_utils
import maya.internal.common.utils.scene as scn_utils
import sys
import os

convertToComponentTagsVersion = '1.0'

#-------------------------------------------------------------------------------
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass

kSceneFlag = ('-sc', '-scene')
kVerboseFlag = ('-vb', '-verbose')

kDfsFlag = ('-dfs', '-deformerSubsets')
kTwkFlag = ('-twk', '-tweaks')
kMtlFlag = ('-mtl', '-materialAssign')

enableMtlAssign = os.getenv('MAYA_MTL_ASSIGN')

#-------------------------------------------------------------------------------
# The command class
#-------------------------------------------------------------------------------
class convertToComponentTagsCmd(OpenMaya.MPxCommand):

    kPluginCmdName='convertToComponentTags'

    def __init__(self):
        OpenMaya.MPxCommand.__init__(self)
        self._clear()


    def _clear(self):
        # setup private data members
        self._fullScene = False

        self._results = list()
        self._verbose = False

        self._convertDfs = False
        self._convertTwk = False
        self._convertMtl = False

        self._deformerNodes = set()
        self._tweakNodes = set()
        self._shapeNodes = set()

    # Create an instance of the command
    @staticmethod
    def cmdCreator():
        return convertToComponentTagsCmd()

    # Make the command undoable
    def isUndoable(self):
        return True

    # Syntax creator : Builds the argument strings up for the command
    @classmethod
    def syntaxCreator(cls):
        syntax = OpenMaya.MSyntax()
        syntax.addFlag(kSceneFlag[0], kSceneFlag[1], [OpenMaya.MSyntax.kNoArg])
        syntax.addFlag(kVerboseFlag[0], kVerboseFlag[1], OpenMaya.MSyntax.kNoArg)
        syntax.addFlag(kDfsFlag[0], kDfsFlag[1], OpenMaya.MSyntax.kNoArg)
        syntax.addFlag(kTwkFlag[0], kTwkFlag[1], OpenMaya.MSyntax.kNoArg)
        if enableMtlAssign:
            syntax.addFlag(kMtlFlag[0], kMtlFlag[1], OpenMaya.MSyntax.kNoArg)

        syntax.setObjectType(syntax.kSelectionList)
        syntax.setMinObjects(0)
        syntax.useSelectionAsDefault(True)
        syntax.enableQuery = False
        syntax.enableEdit = False

        return syntax

    def _parseFlags(self, args):
        argData = OpenMaya.MArgDatabase(self.syntax(), args)

        if argData.isFlagSet(kVerboseFlag[0]):
            self._verbose = True

        if argData.isFlagSet(kSceneFlag[0]):
            self._fullScene = True

        self._convertDfs = argData.isFlagSet(kDfsFlag[0])
        self._convertTwk = argData.isFlagSet(kTwkFlag[0])
        self._convertMtl = False
        if enableMtlAssign:
            argData.isFlagSet(kMtlFlag[0])

        # If no flags were specified, then use them all
        if not self._convertDfs and not self._convertTwk and not self._convertMtl:
            self._convertDfs = True
            self._convertTwk = True
            self._convertMtl = enableMtlAssign

        if self._fullScene:
            if self._convertDfs:
                # Get all the deformers in the scene
                deformers = maya.cmds.ls(type='geometryFilter')
                self._deformerNodes.update(set(deformers))

            if self._convertTwk:
                # Get all the tweaknodes in the scene
                tweaks = maya.cmds.ls(type='tweak')
                self._tweakNodes.update(set(tweaks))

            if self._convertMtl:
                # Get all the shapes in the scene (note: meshes only for the moment)
                shapes = maya.cmds.ls(type='mesh')
                self._shapeNodes.update(set(shapes))

        # Get the objects specified on the command line.
        slist = argData.getObjectList()
        for i in range(0, slist.length()):
            node = slist.getDependNode(i)
            fnNode = OpenMaya.MFnDependencyNode(node)
            nodeName = fnNode.absoluteName()

            if self._convertDfs and node.hasFn(OpenMaya.MFn.kGeometryFilt):
                self._deformerNodes.add(nodeName)

            if self._convertTwk and node.hasFn(OpenMaya.MFn.kTweak):
                self._tweakNodes.add(nodeName)

            if self._convertMtl and node.hasFn(OpenMaya.MFn.kShape):
                self._shapeNodes.add(nodeName)

            if (self._convertDfs or self._convertTwk) and node.hasFn(OpenMaya.MFn.kDagNode):
                # If we specified a dagNode then get all the deformers on it
                deformers = maya.cmds.deformableShape(nodeName, ch=True)
                if deformers is not None:
                    if self._convertDfs:
                        self._deformerNodes.update(set(deformers))

                    if self._convertTwk:
                        for d in deformers:
                            if maya.cmds.objectType(d, isAType='tweak'):
                                self._tweakNodes.add(d)


            if self._convertMtl and node.hasFn(OpenMaya.MFn.kTransform):
                s = geo_utils.extendToShape(nodeName)
                if s:
                    self._shapeNodes.add(s)

                s = geo_utils.extendToIntermediateShape(nodeName)
                if s:
                    self._shapeNodes.add(s)

        return True

    def doIt(self, args):
        if not self._parseFlags(args):
            maya.cmds.error('Failed to parse the arguments of the {} command: See script editor for details'.format(convertToComponentTagsCmd.kPluginCmdName))
            return

        self.redoIt()

    def undoIt(self):
        pass

    def redoIt(self):
        try:
            self.clearResult()
            if self._verbose:
                print ('Converting to use componentTags...')
                sceneInfo = scn_utils.NodeCountInfo()

            if self._convertTwk:
                if self._verbose:
                    print ('Removing obsolete tweaks...')
                for twk in self._tweakNodes:
                    if dfm_utils.removeObsoleteTweak(twk):
                        self._results.append('<{}>'.format(twk))

            if self._convertDfs:
                if self._verbose:
                    print ('Converting deformer subsets...')
                for dfm in self._deformerNodes:
                    if dfm_utils.replaceGroupParts(dfm):
                        self._results.append(dfm)

            if self._convertMtl:
                if self._verbose:
                    print ('Converting material assignments...')
                converter = mtl_utils.MaterialBindConverter()
                for shp in self._shapeNodes:
                    if converter.convert(shp):
                        self._results.append(shp)
                maya.cmds.ogs(reset=True)

            if self._verbose:
                sceneInfo.captureAndAnalyze()
                sceneInfo.printReport()

        except:
          maya.cmds.error('Failed to execute {} command: See script editor for details'.format(convertToComponentTagsCmd.kPluginCmdName))
          self.setResult(-1)

        finally:
            self.setResult(self._results)
            self._clear()

#-------------------------------------------------------------------------------
def initializePlugin(mobject):
    """ Initialize all the needed nodes """
    pluginFn = OpenMaya.MFnPlugin(mobject, 'Autodesk', convertToComponentTagsVersion, 'Any')

    try:
        pluginFn.registerCommand( convertToComponentTagsCmd.kPluginCmdName, convertToComponentTagsCmd.cmdCreator, convertToComponentTagsCmd.syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: %s\n' % convertToComponentTagsCmd.kPluginCmdName )
        raise

#-------------------------------------------------------------------------------
def uninitializePlugin(mobject):
    """ Uninitialize all the nodes """
    pluginFn = OpenMaya.MFnPlugin(mobject, 'Autodesk', convertToComponentTagsVersion, 'Any')

    try:
        pluginFn.deregisterCommand( convertToComponentTagsCmd.kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: %s\n' % convertToComponentTagsCmd.kPluginCmdName )
        raise
