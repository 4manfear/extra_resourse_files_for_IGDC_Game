import maya.cmds as cmds

import mash_repro_utils
import sys
from imp import reload
reload(mash_repro_utils)

import InViewMessageWrapper as ivm
import maya.mel as mel

def switch():

    selection = cmds.ls(sl=True)
    success = 0 # for completion message

    switchedFrom = ""
    switchedTo = ""

    for obj in selection:
        idWaiter = cmds.nodeType(obj)

        if idWaiter != "MASH_Waiter":
            continue

        currentInstancer = cmds.listConnections(obj + ".instancerMessage", d=True, s=False)
        if not currentInstancer:
            success = 3
            continue
        else:
            currentInstancer = currentInstancer[0]

        if cmds.nodeType(currentInstancer) == "instancer":
            children = cmds.listConnections(currentInstancer+'.inputHierarchy')
            inputConnection = cmds.listConnections(currentInstancer + ".inputPoints", d=False, s=True, p=True)[0]

            cmds.disconnectAttr(obj+'.instancerMessage', currentInstancer + ".instancerMessage")
            if inputConnection:
                cmds.disconnectAttr(inputConnection, currentInstancer + ".inputPoints")

            newName = obj+"_Repro"
            instancer = mash_repro_utils.create_mash_repro_node(obj,newName)

            cmds.flushIdleQueue() # force Maya to catch up.

            if children is not None:
                for instObj in children:
                    cmds.reproInstancer(instancer, addObject=True, object=instObj)

            cmds.addAttr(instancer, longName='instancerMessage', hidden=True, at='message')
            cmds.connectAttr(obj+'.instancerMessage', instancer+'.instancerMessage', f=True)
            #bin the default connection from Waiter to Repro
            cmds.disconnectAttr(obj+'.outputPoints', instancer+".inputPoints")
            cmds.connectAttr(inputConnection, instancer+'.inputPoints', f=True)

            cmds.delete(currentInstancer)
            cmds.select(instancer, r=True)
            success = 1

        elif cmds.nodeType(currentInstancer) == "MASH_Repro":
            reproMesh = cmds.listConnections(currentInstancer+'.outMesh', d=True, s=False)

            instancer = cmds.createNode('instancer')

            instancerObjects = cmds.reproInstancer(currentInstancer, q=True, obs=True)

            for instObj in instancerObjects:
                cmds.instancer(instancer, e=True, a=True, obj=instObj)

            inputConnection = cmds.listConnections(currentInstancer + ".inputPoints", d=False, s=True, p=True)[0]
            cmds.disconnectAttr(obj+'.instancerMessage', currentInstancer + ".instancerMessage")

            if inputConnection:
                cmds.disconnectAttr(inputConnection, currentInstancer + ".inputPoints")

            cmds.connectAttr(inputConnection, instancer+'.inputPoints', f=True)
            cmds.addAttr(instancer, longName='instancerMessage', hidden=True, at='message')
            cmds.connectAttr(obj+'.instancerMessage', instancer+'.instancerMessage', f=True)

            cmds.delete(reproMesh[0])
            cmds.select(instancer, r=True)
            newName = obj+"_Instancer"
            cmds.rename(instancer, newName)
            success = 2

    messages = [
        ('getPluginResource("MASH", "kPleaseSelectAWaiter")', 'Warning'),
        ('getPluginResource("MASH", "kSwitchedRepro")', 'Info'),
        ('getPluginResource("MASH", "kSwitchedInstancer")', 'Info'),
        ('getPluginResource("MASH", "kNotSupported")', 'Warning') ]

    message = messages[success]
    ivm.MashInViewMessage(mel.eval(message[0]), message[1])
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
