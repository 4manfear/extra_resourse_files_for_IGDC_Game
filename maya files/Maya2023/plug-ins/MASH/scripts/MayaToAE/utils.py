from __future__ import division
from builtins import range
from builtins import zip
from maya.app.flux.imports import *
import maya.app.flux.core as fx

import maya.OpenMayaUI as omui
import maya.api.OpenMayaAnim as oma
import math
import time

camera = 'camera'
locator = 'locator'
light = 'light'
apiTypes = [camera, light, locator]
commonAttr = ['translate', 'rotate', 'scale']
lightAttr = ['color', 'intensity', 'coneAngle']
cameraAttr = ['focalLength', 'horizontalFilmAperture']
locatorAttr = []
specificAttr = {light:lightAttr, camera:cameraAttr, locator:locatorAttr, 'solid':[], 'mesh':[]}
allSpecificAttributes = [y.lower() for x in list(specificAttr.values()) for y in x]

# ==============
# STRING RESOURCES
# Plug-in has to be loaded or string resources will not initialize
if not cmds.pluginInfo( 'MASH', query=True, loaded=True ):
    cmds.loadPlugin( 'MASH' )
def getResource(name):
    return mel.eval('getPluginResource("MASH", "' + name + '")')

_SR = {
    'Sending To AE ...': getResource('kM2AE_Sending_To'),
    'AE Live Link Export Canceled': getResource('kM2AE_Export_Canceled'),
    'Exported to': getResource('kM2AE_Exported_To'),
    'AE Live Link Import Canceled': getResource('kM2AE_Import_Canceled'),
    'Opening file failed.': getResource('kM2AE_Opening_Failed'),
    'Choose file to import from:': getResource('kM2AE_Choose_File'),
    'Choose file to export to:': getResource('kM2AE_Choose_File_Export')
}

def isValidNode(name):
    return bool(getObjType(name))

def getObjChild(name):
    relatives = cmds.listRelatives(name, f=True)
    if not relatives: return None
    return relatives[0]

def getObjType(name):
    relatives = cmds.listRelatives(name, f=True)

    if (relatives is None) or len(relatives)==0: return None

    nodeType = cmds.nodeType(relatives[0])

    if nodeType and nodeType == 'mesh':
        if 'plane' in name.lower():
            return ['solid', 'mesh']
        else:
            return ['mesh', 'locator']

    for apiType in apiTypes:
        if apiType in nodeType.lower():
            return [apiType, nodeType]

    return None

def getValidAttributes(name):
    mayaAttrs = []
    apiAttrs = []
    vAttrs = {'mayaAttrs':mayaAttrs, 'apiAttrs':apiAttrs}

    myType = getObjType(name)
    if myType is None: return []

    apiType, nodeType = myType
    vAttrs['type'] = nodeType
    
    for attr in commonAttr:
        if cmds.attributeQuery(attr, node=name, ex=True):
            mayaAttrs.append(name + '.' + attr)
            apiAttrs.append(attr)

    child = getObjChild(name)
    if child:
        for attr in specificAttr[apiType]:
            if cmds.attributeQuery(attr, node=child, ex=True):
                mayaAttrs.append(child + '.' + attr)
                apiAttrs.append(attr)

    return vAttrs

def getName():
    return (cmds.file(q=True, sn=True, shortName=True) or 'untitled')

def getPrefs():
    start = cmds.playbackOptions(q=True, ast=True)
    end = cmds.playbackOptions(q=True, aet=True)
    fps = mel.eval("currentTimeUnitToFPS;")

    name = getName()
    width = cmds.getAttr('defaultResolution.width')
    height = cmds.getAttr('defaultResolution.height')
    pixelAspect = cmds.getAttr('defaultResolution.pixelAspect')
    duration = (end - start + 1)/fps
    frameRate = fps
    prefs = {'name':name, 'width':width, 'height':height, 'pixelAspect':pixelAspect, 'duration':duration, 'frameRate':frameRate}
    return prefs


