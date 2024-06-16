#import mash.smartpresets as sp
from builtins import next
from builtins import range
import maya.app.flux.core as fx
import maya.cmds as cmds

OFFSET_FRAMES = 50

def onMayaDroppedPythonFile(object):
    def runPreset():

        # Create controls for the drop window
        # This is a list of lists (an list of steps in the preset if you will, even if you want only 1 step, it still has to be a double list)
        addnControls = []
        menu = cmds.optionMenu('omAnimationMode', label='Animation Mode')
        addnControls.append(cmds.menuItem('miChar', label='Character' ))
        addnControls.append(cmds.menuItem('miWord', label='Word' ))
        addnControls.append(cmds.menuItem('miLine', label='Line' ))

        # IMPORTANT - Remember to delete your controls below (already implimented, you can copy and paste the cleanup to any script)
        controls = [
            [
            cmds.intSliderGrp('offsetSliderGrp', label='Offset (frames)', field=True, value=OFFSET_FRAMES),
            menu
            ]
        ]

        # Create the Drop Window
        fx.DropWindow.getDrop(label='Drag in your type:', callback=lambda data: smartPreset.send(data), title='Type - Slide in', accepts=['transform'], ui=controls)
        node = yield

        # Split the dragged nodes into a list and only use the first object
        typeTransform = node.split('\n')[0]
        typeNode = cmds.listConnections(typeTransform+".message") or []

        if cmds.nodeType(typeNode) != "type":
            return

        # Get the nodes we need
        typeNode = typeNode[0]
        animationDeformer = getAnimationNode(typeNode)

        # Enable type animation
        cmds.setAttr(animationDeformer+".enableAnimation", 1)

        # Set the options for Word/line/character
        animMode = cmds.optionMenu('omAnimationMode', q=True, v=True)
        if animMode == "Character":
            cmds.setAttr(animationDeformer+".animationMode", 1)
        elif animMode == "Word":
            cmds.setAttr(animationDeformer+".animationMode", 2)
        else:
            cmds.setAttr(animationDeformer+".animationMode", 3)
        
        # Set the duration
        offsetFrames = cmds.intSliderGrp('offsetSliderGrp', q=True, v=True)
        cmds.setAttr(animationDeformer+".offsetFrames", offsetFrames)

        #### SET KEYFRAMES FOR type1.animationPositionY ####
        #### These commands are automatically generated ####
        keyCount = 3
        keyTimes = [7.911393707482993, 20.253163435374148, 32.594937925170065]
        keyValues = [0.0, 50.0, 0.0]
        inAngles = [0.0, 0.0, -84.01580284552607]
        outAngles = [0.0, 0.0, -84.01580299484223]
        inWeights = [2.7044438121091217, 9.559827679257644, 21.085489160957767]
        outWeights = [2.7044438121091217, 9.559827679257644, 21.085489319542912]
        channel = animationDeformer+'.animationPositionY'
        for t in range(0, keyCount):
            cmds.setKeyframe( channel, t=keyTimes[t], v=keyValues[t] )
            
            cmds.selectKey(channel, k=True, t=(keyTimes[t],keyTimes[t]))
            cmds.keyTangent(edit=True, weightedTangents=True)
            cmds.keyTangent(weightLock=False)
            cmds.keyTangent(lock=False)
            cmds.keyTangent(itt='flat',ott='flat')
            curve = cmds.listConnections(channel, type='animCurve')
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), outAngle=outAngles[t], outWeight=outWeights[t])
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), inAngle=inAngles[t], inWeight=inWeights[t])
        #### SET KEYFRAMES FOR type1.animationPositionZ ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [7.911393707482993, 32.594937925170065]
        keyValues = [-180.0, 0.0]
        inAngles = [81.42161846178787, 84.25412301883874]
        outAngles = [81.42161840375311, 84.25412332946465]
        inWeights = [34.20620324710641, 42.832850525457125]
        outWeights = [34.206203139084884, 42.83285118482614]
        channel = animationDeformer+'.animationPositionZ'
        for t in range(0, keyCount):
            cmds.setKeyframe( channel, t=keyTimes[t], v=keyValues[t] )
            
            cmds.selectKey(channel, k=True, t=(keyTimes[t],keyTimes[t]))
            cmds.keyTangent(edit=True, weightedTangents=True)
            cmds.keyTangent(weightLock=False)
            cmds.keyTangent(lock=False)
            cmds.keyTangent(itt='flat',ott='flat')
            curve = cmds.listConnections(channel, type='animCurve')
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), outAngle=outAngles[t], outWeight=outWeights[t])
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), inAngle=inAngles[t], inWeight=inWeights[t])
        #### SET KEYFRAMES FOR type1.animationRotationX ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [7.911393707482993, 32.594937925170065]
        keyValues = [0.0, 360.0]
        inAngles = [0.0, 87.46026931367126]
        outAngles = [0.0, 87.46026931127321]
        inWeights = [1.0, 1.0]
        outWeights = [1.0, 1.0]
        channel = animationDeformer+'.animationRotationX'
        for t in range(0, keyCount):
            cmds.setKeyframe( channel, t=keyTimes[t], v=keyValues[t] )
            
            cmds.selectKey(channel, k=True, t=(keyTimes[t],keyTimes[t]))
            cmds.keyTangent(edit=True, weightedTangents=True)
            cmds.keyTangent(weightLock=False)
            cmds.keyTangent(lock=False)
            cmds.keyTangent(itt='flat',ott='flat')
            curve = cmds.listConnections(channel, type='animCurve')
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), outAngle=outAngles[t], outWeight=outWeights[t])
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), inAngle=inAngles[t], inWeight=inWeights[t])
        #### SET KEYFRAMES FOR type1.animationScaleY ####
        #### These commands are automatically generated ####
        keyCount = 7
        keyTimes = [1.0, 6.430380782312925, 11.36708843537415, 32.594937925170065, 34.07594982993197, 36.54430493197279, 40.0]
        keyValues = [1.0, 0.6, 1.1, 1.0, 0.9, 1.05, 1.0]
        inAngles = [-0.008278965337902726, 0.0, 0.0, -0.5045985986908031, 0.0, 0.0, 0.0]
        outAngles = [-0.008278965117003446, 0.0, 0.0, -0.5045985986908031, 0.0, 0.0, 0.0]
        inWeights = [3.7906006268384034, 3.0969376830213724, 5.1738281028421, 7.0762242498310055, 0.493670634920635, 0.8227850340136058, 1.1518983560090703]
        outWeights = [3.790600627391047, 2.7678237177305554, 11.097879478076798, 0.4936897804839934, 0.8227850340136058, 1.1518983560090703, 1.1518983560090703]
        channel = animationDeformer+'.animationScaleY'
        for t in range(0, keyCount):
            cmds.setKeyframe( channel, t=keyTimes[t], v=keyValues[t] )
            
            cmds.selectKey(channel, k=True, t=(keyTimes[t],keyTimes[t]))
            cmds.keyTangent(edit=True, weightedTangents=True)
            cmds.keyTangent(weightLock=False)
            cmds.keyTangent(lock=False)
            cmds.keyTangent(itt='flat',ott='flat')
            curve = cmds.listConnections(channel, type='animCurve')
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), outAngle=outAngles[t], outWeight=outWeights[t])
            cmds.keyTangent(curve, e=True,a=True, t=(keyTimes[t],keyTimes[t]), inAngle=inAngles[t], inWeight=inWeights[t])


        # UI CLEANUP #
        # This is really important, if you want to run your script more then once in a Maya session, you must delete the UI!
        [cmds.deleteUI(y, control=True ) for x in controls for y in x]

        yield
        
    def getAnimationNode(typeNode):
        shellDeformer = cmds.listConnections (typeNode+".animationMessage", d=True, s=False, p=False) or []
        if shellDeformer and cmds.nodeType(shellDeformer[0]) == "shellDeformer":
            return shellDeformer[0]
        else:
            cmds.error("Could not find the Animation Deformer")
        return None

    # run the preset
    smartPreset = runPreset()
    next(smartPreset)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
