from builtins import range
from builtins import object
import json
# Connection data consists of a list of objects (nodes and groups)
class ConnectionData(object):

    # The 'i' in objects is a temporary index, generated per access to obj

    def __init__(self):
        self.data = []
        self.groups = 1
        self.lastOutput = 0
        self.hashedUUIDs = set([])

    def isEmpty(self):
        return len(self.data)==0

    def toString(self):
        return json.dumps({"data":self.data, "groups":self.groups, "lastOutput":self.lastOutput})

    def initFromString(self, string):
        inst = json.loads(string)
        self.data = inst["data"]
        self.groups = inst["groups"]
        self.lastOutput = inst["lastOutput"]
        self.hashedUUIDs = set(self.getAllObjects(uuid=True) or [])

    def makeGroup(self, objects=None):
        group = {"id":self.groups, "name":"Group", "conns":[], "objects":[], "i":[]}
        if not (objects is None):
            for obj in objects:
                group['objects'].append(obj)
        self.groups+=1
        return group

    def makeObject(self, uuid, conns=None):
        if conns is None:
            conns = []
        obj = {"uuid":uuid, "conns":conns, "i":[], "outputId":self.lastOutput}
        self.lastOutput+=1
        self.hashedUUIDs.add(uuid)
        return obj

    def getObject(self, indexesToObject):
        if(len(indexesToObject)==0): return None
        obj = self.data[indexesToObject[0]]
        for i in indexesToObject[1:]:
            obj = obj["objects"][i]
        obj["i"] = [] + indexesToObject    
        return obj

    def getAllObjects(self, group=None, uuid=False):
        allObjects = []
        indexes = []
        if(group is None):
            group = self.data
        elif not self.isGroup(group):
            if not uuid:
                return [group]
            else:
                return [group["uuid"]]
        else:
            indexes = list(group["i"])
            group = group["objects"]

        indexes.append(0)

        for o in group:
            o["i"] = list(indexes)
            if(not self.isGroup(o)):
                if not uuid:
                    allObjects.append(o)
                else:
                    allObjects.append(o["uuid"])
            else:
                allObjects += self.getAllObjects(o, uuid)
            indexes[-1]+=1
        return allObjects

    def insertObject(self, obj, group=None, index=-1):
        objs = None
        indexes = []
        if(group is None):
            objs = self.data
        else:
            objs = group["objects"]
            indexes = group["i"]
        if index==-1:
            index = len(objs)
        objs.insert(index, obj)
        obj["i"] = indexes + [objs.index(obj)]
        self.rebuildIndexesInGroup(group)

    def isGroup(self, obj):
        return ("objects" in obj)

    def getConns(self, obj):
        if obj is None:
            return []
        if not "i" in obj:
            return obj["conns"]
        allConns = self.getParentConns(obj)
        allConns += obj["conns"]
        return allConns

    def getParentConns(self, obj):
        if not "i" in obj:
            return []
        allGroups = self.getObjGroups(obj)
        allConns = []
        for group in allGroups:
            allConns += group["conns"]
        return allConns

    def deleteObject(self, obj):
        groups = self.getObjGroups(obj)
        if len(groups)==0:
            self.data.remove(obj)
        else:
            groups[-1]["objects"].remove(obj)

    def rebuildParentIndex(self, group, newIndex, parentIndexofIndex):
        for obj in group["objects"]:
            obj["i"][parentIndexofIndex] = newIndex
            if self.isGroup(obj):
                self.rebuildParentIndex(obj, newIndex, parentIndexofIndex)

    def rebuildIndexesInGroup(self, group=None):
        if group is None:
            for i in range(len(self.data)):
                dobj = self.data[i]
                dobj["i"][0] = i
                if(self.isGroup(dobj)):
                    self.rebuildParentIndex(dobj, i, 0)
        else:
            iofI = len(group["i"])
            for i in range(len(group["objects"])):
                dobj = group["objects"][i]
                dobj["i"][iofI] = i
                if(self.isGroup(dobj)):
                    self.rebuildParentIndex(dobj, i, iofI)

    def elevateObject(self, obj):
        groups = self.getObjGroups(obj)
        self.removeObject(obj)

        if(len(groups)>=2):
            self.insertObject(obj, groups[-2])
            self.rebuildIndexesInGroup(groups[-2])
        else:
            self.data.append(obj)
            self.rebuildIndexesInGroup()

    def getObjParent(self, obj):
        groups = self.getObjGroups(obj)
        if len(groups)==0:
            return None
        else:
            return groups[-1]

    def getObjGroups(self, obj):
        if not obj or not "i" in obj or len(obj["i"])==0:
            return []
        allGroups = []
        indexes = obj["i"]
        group = self.data[indexes[0]]
        for i in indexes[1:]:
            allGroups.append(group)
            group = group["objects"][i]
        return allGroups

    def moveObjFromTo(self, fromI, toI):
        index = toI[-1]
        group = self.getObjParent(self.getObject(toI[:-1]))

        obj = self.getObject(fromI)
        self.removeObject(obj)
        self.insertObject(obj, group, index)
        self.rebuildIndexesInGroup(group)

    def removeObject(self, obj):
        if not self.isGroup(obj) and (obj['uuid'] in self.hashedUUIDs):
            self.hashedUUIDs.remove(obj['uuid'])

        groups = self.getObjGroups(obj)
        if len(groups)==0:
            self.data.remove(obj)
            self.rebuildIndexesInGroup()
        else:
            groups[-1]["objects"].remove(obj)
            self.rebuildIndexesInGroup(groups[-1])
        del obj["i"][-1]

    def connectionOnAttr(self, obj, attr):
        for conn in obj["conns"]:
            if ('->' + attr) in conn:
                return conn
        return None
        
    def getObjectByUUID(self, uuid):
        for dobj in self.getAllObjects():
            if dobj['uuid'] == uuid:
                return dobj
        return None
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
