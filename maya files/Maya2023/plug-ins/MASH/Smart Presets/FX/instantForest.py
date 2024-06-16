#import mash.smartpresets as sp
from builtins import next
from builtins import range
import maya.app.flux.core as fx
import maya.cmds as cmds
import maya.mel as mel
import MASH.api as mapi
import MASH.genotypeCreator as gtc

def runPreset():

    from os import path as os_path
    from os import environ as os_environ

    # Create controls for the drop window
    # This is a list of lists (an list of steps in the preset if you will, even if you want only 1 step, it still has to be a double list)

    # IMPORTANT - Remember to delete your controls below (already implimented, you can copy and paste the cleanup to any script)
    controls = [
        [
        cmds.checkBox('cbUsePfx', label='Use Default Tree (skip step 2).' )
        ],
        []
    ]

    # Add labels for each step of the smart preset
    steps = [
        'Step 1: Drag in your landscape:', 
        'Step 2: Drag in your trees:'
    ]

    # List the accepted node types for each step
    acceptableNodeTypes = [
        ['transform'], 
        ['transform']
    ]

    # Create the Drop Window
    fx.DropWindow.getDrop(steps, callback=lambda data: smartPreset.send(data), title='Instant Forest', accepts=acceptableNodeTypes, ui=controls)
    node = yield

    # get the landscape
    landscape = node.split('\n')[0]
    lanscapeShape = cmds.listRelatives(landscape, s=True)[0]

    usePfx = cmds.checkBox('cbUsePfx', query=True, value=True)

    trees = []
    #jsonString = '[{"Slope": 0.6, "colorBar": [255, 255, 255], "Id Min": 0, "Name": "Default Genotype", "Seed Count": 4, "Resiliance": 0.2, "Age": 120, "Soil Quality": 0.5, "Id": 0, "Temperature": 0.5, "Rate": 0.12, "Id Max": 0, "Id Color": [0.0, 0.0, 0.0], "Moisture": 0.5, "Variance": 0.2, "Seed Age": 10, "Size": 5.0}]' #
    if not usePfx:
        node = yield
        trees = node.split('\n')
    else:
        mayaLocation = os_environ['MAYA_LOCATION']
        if os_path.isfile(mayaLocation+'/Examples/Paint_Effects/TreesMesh/oakWhiteMedium.mel'):
            mel.eval('source "'+mayaLocation+'/Examples/Paint_Effects/TreesMesh/oakWhiteMedium.mel";')
            cmds.curve(d=3, p=[(0, 0, 0), (0.33, 0, 0), (.66, 0, 0), (1.0, 0, 0)] )
            mel.eval('AttachBrushToCurves;')
            mel.eval('doPaintEffectsToPoly( 1,0,0,1,100000);')
            main = cmds.ls(sl=True)[0]
            leaf = cmds.ls(sl=True)[1]
            transform = cmds.listRelatives(main, p=True)
            trees = cmds.listRelatives(transform, p=True)
            fx.DropWindow.instance.close() # skip and close

    cmds.select(cl=True)
    for tree in trees:
        cmds.select(tree, add=True)

    #create a new MASH network
    mashNetwork = mapi.Network()
    mashNetwork.createNetwork(name='ForestNetwork', geometry='Instancer')
    mashNetwork.meshDistribute(lanscapeShape, 1)
    cmds.setAttr(mashNetwork.distribute + '.pointCount', 20)

    #add a World node
    node = mashNetwork.addNode("MASH_World")
    cmds.setAttr( node.name+".clusterMode", 7)
    cmds.setAttr( node.name+".ecosystemAge", 120)
    node.addGroundPlane(landscape)

    # setup genotype data for each tree
    genoData = gtc.GenotypeInstance(cmds.ls("ForestNetwork_World", uuid=True)[0])
    for x in range(1, len(trees)):
        genoData.addGenotype()
        genoData.setValue(x, 'Id', x)

    # set the correct size for each genotype
    indices = list(range(0, genoData.getCount()))
    genoData.setModelSizes(indices)

    # UI CLEANUP #
    # This is really important, if you want to run your script more then once in a Maya session, you must delete the UI!
    [cmds.deleteUI(y, control=True ) for x in controls for y in x]

    # set to move tool
    cmds.setToolTo( 'moveSuperContext' )
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
