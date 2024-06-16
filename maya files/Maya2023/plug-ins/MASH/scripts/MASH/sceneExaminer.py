# TODO
# Matrix attributes

# Usage:
# import MASH.sceneExaminer as se
# log = se.scanNodes()
# print log

from builtins import zip
from builtins import range
import maya.api.OpenMaya as om
import maya.cmds as cmds
import maya.OpenMaya as oldApi
import maya.app.type.typeUtilityScripts as ttUtil
import six

LOGGING_ERRORS = False
ALLOWED_NON_KEYABLE_DATA_TYPES = ['string', 'enum', 'bool']

def getNodeMObject(nodeName):
    '''
    | Gets the MObject for a node using Maya's Python API 2.0
    | :param  -- nodeName: The node you want an MObject for
    | :return -- An MObject
    '''
    sel = om.MSelectionList()
    sel.add(nodeName)
    thisNode = sel.getDependNode(0)
    return thisNode

def getNodeMObjectOldApi(nodeName):
    '''
    | Gets the MObject for a node using Maya's Python API 1.0
    | :param  -- nodeName: The node you want an MObject for
    | :return -- An MObject
    '''
    sel = oldApi.MSelectionList()
    sel.add(nodeName)
    thisNode = oldApi.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode

def areTuplesAlmostEqual(X, Y):
    '''
    | Compares if all values in 2 tuples are equal to 5 decimal places
    | :param  -- x: A tuple to compare
    | :param  -- y: A tuple to compare against
    | :return -- True or False
    '''
    return all(round(x-y, 5) == 0 for x,y in zip(X, Y))

def tryFunctionSets(attribute, fullName, restore, changeLog):
    '''
    | Assigns function sets to an attribute MObject and logs or restores them
    | :param  -- attribute: The attribute MObject
    | :param  -- fullName: The full attribute path
    | :param  -- restore: Restore this attribute to it's default state
    | :param  -- changeLog: Log of the Maya commands needed to get the attribute into it's current state
    | :return -- None
    '''

    attributeFnSets = [om.MFnNumericAttribute, om.MFnEnumAttribute, om.MFnMatrixAttribute, om.MFnTypedAttribute, om.MFnUnitAttribute]
    
    for fn in attributeFnSets:
        attributeFn = fn(attribute)
        if attributeFn.object().isNull():
            continue
        try:
            inspectAttributeFunctionSet(attributeFn, fullName, changeLog, restore)
        except Exception as e:
            if LOGGING_ERRORS:
                print("Problem with attribute: " + fullName + "\n" + str(e))
        break

