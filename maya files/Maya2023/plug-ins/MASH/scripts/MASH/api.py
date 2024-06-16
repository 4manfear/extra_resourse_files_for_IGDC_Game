from builtins import object
from builtins import range
import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om
import maya.api.OpenMaya as nom
import sys
import MASH.undo as undo
import InViewMessageWrapper as ivm
if sys.version_info[0] >= 3:
    from . import dynamicsUtils as dynamics
else:
    import dynamicsUtils as dynamics
import copy
import json
from maya.app.flux.utils import getPluginStringResource
import openMASH

class Network(object):
    def __init__(self, name=None):
        self.networkName = None
        if name and cmds.objExists(name):
            self.networkName = name
            self.waiter = name
            self.instancer = None
            self.distribute = None

            # get existing Distribute and Instancer/Repro nodes.
            messageConns = cmds.listConnections(self.waiter+'.instancerMessage', d=True, s=False ) or []
            if len(messageConns):
                self.instancer = messageConns[0]

            waiterConns = cmds.listConnections(self.waiter+'.waiterMessage', d=False, s=True ) or []
            if len(waiterConns):
                self.distribute = waiterConns[0]

        self.objs = []
        self.curves = []

        self.position = []
        self.scale = []
        self.rotation = []
        self.pid = []
        self.time = []

    @undo.chunk('Create MASH Network')
    def createNetwork(self, name = None, distributionStyle = 0, mesh = None, geometry='Default'):
        mel.eval('source "AEMASH_WaiterTemplate.mel"') # we'll use some MEL commands from this file

        # set the geometry type if desired
        currentGeometryType = cmds.optionVar( q='mOGTN' )
        if geometry == 'Instancer' or geometry == 'instancer':
            cmds.optionVar( iv=('mOGTN', 2))
        elif geometry == 'Mesh' or geometry == 'mesh' or geometry == 'Repro' or geometry == 'repro':
            cmds.optionVar( iv=('mOGTN', 1))

        if not name:
            if cmds.optionVar(exists='mDNN'):
                name = cmds.optionVar(query='mDNN')
            else:
                name = 'MASH#'

        self.objs = cmds.ls(sl=True)
        nodes = mel.eval('MASHnewNetwork("'+name+'")')
        self.networkName = nodes[0]
        self.waiter = nodes[0]
        self.instancer = nodes[1]
        self.distribute = nodes[2]

        if len(self.objs) > 1:
            mashNode = self.addNode("MASH_ID")
            self.id = mashNode.name

        if distributionStyle > 0:
            cmds.setAttr(self.distribute+'.arrangement', distributionStyle)

        # restore the geometry type
        cmds.optionVar( iv=("mOGTN", currentGeometryType))
        cmds.select(self.waiter, ne=True)

    @undo.chunk('Add MASH Node')
    def addNode(self, nodeType):

        # if adding a curve node, add any curve nodes we're aware of
        if nodeType == "MASH_Curve":
            cmds.select(clear=True)
            cmds.select(self.curves)

        mel.eval('source AEMASH_WaiterTemplate.mel')
        nodeName = mel.eval('MASHaddNode("'+nodeType+'","'+self.waiter+'")')

        if (nodeType == "MASH_ID"):
            self.id = nodeType

        return Node(nodeName)

    @undo.chunk('Create MASH Shell Dynamics')
    def createShellDynamics(self, mesh, freezeTransforms=True, name="MASH Shell Network"):
        waiter = cmds.createNode('MASH_Waiter', n=name)
        cmds.addAttr(waiter, longName='instancerMessage', at='message')

        ftNode = None
        if (cmds.nodeType(mesh)=='transform'):
            ftNode = mesh
            mesh = cmds.listRelatives(mesh, s=True, pa=True)[0]
        else:
            ftNode = cmds.listRelatives(mesh, p=True, pa=True)[0]

        if freezeTransforms:
            cmds.makeIdentity(ftNode, apply=True, t=True, r=True, s=True, n=False, pn=True)

        # simple shell deformer that places polygon shells in world space
        deformer = cmds.deformer(mesh, type='MASH_ShellDeformer', n=waiter + '_ShellDeformer')[0]
        cmds.addAttr(deformer, longName='meshMessage', at='message')
        cmds.addAttr(mesh, longName='deformerMessage', at='message')

        # the deformer message plug is used to locate the mesh, and is thus a required connection if using
        # a 3rd party shell deformer.
        cmds.connectAttr(deformer+'.meshMessage', mesh+'.deformerMessage')
        cmds.connectAttr(waiter+'.outputPoints', deformer+'.inputPoints')
        dynamicsNode = cmds.createNode('MASH_Dynamics', n=waiter + '_Dynamics')
        cmds.connectAttr(dynamicsNode+'.outputPoints', waiter+'.inputPoints')

        anySolvers = cmds.ls(type='MASH_BulletSolver')
        solver = None
        if len(anySolvers) == 0:
            solverTransform = cmds.createNode('transform', n=waiter + '_BulletSolver')
            solver = cmds.createNode('MASH_BulletSolver', p=solverTransform)
        else:
            solver = anySolvers[0]

        dynamics.connectDynamics(dynamicsNode, solver, waiter, deformer)
        initialStateNode = self.setInitialState(dynamicsNode)
        cmds.connectAttr(ftNode+'.worldMatrix[0]', initialStateNode.name+'.inMatrix')

        cmds.select(solver)

    def meshDistribute(self, mesh, mode=1):
        nodeType = cmds.nodeType( mesh )
        if (nodeType == "transform"):
            shapes = cmds.listRelatives(mesh, pa=True)
            mesh = shapes[0]

        cmds.connectAttr(mesh+'.worldMesh', self.distribute+'.inputMesh')
        cmds.setAttr(self.distribute+'.arrangement', 4)
        cmds.setAttr(self.distribute+'.meshType', mode)

    @undo.chunk('Set Point Count')
    def setPointCount(self, count):
        cmds.setAttr(self.distribute+'.pointCount', count)

    def getAllNodesInNetwork(self, name=None, foundNames=None, dest=True):
        if foundNames is None or name is None:
            name = self.waiter #get the Waiter
            foundNames = set([name])

        objs = []
        thisNodeType = cmds.nodeType(name)

         # if we find a merge node we need to cut off the other MASH network otherwise we'll rename both
        if thisNodeType == "MASH_Blend":
            objs = cmds.listConnections(name+".inputPoints", destination=dest, sh=True )
            objs.extend(cmds.listConnections(name+".outputPoints", destination=dest, sh=True ))
        elif thisNodeType == "MASH_BulletSolver":
             pass #expressly ignore solvers as we'd end up renaming every MASH network connected to them
        else:
            objs = cmds.listConnections(name, destination=dest, sh=True )
            plugs = cmds.listConnections(name, destination=dest, sh=True, p=True ) or []
            # if we find a node that's connected to a MASH_Blend (the reverse of the above), we need to remove that entry
            for plug in plugs:
                if "altInputPoints" in plug:
                    idx = plugs.index(plug)
                    del objs[idx]

        if objs == None:
            return foundNames

        for obj in objs:
            if obj in foundNames: continue
            if 'MASH' in cmds.nodeType(obj) or 'instancer' in cmds.nodeType(obj):
                foundNames.add(obj)
                shouldDest = 'MASH_Breakout' != cmds.nodeType(obj)
                if 'MASH_Repro' == cmds.nodeType(obj):
                    foundNames = foundNames.union(cmds.listConnections(obj, source=False, type='mesh') or [])
                mObjs = self.getAllNodesInNetwork(obj, foundNames, shouldDest)
                foundNames = foundNames.union(mObjs)
                relatives = cmds.listRelatives(obj, pa=True)
                if relatives:
                    foundNames = foundNames.union(relatives)
            else:
                relatives = cmds.listRelatives(obj, pa=True)
                if relatives:
                    for rel in relatives:
                        if 'MASH' in cmds.nodeType(rel):
                            foundNames.add(obj)
                            mObjs = self.getAllNodesInNetwork(obj, foundNames)
                            foundNames = foundNames.union(mObjs)
        return foundNames

    def checkForNodeType(self, typeToCheckFor=None):
        nodeNames = self.getAllNodesInNetwork()
        foundTypes = set()
        for node in nodeNames:
            nt = cmds.nodeType(node)
            foundTypes.add(nt)

        if typeToCheckFor in foundTypes:
            return True
        else:
            return False

    def getAllNodesAndReturnList(self, waiter=True):
        nodeNames = self.getAllNodesInNetwork()
        finalNames = []
        for node in nodeNames:
            if waiter == False:
                nt = cmds.nodeType(node)
                if nt != "MASH_Waiter":
                    finalNames.append(node)
            else:
                finalNames.append(node)
        return finalNames

    def getCurrentFrameData(self):
        thisNode = _getMObject(self.waiter)
        fnNode = om.MFnDependencyNode(thisNode)
        pointsAttribute = fnNode.attribute("outputPoints")
        pointsPlug = om.MPlug(thisNode, pointsAttribute)

        handleData = pointsPlug.asMObject()
        inputPointsData = om.MFnArrayAttrsData(handleData)
        channels = inputPointsData.list()

        if "position" in channels:
            position = inputPointsData.getVectorData("position")
            self.channelToList(position, self.position)

        if "rotation" in channels:
            rotation = inputPointsData.getVectorData("rotation")
            self.channelToList(rotation, self.rotation)

        if "scale" in channels:
            scale = inputPointsData.getVectorData("scale")
            self.channelToList(scale, self.scale)

        if "objectIndex" in channels:
            self.pid = inputPointsData.getDoubleData("objectIndex")[:]

        if "frame" in channels:
            self.time = inputPointsData.getDoubleData("frame")[:]

    def channelToList(self, channel, destination):
        if channel == None or channel.length() == 0:
            return

        if channel.__class__.__name__ == "MVectorArray":
            for i in range (0, channel.length(), 1):
                vec = (channel[i].x, channel[i].y, channel[i].z)
                destination.append(vec)

    def rename(self, newPrefix, skipWaiter=False):
        cmds.flushIdleQueue()

        nodesInNetwork = self.getAllNodesAndReturnList()
        # Using Python 3 the MASH_Waiter node is not at the end and fails to
        # properly rename the network.
        nodesInNetwork.sort(reverse=True)
        for mashNode in nodesInNetwork:
            nodeType = cmds.nodeType(mashNode)

            if skipWaiter and nodeType == 'MASH_Waiter':
                continue

            # may get cleared
            underscore = '_'

            # legacy workaround
            if nodeType == 'MASH_Blend':
                nodeType = 'MASH_Merge'

            # truncate name
            if 'MASH_' in nodeType:
                nodeType = nodeType[5:]

            if nodeType == 'transform':
                # don't append mesh or transform
                nodeType = ''
                underscore = ''

                # repro meshes get special treatment
                rels = cmds.listRelatives(mashNode, s=True, pa=True)
                for child in rels:
                    if cmds.nodeType(child) == "mesh":
                        messageConns = cmds.listConnections(child+'.message') or []
                        for conn in messageConns:
                            if cmds.nodeType(conn) == "MASH_Repro":
                                nodeType = 'ReproMesh'
                                underscore = '_'

            newName = newPrefix+underscore+nodeType

            if nodeType == 'Trails':
                transform = cmds.listConnections(mashNode + '.outputMesh')
                if transform:
                     cmds.rename(transform[0], newName + '_Mesh')

            if nodeType == 'Flight':
                parent = cmds.listRelatives(mashNode, p=True, pa=True)[0]
                cmds.rename(parent, newName)
                newName+='Shape'

            #Update stored node names with new names
            if nodeType == 'Waiter':
                newName = newPrefix # since it's the root, don't append node type
                self.networkName = newName
                self.waiter = newName

            if nodeType == 'Repro':
                self.instancer = newName

            if nodeType == 'Distribute':
                self.distribute = newName

            # here we let Maya catch it's breath by queueing up the commands for later execution
            # this is essential to avoid errors with newly created Repro networks.
            try:
                cmds.rename(mashNode, newName)
            except: pass

    @undo.chunk('Add Collider')
    def addCollider(self, colliderName):
        if cmds.objExists(self.instancer+".dynamicsMessage"):
            solverName = cmds.listConnections(self.instancer+".dynamicsMessage" )[0]
            dynamics.connectColliderObject(solverName, colliderName)
        else:
            cmds.error("Dynamics not found on this network")

    @undo.chunk('Add Channel Random')
    def addChannelRandom(self, dynamicsNode):
        if dynamicsNode.__class__.__name__ == "Node":
            dynamicsNode = dynamicsNode.name
        channelRandomNode = ""
        if cmds.nodeType(dynamicsNode) == "MASH_Dynamics" or cmds.nodeType(dynamicsNode) == "MASH_Constraint":
            inputPlug = cmds.listConnections(dynamicsNode+".inputPoints", p=True )[0]
            channelRandomNode = cmds.createNode("MASH_ChannelRandom")
            cmds.connectAttr(inputPlug, channelRandomNode+".inputPoints")
            index = dynamics.nextFreeMulti(dynamicsNode, "dynamicsPP")
            cmds.connectAttr(channelRandomNode+".outputPoints", dynamicsNode+".dynamicsPP["+str(index)+"]")
        else:
            cmds.error(dynamicsNode+" is not a MASH_Dynamics node.")

        return Node(channelRandomNode)

    @undo.chunk('Add Constraint')
    def addConstraint(self, dynamicsNode):
        constraintNode = ""
        if dynamicsNode.__class__.__name__ == "Node":
            dynamicsNode = dynamicsNode.name
        if cmds.nodeType(dynamicsNode) == "MASH_Dynamics":
            inputPlug = cmds.listConnections(dynamicsNode+".inputPoints", p=True )[0]
            constraintNode = cmds.createNode("MASH_Constraint")
            cmds.connectAttr(inputPlug, constraintNode+".inputPoints")
            index = dynamics.nextFreeMulti(dynamicsNode, "dynamicsPP")
            cmds.connectAttr(constraintNode+".outputPoints", dynamicsNode+".constraintsPP["+str(index)+"]")
        # returns neutered node object
        constraint = Node(constraintNode)
        constraint.utilityNode = True
        return constraint

    @undo.chunk('Set Initial State')
    def setInitialState(self, dynamicsNode):
        if dynamicsNode.__class__.__name__ == "Node":
            dynamicsNode = dynamicsNode.name
            
        cmds.addAttr(dynamicsNode, longName='initialStateMessage', at='message')
        initialStateNode = cmds.createNode("MASH_DynamicsInitialState", n=dynamicsNode + 'InitialState#')
        cmds.addAttr(initialStateNode, longName='initialStateMessage', at='message')
        cmds.connectAttr(initialStateNode+'.initialStateMessage', dynamicsNode+'.initialStateMessage', f=True)
        cmds.setDynamicsInitialState(setState=True, name=dynamicsNode)

        inputPlug = cmds.listConnections(dynamicsNode+".inputPoints", p=True ) or []
        if len(inputPlug):
            inputPlug = inputPlug[0]
            cmds.connectAttr(inputPlug, initialStateNode+'.inputPoints', f=True)
        
        cmds.connectAttr(initialStateNode+'.outputPoints', dynamicsNode+'.inputPoints', f=True)
        cmds.setAttr(initialStateNode+".enable", 1)
        return Node(initialStateNode)

    def hasDynamics(self):
        return cmds.objExists(self.instancer+".dynamicsMessage")

    def getSolver(self):
        if self.hasDynamics():
            solvers = cmds.listConnections(self.instancer+".dynamicsMessage", sh=True) or []
            if len(solvers):
                return solvers[0]
        
        return None

    def getSolverIndex(self):
        if self.hasDynamics():
            solverObj = openMASH.mashGetMObjectFromNameOne(self.getSolver())
            fnNode = om.MFnDependencyNode(solverObj)
            outputAttribute = fnNode.attribute("outputPoints")
            outputPlug = om.MPlug(solverObj, outputAttribute)
            numOutputs = outputPlug.numConnectedElements()
            for i in range(numOutputs):
                element = outputPlug.elementByPhysicalIndex(i)
                connections = cmds.listConnections( element.name(), s=False, d=True)
                if self.instancer in connections:
                    return i
        return None

