'''
Command = geometryReport(flags)

This command prints a report on the geometries being used on its incoming
and outgoing plugs. It shows the type of geometries, the number of verts
and the componentTags that may exist on them.

EXAMPLES:

import maya.cmds as cmds
cmds.loadPlugin('geometryReport')

cmds.geometryReport('cluster1')
cmds.geometryReport('pSphere1Shape')

'''

import maya.api.OpenMaya as om
import maya.cmds
import maya.internal.common.utils.connections as con_utils
import maya.internal.common.utils.geometry as geo_utils
import maya.internal.common.utils.componenttag as ctag_utils
import maya.internal.common.utils.transform as xfm_utils
import sys
import itertools

kVerboseFlag = ("-vb", "-verbose")
kInputFlag = ("-in", "-input")
kOutputFlag = ("-out", "-output")
kDeformersFlag = ("-d", "-deformers")
kShapesFlag = ("-s", "-shapes")

#-------------------------------------------------------------------------------
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass

#-------------------------------------------------------------------------------
#
#
#
#-------------------------------------------------------------------------------
class FormatOutput(object):

    def __init__(self):
        pass

    def showPlug(self, plugDict):

        plg = plugDict.get(ctag_utils.NodeInfo.kName, '')
        tpe = plugDict.get(ctag_utils.NodeInfo.kType, None)
        cnt = plugDict.get(ctag_utils.NodeInfo.kCnt, 0)

        print ()
        print ('  {}   ({}) {}'.format('%-30s'%plg.split('.',1)[-1], cnt, tpe))

        # groupId or groupExpression information
        gid = plugDict.get(ctag_utils.NodeInfo.kGid, None)
        cex = plugDict.get(ctag_utils.NodeInfo.kGex, None)
        if gid is not None and cex is not None:
            cmp = plugDict.get(ctag_utils.NodeInfo.kCmp, None)
            cnt = plugDict.get(ctag_utils.NodeInfo.kCnt, 0)

            if gid > 0:
                s = str(gid)
            else:
                s = cex

            print ('  {} : ({}) {}'.format('%30s'%s, cnt, cmp))

        # componentTags on the geometry
        componentTags = plugDict.get('componentTags', [])
        for gtd in componentTags:
            gt  = gtd.get(ctag_utils.NodeInfo.kName, '')
            cmp = gtd.get(ctag_utils.NodeInfo.kCmp, None)
            cnt = gtd.get(ctag_utils.NodeInfo.kCnt, 0)
            ccy = gtd.get(ctag_utils.NodeInfo.kCtg, '')
            print ('  {} : {} = {} ({})'.format('%30s'%gt, '%2s'%ccy, cmp, cnt))

    def showNode(self, nodeDict):
        ''' Print the information in the node dictionary'''
        if nodeDict is None:
            return

        # Node header
        node = nodeDict.get(ctag_utils.NodeInfo.kName, '')
        refFile = nodeDict.get(ctag_utils.NodeInfo.kRef, None)
        if refFile is not None:
            refText = '<Ref = \"{}\">'.format(refFile)
        else:
            refText = ''

        print ()
        print ('-'*80)
        print ('{} {}'.format('%-40s'%node.strip(':'), refText))

        # Inserted tags on node
        insertedTagsArray = nodeDict.get(ctag_utils.NodeInfo.kTags, None)
        if insertedTagsArray is not None:
            print ()
            print ('    Inserted Tags: {}'.format(len(insertedTagsArray)))
            for tagDict in insertedTagsArray:
                name = tagDict.get(ctag_utils.NodeInfo.kName, '')
                cmp  = tagDict.get(ctag_utils.NodeInfo.kCmp, None)
                idx  = tagDict.get(ctag_utils.NodeInfo.kIdx, None)
                if idx is not None:
                    print ('      {}: {} {}'.format("%04d"%idx, "%-30s"%name, cmp))

        # Inserted tags on node
        tagHistoryArray = nodeDict.get(ctag_utils.NodeInfo.kTagHis, None)
        if tagHistoryArray is not None:
            print ()
            print ('    Tag History')
            for tagHisDict in tagHistoryArray:
                name = tagHisDict.get(ctag_utils.NodeInfo.kName, '')
                node = tagHisDict.get(ctag_utils.NodeInfo.kNode, None)
                isRef = False
                isShp = False
                if node:
                    isRef = maya.cmds.referenceQuery(node, isNodeReferenced=True)
                    isShp = maya.cmds.objectType(node, isAType='shape')

                if isShp:
                    s = 'Non Editable' if isRef else 'Editable'
                else:
                    s = 'Ref Procedural' if isRef else 'Procedural'

                print ('    {} : {} ({})'.format('%30s'%name, '%-60s'%node, s))

        # Plug info
        plugArray = nodeDict.get(ctag_utils.NodeInfo.kPlugs, None)
        if plugArray is not None:
            for plugDict in plugArray:
                self.showPlug(plugDict)

