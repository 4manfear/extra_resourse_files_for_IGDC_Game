#import mash.smartpresets as sp
from builtins import next
import maya.app.flux.core as fx
import maya.cmds as cmds
import MASH.sceneExaminer as se
import maya.OpenMaya as om

OFFSET_FRAMES = 50

def onMayaDroppedPythonFile(object):
    def runPreset():

        # Add labels for each step of the smart preset
        steps = [
            'Step 1: Drag in the Type with the style you want to copy:', 
            'Step 2: Drag in the Type to paste it onto:'
        ]

        # List the accepted node types for each step
        acceptableNodeTypes = [
            ['mesh'], 
            ['mesh']
        ]

        # create the drop window
        fx.DropWindow.getDrop(steps, callback=lambda data: smartPreset.send(data), title='Type - Copy Style', accepts=acceptableNodeTypes)
        node = yield

        # Split the dragged nodes into a list and only use the first object
        typeTransform = node.split('\n')[0]
        typeNode = cmds.listConnections(typeTransform+".message", d=True, s=False, p=False) or []
        animationConn = cmds.listConnections (typeNode[0]+".animationMessage", d=True, s=False, p=False) or []
        extrudeConn = cmds.listConnections (typeNode[0]+".extrudeMessage", d=True, s=False, p=False) or []
        remeshConn = cmds.listConnections (typeNode[0]+".remeshMessage", d=True, s=False, p=False) or []

        if cmds.nodeType(typeNode) != 'type':
            return

        log = se.scanNodes(nodes=[typeTransform])

        node = yield

        pasteTypeTransform = node.split('\n')[0]
        pasteTypeNode = cmds.listConnections(pasteTypeTransform+".message", d=True, s=False, p=False) or []
        pasteAnimationConn = cmds.listConnections (pasteTypeNode[0]+".animationMessage", d=True, s=False, p=False) or []
        pasteExtrudeConn = cmds.listConnections (pasteTypeNode[0]+".extrudeMessage", d=True, s=False, p=False) or []
        pasteRemeshConn = cmds.listConnections (pasteTypeNode[0]+".remeshMessage", d=True, s=False, p=False) or []

        exCmd = ''
        # switch the commands from the old type to the new one
        for line in log:
            line = line.replace(typeTransform, pasteTypeTransform, 1)
            line = line.replace(typeNode[0], pasteTypeNode[0], 1)
            line = line.replace(animationConn[0], pasteAnimationConn[0], 1)
            line = line.replace(extrudeConn[0], pasteExtrudeConn[0], 1)
            line = line.replace(remeshConn[0], pasteRemeshConn[0], 1)
            exCmd += line+"\n"
        
        # start an undo chunk
        cmds.undoInfo(ock=True)
        # run the script
        exec(exCmd, globals())
        # end the undo chunk
        cmds.undoInfo(cck=True)

        yield

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