# Copy of the instance function
def getAllNodesInNetwork(name=None, foundNames=None, dest=True):
    if foundNames is None:
        foundNames = set()
    objs = []

    objs = cmds.listConnections(name, destination=dest, sh=True )

    if objs == None:
        return foundNames

    for obj in objs:
        if obj in foundNames: continue
        if 'MASH' in cmds.nodeType(obj) or 'instancer' in cmds.nodeType(obj):
            foundNames.add(obj)
            shouldDest = 'MASH_Breakout' != cmds.nodeType(obj)
            if 'MASH_Repro' == cmds.nodeType(obj):
                foundNames = foundNames.union(cmds.listConnections(obj, source=False, type='mesh') or [])
            mObjs = getAllNodesInNetwork(obj, foundNames, shouldDest)
            foundNames = foundNames.union(mObjs)
            relatives = cmds.listRelatives(obj, pa=True)
            if relatives:
                foundNames = foundNames.union(relatives)
        else:
            relatives = cmds.listRelatives(obj, pa=True)
            if relatives:
                for rel in relatives:
                    if 'MASH' in cmds.nodeType(rel):
                        foundNames.add(obj)
                        mObjs = getAllNodesInNetwork(obj, foundNames)
                        foundNames = foundNames.union(mObjs)
    return foundNames