#-------------------------------------------------------------------------------
# The command class
#-------------------------------------------------------------------------------
class geometryReportCmd(om.MPxCommand):

    kPluginCmdName="geometryReport"

    def __init__(self):
        om.MPxCommand.__init__(self)
        self._clear()

    def _clear(self):
        # setup private data members
        self._nodes = set()
        self._deformers = set()
        self._shapes = set()
        self._results = list()
        self._verbose = False
        self._useInput = True
        self._useOutput = True

        self._showDeformer = False
        self._showShape = False

    # Create an instance of the command
    @staticmethod
    def cmdCreator():
        return geometryReportCmd()

    # Make the command not undoable
    def isUndoable(self):
        return False

    # Syntax creator : Builds the argument strings up for the command
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        #syntax.addFlag(kSceneFlag[0], kSceneFlag[1], [om.MSyntax.kNoArg])
        syntax.addFlag(kVerboseFlag[0], kVerboseFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kDeformersFlag[0], kDeformersFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kShapesFlag[0], kShapesFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kInputFlag[0], kInputFlag[1], om.MSyntax.kBoolean)
        syntax.addFlag(kOutputFlag[0], kOutputFlag[1], om.MSyntax.kBoolean)

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

        if argData.isFlagSet(kDeformersFlag[0]):
            self._showDeformer = True

        if argData.isFlagSet(kShapesFlag[0]):
            self._showShape = True

        if argData.isFlagSet(kInputFlag[0]):
            self._useInput = argData.flagArgumentBool(kInputFlag[0], 0)
        if argData.isFlagSet(kOutputFlag[0]):
            self._useOutput = argData.flagArgumentBool(kOutputFlag[0], 0)

        # Get the objects specified on the command line.
        slist = argData.getObjectList()
        for i in range(0, slist.length()):
            node = slist.getDependNode(i)
            fnNode = om.MFnDependencyNode(node)
            nodeName = fnNode.absoluteName()

            self._nodes.add(nodeName)

            if self._showShape:
                if node.hasFn(om.MFn.kShape):
                    self._shapes.add(nodeName)

                if node.hasFn(om.MFn.kTransform):
                    s = geo_utils.extendToShape(nodeName)
                    if s:
                        self._shapes.add(s)

                    s = geo_utils.extendToIntermediateShape(nodeName)
                    if s:
                        self._shapes.add(s)

                if node.hasFn(om.MFn.kGeometryFilt):
                    geoms = maya.cmds.deformer(nodeName, q=True, geometry=True) or []
                    for g in geoms:
                        self._shapes.add(g)
                        og = maya.cmds.deformableShape(g, og=True) or []
                        if len(og) > 0:
                            self._shapes.add(og[0].split('.',1)[0])

            if self._showDeformer:
                if node.hasFn(om.MFn.kGeometryFilt):
                    self._deformers.add(nodeName)

                if node.hasFn(om.MFn.kDagNode):
                    if node.hasFn(om.MFn.kTransform):
                        deformers = maya.cmds.deformableShape(geo_utils.extendToShape(nodeName), ch=True)
                    else:
                        deformers = maya.cmds.deformableShape(nodeName, ch=True)
                    if deformers is not None:
                        self._deformers.update(set(deformers))


        return True


    def doIt(self, args):
        if not self._parseFlags(args):
            maya.cmds.error("Failed to parse the arguments of the geometryReport command: See script editor for details")
            return

        self.redoIt()

    def redoIt(self):
        try:
            self.clearResult()

            nodeInfo = ctag_utils.NodeInfo(self._useInput, self._useOutput)
            formatOutput = FormatOutput()

            if self._showDeformer:
                for d in self._deformers:
                    formatOutput.showNode(nodeInfo.infoDeformer(d))

            if self._showShape:
                for s in self._shapes:
                    formatOutput.showNode(nodeInfo.infoShape(s))

            if not self._showDeformer and not self._showShape:
                for n in self._nodes:
                    formatOutput.showNode(nodeInfo.infoPlugs(n))

        except:
           maya.cmds.error("Failed to execute geometryReport command: See script editor for details")
           self.setResult(-1)

        finally:
            self._clear()

#-------------------------------------------------------------------------------
# Initialize the script plug-in
#-------------------------------------------------------------------------------
def initializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, "Autodesk", "1.0", "Any")
    try:
        pluginFn.registerCommand( geometryReportCmd.kPluginCmdName, geometryReportCmd.cmdCreator, geometryReportCmd.syntaxCreator )
    except:
        sys.stderr.write( "Failed to register command: %s\n" % geometryReportCmd.kPluginCmdName )
        raise

#-------------------------------------------------------------------------------
# Uninitialize the script plug-in
#-------------------------------------------------------------------------------
def uninitializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject)
    try:
        pluginFn.deregisterCommand( geometryReportCmd.kPluginCmdName )
    except:
        sys.stderr.write( "Failed to unregister command: %s\n" % geometryReportCmd.kPluginCmdName )
        raise


