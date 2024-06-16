import maya
maya.utils.loadStringResourcesForModule(__name__)

from builtins import next
import maya.cmds as cmds
import MASH.api as mapi
import maya.mel as mel
import maya.app.flux.core as fx

def onMayaDroppedPythonFile(object):

    def largestBoundingBoxDimensions(obj):
        # Extract the bounding box for obj and determine the dimension of the bounding box with the largest size.
        bbox = cmds.exactWorldBoundingBox(obj)
        dims = [x-y for x, y in zip(bbox[3:6],bbox[0:3])]
        return max(dims)

    def runPreset():
        cmds.select(clear=True)

        #
        # Drop Window
        #

        # Add labels for each step of the smart preset
        steps = [
            maya.stringTable['y_pileOfStuff.kPileOfStuffStep1' ],
            maya.stringTable['y_pileOfStuff.kPileOfStuffStep2' ]
        ]

        # List the accepted node types for each step
        acceptableNodeTypes = [
            ['mesh'], 
            ['mesh']
        ]

        # create the drop window
        fx.DropWindow.getDrop(steps, callback=lambda data: smartPreset.send(data), title=maya.stringTable['y_pileOfStuff.kPileOfStuffTitle'], accepts=acceptableNodeTypes)
        node = yield

        # split the dragged nodes into a list and only use the first object
        nodes = node.split('\n')

        # get the largest bbox dimension, this will be the voxel size
        longestSide = max([largestBoundingBoxDimensions(obj) for obj in nodes] + [0])
        longestSide *= .8

        # create a new MASH network
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(name='MASH_Pile', geometry='Instancer')

        # get the second step drop
        node = yield

        # split the dragged nodes into a list and only use the first object
        node = node.split('\n')[0]

        # put the ground undreneath the pile object
        groundBBox = cmds.exactWorldBoundingBox(node)
        groundPosition = groundBBox[1]

        # set up the MASH network
        mashNetwork.meshDistribute(node, 6)
        attrs = { 'voxelDensity' : longestSide, 'voxelMode' : 3 }
        for key, value in attrs.items():
            cmds.setAttr('{}.{}'.format(mashNetwork.distribute, key), value)

        # random rotations
        randomNode = mashNetwork.addNode('MASH_Random')
        attrs = { 'positionX' : 0, 'positionY' : 0, 'positionZ' : 0, 'rotationX' : 360, 'rotationY' : 360, 'rotationZ' : 360 }
        for key, value in attrs.items():
            cmds.setAttr('{}.{}'.format(randomNode.name, key), value)

        # add dynamics
        dynamicsNode = mashNetwork.addNode('MASH_Dynamics')
        attrs = { 'collisionShape' : 4, 'friction' : 1, 'rollingFriction' : 1, 'bounce' : 0, 'mass' : 10 }
        for key, value in attrs.items():
            cmds.setAttr('{}.{}'.format(dynamicsNode.name, key), value)

        solver = cmds.listConnections(dynamicsNode.name+('.enable'))[0] or []
        attr = 'groundPlanePositionZ' if cmds.optionVar (query='upAxisDirection') == 'z' else 'groundPlanePositionY'
        cmds.setAttr('{}.{}'.format(solver, attr), groundPosition)

        # hide the pile shape object
        cmds.hide(node)
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