def getWaiterFromNode(nodeName):
    allNodes = list(getAllNodesInNetwork(nodeName) or [])
    for n in allNodes:
        if cmds.nodeType(n) == 'MASH_Waiter':
            return n

    return None

class Node(object):

    def __init__(self, nodeName):
        self.name = nodeName
        self.falloffs = []
        self.map = None
        self.utilityNode = False

    def addFalloff(self):
        if self.utilityNode:
            return
        mel.eval('source MASHfalloffButtons.mel')
        falloff = mel.eval('MASH_FalloffButtonCmds("'+self.name+'",1)')
        self.falloffs.append(falloff)
        return falloff

    def getFalloffs(self):
        if self.utilityNode:
            return
        self.falloffs = []
        falloffs = None
        if cmds.objExists(self.name+'.strengthPP'):
            falloffs = cmds.listConnections(self.name+'.strengthPP', sh=True)
        if falloffs:
            for conn in falloffs:
                if (cmds.nodeType(conn) == "MASH_Falloff"):
                    self.falloffs.append(conn)
        return self.falloffs

    def addGroundPlane(self, groundTranform):
        if cmds.nodeType(self.name) != "MASH_World":
            return

        cmds.connectAttr(  '%s.worldMatrix[0]' % (groundTranform), '%s.groundMatrix' % (self.name), force=True )
        groundShape = cmds.listRelatives(groundTranform, s=True, pa=True)[0]
        cmds.connectAttr(  '%s.worldMesh[0]' % (groundShape), '%s.groundMesh' % (self.name), force=True )

    def addExplodeMesh(self, explodeMesh):
        if cmds.nodeType(self.name) != "MASH_Explode":
            return

        if cmds.nodeType(explodeMesh) == "transform":
            explodeMesh = cmds.listRelatives(explodeMesh, s=True, pa=True)[0]

        cmds.connectAttr(explodeMesh+".worldMesh[0]", self.name+".inputMesh")
        command = 'source "AEMASH_ExplodeTemplate.mel"'
        mel.eval(command)
        command = 'evalDeferred \"explodeButtonCMDS(\\"'+ self.name + '\\", \\"'+ explodeMesh+ '\\",1)\"'
        mel.eval(command)

    def snapPlacerPointsToPaintMeshes(self):
        if cmds.nodeType(self.name) != "MASH_Placer":
            return

        paintMeshes = cmds.listConnections(self.name+'.paintMeshes', sh=True)
        if paintMeshes:
            paintJson = cmds.getAttr(self.name+'.paintJson')
            jsonObj = json.loads(paintJson)

            positions = jsonObj["positions"]
            meshFnSets = []
            for mesh in paintMeshes:
                meshPath = _getDagPath(mesh)
                meshFnSets.append(nom.MFnMesh(meshPath))

            for x in range(0, len(positions)):
                distance = 9999999.9
                pt = nom.MPoint(positions[x][0], positions[x][1], positions[x][2])
                finalPoint = []
                for meshFn in meshFnSets:
                    point = meshFn.getClosestPoint(pt, om.MSpace.kWorld)[0]
                    delta = nom.MVector(pt.x-point.x, pt.y-point.y, pt.z-point.z).length()
                    if (delta < distance):
                        distance = delta
                        finalPoint = [point.x, point.y, point.z]
                jsonObj["positions"][x] = finalPoint

            cmds.setAttr(self.name+".paintJson", json.dumps(jsonObj), type='string')
        else:
            kNoPaintMeshes = getPluginStringResource('kNoPaintMeshes')
            ivm.MashInViewMessage(kNoPaintMeshes, 'Warning')


def _getDagPath(uniquePathToNode):
    sel = nom.MSelectionList()
    sel.add(uniquePathToNode)
    return sel.getDagPath(0)
 
def _getMObject(uniquePathToNode):
    sel = om.MSelectionList()
    sel.add(uniquePathToNode)
    thisNode = om.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
