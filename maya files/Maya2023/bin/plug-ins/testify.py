'''
Test to make sure the matrix nodes are set up correctly
'''
from builtins import object
from builtins import range
import maya.cmds as cmds
import re
import os

def shapeFromTestifyNode(ts):
    try:
        shape = cmds.getAttr(f'{ts}.testifyShape')
    except:
        shape = None

    if not shape:
        shape = ts[5:]

    return shape if cmds.objExists(shape) else None

def referenceFromTestifyNode(ts):
    rn = 'reference_' + ts[5:]
    return rn if cmds.objExists(rn) else None


def retestify():
    testShapes = cmds.ls("test_*")
    shapes = [shapeFromTestifyNode(t) for t in testShapes]
    references = [referenceFromTestifyNode(t) for t in testShapes]

    cmds.delete(testShapes)
    cmds.delete(references)
    if shapes:
        testify(geoms=shapes)



def getOutputNameBasedOnType(geomType):
    if geomType == "mesh":
         return "worldMesh"
    elif geomType == "lattice":
         return "worldLattice"
    elif geomType in cmds.nodeType("nurbsSurface",d=True, isTypeName=True)  or geomType in cmds.nodeType("nurbsCurve",d=True, isTypeName=True):
         return "worldSpace"

    return "worldMatrix"

def makeNodeName(geomPath, pfx=""):
    shortName = cmds.ls(geomPath)
    baseName = shortName[0] if len(shortName) else geomPath
    return pfx + baseName.replace('|','_').strip('_ ')

def testify(geoms=[], root=None):
    cmds.loadPlugin( 'geometrytools', qt=True)
    start = int(cmds.playbackOptions(q=True, minTime=True))
    stop = int(cmds.playbackOptions(q=True, maxTime=True)) 
    selectors =[cmds.createNode("choice") for g in geoms]
    refs = [(cmds.createNode("transform", name=makeNodeName(g, "reference_"))) for g in geoms]
    if root:
        [cmds.parent(r, root) for r in refs]
        refs = [(root + "|" + ref) for ref in refs]
    for f in range(start, stop+1):
        cmds.currentTime(f)
        for g,s,ref in zip(geoms, selectors, refs):
            duplicated = cmds.duplicate(g, rr=True, f=True)
            relatives = cmds.listRelatives(duplicated, f=True)
            for r in relatives:
                if re.search("Orig", r):
                    cmds.delete(r)
                else:
                    gdup = r

            parent = cmds.parent(gdup, ref)
            gdup = "%s|%s"%(ref,"|".join(gdup.split("|")[-2:]))
            geomType = cmds.nodeType(gdup)
            cmds.connectAttr("%s.%s[0]"%(gdup,getOutputNameBasedOnType(geomType)) , "%s.input[%d]"%(s,f))

    for g,s,ref in zip(geoms,selectors,  refs):
        cmds.connectAttr("time1.outTime", "%s.selector"%s)
        mc = cmds.createNode("compare")

        geomType = cmds.nodeType(g)
        cmds.connectAttr("%s.%s[0]"%(g,getOutputNameBasedOnType(geomType)), "%s.inputA"%mc)

        cmds.connectAttr("%s.output"%s, "%s.inputB"%mc)
        tn = makeNodeName(g, "test_")
        testNode = cmds.createNode("transform", name=tn)

        # Store the name of the shape in a custom attribute
        cmds.addAttr(testNode, ln='testifyShape', dt='string')
        cmds.setAttr(f'{testNode}.testifyShape', g, type="string")

        if root:
            cmds.parent(testNode, root)
            testNode = root + "|" + testNode

        cmds.addAttr(testNode, ln="result", sn="res", at="bool")
        cmds.connectAttr("%s.outValue"%mc,"%s.result"%testNode)


        cmds.setAttr("%s.visibility"%ref, False)
        indShape = cmds.createNode("locator", name="indicator")
        cmds.setAttr("%s.overrideEnabled"%indShape, 1)
        bc = cmds.createNode("blendColors")
        cmds.connectAttr("%s.result"%testNode, "%s.blender"%bc)
        cmds.setAttr("%s.color1"%bc, 0,1,0)
        cmds.setAttr("%s.color2"%bc, 1,0,0)
        cmds.connectAttr("%s.output"%bc, "%s.overrideColorRGB"%indShape)
        cmds.setAttr("%s.overrideRGBColors"%indShape, 1)
        cmds.parent(indShape, testNode)
        bb = cmds.exactWorldBoundingBox(g)
        cmds.move(bb[0] + (bb[3] - bb[0])/2.0, bb[4] + 0.1* (bb[4] - bb[1]),  bb[2] + (bb[5] - bb[2])/2.0, indShape)




