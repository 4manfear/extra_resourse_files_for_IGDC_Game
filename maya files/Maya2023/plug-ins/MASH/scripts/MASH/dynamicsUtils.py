# -*- coding: utf-8 -*-

from builtins import object
from builtins import range
import maya.cmds as cmds
from openMASH import mashGetMObjectFromNameOne
import maya.OpenMaya as old
import maya.api.OpenMaya as om
import sys
if sys.version_info[0] >= 3:
    from . import api as mapi
else:
    import api as mapi
import openMASH
import InViewMessageWrapper as ivm
from maya.app.flux.ae.Custom import Custom
import maya.mel as mel
import maya.app.flux.core as fx

def connectDynamics(dynamicsNode, solverNode, waiterNode, instancerNode):
    solverConnId = str(nextFreeMulti(solverNode, "inputNetworks"))
    cmds.connectAttr(dynamicsNode+'.enable', solverNode+'.inputNetworks['+solverConnId+'].mashEnable')
    cmds.connectAttr(dynamicsNode+'.bounce', solverNode+'.inputNetworks['+solverConnId+'].mashBounce')
    cmds.connectAttr(dynamicsNode+'.friction', solverNode+'.inputNetworks['+solverConnId+'].mashFriction')
    cmds.connectAttr(dynamicsNode+'.damping', solverNode+'.inputNetworks['+solverConnId+'].mashDamping')
    cmds.connectAttr(dynamicsNode+'.rollingFriction', solverNode+'.inputNetworks['+solverConnId+'].mashRollingFriction')
    cmds.connectAttr(dynamicsNode+'.rollingDamping', solverNode+'.inputNetworks['+solverConnId+'].mashRollingDamping')
    cmds.connectAttr(dynamicsNode+'.mass', solverNode+'.inputNetworks['+solverConnId+'].mashMass')
    cmds.connectAttr(dynamicsNode+'.positionStrength', solverNode+'.inputNetworks['+solverConnId+'].mashPositionStrength')
    cmds.connectAttr(dynamicsNode+'.rotationalStrength', solverNode+'.inputNetworks['+solverConnId+'].mashRotationalStrength')
    cmds.connectAttr(dynamicsNode+'.collisionObjectScale', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionObjectScale')
    cmds.connectAttr(dynamicsNode+'.collisionShapeLength', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionShapeLength')
    cmds.connectAttr(dynamicsNode+'.collisionShapeAxis', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionShapeAxis')
    cmds.connectAttr(dynamicsNode+'.maxVelocity', solverNode+'.inputNetworks['+solverConnId+'].mashMaxVelocity')
    cmds.connectAttr(dynamicsNode+'.maxAngularVelocity', solverNode+'.inputNetworks['+solverConnId+'].mashAngularVelocity')
    cmds.connectAttr(dynamicsNode+'.collisionShape', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionShape')
    cmds.connectAttr(dynamicsNode+'.initiallySleeping', solverNode+'.inputNetworks['+solverConnId+'].mashInitiallySleeping')
    cmds.connectAttr(dynamicsNode+'.initialVelocity', solverNode+'.inputNetworks['+solverConnId+'].mashInitialVelocity')
    cmds.connectAttr(dynamicsNode+'.initialRotationalVelocity', solverNode+'.inputNetworks['+solverConnId+'].mashInitialRotationalVelocity')
    cmds.connectAttr(dynamicsNode+'.emitFromCollisions', solverNode+'.inputNetworks['+solverConnId+'].mashEmitFromCollisions')
    cmds.connectAttr(dynamicsNode+'.collisionDistanceThreshold', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionDistanceThreshold')
    cmds.connectAttr(dynamicsNode+'.ignoreInvisible', solverNode+'.inputNetworks['+solverConnId+'].mashIgnoreInvisible')
    cmds.connectAttr(dynamicsNode+'.autoFit', solverNode+'.inputNetworks['+solverConnId+'].mashAutoFit')
    cmds.connectAttr(dynamicsNode+'.linearVelocityThreshold', solverNode+'.inputNetworks['+solverConnId+'].mashLinearVelocityThreshold')
    cmds.connectAttr(dynamicsNode+'.angularVelocityThreshold', solverNode+'.inputNetworks['+solverConnId+'].mashAngularVelocityThreshold')
    cmds.connectAttr(dynamicsNode+'.collisionJitter', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionJitter')
    cmds.connectAttr(dynamicsNode+'.contactMaskLayers', solverNode+'.inputNetworks['+solverConnId+'].mashContactMaskLayers')
    cmds.connectAttr(dynamicsNode+'.collisionMaskLayers', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionMaskLayers')
    cmds.connectAttr(dynamicsNode+'.collisionGroupLayers', solverNode+'.inputNetworks['+solverConnId+'].mashCollisionGroupLayers')
    cmds.connectAttr(dynamicsNode+'.hierarchyMode', solverNode+'.inputNetworks['+solverConnId+'].mashHierarchyMode')
    cmds.connectAttr(dynamicsNode+'.initialStateJSON', solverNode+'.inputNetworks['+solverConnId+'].mashInitialStateJSON')
    cmds.connectAttr(dynamicsNode+'.useDensity', solverNode+'.inputNetworks['+solverConnId+'].mashUseDensity')
    cmds.connectAttr(dynamicsNode+'.initialVelocitySpace', solverNode+'.inputNetworks['+solverConnId+'].mashInitialVelocitySpace')

    cmds.connectAttr(solverNode+'.outputPoints['+solverConnId+']', instancerNode+'.inputPoints', force=True)
    cmds.connectAttr(waiterNode+'.outputPoints', solverNode+'.inputNetworks['+solverConnId+'].inputPoints')

    #these attributes might already exist
    if not cmds.objExists(solverNode+".instancerMessage"):
        cmds.addAttr(solverNode, longName='instancerMessage', at='message', hidden=True)

    if not cmds.objExists(instancerNode+".dynamicsMessage"):
        cmds.addAttr(instancerNode, longName='dynamicsMessage', at='message', hidden=True)

    if not cmds.objExists(waiterNode+".dynamicsMessage"):
        cmds.addAttr(waiterNode, longName='dynamicsMessage', at='message', hidden=True)

    if not cmds.objExists(dynamicsNode+".waiterMessage"):
        cmds.addAttr(dynamicsNode, longName='waiterMessage', at='message', hidden=True)

    # these nodes need to know about each other for automated deletion / disconnection / assingment
    cmds.connectAttr(solverNode+'.instancerMessage', instancerNode+'.dynamicsMessage', force=True)
    if not cmds.isConnected( dynamicsNode+'.waiterMessage', waiterNode+'.dynamicsMessage' ):
        cmds.connectAttr(dynamicsNode+'.waiterMessage', waiterNode+'.dynamicsMessage', force=True)

def connectConstraint(dynamicsNode, constraintNode):
    pass

def nextFreeMulti(nodeName, attributeName):
    thisNode = mashGetMObjectFromNameOne(nodeName)
    fnNode = old.MFnDependencyNode(thisNode)
    attribute = fnNode.attribute(attributeName)
    inPlug = old.MPlug( thisNode, attribute )
    count = inPlug.numConnectedElements()
    existingArray = old.MIntArray()
    inPlug.getExistingArrayAttributeIndices(existingArray)

    if existingArray:
        start = 0
        limit = len(existingArray)
        start = start if start is not None else existingArray[0]
        limit = limit if limit is not None else existingArray[-1]
        return [i for i in range(start,limit + 1) if i not in existingArray][0]
    else:
        return 0

    return freeIndex

def setupAEInjection():
    cmds.callbacks(addCallback=aeInjectCallback,
                   hook="AETemplateCustomContent",
                   owner="MASH")

def aeInjectCallback(node):
    if cmds.nodeType(node) == 'mesh':
        import maya.app.flux.ae.api as aeAPI
        aeAPI.addCustom(DynamicsColliderCustom(node))

class DynamicsColliderCustom(Custom):
    def buildUI(self, nodeName):
        self.prefix = 'dynamics_collider_'
        isCollider = cmds.objExists(self.name+'.collisionShape')
        self.hasControls = False

        with self.frameLayout('MASH', ref='mashFrame'):
            with self.verticalLayout(height=fx.pix(220)):
                self.frameParent = cmds.setParent(q=True)

        self.updateVisibility()

    def addAttributes(self):
        cmds.setParent(self.frameParent)

        cmds.attrFieldSliderGrp(self.prefix + 'bounce', attribute=self.name + '.bounce', label=fx.res('kBounce'))
        cmds.attrFieldSliderGrp(self.prefix + 'friction', attribute=self.name + '.friction', label=fx.res('kFriction'))
        cmds.attrFieldSliderGrp(self.prefix + 'damping', attribute=self.name + '.damping', label=fx.res('kDamping'))
        cmds.attrFieldSliderGrp(self.prefix + 'mass', attribute=self.name + '.mass', label=fx.res('kMass'))
        cmds.attrEnumOptionMenuGrp(self.prefix + 'collisionShape', attribute=self.name + '.collisionShape', label=fx.res('kCollisionShape'))
        cmds.attrFieldSliderGrp(self.prefix + 'collisionShapeScale', attribute=self.name + '.collisionShapeScale', label=fx.res('kCollisionShapeScale'))
        cmds.attrControlGrp(self.prefix + 'collisionContactMaskLayers', attribute=self.name + '.collisionContactMaskLayers', label=fx.res('kCollisionContactMaskLayers'))
        cmds.attrControlGrp(self.prefix + 'collisionMaskLayers', attribute=self.name + '.collisionMaskLayers', label=fx.res('kCollisionMaskLayers'))
        cmds.attrControlGrp(self.prefix + 'collisionGroupLayers', attribute=self.name + '.collisionGroupLayers', label=fx.res('kCollisionGroupLayers'))
        self.hasControls = True

    def removeControls(self):
        if self.hasControls:
            cmds.deleteUI(self.prefix + 'bounce', control=True)
            cmds.deleteUI(self.prefix + 'friction', control=True)
            cmds.deleteUI(self.prefix + 'damping', control=True)
            cmds.deleteUI(self.prefix + 'mass', control=True)
            cmds.deleteUI(self.prefix + 'collisionShape', control=True)
            cmds.deleteUI(self.prefix + 'collisionShapeScale', control=True)
            cmds.deleteUI(self.prefix + 'collisionContactMaskLayers', control=True)
            cmds.deleteUI(self.prefix + 'collisionMaskLayers', control=True)
            cmds.deleteUI(self.prefix + 'collisionGroupLayers', control=True)
            self.hasControls = False

    def updateVisibility(self):
        self.removeControls()
        isCollider = cmds.objExists(self.name+'.collisionShape')

        if isCollider:
            self.setLayoutHidden('mashFrame', False)
            self.addAttributes()
        else:
            self.setLayoutHidden('mashFrame', True)

    def nodeChanged(self):
        self.updateVisibility()

def createColliderAttributes(node):
    cmds.addAttr(node, longName='bounce', min=0, softMaxValue=1, dv=0.2, at='double', hidden=True)
    cmds.addAttr(node, longName='friction', min=0, softMaxValue=1, dv=0.2, at='double', hidden=True)
    cmds.addAttr(node, longName='damping', min=0, softMaxValue=1, dv=0.01, at='double', hidden=True)
    cmds.addAttr(node, longName='mass', dv=1000, at='double', hidden=True)
    cmds.addAttr(node, longName='collisionShape', en="Automatic=0:Cube=1:Sphere=2:Hull=4:Mesh=5:Infinite Plane=6", at='enum', hidden=True)
    cmds.setAttr(node +'.collisionShape', 0) # Maya will default to 0 even if that's not one of the valid enums.
    cmds.addAttr(node, longName='collisionShapeScale', dv=1, at='double', hidden=True)
    cmds.addAttr(node, longName='collisionContactMaskLayers', dt='string', hidden=True)
    cmds.addAttr(node, longName='collisionMaskLayers', dt='string', hidden=True)
    cmds.addAttr(node, longName='collisionGroupLayers', dt='string', hidden=True)
    cmds.setAttr(node +'.collisionContactMaskLayers', "0", type='string')
    cmds.setAttr(node +'.collisionMaskLayers', "0", type='string')
    cmds.setAttr(node +'.collisionGroupLayers', "0", type='string')

def connectColliderObject(solverNode, colliderNode):
    #in case the object has been added and removed.
    if not cmds.objExists(colliderNode+'.collisionShape'):
        createColliderAttributes(colliderNode)

    if cmds.nodeType(solverNode) == "transform":
        solverNode = cmds.listRelatives(solverNode, s=True)[0]

    solverConnId = str(nextFreeMulti(solverNode, "collisionObjects"))
    cmds.connectAttr(colliderNode+'.bounce', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeBounce')
    cmds.connectAttr(colliderNode+'.friction', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeFriction')
    cmds.connectAttr(colliderNode+'.damping', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeDamping')
    cmds.connectAttr(colliderNode+'.mass', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeMass')
    cmds.connectAttr(colliderNode+'.collisionShape', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeType')
    cmds.connectAttr(colliderNode+'.worldMatrix[0]', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeMatrix')
    cmds.connectAttr(colliderNode+'.worldMesh[0]', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeMesh')
    cmds.connectAttr(colliderNode+'.collisionShapeScale', solverNode+'.collisionObjects['+solverConnId+'].collisionShapeScale')
    cmds.connectAttr(colliderNode+'.collisionContactMaskLayers', solverNode+'.collisionObjects['+solverConnId+'].collisionContactMaskLayers')
    cmds.connectAttr(colliderNode+'.collisionMaskLayers', solverNode+'.collisionObjects['+solverConnId+'].collisionMaskLayers')
    cmds.connectAttr(colliderNode+'.collisionGroupLayers', solverNode+'.collisionObjects['+solverConnId+'].collisionGroupLayers')

    relatives = cmds.listRelatives(colliderNode, type='transform') or []
    for transform in relatives:
        cmds.makeIdentity(relatives, apply=True, t=False, r=True, s=False, n=False, pn=True)

def removeSolverEntry(delete=True):
    selectedNodes = cmds.ls(sl=True)

    if len(selectedNodes) == 0:
        ivm.MashInViewMessage(fx.res('kSelectSolver'), "Warning")

    for solverNode in selectedNodes:
        if cmds.nodeType(solverNode) != "MASH_BulletSolver":
            shapes = cmds.listRelatives(solverNode, s=True)
            if not shapes:
                continue
            for shape in shapes:
                if cmds.nodeType(shape) == "MASH_BulletSolver":
                    removeSolver(shape, solverNode, delete)
        else:
            removeSolver(solverNode, solverNode, delete)

def removeSolver(solverNode, parent, delete):
    connectionDict = []
    #if the solver is disconnected from everything, we can just delete it
    sourceConns = cmds.listConnections(solverNode, plugs=True, connections=True, destination=False) or []
    destinationConns = cmds.listConnections(solverNode, plugs=True, connections=True, source=False) or []
    if len(sourceConns) == 0 and len(destinationConns) == 0:
        cmds.delete(parent)
        return

    solverObj = openMASH.mashGetMObjectFromNameTwo(solverNode)
    fnNode = om.MFnDependencyNode(solverObj)
    inputAttribute = fnNode.attribute("inputNetworks")
    inputPlug = om.MPlug(solverObj, inputAttribute)
    numNetworks = inputPlug.numConnectedElements()
    for i in range(numNetworks):
        element = inputPlug.elementByPhysicalIndex(i)
        inputPointsPlug = element.child(0)
        if "inputPoints" in inputPointsPlug.partialName():
            connection = cmds.listConnections( inputPointsPlug.name(), s=True, d=False, p=True)
            if connection:
                connection = connection[0]
            else:
                return # short circuit in node deletion callback
            pair = [connection, []]
            connectionDict.append(pair)
            cmds.disconnectAttr(connection, inputPointsPlug.name())

    outputAttribute = fnNode.attribute("outputPoints")
    outputPlug = om.MPlug(solverObj, outputAttribute)
    numOutputs = outputPlug.numConnectedElements()
    for i in range(numOutputs):
        element = outputPlug.elementByPhysicalIndex(i)
        connections = cmds.listConnections( element.name(), s=False, d=True, p=True)
        connectionDict[i][1] = connections

    for connection in connectionDict:
        input = connection[0]
        for output in connection[1]:
            cmds.connectAttr(input, output, force=True)

    if cmds.objExists(solverNode+".instancerMessage"):
        instancerConnection = cmds.listConnections(solverNode+'.instancerMessage', s=False, d=True, p=True)
        if instancerConnection:
            cmds.disconnectAttr(solverNode+'.instancerMessage', instancerConnection[0])

    if delete:
        cmds.delete(parent)

def addSolver():
    return cmds.createNode("MASH_BulletSolver")

class DynamicsAssignSolver(object):
    def __init__(self):
        self.dynamics = None
        self.waiter = None
        self.instancer = None
        self.newSolver = None

    def getNodes(self):
        selected = cmds.ls(sl=True)
        for node in selected:
            if cmds.nodeType(node) == "MASH_Waiter":
                self.waiter = node
                network = mapi.Network(self.waiter)
                allNodes = network.getAllNodesAndReturnList()
                for netNode in allNodes:
                    if cmds.nodeType(netNode) == "MASH_Dynamics":
                        self.dynamics = netNode
                    elif cmds.nodeType(netNode) == "MASH_Repro":
                        self.instancer = netNode
                    elif cmds.nodeType(netNode) == "instancer":
                        self.instancer = netNode
            elif cmds.nodeType(node) == "MASH_BulletSolver":
                self.newSolver = node
            elif cmds.nodeType(node) == "transform":
                shapes = cmds.listRelatives(node, s=True)
                for shape in shapes:
                    if cmds.nodeType(shape) == "MASH_BulletSolver":
                        self.newSolver = shape

        return self.assignNewSolver()

    def assignNewSolver(self):
        if not self.waiter:
            cmds.error("No MASH_Waiter selected.")
            return False
        elif not self.newSolver:
            cmds.error("No MASH_BulletSolver selected.")
            return False

        if self.dynamics:
            #disconnect from solver if connected to one already
            solver = cmds.listConnections(self.dynamics+".enable", shapes=True)
            if solver:
                solver = solver[0]
                solverParent= cmds.listRelatives(solver, p=True)[0]
                # disconnect the old solver from the network
                removeSolver(solver, solverParent, False)

                # disconnect the Dynamics node from the old solver
                allConnections = cmds.listConnections(self.dynamics, connections=True, p=True)
                for i in range(len(allConnections)):
                    if solver in allConnections[i]:
                        cmds.disconnectAttr(allConnections[i-1], allConnections[i])
        else:
            network = mapi.Network(self.waiter)
            self.dynamics = cmds.createNode('MASH_Dynamics')
            waiterInput = cmds.listConnections(self.waiter, d=False, s=True, p=True)[0]
            cmds.connectAttr(waiterInput, self.dynamics+'.inputPoints')
            cmds.connectAttr(self.dynamics+'.outputPoints',self.waiter+'.inputPoints', force=True)

        if self.waiter and self.instancer and self.newSolver:
            # connect the dynamics node to the new solver
            connectDynamics(self.dynamics, self.newSolver, self.waiter, self.instancer)
        else:
            cmds.error("No valid MASH network selected")
            return False
        return True

def assignSolver():
    solverAssign = DynamicsAssignSolver()
    return solverAssign.getNodes()

def isHeirarchyAnimated(nodenName):
    # if the mesh has an incoming connection it could be proceedural (eg. Repro) and an animCurve check won't be enough
    if cmds.nodeType(nodenName) == "mesh":
        conns = cmds.listConnections(nodenName+".inMesh") or []
        if len(conns):
            return True

    # anim curve check
    longName = mel.eval('ls -l '+nodenName) # run in mel as this will fail in Python when executed from C++
    parents = longName[0].split('|')[1:-1]
    for node in parents:
        crvs = cmds.listConnections(node, type='animCurve') or []
        if len(crvs):
            return True

    return False

def shellDynamicsEntry(name='MASH#'):
    selected = cmds.ls(sl=True)
    for node in selected:
        if cmds.nodeType(node)=='transform' or cmds.nodeType(node)=='mesh':
            mashNetwork = mapi.Network()
            mashNetwork.createShellDynamics(node, name=name)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
