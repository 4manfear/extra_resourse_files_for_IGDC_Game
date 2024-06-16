from builtins import next
import sys
if sys.version_info[0] >= 3:
    from importlib import reload

import maya.cmds as cmds
import MASH.api as mapi
reload(mapi)
import maya.mel as mel
import maya.app.flux.core as fx

def onMayaDroppedPythonFile(object):

    def runPreset():
        cmds.select(clear=True)

        # create a new MASH network
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(name = "MASH_Explode", geometry="Instancer")

        # create the Drop Window
        fx.DropWindow.getDrop('Drag in an object to Explode:', callback=lambda data: smartPreset.send(data), title='MASH - Explode This Mesh', accepts=['mesh'])
        node = yield

        # split the dragged nodes into a list and only use the first object
        node = node.split('\n')[0]

        # freeze transforms
        cmds.makeIdentity(node, apply=True, t=True,s=True)
        bbox = cmds.exactWorldBoundingBox(node)
        scaleX = bbox[3] - bbox[0];
        scaleY = bbox[4] - bbox[1];
        scaleZ = bbox[5] - bbox[2];
        pos = cmds.xform(node, q=True, ws=True, rp=True)

        # mesh distribute onto this node
        mashNetwork.meshDistribute(node)
        
        cmds.setAttr(mashNetwork.distribute + '.meshType', 4)
        cmds.setAttr(mashNetwork.distribute + '.floodMesh', 1)

        offsetNode = mashNetwork.addNode("MASH_Offset")
        cmds.setAttr(offsetNode.name + '.offsetType', 4)
        cmds.setAttr(offsetNode.name + '.enablePosition', 0)
        

        cmds.setAttr(offsetNode.name + '.scaleOffset0', 0)
        cmds.setAttr(offsetNode.name + '.scaleOffset1', 0)
        cmds.setAttr(offsetNode.name + '.scaleOffset2', 0)

        falloffShape = offsetNode.addFalloff()
        falloffTransform = cmds.listRelatives(falloffShape, p=True)[0]
        cmds.setAttr(falloffTransform+ '.translateX', pos[0]+scaleX*0.5)
        cmds.setAttr(falloffTransform+ '.translateY', pos[1])
        cmds.setAttr(falloffTransform+ '.translateZ', pos[2])

        explodeNode = mashNetwork.addNode("MASH_Explode")
        explodeNode.addExplodeMesh(node)

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