def createAttrFromData(name, attr, values, times):
    if len(times) == 0:
        cmds.setAttr(name + '.' + attr, values[0])
    else:
        if 'rotate' in attr.lower():
            values = [math.radians(x) for x in values]
        curve = oma.MFnAnimCurve()
        plug = getAttributePlug(name, attr)
        curve.create(plug)
        curve.addKeys(times, values)

def createTrippleAttrFromData(name, attr, ext, values, times):
    for i in range(3):
        v = [x[i] for x in values]
        createAttrFromData(name, attr + ext[i], v, times)

def registerLayers(data, globalScale):
    globalScale = 1.0 / globalScale
    fps = mel.eval("currentTimeUnitToFPS;")

    for layer in data:

        #Create node
        name = None

        if layer['type'] == 'camera':
            name = cmds.camera()

        if layer['type'] == 'light':

            if layer['lightType'] == 'point':
                name = cmds.pointLight()
            elif layer['lightType'] == 'spot':
                name = cmds.spotLight()
            elif layer['lightType'] == 'ambient':
                name = cmds.ambientLight()
            elif layer['lightType'] == 'directional':
                name = cmds.directionalLight()

            # Get transformer name - maya bug
            name = cmds.listRelatives(name, parent=True, f=True)

        if layer['type'] == 'locator':
            name = cmds.spaceLocator()

        if layer['type'] == 'solid':
            name = cmds.polyPlane()
        
        name = name[0]

        node = getMObjectFromName(name)
        fnNode = nom.MFnDependencyNode(node)
        name = fnNode.setName('AE_' + layer['name'])

        #Create Attributes
        transformExt = ['X', 'Y', 'Z']
        colorExt = ['R', 'G', 'B']
        attrs = ['translate', 'rotate', 'scale', 'color', 'intensity', 'coneAngle', 'zoom']

        for attr in attrs:
            if attr in layer:
                values = layer[attr]['values']
                times = layer[attr]['times']
                times = [x * fps for x in times]

                if attr == 'translate':
                    values = [convertTranslations(v) for v in values]
                    for i,v in enumerate(values):
                        values[i] = [x * globalScale for x in v]
                    createTrippleAttrFromData(name, attr, transformExt, values, times) 

                elif attr == 'rotate':
                    values = [convertRotationsBack(v) for v in values]

                    if layer['type'] == 'solid':
                        values = [[v[0] + 90, v[1], v[2]] for v in values]

                    createTrippleAttrFromData(name, attr, transformExt, values, times)

                elif attr == 'scale':
                    if layer['type'] == 'solid':
                        values = [[v[0] / 100.0, v[1] / 100.0, v[2] / 100.0] for v in values]
                    for i,v in enumerate(values):
                        values[i] = [x * globalScale for x in v]

                    createTrippleAttrFromData(name, attr, transformExt, values, times)

                elif attr == 'color':
                    createTrippleAttrFromData(name, attr, colorExt, values, times)

                elif attr == 'intensity':
                    values = [v / 100.0 for v in values]
                    createAttrFromData(name, attr, values, times)

                elif attr == 'coneAngle':
                    createAttrFromData(name, attr, values, times)

                elif attr == 'zoom':
                    horizontalFilmAperture = cmds.getAttr(name + '.horizontalFilmAperture') * 25.4
                    compWidth = float(layer['compWidth'])
                    values = [v * horizontalFilmAperture / compWidth for v in values]
                    createAttrFromData(name, 'focalLength', values, times)


def getNodeDataForAttr(data, name, attr):
    data += getKeyFrames(name, attr)

    if attr == 'translate':
        for camera in getAimCameras(name):
            data += getKeyFrames(camera, 'rotate')
    if attr == 'rotate' or attr == 'scale':
        data += getKeyFrames(name, 'translate')


def getNodeDataForAllAttr(data, uuid):
    name = cmds.ls(uuid, long=True)[0]
    vAttrs = getValidAttributes(name)
    if vAttrs:
        for attr in vAttrs['apiAttrs']:
            data += getKeyFrames(name, attr)


