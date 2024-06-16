#THIS CLASS MIXES PYTHON API 2.0 with 1.0

from builtins import object
from builtins import range
import math

import maya.cmds as mc
import maya.api.OpenMaya as nom
import maya.OpenMaya as old
from maya.api.OpenMayaAnim import MAnimControl

"""
    Given a node name this returns the MObject for that node.
    Python API 2.0
    :return: returns The node's MObject
"""
def mashGetMObjectFromNameTwo(nodeName):
    sel = nom.MSelectionList()
    sel.add(nodeName)
    thisNode = sel.getDependNode(0)
    return thisNode

"""
    Given a node name this returns the MObject for that node.
    Python API 1.0
    :return: returns The node's MObject
"""
def mashGetMObjectFromNameOne(nodeName):
    sel = old.MSelectionList()
    sel.add(nodeName)
    thisNode = old.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode

class MASHData(object):
    """
    MASHData prepares data from a MASH network, ready for use with the MASH_Python node.
    It also provides utility funcitons to make working with this data easier.
    This class uses the MAYA Python API 2.0
    """
    def __init__(self, nodeName):
        """
        Construct a new 'MASHData' object.

        :param  -- nodeName: The name of the MASH Python node
        :object -- thisNode: The MObject of this node
        :object -- fnNode: MFnDependencyNode function set of this node
        :return -- nothing
        """
        self.usingDynamicArrays = False
        self.initialised = False
        self.nodeName = nodeName
        self.thisNode = mashGetMObjectFromNameTwo(nodeName)
        self.fnNode = nom.MFnDependencyNode(self.thisNode)
        self.position = nom.MVectorArray()
        self.scale = nom.MVectorArray()
        self.rotation = nom.MVectorArray()
        self.id = nom.MDoubleArray()
        self.visibility = nom.MDoubleArray()
        #dynamic array attributes (used if the Python node is placed between the Waiter and the Repro node)
        self.color = nom.MVectorArray()
        self.uvTile = nom.MVectorArray()
        self.frame = nom.MDoubleArray()
        self.isAnimated = nom.MIntArray()
        self.velocity = nom.MDoubleArray()
        self.angularVelocity = nom.MDoubleArray()
        self.velocityVec = nom.MVectorArray()
        self.angularVelocityVec = nom.MVectorArray()
        self.strength = nom.MVectorArray()

        #set up out arrays
        self.outPosition = nom.MVectorArray()
        self.outRotation = nom.MVectorArray()
        self.outScale = nom.MVectorArray()
        self.outId = nom.MDoubleArray()
        self.outVisibility = nom.MDoubleArray()
        #dynamic array attributes (used if the Python node is placed between the Waiter and the Repro node)
        self.outColor = nom.MVectorArray()
        self.outUvTile = nom.MVectorArray()
        self.outFrame = nom.MDoubleArray()
        self.outIsAnimated = nom.MIntArray()
        self.outVelocity = nom.MDoubleArray()
        self.outVelocityVec = nom.MVectorArray()
        self.outAngularVelocity = nom.MDoubleArray()
        self.outAngularVelocityVec = nom.MVectorArray()

        pointsAttribute = self.fnNode.attribute("outputPoints")
        pointsPlug = nom.MPlug(self.thisNode, pointsAttribute)
        self.usingDynamicArrays = pointsPlug.isConnected

        self.getData() #get the input data

    def getColorSet(self, setName):
        thisNodeOld = mashGetMObjectFromNameOne(self.nodeName)
        fnThisNode = old.MFnDependencyNode(thisNodeOld)
        inPointsAttribute = fnThisNode.attribute("inputPoints")
        inPointsPlug = old.MPlug( thisNodeOld, inPointsAttribute )
        inPointsObj = inPointsPlug.asMObject()
        inputPointsData = old.MFnArrayAttrsData(inPointsObj)
        colourSetName = "cs_"+setName
        dataType = old.MFnArrayAttrsData.Type
        if inputPointsData.checkArrayExist(colourSetName, dataType):
            pass

    #get a specific Transformation Matrix
    def getMatrix(self, pointId):
        """
        Returns an MTransformationMatrix of the specified point.
        """
        tm = nom.MTransformationMatrix()
        tm.setTranslation(self.position[pointId], nom.MSpace.kWorld)
        tm.setScale(self.scale[pointId], nom.MSpace.kWorld)
        ro = nom.MTransformationMatrix.kXYZ;
        rotation = self.rotation[pointId]
        angles =  nom.MEulerRotation(math.radians(rotation.x),math.radians(rotation.y),math.radians(rotation.z))
        tm.setRotation(angles)
        return tm

    #get a specific Transformation Matrix
    def setMatrix(self, matrix, pointId):
        """
        Sets the MTransformationMatrix for the specific point.
        """
        pos = matrix.translation(nom.MSpace.kWorld)
        eulerRot = matrix.rotation()
        angles = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
        scale = matrix.scale(nom.MSpace.kWorld)
        self.outPosition[pointId] = pos
        self.outRotation[pointId] = angles
        self.outScale[pointId] = scale

    def createLocalMatrix(position, rotation, scale):
        """
        Returns a local MTransformationMatrix
        """
        tm = om.MTransformationMatrix()
        tm.setTranslation(position, om.MSpace.kObject)
        tm.setScale((scale.x,scale.y,scale.z), om.MSpace.kWorld)
        ro = om.MTransformationMatrix.kXYZ
        radAngles = om.MVector(math.radians(rotation.x),math.radians(rotation.y), math.radians(rotation.z))
        eulerRot = om.MEulerRotation(radAngles, ro  )
        tm.rotateBy(eulerRot, om.MSpace.kObject)
        return tm

    def getData(self):
        """
        Internal - called from init. Gets the data from the in attributes and sets it to the class variables.
        """
        self.position = self.getVectorArray("positionInPP")
        self.rotation = self.getVectorArray("rotationInPP")
        self.scale = self.getVectorArray("scaleInPP")

        inVis = self.getVectorArray("visibilityInPP")
        inId = self.getVectorArray("idInPP")

        #vis and id travel through MASH as vectors
        self.visibility = nom.MDoubleArray(len(self.position), 1.0)
        for i in (list(range(0, len(inVis)))):
            self.visibility[i] = inVis[i].x

        self.id = nom.MDoubleArray(len(self.position), 0.0)
        for i in (list(range(0, len(inId)))):
            self.id[i] = inId[i].x

        self.outPosition = self.position
        self.outRotation = self.rotation
        self.outScale = self.scale
        self.outVisibility = self.visibility
        self.outId = self.id

        #get all the axillury channels
        if self.usingDynamicArrays:
            self.color = self.getVectorArray("colorInPP")
            self.uvTile = self.getVectorArray("uvTileInPP")
            self.frame = self.getDoubleArray("frameInPP")
            self.velocity = self.getDoubleArray("velocityInPP")
            self.isAnimated = self.getIntArray("isAnimatedInPP")
            self.angularVelocity = self.getDoubleArray("angularVelocityInPP")
            self.velocityVec = self.getVectorArray("velocityVecInPP")
            self.angularVelocityVec = self.getVectorArray("angularVelocityVecInPP")
            self.strength = self.getVectorArray("calculatedStrength")

            self.outColor = self.color
            self.outUvTile = self.uvTile
            self.outFrame = self.frame
            self.outVelocity = self.velocity
            self.outIsAnimated = self.isAnimated
            self.outAngularVelocity = self.angularVelocity
            self.outVelocityVec = self.velocityVec
            self.outAngularVelocityVec = self.angularVelocityVec

    #returns the number of points
    def count(self):
        """
        Returns the number of points in the MASH network.
        """
        return len(self.position)

    def setData(self):
        """
        Set the data to the out attributes.
        """
        self.setVectorArray("positionOutPP", self.outPosition)
        self.setVectorArray("rotationOutPP", self.outRotation)
        self.setVectorArray("scaleOutPP", self.outScale)

        #for legacy reasons, out visibility and ID travel through MASH as vector arrays, so convert the doubles to vectors
        outVis = nom.MVectorArray(len(self.position), nom.MVector(1.0, 1.0, 1.0))
        for i in (list(range(0, len(self.outVisibility)))):
            outVis[i] = nom.MVector(self.outVisibility[i], self.outVisibility[i], self.outVisibility[i])

        outId = nom.MVectorArray(len(self.position), nom.MVector(0.0, 0.0, 0.0))
        for i in (list(range(0, len(self.outId)))):
            outId[i] = nom.MVector(self.outId[i], self.outId[i], self.outId[i])

        self.setVectorArray("visibilityOutPP", outVis)
        self.setVectorArray("idOutPP", outId)

        if self.usingDynamicArrays:
            self.setVectorArray("colorOutPP", self.outColor)
            self.setVectorArray("uvTileOutPP", self.outUvTile)
            self.setDoubleArray("frameOutPP", self.outFrame)
            self.setDoubleArray("velocityOutPP", self.outVelocity)
            self.setVectorArray("velocityVecOutPP", self.outVelocityVec)
            self.setDoubleArray("angularVelocityOutPP", self.outAngularVelocity)
            self.setVectorArray("angularVelocityVecOutPP", self.outAngularVelocityVec)
            self.setIntArray("isAnimatedOutPP", self.outIsAnimated)

    def setVectorArray(self, channelName, array):
        """
        Sets the specified vector array to the specified attribute
        """
        outAttribute = self.fnNode.attribute(channelName)
        outPlug = nom.MPlug( self.thisNode, outAttribute )
        outData = nom.MFnVectorArrayData()
        outData.create(array)
        outPlug.setMObject(outData.object())

    def setDoubleArray(self, channelName, array):
        """
        Sets the specified double array to the specified attribute
        """
        outAttribute = self.fnNode.attribute(channelName)
        outPlug = nom.MPlug( self.thisNode, outAttribute )
        outData = nom.MFnDoubleArrayData()
        outData.create(array)
        outPlug.setMObject(outData.object())

    def setIntArray(self, channelName, array):
        """
        Sets the specified double array to the specified attribute
        """
        outAttribute = self.fnNode.attribute(channelName)
        outPlug = nom.MPlug( self.thisNode, outAttribute )
        outData = nom.MFnIntArrayData()
        outData.create(array)
        outPlug.setMObject(outData.object())

    def getDoubleArray(self, channelName):
        """
        Returns a double array from the specified attribute
        """
        inAttribute = self.fnNode.attribute(channelName)
        inPlug = nom.MPlug( self.thisNode, inAttribute )
        inPointsObj = inPlug.asMObject()
        inputPPData = nom.MFnDoubleArrayData(inPointsObj)
        inArray = inputPPData.array()
        copiedArray = inArray[:] #we absolutly do not want to work with a refrence
        return copiedArray

    def getIntArray(self, channelName):
        """
        Returns an int array from the specified attribute
        """
        inAttribute = self.fnNode.attribute(channelName)
        inPlug = nom.MPlug( self.thisNode, inAttribute )
        inPointsObj = inPlug.asMObject()
        inputPPData = nom.MFnIntArrayData(inPointsObj)
        inArray = inputPPData.array()
        copiedArray = inArray[:] #we absolutly do not want to work with a refrence
        return copiedArray

    def getVectorArray(self, channelName):
        """
        Returns a vector array from the specified attribute
        """
        inAttribute = self.fnNode.attribute(channelName)
        inPlug = nom.MPlug( self.thisNode, inAttribute )
        inPointsObj = inPlug.asMObject()
        inputPPData = nom.MFnVectorArrayData(inPointsObj)
        inArray = inputPPData.array()
        copiedArray = inArray[:] #we absolutly do not want to work with a refrence
        return copiedArray

    def getNamedArray(self, channelName, typeName):
        """
        Returns a vector array from the specified channel name
        Please note, there is no write equivalent of this method.
        """
        copiedArray = []
        thisNodeOld = mashGetMObjectFromNameOne(self.nodeName)
        fnNode = old.MFnDependencyNode(thisNodeOld)
        pointsAttribute = fnNode.attribute("inputPoints")
        pointsPlug = old.MPlug(thisNodeOld, pointsAttribute)
        handle = pointsPlug.asMDataHandle();
        handleData = handle.data();
        inputPointsData = old.MFnArrayAttrsData(handleData)
        channels = inputPointsData.list()
        if channelName in channels:
            if typeName == "vector":
                dynamicArray = inputPointsData.getVectorData(channelName)
                self.channelToList(dynamicArray, copiedArray)
            elif typeName == "double":
                copiedArray = inputPointsData.getDoubleData(channelName)[:]
        pointsPlug.destructHandle(handle)
        return copiedArray

    def getNamedArrays(self):
        """
        Returns all the array names in the dynamic array data
        """
        thisNodeOld = mashGetMObjectFromNameOne(self.nodeName)
        fnNode = old.MFnDependencyNode(thisNodeOld)
        pointsAttribute = fnNode.attribute("inputPoints")
        pointsPlug = old.MPlug(thisNodeOld, pointsAttribute)
        handle = pointsPlug.asMDataHandle();
        handleData = handle.data();
        inputPointsData = old.MFnArrayAttrsData(handleData)
        channels = inputPointsData.list()
        pointsPlug.destructHandle(handle)
        return channels

    def getFalloffsCount(self):
        """
        Returns the number of falloff objects.
        """
        inAttribute = self.fnNode.attribute("strengthPP")
        inPlug = nom.MPlug( self.thisNode, inAttribute )
        return inPlug.numConnectedElements()

    #we get falloffs individually because it's more flexible
    def getFalloff(self, index):
        """
        Returns a doubleArray of strengths from a falloff object at the index specified.
        This happens through the old Maya Python API due to lack of support for MFnFloatArrayData in 2.0
        """
        oneNode = mashGetMObjectFromNameOne(self.nodeName)
        oneNodeFn = old.MFnDependencyNode(oneNode)
        inAttribute = oneNodeFn.attribute("strengthPP")
        inPlug = old.MPlug( oneNode, inAttribute )
        if (inPlug.numConnectedElements() > index):
            inPlug = inPlug.connectionByPhysicalIndex( index )
            inPointsObj = inPlug.asMObject()
            inputPPData = old.MFnFloatArrayData(inPointsObj)
            inArray = inputPPData.array()
            return inArray[:]

    def getFrame(self):
        """
        Returns the current frame. We do this via the MAnimControl and so it works reguardless of the state of the time attribute.
        """
        currentTime = MAnimControl.currentTime()
        timeUnit = nom.MTime.uiUnit()
        frame = int(currentTime.asUnits(timeUnit))
        return frame

    def setPointCount(self, count):
        """
        Resizes all the out arrays with default values - thus changing the point count.
        """
        self.resizeMArray(self.outPosition, count, nom.MVector(0.0,0.0,0.0))
        self.resizeMArray(self.outRotation, count, nom.MVector(0.0,0.0,0.0))
        self.resizeMArray(self.outScale, count, nom.MVector(1.0,1.0,1.0))
        self.resizeMArray(self.outVisibility, count, 1)
        self.resizeMArray(self.outId, count, 0)

        if self.usingDynamicArrays:
            self.resizeMArray(self.outColor, count, nom.MVector(0.0,0.0,0.0))
            self.resizeMArray(self.outUvTile, count, nom.MVector(0.0,0.0,0.0))
            self.resizeMArray(self.outFrame, count, 0)
            self.resizeMArray(self.outVelocity, count, 0)
            self.resizeMArray(self.outAngularVelocity, count, 0)
            self.resizeMArray(self.outVelocityVec, count, nom.MVector(0.0,0.0,0.0))
            self.resizeMArray(self.outAngularVelocityVec, count, nom.MVector(0.0,0.0,0.0))
            self.resizeMArray(self.outIsAnimated, count, 0)

    def resizeMArray(self, l, newsize, obj=None):
        """
        If growing:
        Rather then using .setLength() we append to an MArray one by one in order to give ourselves a default value.
        If shrinking:
        Delete the unneeded entries.
        """
        if newsize > len(l):
            #append one by one to give us a default value
            for i in range (len(l), newsize, 1):
                l.append(obj)
        else:
            del l[newsize:]

    def channelToList(self, channel, destination):
        if channel == None or channel.length() == 0:
            return

        if channel.__class__.__name__ == "MVectorArray":
            for i in range (0, channel.length(), 1):
                vec = (channel[i].x, channel[i].y, channel[i].z)
                destination.append(vec)# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
