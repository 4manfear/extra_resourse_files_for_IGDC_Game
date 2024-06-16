from builtins import range
import maya.OpenMaya as om
import maya.mel as mel
import maya.cmds as cmds
import json
import math
import maya.mel

def getLightFrameForAE(aeDictionary, lights, frame):
    for obj in lights:
        #get the light specific attributes
        lightColour = cmds.getAttr(obj+'.color')
        lightIntensity = cmds.getAttr(obj+'.intensity')

        lightShape = cmds.listRelatives(obj)
        lightType = "point" #unknown lights are point lights.
        coneAngle = 0 #only spots
        if cmds.nodeType( lightShape[0] ) == "spotLight":
            lightType = "spotLight"
            coneAngle = cmds.getAttr(obj+'.coneAngle')
        if cmds.nodeType( lightShape[0] ) == "pointLight":
            lightType = "pointLight"
        if cmds.nodeType( lightShape[0] ) == "ambientLight":
            lightType = "ambientLight"
        if cmds.nodeType( lightShape[0] ) == "directionalLight":
            lightType = "directionalLight"

        framePosition = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        frameScaleOut = cmds.getAttr(obj+'.scale')
        frameMatrixList = cmds.getAttr('%s.worldMatrix'%obj)
        frameRotation = convertRotations(frameMatrixList)
        frameLightColour = cmds.getAttr(obj+'.color')
        frameLightIntensity = cmds.getAttr(obj+'.intensity')
        aeDictionary["lights"][obj]["animation"][frame] = {u"lightStrength": frameLightIntensity, u"coneAngle": coneAngle, u"colour": [frameLightColour[0][0], frameLightColour[0][1], frameLightColour[0][2]], u"position": [framePosition[0], framePosition[1], framePosition[2]], u"rotation": [frameRotation[0], frameRotation[1], frameRotation[2]], u"scale": [frameScaleOut[0][0], frameScaleOut[0][1], frameScaleOut[0][2]]}

    return aeDictionary

def getSolidFrameForAE(aeDictionary, solids, frame):
    for obj in solids:
        framePosition = cmds.xform(obj,q=1,ws=1,rp=1)
        frameScaleOut = cmds.getAttr(obj+'.scale')
        frameMatrixList = cmds.getAttr('%s.worldMatrix'%obj)
        frameRotation = convertRotations(frameMatrixList)
        aeDictionary["solids"][obj]["animation"][frame] = {u"position": [framePosition[0], framePosition[1], framePosition[2]], u"rotation": [frameRotation[0], frameRotation[1], frameRotation[2]], u"scale": [frameScaleOut[0][0], frameScaleOut[0][1], frameScaleOut[0][2]]}

    return aeDictionary

def getNullFrameForAE(aeDictionary, nulls, frame):
    for obj in nulls:
        framePosition = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        frameScaleOut = cmds.getAttr(obj+'.scale')
        frameMatrixList = cmds.getAttr('%s.worldMatrix'%obj)
        frameRotation = convertRotations(frameMatrixList)
        aeDictionary["nulls"][obj]["animation"][frame] = {u"position": [framePosition[0], framePosition[1], framePosition[2]], u"rotation": [frameRotation[0], frameRotation[1], frameRotation[2]], u"scale": [frameScaleOut[0][0], frameScaleOut[0][1], frameScaleOut[0][2]]}
    return aeDictionary

def getCameraFrameForAE(aeDictionary, cameras, frame):
    for obj in cameras:
        #get camera specific attributes
        shapes = cmds.listRelatives(obj)
        focalLength = cmds.getAttr(shapes[0]+'.focalLength')
        horizontalViewPlane = cmds.getAttr(shapes[0]+'.horizontalFilmAperture')
        horizontalViewPlane *= 25.4 #inches(!) to mm

        framePosition = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        frameScaleOut = cmds.getAttr(obj+'.scale')
        frameMatrixList = cmds.getAttr('%s.worldMatrix'%obj)
        frameRotation = convertRotations(frameMatrixList)
        shapes = cmds.listRelatives(obj)
        focalLength = cmds.getAttr(shapes[0]+'.focalLength')
        horizontalViewPlane = cmds.getAttr(shapes[0]+'.horizontalFilmAperture')
        horizontalViewPlane *= 25.4
        aeDictionary["cameras"][obj]["animation"][frame] = {u"focalLength": focalLength, u"horizontalFilmPlane": horizontalViewPlane, u"position": [framePosition[0], framePosition[1], framePosition[2]], u"rotation": [frameRotation[0], frameRotation[1], frameRotation[2]]}
    return aeDictionary