def getKeyFrames(name, attr):
    uuid = cmds.ls(name, uuid=True)[0]
    apiType, mayaType = getObjType(name)
    objData = {'name': name, 'type': mayaType, 'uuid':uuid}

    if apiType == 'mesh':
        objData['name'] += '_Location'

    if (apiType not in ['locator', 'solid', 'mesh']) and attr=='scale':
        return []

    times = []
    values = []

    minF, maxF = getFramesToSample(name, attr)
    if minF is None or maxF is None:
        minF, maxF = -1, -1

    if attr == 'translate' and len(getAllParents(uuid)) > 0:
        rminF, rmaxF = getFramesToSample(name, 'rotate')
        if rminF is not None:
            if minF == -1:
                minF, maxF = rminF, rmaxF
            else:
                minF = min(minF, rminF)
                maxF = max(maxF, rmaxF)

    if attr in commonAttr:
        values = getTransformAttr(name, attr, minF, maxF)
    else:
        values = getSpecificAttr(name, attr, minF, maxF)
        attr = convertSpecificAttribute(name, attr, minF, maxF, values)
        
    # Create time array
    if minF > -1:
        frameRate = mel.eval("currentTimeUnitToFPS;")
        for i in range(minF, maxF+1):
            times.append(i/frameRate)

    # light aim
    if mayaType.lower() == 'directionalLight'.lower():
        translateValues = getMayaAttr(name, 'translate', minF, maxF)
        rotateValues = getMayaAttr(name, 'rotate', minF, maxF)
        origin = [0, 0, -10]
        poiValues = []
        for i in range(len(values)):
            rotations = rotateValues[i]
            position = translateValues[i]
            aim = fx.applyRotations(rotations, origin)
            aim = [sum(x) for x in zip(aim, position)]
            aim = convertTranslations(aim)
            poiValues.append(aim)
        objData['poiValues'] = poiValues

    objData['values'] = values
    objData['times'] = times
    objData['attr'] = attr
    return [objData]

def convertSpecificAttribute(name, attr, minF, maxF, values):
    if attr == 'focalLength' or attr == 'horizontalFilmAperture':
        focalLength = values
        horizontalFilmAperture = values

        if attr == 'focalLength':
            horizontalFilmAperture = getSpecificAttr(name, 'horizontalFilmAperture', minF, maxF)
        else:
            focalLength = getSpecificAttr(name, 'focalLength', minF, maxF)

        for i in range(len(values)):
            values[i] = roundOff(focalLength[i] / (horizontalFilmAperture[i] * 25.4))

        return 'zoom'

    elif attr == 'intensity':
        for i in range(len(values)):
            values[i] *=100

        return 'intensity'

    elif attr == 'coneAngle':
        for i in range(len(values)):
            values[i] = roundOff(math.degrees(values[i]))

        return 'coneAngle'

    return attr

def getMObjectFromName(nodeName):
    sel = nom.MSelectionList()
    sel.add(nodeName)
    thisNode = sel.getDependNode(0)
    return thisNode

def getAttributePlug(name, attr):
    thisNode = getMObjectFromName(name)
    fnThisNode = nom.MFnDependencyNode ( thisNode )
    fnThisNode.name()
    outAttribute = fnThisNode.attribute(attr)
    outPlug = nom.MPlug( thisNode, outAttribute )
    return outPlug

def getDagPathFromName(nodeName):
    sl = nom.MSelectionList()
    sl.add(nodeName)
    return sl.getDagPath(0)

def getAllParents(uuid):
    parentNames = cmds.ls(uuid, long=True)[0].split('|')
    parents = []
    for i in range(len(parentNames)-1):
        if len(parentNames[i])>0:
            parents.append( '|'.join(parentNames[:i+1]) )
    return parents

def isCameraWithAim(name):
    return (cmds.aimConstraint(name, q=True) is not None )

