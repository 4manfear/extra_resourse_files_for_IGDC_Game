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

        # Used to determine how far the text will travel
        bbox = cmds.exactWorldBoundingBox(typeTransform)
        pos = cmds.xform(typeTransform, q=True, ws=True, rp=True)
        scaleX = bbox[3] - bbox[0];
        scaleY = bbox[4] - bbox[1];
        scaleZ = bbox[5] - bbox[2];

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

        keyCount = 6
        keyTimes = [1.0, 15.0, 21.0, 27.0, 31.0, 35.0]
        keyValues = [48.0, 0.0, 1.9875000000000007, 0.0, 0.75, 0.0]
        inAngles = [0.0, -77.3404994843564, 0.0, -38.91456403450781, 0.0, -25.700965602292626]
        outAngles = [0.0, 44.76764031449212, 0.0, 26.947006994830463, 0.0, -25.700965231624743]
        inWeights = [4.666666666666667, 10.723183763139309, 2.0, 2.865508023269403, 1.333333333333334, 1.5564676724238005]
        outWeights = [4.666666666666667, 2.396222827424176, 2.0, 1.986026215441048, 1.3333333333333321, 1.556467668172212]
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

        # UI CLEANUP #
        # This is really important, if you want to run your script more then once in a Maya session, you must delete the UI!
        [cmds.deleteUI(x, control=True ) for x in addnControls]
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