def getLightsForAE(aeDictionary, lights, startFrame, endFrame):
    aeDictionary["lights"] = {}
    for obj in lights:
        position = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        matrixList = cmds.getAttr('%s.worldMatrix'%obj)
        rotation = convertRotations(matrixList)
        scaleOut = cmds.getAttr(obj+'.scale')

        #get the light specific attributes
        lightColour = cmds.getAttr(obj+'.color')
        lightIntensity = cmds.getAttr(obj+'.intensity')

        lightShape = cmds.listRelatives(obj)
        lightType = "point" #unknown lights are point lights.
        coneAngle = 0 #only spots
        if cmds.nodeType( lightShape[0] ) == "spotLight":
            lightType = "spotLight"
            coneAngle = cmds.getAttr(obj+'.coneAngle')
        if cmds.nodeType( lightShape[0] ) == "pointLight":
            lightType = "pointLight"
        if cmds.nodeType( lightShape[0] ) == "ambientLight":
            lightType = "ambientLight"
        if cmds.nodeType( lightShape[0] ) == "directionalLight":
            lightType = "directionalLight"

        aeDictionary["lights"][obj] = {u"lightType": lightType, u"lightStrength": lightIntensity, u"coneAngle": coneAngle, u"colour": [lightColour[0][0], lightColour[0][1], lightColour[0][2]], u"position": [position[0], position[1], position[2]], u"rotation": [rotation[0], rotation[1], rotation[2]], u"scale": [scaleOut[0][0], scaleOut[0][1], scaleOut[0][2]]}
        aeDictionary["lights"][obj]["animation"] = {}

    return aeDictionary

def getSolidsForAE(aeDictionary, solids, startFrame, endFrame):
    aeDictionary["solids"] = {}
    for obj in solids:
        position = cmds.xform(obj,q=1,ws=1,rp=1) #query rotate pivot point
        matrixList = cmds.getAttr('%s.worldMatrix'%obj)
        rotation = convertRotations(matrixList)
        scaleOut = cmds.getAttr(obj+'.scale')
        aeDictionary["solids"][obj] = {u"position": [position[0], position[1], position[2]], u"rotation": [rotation[0], rotation[1], rotation[2]], u"scale": [scaleOut[0][0], scaleOut[0][1], scaleOut[0][2]]}
        aeDictionary["solids"][obj]["animation"] = {}

    return aeDictionary


def getNullsForAE(aeDictionary, nulls, startFrame, endFrame):
    aeDictionary["nulls"] = {}
    for obj in nulls:
        position = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        matrixList = cmds.getAttr('%s.worldMatrix'%obj)
        rotation = convertRotations(matrixList)
        scaleOut = cmds.getAttr(obj+'.scale')
        aeDictionary["nulls"][obj] = {u"position": [position[0], position[1], position[2]], u"rotation": [rotation[0], rotation[1], rotation[2]], u"scale": [scaleOut[0][0], scaleOut[0][1], scaleOut[0][2]]}
        aeDictionary["nulls"][obj]["animation"] = {}

    return aeDictionary


def getCamerasForAE(aeDictionary, cameras, startFrame, endFrame):
    aeDictionary["cameras"] = {}
    for obj in cameras:
        position = cmds.xform(obj, q=1,translation=1,worldSpace=1)
        scaleOut = cmds.getAttr(obj+'.scale')
        matrixList = cmds.getAttr('%s.worldMatrix'%obj)
        rotation = convertRotations(matrixList)

        #get camera specific attributes
        shapes = cmds.listRelatives(obj)
        focalLength = cmds.getAttr(shapes[0]+'.focalLength')
        horizontalViewPlane = cmds.getAttr(shapes[0]+'.horizontalFilmAperture')
        horizontalViewPlane *= 25.4 #inches(!) to mm

        #look through the baking camera
        cmds.lookThru( obj, 'perspView' )

        #write attributes in case there's no animation (I know, I know)
        aeDictionary["cameras"][obj] = {u"focalLength": focalLength, u"horizontalFilmPlane": horizontalViewPlane, u"position": [position[0], position[1], position[2]], u"rotation": [rotation[0], rotation[1], rotation[2]], u"scale": [scaleOut[0][0], scaleOut[0][1], scaleOut[0][2]]}
        aeDictionary["cameras"][obj]["animation"] = {}

    return aeDictionary