def getAimCameras(name):
    objs = cmds.listConnections(name, type='lookAt')
    if not objs: return []
    objs = list(set(objs))
    cameras = []
    for obj in objs:
        cms = cmds.listConnections(obj, type='camera')
        if not cms: continue
        cameras += cms
    cameras = list(set(cameras))
    return cameras

def convertTranslations(translation):

    translation[1] = -translation[1]
    translation[2] = -translation[2]
    return translation

def convertRotations(rotation):
    #Reorder in ZYX
    rotation = [math.radians(x) for x in rotation]
    vector = nom.MVector(rotation[0], rotation[1], rotation[2])
    er = nom.MEulerRotation(vector)
    er.reorderIt(nom.MEulerRotation.kZYX)
    rotation = [math.degrees(angle) for angle in (er.x, er.y, er.z)]

    rotation[1] = -rotation[1];
    rotation[2] = -rotation[2];
    rotation[0]%=360;
    rotation[1]%=360;
    rotation[2]%=360;
    return rotation

def convertRotationsBack(rotation):
    rotation[1] = -rotation[1];
    rotation[2] = -rotation[2];

    rotation = [math.radians(x) for x in rotation]
    vector = nom.MVector(rotation[0], rotation[1], rotation[2])
    er = nom.MEulerRotation(vector, nom.MEulerRotation.kZYX)
    er.reorderIt(nom.MEulerRotation.kXYZ)
    rotation = [math.degrees(angle) for angle in (er.x, er.y, er.z)]
    return rotation

def getTransformAttrInFrame(name, attr, frame):
    ctx = nom.MDGContext(nom.MTime(frame, nom.MTime.uiUnit()))
    uuid = cmds.ls(name, uuid=True)[0]
    if 'translate' in attr:
        return convertTranslations(getTranslateInFrame(name, ctx, uuid))
    elif 'rotate' in attr:
        return convertRotations(getRotateInFrame(name, ctx, uuid))
    elif 'scale' in attr:
        return getScaleInFrame(name, ctx, uuid)

def getMayaAttrInFrame(name, attr, frame):
    ctx = nom.MDGContext(nom.MTime(frame, nom.MTime.uiUnit()))
    uuid = cmds.ls(name, uuid=True)[0]
    if 'translate' in attr:
        return getTranslateInFrame(name, ctx, uuid)
    elif 'rotate' in attr:
        return getRotateInFrame(name, ctx, uuid)
    elif 'scale' in attr:
        return getScaleInFrame(name, ctx, uuid)

def getEulerRotation(rot):
    inRadians = [math.radians(x) for x in rot]
    inMaya = nom.MEulerRotation(*inRadians)
    return inMaya
    
def getAbsolutePosition(ppos, prot, pscale, rpos):
    m = nom.MTransformationMatrix()
    m.setRotatePivot(nom.MPoint(*ppos), nom.MSpace.kWorld, False)
    m.rotateBy(getEulerRotation(prot), nom.MSpace.kTransform)
    m.setScalePivot(nom.MPoint(*ppos), nom.MSpace.kWorld, False)
    m.scaleBy(pscale, nom.MSpace.kTransform)

    pos = nom.MVector(*rpos) * m.asMatrix()
    rot = nom.MEulerRotation.decompose(m.asMatrix(), nom.MEulerRotation.kXYZ)
    rot = [math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z)]
    rot = [round(x, 3) for x in rot]
    pos = [sum(x) for x in zip(ppos, pos)]    
    return pos
    
def getAbsoluteRotation(prot, rrot):
    p = getEulerRotation(prot)
    c = getEulerRotation(rrot)

    rot = c.asQuaternion() * p.asQuaternion()
    rot = rot.asEulerRotation()
    rot = [math.degrees(rot.x), math.degrees(rot.y), math.degrees(rot.z)]
    rot = [round(x, 3) for x in rot]
    return rot