import maya.api.OpenMaya as om
import maya.cmds
import maya.internal.common.utils.transform as xfm_utils
import maya.internal.common.utils.ui as ui_utils
import maya.internal.common.utils.time as time_utils
import sys

#-------------------------------------------------------------------------------
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass

kAttestFlag = ('-a', '-attest')
kReAttestFlag = ('-r', '-reattest')

#-------------------------------------------------------------------------------
# The command class
#-------------------------------------------------------------------------------
class testifyCmd(om.MPxCommand):

    kPluginCmdName = 'testify'
    kPluginVersion = '1.0'

    def __init__(self):
        om.MPxCommand.__init__(self)
        self._clear()

    def _clear(self):
        self._attest = False
        self._reattest = False
        self._dpSrcList = list()

    # Create an instance of the command
    @staticmethod
    def cmdCreator():
        return testifyCmd()

    # Make the command undoable
    def isUndoable(self):
        return True


    # Syntax creator : Builds the argument strings up for the command
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()
        syntax.addFlag(kAttestFlag[0], kAttestFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kReAttestFlag[0], kReAttestFlag[1], om.MSyntax.kNoArg)
        syntax.setObjectType(syntax.kSelectionList)
        syntax.setMinObjects(0)
        syntax.useSelectionAsDefault(True)
        syntax.enableQuery = False
        syntax.enableEdit = False

        return syntax


    def _parseFlags(self, args):
        try:
            argData = om.MArgDatabase(self.syntax(), args)
        except:
            maya.cmds.error('Failed to get the objects for {} command: See script editor for details'.format(testifyCmd.kPluginCmdName))
            return

        if argData.isFlagSet(kAttestFlag[0]):
            self._attest = True

        if argData.isFlagSet(kReAttestFlag[0]):
            self._reattest = True

        # Get the objects specified on the command line.
        slist = argData.getObjectList()
        for i in range(0, slist.length()):
            self._dpSrcList.append(slist.getDagPath(i))

        return True


    def doIt(self, args):
        # Check if all the flags can be parsed correctly
        if not self._parseFlags(args):
            maya.cmds.error('Failed to parse the arguments of the {} command: See script editor for details'.format(testifyCmd.kPluginCmdName))
            return

        self.redoIt()

    def undoIt(self):
        pass

    def redoIt(self):
        if self._attest:
            stages = cmds.ls(type="stage")
            if "rootStage" in stages:
                idx = stages.index("rootStage")
                rootStage = stages[idx]
                cmds.stage(rootStage, e=True, a=True)
                nextStage = cmds.stage(rootStage, e=True, n=True)[0]
                while nextStage != "":
                    rootNode = cmds.createNode("transform", n=(nextStage+ "_ref"))
                    testify(geoms=[o.fullPathName() for o in self._dpSrcList], root=rootNode)
                    nextStage = cmds.stage(nextStage, e=True, n=True)[0]
            else:
                testify(geoms=[o.fullPathName() for o in self._dpSrcList])
        elif self._reattest:
            retestify()


#-------------------------------------------------------------------------------
# Initialize the script plug-in
#-------------------------------------------------------------------------------
def initializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', testifyCmd.kPluginVersion, 'Any')

    try:
        pluginFn.registerCommand( testifyCmd.kPluginCmdName, testifyCmd.cmdCreator, testifyCmd.syntaxCreator )
    except:
        sys.stderr.write( 'Failed to register command: {}\n'.format(testifyCmd.kPluginCmdName) )
        raise

#-------------------------------------------------------------------------------
# Uninitialize the script plug-in
#-------------------------------------------------------------------------------
def uninitializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', testifyCmd.kPluginVersion, 'Any')

    try:
        pluginFn.deregisterCommand( testifyCmd.kPluginCmdName )
    except:
        sys.stderr.write( 'Failed to unregister command: {}\n'.format(testifyCmd.kPluginCmdName) )
        raise