def scanNodes(restore=False, attributes=None, skipAttributes=None, nodes=None):
    '''
    | Scans nodes and resets them to their default state or logs the changes that have been made to them
    | :param  -- restore: Restore this attribute to it's default state
    | :param  -- attributes: Optional list - The attributes to check on the nodes
    | :param  -- nodes: Optional list - The noes to check in the scene, if this list is empty, the selected nodes will be checked
    | :return -- None
    '''
    changeLog = []

    if nodes is None:
        nodes = cmds.ls(sl=True)

    for node in nodes:
        workingWithType = False
        if cmds.nodeType(node) == "transform":
            # find a type node if there is one
            messageConn = cmds.listConnections (node+".message", d=True, s=False, p=False) or []
            typeNode = None
            for connNode in messageConn:
                 if cmds.nodeType(connNode) == "type":
                     typeNode = connNode
                     break
                     
            if typeNode:
                nodes.append(typeNode)
                animationConn = cmds.listConnections (typeNode+".animationMessage", d=True, s=False, p=False) or []
                extrudeConn = cmds.listConnections (typeNode+".extrudeMessage", d=True, s=False, p=False) or []
                remeshConn = cmds.listConnections (typeNode+".remeshMessage", d=True, s=False, p=False) or []
                if len(animationConn):
                    nodes.append(animationConn[0])
                if len(extrudeConn):
                    nodes.append(extrudeConn[0])
                if len(remeshConn):
                    nodes.append(remeshConn[0])
                workingWithType = True
                if skipAttributes is None:
                    skipAttributes = ['textInput', 'homeFolder', 'fontError']

        changeLog.append("#### SET ATTRIBUTES FOR "+node+" ####")
        changeLog.append("#### These commands are automatically generated ####")

        thisNode = getNodeMObject(node)
        fnNode = om.MFnDependencyNode(thisNode)

        checkAttributes = []
        if attributes is None:
            checkAttributes = cmds.listAttr(node, multi=False, inUse=True, hasData=True)
        else:
            checkAttributes = attributes
        
        # Scan all attributes in the checkAttributes list
        for attr in checkAttributes:
            # skip unwanted attributes
            if skipAttributes and attr in skipAttributes:
                continue

            # user may have specified attributes that don't exist
            dataType = ''
            if cmds.objExists(node+'.'+attr):
                dataType = cmds.getAttr(node+'.'+attr, type=True)
            else:
                continue

            # ignore leaf attributes
            attr = attr.split('.')[0]

            # get the plug
            attribute = fnNode.attribute(attr)    
            plug = om.MPlug( thisNode, attribute )
            fullName = ""

            # check the plug is valid
            if not plug.isNull and not plug.isLocked and not plug.isConnected and plug.isKeyable or plug.isArray or dataType in ALLOWED_NON_KEYABLE_DATA_TYPES:
                fullName = plug.partialName(includeNodeName=True, useFullAttributePath=True, useLongNames=True)
            else:
                continue

            # Handle MCurveAttributes and MRampAttributes which are special compounds
            if plug.isArray:
                # First we need to 'fix' the MCurveAttribute so that setAttr will work
                # As Maya's Python 2.0 API doesn't contain a curve attribute wrapper we revert to 1.0 for this
                try:
                    oldNode = getNodeMObjectOldApi(node)
                    oldFnNode = oldApi.MFnDependencyNode(oldNode)
                    oldAttribute = oldFnNode.attribute(attr)    
                    oldPlug = oldApi.MPlug( oldNode, oldAttribute )
                    curveAttribute = oldApi.MCurveAttribute(oldNode, oldAttribute)
                    curveAttribute.pack()
                    curveAttribute.sort()
                except:
                    pass

                for x in range(0,plug.numElements()):
                    child = plug.elementByPhysicalIndex(x)
                    # These two conditions are satisfied by Curve and Ramp attrs
                    if child.isCompound and child.numChildren() == 2:
                        positionPlug = child.child(0)
                        valuePlug = child.child(1)
                        positionName = positionPlug.partialName(includeNodeName=True, useFullAttributePath=True,useLongNames=True)
                        valueName = valuePlug.partialName(includeNodeName=True, useFullAttributePath=True,useLongNames=True)
                        # Final safety check
                        if "Value" in valueName and "Position" in positionName:
                            tryFunctionSets(positionPlug.attribute(), positionName, restore, changeLog)
                            tryFunctionSets(valuePlug.attribute(), valueName, restore, changeLog)
                            # We can only reset Type curves because defaults are not discoverable for other nodes that use curves/ramps
                            if workingWithType and restore:
                                ttUtil.resetTypeCurve(node,attr)

                # Otherwise we don't support compounds.
                continue
            
            # we're now done with edge cases, so lets examine any other supported attributes
            tryFunctionSets(attribute, fullName, restore, changeLog)
        
        '''
        # This section scans for animated attributes
        # It can either disconnect the animation curve (and delete it)
        # Or it can log a script that would recreate this animation from scratch
        '''
        animatedChannels = cmds.listConnections(node, type="animCurve", c=True) or []
        for x in range  (0, len(animatedChannels), 2):
            curve = animatedChannels[x+1]
            channel = animatedChannels[x]
            
            changeLog.append("#### SET KEYFRAMES FOR "+node+" ####")
            changeLog.append("#### These commands are automatically generated ####")

            keyCount = cmds.keyframe( channel, query=True, keyframeCount=True )

            keyTimes = cmds.keyframe( channel, query=True, timeChange=True)
            keyValues = cmds.keyframe( channel, query=True, valueChange=True)
            inAngles =  cmds.keyTangent( channel, query=True, inAngle=True)
            outAngles =  cmds.keyTangent( channel, query=True, outAngle=True)
            inWeights =  cmds.keyTangent( channel, query=True, inWeight=True)
            outWeights =  cmds.keyTangent( channel, query=True, outWeight=True)

            changeLog.append("keyCount = " + str(keyCount))
            changeLog.append("keyTimes = " + str(keyTimes))
            changeLog.append("keyValues = " + str(keyValues))
            changeLog.append("inAngles = " + str(inAngles))
            changeLog.append("outAngles = " + str(outAngles))
            changeLog.append("inWeights = " + str(inWeights))
            changeLog.append("outWeights = " + str(outWeights))
            changeLog.append("channel = '" + channel + "'")

            changeLog.append("for t in range(0, keyCount):" )
            changeLog.append("    cmds.setKeyframe( channel, t=keyTimes[t], v=keyValues[t] )")

            changeLog.append("    cmds.selectKey(clear=True)")
            changeLog.append("    cmds.selectKey(channel, k=True, t=(keyTimes[t],keyTimes[t]))")
            changeLog.append("    cmds.keyTangent(edit=True, weightedTangents=True)")
            changeLog.append("    cmds.keyTangent(weightLock=False)")
            changeLog.append("    cmds.keyTangent(lock=False)")
            changeLog.append("    cmds.keyTangent(itt='flat',ott='flat')")

            changeLog.append("    curve = cmds.listConnections(channel, type='animCurve')")
            changeLog.append("    cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), outAngle=outAngles[t], outWeight=outWeights[t])")
            changeLog.append("    cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), inAngle=inAngles[t], inWeight=inWeights[t])")
        
            if restore:
                cmds.delete(channel)
                
    return changeLog

