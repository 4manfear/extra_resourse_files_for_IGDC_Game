
import maya.cmds as cmds
import maya.mel as mel
import MASH.api as MASH

kConnectToTypeWarning = mel.eval('getPluginResource("MASH", "kConnectToTypeWarning")')

def connectToVector():
    sel = cmds.ls(sl=True)
    success = False

    waiterNode = None
    vectorNode = None

    for obj in sel:
        nodeId = cmds.nodeType(obj)
        if (nodeId == "MASH_Waiter"):
            waiterNode = obj
        elif (nodeId == "transform"):
            messageConns = cmds.listConnections(obj+".message", d=True, s=False, p=False)
            for conn in messageConns:
                if cmds.nodeType(conn) == "type" or cmds.nodeType(conn) == "svgToPoly":
                    vectorNode = conn

    if waiterNode and vectorNode:
        shellDeformer = cmds.listConnections (vectorNode+".animationMessage", d=True, s=False, p=False)
        if shellDeformer:
            success = True
            distMessage = cmds.listConnections (waiterNode+".waiterMessage", d=False, s=True, p=False)
            adjustMessage = None

            # Only Type has an adjustment node
            if cmds.nodeType(vectorNode) == "type":
                adjustMessage = cmds.listConnections (vectorNode+".alignmentMode", d=True, s=False, p=False)

            if distMessage:
                nodeWithShellPositions = None

                if adjustMessage:
                    nodeWithShellPositions = adjustMessage[0]
                elif cmds.nodeType(vectorNode) == "svgToPoly":
                    nodeWithShellPositions = vectorNode

                if nodeWithShellPositions:
                    shellPlug = nodeWithShellPositions+".shellPositions"

                    conns = cmds.listConnections(shellPlug, p=True) or []
                    for c in conns:
                        try:
                            cmds.disconnectAttr(shellPlug, c)
                        except:
                            pass
                    cmds.connectAttr(shellPlug, distMessage[0]+".inPositionPP",force=True)
                    cmds.connectAttr(shellPlug, waiterNode+".shellPositions",force=True)

                cmds.setAttr (distMessage[0]+".arrangement", 5)
                cmds.setAttr (distMessage[0]+".zeroScale", 1)
                cmds.connectAttr(waiterNode+".outputPoints",shellDeformer[0]+".inputPoints",force=True)
                cmds.setAttr (shellDeformer[0]+".enableAnimation", 1)
            else:
                success = False

    if not success:
        mel.eval('MASHinViewMessage("'+kConnectToTypeWarning+'", "Warning")')

# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