def getTranslateInFrame(name, ctx, uuid):
    plug = getAttributePlug(name, 'translate')
    handle = plug.asMDataHandle(ctx)
    nTranslate = handle.asDouble3()

    relativePosition = nTranslate

    for p in getAllParents(uuid)[::-1]:
        pPlug = getAttributePlug(p, 'translate')
        pHandle = pPlug.asMDataHandle(ctx)
        parentPosition = pHandle.asDouble3()
        pPlug.destructHandle(pHandle)

        pPlug = getAttributePlug(p, 'rotate')
        pHandle = pPlug.asMDataHandle(ctx)
        parentRotation = [math.degrees(x) for x in pHandle.asDouble3()]
        pPlug.destructHandle(pHandle)

        pPlug = getAttributePlug(p, 'scale')
        pHandle = pPlug.asMDataHandle(ctx)
        parentScale = pHandle.asDouble3()
        pPlug.destructHandle(pHandle)

        relativePosition = getAbsolutePosition(parentPosition, parentRotation, parentScale, relativePosition)

    nTranslate = relativePosition
    plug.destructHandle(handle)
    return nTranslate

def getRotateInFrame(name, ctx, uuid):
    plug = getAttributePlug(name, 'rotate')
    handle = plug.asMDataHandle(ctx)
    nDegrees = [math.degrees(x) for x in handle.asDouble3()]

    relativeRotation = nDegrees
    for p in getAllParents(uuid)[::-1]:
        pPlug = getAttributePlug(p, 'rotate')
        pHandle = pPlug.asMDataHandle(ctx)
        parentRotation = [math.degrees(x) for x in pHandle.asDouble3()]
        relativeRotation = getAbsoluteRotation(parentRotation, relativeRotation)
        pPlug.destructHandle(pHandle)

    nDegrees = relativeRotation
    plug.destructHandle(handle)

    #nDegrees = rrot

    if getObjType(name)[0] == 'solid':
        nDegrees[0] -= 90

    for i in range(3): nDegrees[i]%=360
    return nDegrees

def getScaleInFrame(name, ctx, uuid):
    plug = getAttributePlug(name, 'scale')
    handle = plug.asMDataHandle(ctx)
    nScale = handle.asDouble3()
    for p in getAllParents(uuid):
        pPlug = getAttributePlug(p, 'scale')
        pHandle = pPlug.asMDataHandle(ctx)
        pScale = pHandle.asDouble3()
        for i in range(3): nScale[i]*=pScale[i]
        pPlug.destructHandle(pHandle)
    if getObjType(name)[0] == 'solid':
        nScale = [x*100 for x in nScale]
    plug.destructHandle(handle)
    return nScale

def getFramesToSample(name, attr):
    frameRange = [None, None]
    minFrame = -1
    maxFrame = -1
    attrs = None

    if attr in ['focalLength', 'horizontalFilmAperture']:
        attrs = ['focalLength', 'horizontalFilmAperture']
    else:
        attrs = cmds.listAttr(name+'.'+attr, scalar=True)

    nodesToSample = [name]
    if attr in commonAttr:
        uuid = cmds.ls(name, uuid=True)[0]
        nodesToSample += getAllParents(uuid)

    for node in nodesToSample:
        #Check if any of the attributes has an incomming connection and bake the whole timeline
        for a in set(attrs + [attr]):
            plugName = node + '.' + a
            curves = cmds.listConnections(plugName, t='animCurve')
            connections = cmds.listConnections(plugName, d=False)
            if len(connections or []) - len(curves or []) > 0:
                frameRange[0] = int(cmds.playbackOptions(q=True, ast=True))
                frameRange[1] = int(cmds.playbackOptions(q=True, aet=True))
                return frameRange

        for a in attrs:
            curves = cmds.listConnections(node + '.' + a, t='animCurve')
            if not curves: continue

            curve = oma.MFnAnimCurve(getMObjectFromName(curves[0]))
            minF = int(curve.input(0).value)
            maxF = int(curve.input(curve.numKeys - 1).value)
            if frameRange[0] is None:
                frameRange[0] = minF
                frameRange[1] = maxF
            else:
                if minF < frameRange[0]: frameRange[0] = minF
                if maxF > frameRange[1] : frameRange[1] = maxF
    return frameRange

