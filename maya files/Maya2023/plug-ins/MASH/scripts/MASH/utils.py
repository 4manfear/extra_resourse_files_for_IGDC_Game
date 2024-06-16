import maya.cmds as cmds

def getNetworkFromNode(name=None, foundNames=None, dest=True):
    if foundNames is None:
        foundNames = set([name])
    objs = cmds.listConnections(name, destination=dest, sh=True )
    
    if objs == None:
        return foundNames

    for obj in objs:
        if obj in foundNames: continue

        if 'MASH' in cmds.nodeType(obj) or 'instancer' in cmds.nodeType(obj):
            foundNames.add(obj)
            shouldDest = 'MASH_Breakout' != cmds.nodeType(obj)
            if 'MASH_Repro' == cmds.nodeType(obj):
                foundNames = foundNames.union(cmds.listConnections(obj, source=False, type='mesh'))
            mObjs = getNetworkFromNode(obj, foundNames, shouldDest)
            foundNames = foundNames.union(mObjs)
            relatives = cmds.listRelatives(obj)
            if relatives:
                foundNames = foundNames.union(relatives)
        else:
            relatives = cmds.listRelatives(obj)
            if relatives:
                for rel in relatives:
                    if 'MASH' in cmds.nodeType(rel):
                        foundNames.add(obj)
                        mObjs = getNetworkFromNode(obj, foundNames)
                        foundNames = foundNames.union(mObjs)
        return foundNames
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
