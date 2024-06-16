from builtins import range
from builtins import object
from maya.app.flux.imports import *
import MayaToAE.utils as AEUtils

import maya.api.OpenMayaAnim as oma


class AECallbacksManager(qt.QObject):
    # SLOTS
    sceneClosing = None
    sceneOpened = None
    scrJob = None
    objRenamed = None
    manageRename = None
    nodeRemovedCallback = None
    animCurveEdited = None
    timeChanged = None
    prefsChanged = None

    sceneCallbacks = []
    dagCallbackManager = None
    nodeDeleteCallback = None
    animCurveCallback = None
    timeChangedCallback = None
    renameCallbacks = {}
    attrJobs = {}
    prefJobs = []
    frameRateCallback = None
    playbackCallback = None

    def registerSceneCloseCallbacks(self):
        self.sceneCallbacks = []
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kBeforeOpen, self.sceneClosing, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kBeforeNew, self.sceneClosing, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kBeforeImport, self.sceneClosing, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))

    def registerSceneOpenCallbacks(self):
        self.sceneCallbacks = []
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kAfterOpen, self.sceneOpened, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kAfterNew, self.sceneOpened, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kAfterImport, self.sceneOpened, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))
        cb = nom.MSceneMessage.addCallback(nom.MSceneMessage.kMayaExiting, self.sceneOpened, None) 
        self.sceneCallbacks.append(MCallbackIdWrapper(cb))

    def deregisterSceneCallbacks(self):
        self.sceneCallbacks = []

    def registerCallbacks(self):
        self.dagCallbackManager = DAGCallbackManager()
        self.dagCallbackManager.manageRename = self.manageRename
        self.dagCallbackManager.scrJob = self.scrJob
        self.nodeDeleteCallback = nom.MDGMessage.addNodeRemovedCallback(self.nodeRemovedCallback, 'transform', None)   
        self.animCurveCallback = oma.MAnimMessage.addAnimCurveEditedCallback(self.animCurveEdited, None)
        self.timeChangedCallback = nom.MDGMessage.addTimeChangeCallback(self.timeChanged, None)

        # Preferences
        self.prefJobs.append(cmds.scriptJob(runOnce=False, attributeChange=['defaultResolution.width', self.prefsChanged]))
        self.prefJobs.append(cmds.scriptJob(runOnce=False, attributeChange=['defaultResolution.height', self.prefsChanged]))
        self.prefJobs.append(cmds.scriptJob(runOnce=False, attributeChange=['defaultResolution.pixelAspect', self.prefsChanged]))
        self.frameRateCallback = nom.MEventMessage.addEventCallback('timeUnitChanged', self.prefsChanged)
        self.playbackCallback = nom.MEventMessage.addEventCallback('playbackRangeSliderChanged', self.prefsChanged)

    def deregisterCallbacks(self):
        # NodeDelete Callback
        if self.nodeDeleteCallback:
            nom.MMessage.removeCallback(self.nodeDeleteCallback)
            self.nodeDeleteCallback = None

        # AnimCurve Callback
        if self.animCurveCallback:
            oma.MAnimMessage.removeCallback(self.animCurveCallback)
            self.animCurveCallback = None

        # TimeChanged Callback
        if self.timeChangedCallback:
            nom.MDGMessage.removeCallback(self.timeChangedCallback)
            self.timeChangedCallback = None

        # Rename Callbacks
        for uuid in list(self.renameCallbacks.keys()):
            self.removeRenameCallback(uuid)

        # Attribute Jobs
        for uuid in list(self.attrJobs.keys()):
            self.deregisterNodeAttrJobs(uuid)

        # DAG Callbacks
        if self.dagCallbackManager:
            self.dagCallbackManager.removeAll()
            self.dagCallbackManager = None

        # Preferences
        for job in self.prefJobs:
            if cmds.scriptJob(exists=job):
                cmds.scriptJob(kill=job, force=True)
        self.prefJobs = []

        if self.frameRateCallback:
            nom.MMessage.removeCallback(self.frameRateCallback)
            self.frameRateCallback = None
        if self.playbackCallback:
            nom.MMessage.removeCallback(self.playbackCallback)
            self.playbackCallback = None

    def registerNode(self, uuid):
        # Rename callback
        self.addRenameCallback(uuid)
        # Attr jobs
        self.registerNodeAttrJobs(uuid)
        # DAG callback
        self.dagCallbackManager.registerNode(uuid)

    def deregisterNode(self, uuid):
        # Rename callback
        self.removeRenameCallback(uuid)
        # Attr jobs
        self.deregisterNodeAttrJobs(uuid)
        # DAG callback
        if self.dagCallbackManager:
            self.dagCallbackManager.removeNode(uuid)

    def registerNodeAttrJobs(self, uuid):
        name = cmds.ls(uuid, long=True)[0]

        if uuid not in self.attrJobs:
            self.attrJobs[uuid] = {}

        jobs = self.attrJobs[uuid]

        vAttrs = AEUtils.getValidAttributes(name)
        mayaAttrs = vAttrs['mayaAttrs']
        apiAttrs = vAttrs['apiAttrs']

        for i, apiAttr in enumerate(apiAttrs):
            if apiAttr not in jobs:
                attr = mayaAttrs[i]
                jobs[apiAttr] = self.registerJob(attr, apiAttr, uuid)

    # Needs to be in a separate function to work without Maya bug
    def registerJob(self, attr, apiAttr, uuid):
        func = lambda: self.scrJob(uuid, apiAttr)
        return cmds.scriptJob(runOnce=False, attributeChange=[attr, func])

    def deregisterNodeAttrJobs(self, uuid):
        if uuid not in self.attrJobs:
            return

        jobs = self.attrJobs[uuid]
        for attr in jobs:
            job = jobs[attr]
            if cmds.scriptJob(exists=job):
                cmds.scriptJob(kill=job, force=True)

        del self.attrJobs[uuid]

    def addRenameCallback(self, uuid):
        name = cmds.ls(uuid, long=True)[0]
        node = AEUtils.getMObjectFromName(name)
        self.renameCallbacks[uuid] = nom.MNodeMessage.addNameChangedCallback(node, self.objRenamed, name)

    def removeRenameCallback(self, uuid):
        if uuid in self.renameCallbacks:
            nom.MNodeMessage.removeCallback(self.renameCallbacks[uuid])
            del self.renameCallbacks[uuid]

    def renameNode(self, uuid):
        self.removeRenameCallback(uuid)
        self.addRenameCallback(uuid)

    def isObservableParent(self, pUUID):
        return self.dagCallbackManager.isObservableParent(pUUID)

    def getAffectedNodeNamesByParent(self, pUUID):
        return self.dagCallbackManager.getAffectedNodeNamesByParent(pUUID)

    def dagScrJob(self, uuid, attr):
        self.scrJob(uuid, attr)

    def dagManageRename(self, uuid):
        self.manageRename(uuid)