def roundOff(value):
    rounding = 4
    newValue = None
    if isinstance(value, list):
        newValue = [ round(elem, rounding) for elem in value ]
    else:
        newValue = round(value, rounding)
    return newValue

def getTransformAttr(name, attr, startFrame=-1, endFrame=-1):
    values = []
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
    cmds.progressBar( gMainProgressBar,
                                edit=True,
                                beginProgress=True,
                                isInterruptable=True,
                                status=_SR['Sending To AE ...'],
                                maxValue=(endFrame+1-startFrame) )
    for frame in range(startFrame, endFrame+1):
        value = getTransformAttrInFrame(name, attr, frame)
        value = roundOff(value)
        values.append(value)
        cmds.progressBar(gMainProgressBar, edit=True, step=1)
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return values

def getMayaAttr(name, attr, startFrame=-1, endFrame=-1):
    values = []
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
    cmds.progressBar( gMainProgressBar,
                                edit=True,
                                beginProgress=True,
                                isInterruptable=True,
                                status=_SR['Sending To AE ...'],
                                maxValue=(endFrame+1-startFrame) )
    for frame in range(startFrame, endFrame+1):
        value = getMayaAttrInFrame(name, attr, frame)
        value = roundOff(value)
        values.append(value)
        cmds.progressBar(gMainProgressBar, edit=True, step=1)
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return values

def getSpecificAttr(name, attr, startFrame=-1, endFrame=-1):
    name = cmds.listRelatives(name, f=True)[0]
    plug = getAttributePlug(name, attr)
    values = []
    gMainProgressBar = mel.eval('$tmp = $gMainProgressBar');
    cmds.progressBar( gMainProgressBar,
                                edit=True,
                                beginProgress=True,
                                isInterruptable=True,
                                status=_SR['Sending To AE ...'],
                                maxValue=(endFrame+1-startFrame) )
    for frame in range(startFrame, endFrame+1):
        ctx = nom.MDGContext(nom.MTime(frame, nom.MTime.uiUnit()))
        value = None
        if attr == 'color':
            handle = plug.asMDataHandle(ctx)
            value = handle.asFloat3()
            value = roundOff(value)
            plug.destructHandle(handle)

        else:
            value = plug.asFloat(ctx)
            value = roundOff(value)
        values.append(value)

        cmds.progressBar(gMainProgressBar, edit=True, step=1)
    cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
    return values

def exportToFile(jsonData):
    from os import path as os_path
    basicFilter = "*.json"
    saveLocation = ""
    saveLocation = cmds.fileDialog2(dialogStyle=2, fm=0, fileFilter=basicFilter, caption=_SR['Choose file to export to:'])

    #did the user press cancel ?
    if (saveLocation is None) or (len(saveLocation[0]) == 0):
        nom.MGlobal.displayInfo(_SR['AE Live Link Export Canceled'])
    else:
        try:
            #file location
            fileName = saveLocation[0]
            fileName = fileName and os_path.normpath(fileName) #hoping this fixes the file path on PCs

            f = open(fileName, "w")
            try:
                f.write(jsonData) # Write the json dump to the file
                nom.MGlobal.displayInfo(_SR['Exported to'] + ' ' + fileName)
            finally:
                f.close()
        except IOError:
            pass

def importFromFile():
    from os import path as os_path
    basicFilter = "*.json"
    saveLocation = ""
    saveLocation = cmds.fileDialog2(dialogStyle=2, fm=1, fileFilter=basicFilter, caption=_SR['Choose file to import from:'])

    #did the user press cancel ?
    if (saveLocation is None) or (len(saveLocation[0]) == 0):
        nom.MGlobal.displayInfo(_SR['AE Live Link Import Canceled'])
    else:
        try:
            fileName = saveLocation[0]
            fileName = fileName and os_path.normpath(fileName) #hoping this fixes the file path on PCs

            with open(fileName, 'r') as content_file:
                return content_file.read()
        except:
            nom.MGlobal.displayInfo(_SR['Opening file failed.'])

        return ''
            
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
