from builtins import zip
import MASH.dynamicsUtils as dynamics
import MASH.api as mapi
import maya.cmds as cmds
import maya.api.OpenMaya as om
import openMASH
import maya.app.flux.core as fx

'''
import MASH.deleteMashNode as dmn
reload(dmn)
dmn.deleteMashNode("MASH1_Dynamics")
'''

'''
import MASH.deleteMASHNode as dmn
reload(dmn)
dmn.deleteMashNode("MASH2")
'''

def deleteMashNode(nodeName):
    nodeType = cmds.nodeType(nodeName)
    # is there a parent to delete?
    parent = None
    if nodeType == "MASH_Flight" or nodeType == "MASH_Points":
        parent = cmds.listRelatives(nodeName, p=True)[0] or None

    if nodeType == "MASH_Dynamics":
        deleteSolver = False
        if not cmds.objExists(nodeName+".inputPoints") or not cmds.objExists(nodeName+".outputPoints"):
            cmds.error(fx.res('kMASH_delete_error'))
            return

        inConnections = cmds.listConnections( nodeName+".inputPoints", s=True, d=False, p=True) or []
        outConnections = cmds.listConnections( nodeName+".outputPoints", s=False, d=True, p=True) or []

        for conn in outConnections:
            cmds.disconnectAttr(nodeName+".outputPoints", conn)
            if inConnections:
                cmds.connectAttr(inConnections[0], conn, force=True)

        for conn in inConnections:
            cmds.disconnectAttr(conn, nodeName+".inputPoints")

        waiter = cmds.listConnections( nodeName+".waiterMessage", s=False, d=True)[0]
        waiterConn = cmds.listConnections( nodeName+".waiterMessage", s=False, d=True, p=True)
        if waiterConn:
            cmds.disconnectAttr(nodeName+".waiterMessage", waiterConn[0])

        # see if we need to delete the solver (MAYA-81531)
        solver = cmds.listConnections( nodeName+".enable", s=False, d=True)
        if solver:
            solver=solver[0]
            solverShape = cmds.listRelatives(solver, shapes=True)[0]
            solverObj = openMASH.mashGetMObjectFromNameTwo(solverShape)
            fnNode = om.MFnDependencyNode(solverObj)
            inputPlug = fnNode.findPlug('inputNetworks', False)
            numNetworks = inputPlug.numConnectedElements()
            # if there's only one solver, we should delete it
            if numNetworks == 1:    
                deleteSolver = True
            else:
                # just disconnect the MASH network from the solver
                outputPlugs = cmds.listConnections( waiter+".outputPoints", s=False, d=True, p=True)
                solverConnection = None
                for conn in outputPlugs:
                    node = conn.split('.')[0]
                    if cmds.nodeType(node) == "MASH_BulletSolver":
                        solverConnection = conn
                        break

                if solverConnection == None:
                    cmds.error(fx.res('kMASH_delete_error2'))
                    return

                index = solverConnection[solverConnection.find("[")+1:solverConnection.find("]")]
                solverOutConnection = cmds.listConnections(solver+'.outputPoints['+index+']', s=False, d=True, p=True)[0]
                cmds.disconnectAttr(solver+'.outputPoints['+index+']', solverOutConnection)
                cmds.disconnectAttr(waiter+".outputPoints", solverConnection)
                cmds.connectAttr(waiter+".outputPoints", solverOutConnection, force=True)
                # brute force remove the input, MASH will automatically pair the correct inputs/ outputs.
                cmds.removeMultiInstance(solver+'.inputNetworks['+index+']', b=True)

                instancerConnection = cmds.listConnections( waiter+".instancerMessage", s=False, d=True, p=True)[0]
                cmds.disconnectAttr(waiter+".instancerMessage", instancerConnection)

        try:
            cmds.delete(nodeName)
            if deleteSolver:
                cmds.select(clear=True)
                cmds.select(solver)
                cmds.delete(solver)
        except:
            pass

    elif nodeType == "MASH_Waiter":
        # short circuit
        if not cmds.objExists(nodeName+'.instancerMessage'):
            return

        mashNetwork = mapi.Network(nodeName)
        allNodes = mashNetwork.getAllNodesAndReturnList(False)

        # Get the network clear of Dynamics first
        for node in allNodes:
            if cmds.objExists(node) and cmds.nodeType(node) == "MASH_Dynamics":
                deleteMashNode(node)

        
        # Required to let any solvers catch up with us
        cmds.flushIdleQueue()

        # Refresh the list
        allNodes = mashNetwork.getAllNodesAndReturnList(False)
        disconnectAll(nodeName)
        # DEBUG print allNodes

        # Disconnect all connections on all nodes to avoid loops
        for node in allNodes:
            if cmds.nodeType(node) == "MASH_BulletSolver":
                allNodes.remove(node)

        # Except should never happen
        for node in allNodes:
            try:
                if cmds.objExists(node):
                    cmds.delete(node)
            except:
                cmds.error(fx.res('kMASH_delete_error3')) # SNH!
        
    elif nodeType == "MASH_Deformer":
        inConnections = cmds.listConnections( nodeName+".inputPoints", s=True, d=False, p=True)
        if inConnections:
            for conn in inConnections:
                cmds.disconnectAttr(conn, nodeName+".inputPoints")

    elif nodeType == "MASH_Explode":
        conns = cmds.listConnections(nodeName+".inputMesh", sh=True) or []

        if conns:
            cmds.setAttr(conns[0]+".intermediateObject", 0)
            cmds.disconnectAttr(conns[0]+".worldMesh[0]", nodeName+".inputMesh")

        cmds.delete(nodeName)

    elif nodeType == "MASH_Trails":
        # Remove mesh, without registering it in the undo queue, as Trails creates its mesh on createMesh and we would end up with 2 meshes
        cmds.undoInfo(st=False)
        try:
            outMesh = cmds.listConnections( nodeName+".outputMesh", s=False, d=True) or []
            for conn in outMesh:
                cmds.disconnectAttr(nodeName+".outputMesh", conn+".inMesh")
                cmds.delete(conn)
        finally:
            cmds.undoInfo(st=True)

        # Manage MASH connections and delete Trails
        inConnections = cmds.listConnections( nodeName+".inputPoints", s=True, d=False, p=True) or []
        outConnections = cmds.listConnections( nodeName+".outputPoints", s=False, d=True, p=True) or []

        for conn in outConnections:
            cmds.disconnectAttr(nodeName+".outputPoints", conn)

        for conn in inConnections:
            cmds.disconnectAttr(conn, nodeName+".inputPoints")

        cmds.delete(nodeName)

    else:
        # disconnect outgoing
        inConns = cmds.listConnections(nodeName + '.inputPoints', d=False, s=True, p=True) or []
        outConns = []

        if cmds.objExists(nodeName+'.outputPoints'):
            outConns = cmds.listConnections(nodeName + '.outputPoints', d=True, s=False, p=True) or []

        for conn in outConns:

            try: cmds.disconnectAttr(conn, nodeName + '.outputPoints')
            except: pass

            # connect the inputPoints connection to all outgoing connections on the deleted node.
            try: cmds.connectAttr(inConns[0], conn, force=True)
            except: pass

        # disconnect incoming
        for conn in inConns:
            try: cmds.disconnectAttr(conn, nodeName + '.inputPoints')
            except: pass

        disconnectAll(nodeName)

        # delete the node
        cmds.delete(nodeName)

        if parent:
            cmds.delete(parent)

# Disconect all connections on a node
def disconnectAll(nodeName):
    connectionPairs = []
    conns = cmds.listConnections(nodeName, plugs=True, connections=True, destination=False) or []
    if conns:
        connectionPairs.extend(list(zip(conns[1::2], conns[::2])))

    conns = cmds.listConnections(nodeName, plugs=True, connections=True, source=False) or []
    if conns:
        connectionPairs.extend(list(zip(conns[::2], conns[1::2])))

    for srcAttr, destAttr in connectionPairs:
        cmds.disconnectAttr(srcAttr, destAttr)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