class DAGCallbackManager(dict):
    manageRename = None
    scrJob = None

    def __init__(self, *args):
        dict.__init__(self, *args)
        self.allRegisteredParents = {}
        self.callbackId = nom.MDagMessage.addParentAddedCallback(self.parentChanged, None)

    def parentChanged(self, child, parent, clientData):
        #Object creation/deletion
        if len(child.fullPathName().split('|')[-1])==0: return

        childTree = self.getTree(child)
        affected = set( self.keys() ).intersection(set( childTree ))
        for uuid in affected:
            name = cmds.ls(uuid, long=True)[0]
            parentNames = AEUtils.getAllParents(uuid)
            parentUUIDs = [cmds.ls(x, uuid=True)[0] for x in parentNames]
            oldParents = list(self[uuid]['pJobs'].keys())
            removedParents = set(oldParents).difference(set(parentUUIDs))
            addedParents = set(parentUUIDs).difference(set(oldParents))

            nodeData = self[uuid]
            allParentJobs = nodeData['pJobs']

            for pUUID in addedParents:
                pName = cmds.ls(pUUID, long=True)[0]
                parentJobs = self.registerObjParent(name, pName)
                self.addParentToRegister(pUUID, uuid)
                allParentJobs[pUUID] = parentJobs

            for pUUID in removedParents:
                if pUUID in allParentJobs:
                    nodeParentJobs = allParentJobs[pUUID]
                    self.clearNodeParentJobs(nodeParentJobs)
                    self.removeParentFromRegister(pUUID, uuid)
                    del allParentJobs[pUUID]

            self.manageRename(uuid)
            self.scrJob(uuid, 'translate')
            self.scrJob(uuid, 'rotate')
            self.scrJob(uuid, 'scale')

    def registerNode(self,uuid):
        if uuid in self:
            return
        nodeName = cmds.ls(uuid, long=True)[0]
        nodeDagPath = AEUtils.getDagPathFromName(nodeName)

        nodeData = {}
        nodeData['pJobs'] = self.getAllParentJobs(nodeName, uuid)
        self[uuid] = nodeData

    def removeNode(self,uuid):
        if uuid not in self:
            return

        nodeData = self[uuid]
        for pUUID in list(nodeData['pJobs'].keys()):
            nodeParentJobs = nodeData['pJobs'][pUUID]
            self.clearNodeParentJobs(nodeParentJobs)
            self.removeParentFromRegister(pUUID, uuid)

        del self[uuid]

    def removeAll(self):
        for uuid in list(self.keys()):
            self.removeNode(uuid)
        nom.MMessage.removeCallback(self.callbackId)

    def clearNodeParentJobs(self, nodeParentJobs):
        for pJob in nodeParentJobs:
            if cmds.scriptJob(exists=pJob):
                cmds.scriptJob(kill=pJob, force=True)

    def getAllParentJobs(self, nodeName, uuid):
        nodeParents = AEUtils.getAllParents(uuid)
        allParentJobs = {}
        for nodeParent in nodeParents:
            pUUID = cmds.ls(nodeParent, uuid=True)[0]
            parentJobs = self.registerObjParent(nodeName, nodeParent)
            self.addParentToRegister(pUUID, uuid)
            allParentJobs[pUUID] = parentJobs
        return allParentJobs

    def registerObjParent(self, nodeName, nodeParent):
        jobIds = []
        for attr in AEUtils.commonAttr:
            plugName = nodeParent + '.' + attr
            arg = nodeName + '.'+ attr
            jobId = self.registerJob(plugName, arg)
            jobIds.append(jobId)

        return jobIds

    def registerJob(self, plugName, arg):
        uuid = cmds.ls(arg.split('.')[0], uuid=True)[0]
        arg = '.'.join(arg.split('.')[1:])
        jobId = cmds.scriptJob( runOnce=False, attributeChange=[plugName,lambda: self.scrJob(uuid, str(arg))] )
        return jobId

    def addParentToRegister(self, pUUID, nodeUUID):
        if pUUID in self.allRegisteredParents:
            self.allRegisteredParents[pUUID].append(nodeUUID)
        else:
            self.allRegisteredParents[pUUID] = [nodeUUID]

    def removeParentFromRegister(self, pUUID, nodeUUID):
        if pUUID in self.allRegisteredParents:
            if nodeUUID in self.allRegisteredParents[pUUID]:
                self.allRegisteredParents[pUUID].remove(nodeUUID)
            if len(self.allRegisteredParents[pUUID]) == 0:
                del self.allRegisteredParents[pUUID]

    def isObservableParent(self, pUUID):
        return pUUID in self.allRegisteredParents

    def getAffectedNodeNamesByParent(self, pUUID):
        if self.isObservableParent(pUUID):
            return [cmds.ls(x, long=True)[0] for x in self.allRegisteredParents[pUUID] ]
        else:
            return []

    def getAllNodeParentNames(self, nodeUUID):
        if nodeUUID in self:
            nodeData = self[nodeUUID]
            return [cmds.ls(x, long=True)[0] for x in list(nodeData['pJobs'].keys())]
        return []

    def getTree(self, dag):
        name = dag.fullPathName()
        #We're only interested in kTransforms
        if not cmds.objExists(name) or cmds.nodeType(name, api=True) != 'kTransform':
            return []

        uuid = cmds.ls(name, uuid=True)[0]

        children = [uuid]
        for i in range(dag.childCount()):
            child = nom.MFnDagNode(dag.child(i))
            children += self.getTree(child)
        return children

class MCallbackIdWrapper(object):
    '''Wrapper class to handle cleaning up of MCallbackIds from registered MMessage
    '''
    def __init__(self, callbackId):
        super(MCallbackIdWrapper, self).__init__()
        self.callbackId = callbackId

    def __del__(self):
        nom.MMessage.removeCallback(self.callbackId)

    def __repr__(self):
        return 'MCallbackIdWrapper(%r)'%self.callbackId# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
