#MASHbakeInstancer
#This function takes an instancer, and turns all the particles being fed into it to real geometry.

from builtins import range
import maya.cmds as cmds
import maya.OpenMaya as om
import maya.OpenMayaFX as omfx
import gc

def mashGetMObjectFromName(nodeName):
    sel = om.MSelectionList()
    sel.add(nodeName)
    thisNode = om.MObject()
    sel.getDependNode( 0, thisNode )
    return thisNode

#if animation is true, the playback range will be baked, otherwise just this frame will be.
def MASHbakeInstancer(animationFlag):
    #get interface settings
    translateFlag = cmds.checkBox("bakeCbTranslate", query=True, value=True)
    rotationFlag = cmds.checkBox("bakeCbRotate", query=True, value=True)
    scaleFlag = cmds.checkBox("bakeCbScale", query=True, value=True)
    visibilityFlag = cmds.checkBox("bakeCbVis", query=True, value=True)
    bakeToIntancesFlag = cmds.checkBox("bakeCbToInstances", query=True, value=True)
    expressBaking = cmds.checkBox("bakeCbCloseEditor", query=True, value=True)
    flushUndo = cmds.checkBox("bakeCbUndo", query=True, value=True)
    garbageCollect = cmds.checkBox("bakeCbGarbage", query=True, value=True)

    if expressBaking:
        scriptEditorOpen = cmds.window ("scriptEditorPanel1Window", exists=True)
        if scriptEditorOpen:
            cmds.deleteUI ("scriptEditorPanel1Window",  window = True)
            cmds.flushIdleQueue()

    #get the selection
    li = []
    l = cmds.ls(sl=True) or []
    #check it's an instancer
    for instancerNode in l:
        if cmds.nodeType(instancerNode) != "instancer":
            continue
        li.append(instancerNode)

    #did we find at least 1?
    if len(li) == 0:
        raise Exception('Select an instancer node.')

    l = []

    for instancerNode in li:
        cmds.select(instancerNode)
        #reused vars for the particles
        m = om.MMatrix()
        dp = om.MDagPath()
        dpa = om.MDagPathArray()
        sa = om.MScriptUtil()
        sa.createFromList([0.0, 0.0, 0.0], 3)
        sp = sa.asDoublePtr()
        
        #Get the instancer function set
        thisNode = mashGetMObjectFromName(instancerNode)
        fnThisNode = om.MFnDependencyNode(thisNode)

        #start frame, end frame, animation
        sf = int(cmds.playbackOptions(q=True, min=True))-1
        ef = int(cmds.playbackOptions(q=True, max=True))+2

        if (animationFlag==False):
            sf = cmds.currentTime( query=True )
            ef = sf+1

        for i in range(int(sf), int(ef)):
            #set the time
            cmds.currentTime(i)
            g = instancerNode+"_objects"
            
            #get the visibility array - which isn't provided by the MFnInstancer function set
            inPointsAttribute = fnThisNode.attribute("inputPoints")
            inPointsPlug = om.MPlug( thisNode, inPointsAttribute )
            inPointsObj = inPointsPlug.asMObject()
            inputPPData = om.MFnArrayAttrsData(inPointsObj)
            visibility_exists = inputPPData.checkArrayExist("visibility")
            if visibility_exists[0]:
                visList = inputPPData.getDoubleData("visibility")[:]
            else:
                visList = []

            #if this is the first frame, create a transform to store everything under
            if i == sf:
                if cmds.objExists(g) == True:
                    cmds.delete(g)
                g = cmds.createNode("transform", n=g)
                l.append(g)

            #get the instancer
            sl = om.MSelectionList()
            sl.add(instancerNode)
            sl.getDagPath(0, dp)
            #create mfninstancer function set
            fni = omfx.MFnInstancer(dp)

            if len(visList) == 0:
                visList =  [True] * fni.particleCount()

            #cycle through the particles
            for j in range(fni.particleCount()):
                visibility = visList[j]
                #get the instancer object
                fni.instancesForParticle(j, dpa, m)
                for ki in range(dpa.length()):
                    #get the instancer object name
                    fullPathName = dpa[ki].partialPathName()
                    #support namespaces, refrences, crap names
                    nameSpaceRemoved = fullPathName.rsplit(':', 1)[-1]
                    pipesRemoved = nameSpaceRemoved.rsplit('|', 1)[-1]
                    numCreatedPoints = len(cmds.listRelatives(g, shapes=False) or [])
                    n = pipesRemoved+"_"+instancerNode+"_"+str(j)

                    #if we haven't got a node with the new name, make one, give it a safe name (which we will continue to identify it by).
                    if cmds.objExists(n) == False:
                        #duplicate the object
                        if bakeToIntancesFlag:
                            n2 = cmds.instance(dpa[ki].fullPathName(), leaf=True )[0]
                        else:
                            n2 = cmds.duplicate(dpa[ki].fullPathName(), rr=True, un=True)[0]
                        #rename it to the safe name
                        n = cmds.rename(n2, n, ignoreShape=bakeToIntancesFlag)

                        #parent it to the transform we created above
                        if cmds.listRelatives(n, p=True) != g:
                            try:
                                n = cmds.parent(n, g)[0]
                            except:
                                pass

                        # if the object doesn't appear on frame 0 (animated creation), set the visibility when it first appears
                        cmds.setKeyframe(n+".visibility", v=0, t=cmds.currentTime(q=True)-1)
                        cmds.setKeyframe(n+".visibility", v=1)


                    #empty transformMatrix for the particle
                    tm = om.MTransformationMatrix(m)
                    instancedPath = dpa[ki]
                    #get the matrix from the instancer
                    instancedPathMatrix = instancedPath.inclusiveMatrix()
                    finalMatrixForPath = instancedPathMatrix * m
                    finalPoint = om.MPoint.origin * finalMatrixForPath;

                    t = tm.getTranslation(om.MSpace.kWorld)
                    #set the translate
                    try:
                        cmds.setAttr(n+".t", finalPoint.x, finalPoint.y, finalPoint.z)
                        if translateFlag and animationFlag:
                            cmds.setKeyframe(n+".t")
                    except:
                        pass

                    #set the rotate
                    r = tm.eulerRotation().asVector()
                    try:
                        cmds.setAttr(n+".r", r[0]*57.2957795, r[1]*57.2957795, r[2]*57.2957795)
                        if rotationFlag and animationFlag:
                            cmds.setKeyframe(n+".r")
                    except:
                        pass

                    #set the scale
                    tm.getScale(sp, om.MSpace.kWorld)
                    if scaleFlag:
                        doubleArrayItem = lambda i : om.MScriptUtil.getDoubleArrayItem(sp,i)
                        sx, sy, sz    = doubleArrayItem(0), doubleArrayItem(1), doubleArrayItem(2)

                        s = om.MTransformationMatrix(dpa[ki].inclusiveMatrix()).getScale(sp, om.MSpace.kWorld)
                        sx2, sy2, sz2 = doubleArrayItem(0), doubleArrayItem(1), doubleArrayItem(2)

                        try:
                            cmds.setAttr(n+".s", sx*sx2, sy*sy2, sz*sz2)
                            if animationFlag:
                                cmds.setKeyframe(n+".s")
                        except:
                            pass

                    # set visibility
                    if visibilityFlag:
                        cmds.setAttr(n+".v", visibility)
                        if animationFlag:
                            cmds.setKeyframe(n+".v")

        #flush undo
        if flushUndo:
            cmds.flushUndo()

        #python garbage collect
        if garbageCollect:
            gc.collect()
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