'''
| This method takes a function set, tries to work out what kind of attribute it is and depending on the supplied arguements
| It will reset the attributes to their default values.
| And/ Or
| Log the Maya commands needed to recreate this node state on another node of this type.
| :param  -- attributeFn: The attribute function set
| :param  -- fullName: The full attribute path
| :param  -- restore: Restore this attribute to it's default state
| :param  -- logChanges: Log of the Maya commands needed to get the attribute into it's current state
| :return -- None
'''
def inspectAttributeFunctionSet(attributeFn, fullName, changeLog, restore=True):
    defaultValue = attributeFn.default
    if type(defaultValue) is tuple:
        value = cmds.getAttr(fullName)[0]
        almostEqual = areTuplesAlmostEqual(defaultValue, value)
        if not almostEqual:
            command = "cmds.setAttr('"+fullName+"'"
            for entry in value:
                command += ", "+str(entry)
            changeLog.append(command+")")
            if restore:
                cmds.setAttr(fullName, defaultValue[0], defaultValue[1], defaultValue[2])
    elif type(defaultValue) is om.MDistance or type(defaultValue) is om.MAngle or type(defaultValue) is om.MTime:
        value = cmds.getAttr(fullName)
        if defaultValue.value != value and isinstance(value, (six.integer_types, float)):
            changeLog.append("cmds.setAttr('"+fullName+"', "+str(value)+")")
        if restore:
            cmds.setAttr(fullName, defaultValue.value)
    else:
        try:
            attributeFn.attrType() == om.MFnData.kString
            data = om.MFnStringData(defaultValue)
            value = cmds.getAttr(fullName)
            if data.string() != value:
                changeLog.append("cmds.setAttr('"+fullName+"', '"+value+"', type='string')")
            if restore:
                cmds.setAttr(fullName, data.string(), type='string')
        except AttributeError:
            value = cmds.getAttr(fullName)
            if defaultValue != value and isinstance(value, (six.integer_types, float)):
                changeLog.append("cmds.setAttr('"+fullName+"', "+str(value)+")")
            if restore:
                cmds.setAttr(fullName, defaultValue)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
