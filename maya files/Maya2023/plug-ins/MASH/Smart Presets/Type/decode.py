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
            menu,
            cmds.checkBox('cbRandomise', label='Randomize' )
            ]
        ]

        # Create the Drop Window
        fx.DropWindow.getDrop(label='Drag in your type:', callback=lambda data: smartPreset.send(data), title='Type - Decode', accepts=['transform'], ui=controls)
        node = yield

        # Split the dragged nodes into a list and only use the first object
        typeTransform = node.split('\n')[0]
        typeNode = cmds.listConnections(typeTransform+".message") or []

        if cmds.nodeType(typeNode) != "type":
            return

        # Get the nodes we need
        typeNode = typeNode[0]
        animationDeformer = getAnimationNode(typeNode)

        randomiseOrder = cmds.checkBox('cbRandomise', query=True, value=True)

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

        #### SET ATTRIBUTES FOR type1 ####
        #### These commands are automatically generated ####
        cmds.setAttr(typeNode+'.generator', 8)
        cmds.setAttr(typeNode+'.randomSeed', 1)
        cmds.setAttr(typeNode+'.delay', 50.0)
        cmds.setAttr(typeNode+'.randomizerMode', 0)
        if randomiseOrder:
            cmds.setAttr(typeNode+'.random', True)

        #### SET KEYFRAMES FOR type1.percent ####
        #### These commands are automatically generated ####
        keyCount = 2
        keyTimes = [1.0, 49.0]
        keyValues = [12.0, 0.0]
        inAngles = [0.0, -14.036243467926479]
        outAngles = [-14.036243467926479, 0.0]
        inWeights = [1.0, 1.0]
        outWeights = [1.0, 1.0]
        channel = typeNode+'.percent'
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
