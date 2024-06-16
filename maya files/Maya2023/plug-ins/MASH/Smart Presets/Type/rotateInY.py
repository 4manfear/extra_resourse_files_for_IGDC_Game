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

        #### SET KEYFRAMES FOR type1.animationRotationY ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [1.0, 50.0]
        keyValues = [90.0, 0.0]
        inAngles = [0.0, 0.0]
        outAngles = [0.0, 0.0]
        inWeights = [16.333333333333332, 31.737599690755204]
        outWeights = [16.333333333333332, 31.737599690755204]
        channel = animationDeformer+'.animationRotationY'
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
        #### SET KEYFRAMES FOR type1.animationScaleX ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [1.0, 50.0]
        keyValues = [0.001, 1.0]
        inAngles = [0.0, 0.0]
        outAngles = [2.878411376467501, 0.0]
        inWeights = [16.333333333333336, 34.8653842860216]
        outWeights = [9.205520463230911, 16.333333333333336]
        channel = animationDeformer+'.animationScaleX'
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
        keyCount = 2
        keyTimes = [1.0, 50.0]
        keyValues = [0.001, 1.0]
        inAngles = [0.0, 0.0]
        outAngles = [2.878411376467501, 0.0]
        inWeights = [16.333333333333336, 34.8653842860216]
        outWeights = [9.205520463230911, 16.333333333333336]
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
        #### SET KEYFRAMES FOR type1.animationScaleZ ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [1.0, 50.0]
        keyValues = [0.001, 1.0]
        inAngles = [3.044213991967701, 0.0]
        outAngles = [3.0442141361521005, 0.0]
        inWeights = [9.298075358072914, 33.662620544433594]
        outWeights = [9.298074722290037, 33.662620544433594]
        channel = animationDeformer+'.animationScaleZ'
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