def exportToAE():
    from os import path as os_path

    #resolution and frame rate
    width = cmds.getAttr('defaultResolution.width')
    height = cmds.getAttr('defaultResolution.height')
    frameRate = maya.mel.eval("currentTimeUnitToFPS;")
    maxTime = cmds.playbackOptions( maxTime=True, q=True )
    minTime = cmds.playbackOptions( minTime=True, q=True )
    sceneName = cmds.file(sceneName=True,shortName=True,query=True)
    aeDictionary = {u"resolution": [width, height]}

    #animation export range
    aeDictionary["frameRate"] = frameRate
    aeDictionary["animationLength"] = maxTime
    aeDictionary["animationStart"] = minTime
    aeDictionary["projectName"] = sceneName

    if cmds.objExists('MayaToAE'):
        cmds.select('MayaToAE')
    else:
        kAEInstructions = mel.eval('getPluginResource("MASH", "kAEInstructions")')
        mel.eval('MASHinViewMessage("'+kAEInstructions+'", "Error"); ')

    allSetObjects = cmds.select( 'MayaToAE' )

    everything = cmds.ls(selection=True)
    if len(everything) == 0:
        kNoObjectsToExport = mel.eval('getPluginResource("MASH", "kNoObjectsToExport")')
        mel.eval('MASHinViewMessage("'+kNoObjectsToExport+'", "Error"); ')

   #isolate select what's being exported
    modelPanels = cmds.getPanel( type='modelPanel' )
    for panes in modelPanels:
        cmds.isolateSelect(panes, state=1 )
        cmds.isolateSelect(panes, addSelected=True )

    #sort out everything for export
    nulls = []
    lights = []
    solids = []
    cameras = []
    aimCameras = []
    for obj in everything:
        shapes = cmds.listRelatives(obj)
        if cmds.nodeType( shapes[0] ) == "camera":
            cameras.append(obj)
        if cmds.nodeType( shapes[0] ) == "mesh":
            solids.append(obj)
        if cmds.nodeType( shapes[0] ) == "locator":
            nulls.append(obj)
        if (cmds.nodeType( shapes[0] ) == "spotLight") or (cmds.nodeType( shapes[0] ) == "pointLight") or (cmds.nodeType( shapes[0] ) == "ambientLight") or (cmds.nodeType( shapes[0] ) == "directionalLight"):
            lights.append(obj)
        if cmds.nodeType( obj ) == "lookAt":
            aimCameras.append(obj)
        if cmds.nodeType( shapes[0] ) == "transform":
            nulls.append(obj)   #get groups and treat them as nulls

    #aim cameras are really just cameras, follow that thought:
    for children in aimCameras:
        groupChildren = cmds.listRelatives(children) #gives us camera and aim locators
        for objects in groupChildren:
            shapes = cmds.listRelatives(objects) #gives us shape object
            if cmds.nodeType( shapes[0] ) == "camera": #which could be a camera
                cameras.append(objects) #add it to the camera array

    #generate the export entries
    getSolidsForAE(aeDictionary, solids, minTime, maxTime)
    getCamerasForAE(aeDictionary, cameras, minTime, maxTime)
    getNullsForAE(aeDictionary, nulls, minTime, maxTime)
    getLightsForAE(aeDictionary, lights, minTime, maxTime)

    for frame in range (int(minTime), int(maxTime+1)):
        cmds.currentTime(frame,update=1)
        getLightFrameForAE(aeDictionary, lights, frame)
        getSolidFrameForAE(aeDictionary, solids, frame)
        getCameraFrameForAE(aeDictionary, cameras, frame)
        getNullFrameForAE(aeDictionary, nulls, frame)

    #take a big steaming dump
    toWrite = (json.dumps(aeDictionary, indent=4, separators=(',', ': ')))

    # write mode either creates a new file or overwrites the existing content of the file.
    basicFilter = "*.json"
    saveLocation = ""
    kExportLocation = mel.eval('getPluginResource("MASH", "kExportLocation")')
    saveLocation = cmds.fileDialog2(dialogStyle=2, fm=0, fileFilter=basicFilter, caption=kExportLocation)
    if len(sceneName) == 0:
        sceneName = "MayaSceneToAE"

    #did the user press cancel ?
    if (saveLocation is None) or (len(saveLocation[0]) == 0):
        kExportCancelled = mel.eval('getPluginResource("MASH", "kExportCancelled")')
        mel.eval('MASHinViewMessage("'+ kExportCancelled +'", "Warning"); ')
    else:
        try:
            #file location
            fileName = saveLocation[0]
            fileName = fileName and os_path.normpath(fileName) #hoping this fixes the file path on PCs

            f = open(fileName, "w")
            try:
                f.write(toWrite) # Write the json dump to the file
                kSceneExportedTo = mel.eval('getPluginResource("MASH", "kSceneExportedTo")')
                print (kSceneExportedTo + " " + fileName)
                kExport = mel.eval('getPluginResource("MASH", "kExportOk")')
                mel.eval('MASHinViewMessage("'+ kExport +'", "Warning"); ')
            finally:
                f.close()
        except IOError:
            pass

    #TODO: restore selection
    #turn off isolate select
    modelPanels = cmds.getPanel( type='modelPanel' )
    for panes in modelPanels:
        cmds.isolateSelect(panes, state=0 )

#utility function, converts Maya rotations into AE rotations.
def convertRotations(matrixList):
    mMatrix = om.MMatrix()
    om.MScriptUtil.createMatrixFromList(matrixList, mMatrix)
    mTransformMtx = om.MTransformationMatrix(mMatrix)
    eulerRot = mTransformMtx.eulerRotation()
    eulerRot.reorderIt(5)
    rotation = [math.degrees(angle) for angle in (eulerRot.x, eulerRot.y, eulerRot.z)]
    return rotation


# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
