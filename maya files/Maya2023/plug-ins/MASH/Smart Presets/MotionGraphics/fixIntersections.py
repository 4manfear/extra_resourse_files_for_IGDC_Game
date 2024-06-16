from builtins import range
from builtins import next
import maya.cmds as cmds
import MASH.api as mapi
import maya.mel as mel
import maya.app.flux.core as fx
import MASH.deleteMashNode as dmn

def onMayaDroppedPythonFile(object):

    def runPreset():
        cmds.select(clear=True)

        # Create controls for the drop window
        # This is a list of lists (an list of steps in the preset if you will, even if you want only 1 step, it still has to be a double list)
        # IMPORTANT - Remember to delete your controls below (already implimented, you can copy and paste the cleanup to any script)
        controls = [
            [cmds.intSliderGrp('iterationsSliderGrp', label='Iterations', field=True, min=0, max=20, value=10)]
        ]

        # create the Drop Window
        fx.DropWindow.getDrop(label='Drag in a MASH Waiter:', callback=lambda data: smartPreset.send(data), title='MASH - Fix Intersections', accepts=['MASH_Waiter'], ui=controls)
        node = yield

        # split the dragged nodes into a list and only use the first object
        nodes = node.split('\n')[0]
    
        # create a new MASH network
        mashNetwork = mapi.Network(node)

        # add dynamics
        dynamicsNode = mashNetwork.addNode('MASH_Dynamics')
        attrs = { 'damping' : 1, 'rollingDamping' : 1, 'positionStrength' : 100, 'rotationalStrength' : 100, 'mass' : 10 }
        for key, value in attrs.items():
            cmds.setAttr('{}.{}'.format(dynamicsNode.name, key), value)

        iterations = cmds.intSliderGrp('iterationsSliderGrp', q=True, v=True)
        for x in range(1, iterations):
            cmds.currentTime(x)

        mashNetwork.setInitialState(dynamicsNode)

        # UI CLEANUP #
        # This is really important, if you want to run your script more then once in a Maya session, you must delete the UI!
        [cmds.deleteUI(y, control=True ) for x in controls for y in x]

        dmn.deleteMashNode(dynamicsNode.name)
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
