# Copyright (C) Mainframe
# Created by Alan Stanzione on 14/09/2015.

from builtins import object
from builtins import range
import maya.cmds
import maya.mel
import maya.OpenMaya as om
import re


class ReproUpdating(object):
    def __init__(self, repro_node):
        self.repro_node = repro_node

    def __enter__(self):
        maya.cmds.setAttr("%s.updating" % self.repro_node, 1)

    def __exit__(self, type, value, traceback):
        maya.cmds.setAttr("%s.updating" % self.repro_node, 0)
        if  maya.cmds.getAttr("%s.finishUpdating" % self.repro_node):
            maya.cmds.setAttr("%s.finishUpdating" % self.repro_node, 0)
        else:
            maya.cmds.setAttr("%s.finishUpdating" % self.repro_node, 1)

def create_mash_repro_node(mash_network_node=None, name=None):
    """
    Create a repro node and attach it to the selected MASH Waiter node or to the node specified by mash_network_node

    :param mash_network_node: Mash Waiter node or None to use the selected one
    :return: Repro node
    """
    if mash_network_node is None:
        mash_nodes = maya.cmds.ls(sl=1, type="MASH_Waiter") or []
        if len(mash_nodes) > 0:
            repro_node = None
            for node in mash_nodes:
                repro_node = create_mash_repro_node(node)
            return repro_node

    repro_node = maya.cmds.createNode("MASH_Repro", ss=True, name=name or "MASH_Repro")
    repro_mesh_shape = maya.cmds.createNode("mesh",n=repro_node + "MeshShape")
    repro_mesh = maya.cmds.listRelatives(repro_mesh_shape, p=True)[0]
    maya.cmds.addAttr( repro_mesh, longName='mashOutFilter', attributeType='bool' )
    maya.cmds.connectAttr("%s.outMesh" % repro_node, "%s.inMesh" % repro_mesh_shape)
    maya.cmds.connectAttr("%s.worldInverseMatrix[0]" % repro_mesh_shape, "%s.meshMatrix" % repro_node)
    maya.cmds.connectAttr("%s.message" % repro_mesh_shape, "%s.meshMessage" % repro_node)
    if mash_network_node is not None:
        if maya.cmds.objExists(mash_network_node):
            maya.cmds.connectAttr("%s.outputPoints" % mash_network_node,  "%s.inputPoints" % repro_node, f=True)
    #TODO: Move to C++ legacy check
    maya.cmds.setAttr(repro_node+".normalMode", 1)
    return repro_node


def new_non_numeric_multi_add_new_item(node, multi_attr):
    """
    Create a new index inside the multi array, using the first available

    :param node: Node name
    :param multi_attr: Multi attribute name
    :return: new index created
    """
    attr = "%s.%s" % (node, multi_attr)
    # Find the next available index
    next_available = 0
    multi = maya.cmds.getAttr(attr, mi=True) or []
    found_next = False
    while not found_next:
        found_next = not (next_available in multi)
        if not found_next:
            next_available += 1
        else:
            break
    # Creat a new plug.
    maya.cmds.getAttr("%s[%d]" % (attr, next_available), type=True)
    return next_available


def get_meshes_from_group(group_node):
    """
    Get all mesh nodes inside a group

    :param group_node: Group node name
    :return: List of meshes
    """
    mashes = maya.cmds.ls(group_node, l=True, type="mesh", dag=True, lf=True, ni=True) or []
    return mashes


def clean_index(mash_repro_node, index):
    """
    Remove an index from the Repro node

    :param mash_repro_node: MASH Repro node
    :param index: Object index
    """
    # delete groupIds attached
    mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh" % (mash_repro_node, index), mi=True) or []
    for i in mi:
        gi_mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].groupId" % (mash_repro_node, index, i), mi=1) or []
        for gid in gi_mi:
            groupId = maya.cmds.listConnections("%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (mash_repro_node, index, i, gid), s=True, t="groupId") or []
            if groupId:
                group_ids_connections = maya.cmds.listConnections("%s.groupId" % groupId[0], d=1, p=1) or []
                for groupIdConn in group_ids_connections:
                    if not re.search(".instObjGroups.objectGroups\[\d\].objectGroupId", groupIdConn):
                        continue
                    maya.cmds.removeMultiInstance('.'.join(groupIdConn.split('.')[:-1]), b=True)
                maya.cmds.delete(groupId)
    mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (mash_repro_node, index), mi=True) or []
    for i in mi:
        clean_proxy_index(mash_repro_node, index, i)
    return maya.cmds.removeMultiInstance("%s.instancedGroup[%d]" % (mash_repro_node, index), b=True)


def clean_proxy_index(mash_repro_node, instance_index, index):
    """
    Remove a proxy index from the Repro node

    :param mash_repro_node: MASH Repro node
    :param instance_index: Object index
    :param index: Proxy index
    """
    mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy" % (mash_repro_node, instance_index, index), mi=True) or []
    for i in mi:
        gi_mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId" % (mash_repro_node, instance_index, index, i), mi=1) or []
        for gid in gi_mi:
            group_id = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (mash_repro_node, instance_index, index, i, gid), s=True, t="groupId") or []
            if group_id:
                group_ids_connections = maya.cmds.listConnections("%s.groupId" % group_id[0], d=1, p=1) or []
                for groupIdConn in group_ids_connections:
                    if not re.search(".instObjGroups.objectGroups\[\d\].objectGroupId", groupIdConn):
                        continue
                    maya.cmds.removeMultiInstance('.'.join(groupIdConn.split('.')[:-1]), b=True)
                maya.cmds.delete(group_id)
    return maya.cmds.removeMultiInstance("%s.instancedGroup[%d].proxyGroup[%d]" % (mash_repro_node, instance_index, index), b=True)


def initialize_index(mash_repro_node, index):
    """
    Initialize a instanced object index

    :param mash_repro_node: MASH Repro node
    :param index: Object index
    :return: Attribute name created and his index
    """
    if index is not None:
        clean_index(mash_repro_node, index)
        maya.cmds.getAttr("%s.instancedGroup[%d]" % (mash_repro_node, index), type=True)
    else:
        index = new_non_numeric_multi_add_new_item(mash_repro_node, "instancedGroup")
    maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[0]" % (mash_repro_node, index), type=True)
    return "%s.instancedGroup[%d]" % (mash_repro_node, index), index


def initialize_proxy_index(mash_repro_node, instance_index, index):
    """
    Initialize a proxy object index

    :param mash_repro_node: MASH Repro node
    :param instance_index: Object index
    :param index: Proxy index
    :return: Attribute name created and his index
    """
    if index is not None:
        clean_proxy_index(mash_repro_node, instance_index, index)
        maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d]" % (mash_repro_node, instance_index, index), type=True)
    else:
        index = new_non_numeric_multi_add_new_item(mash_repro_node, "instancedGroup[%d].proxyGroup" % instance_index)
    maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[0]" % (mash_repro_node, instance_index, index), type=True)
    return "%s.instancedGroup[%d].proxyGroup[%d]" % (mash_repro_node, instance_index, index), index


def get_shading_groups(shape_node):
    """
    Get all shading groups connected to the shape node

    :param shape_node: Maya shape node
    :return: List of shading groups attached to the shape node
    """
    sg_nodes = maya.cmds.listConnections(shape_node, type='shadingEngine') or []
    return sg_nodes


def get_groupids_and_shaders(shape_node):
    """
    Get all groups ids and shading groups connected to the shape node

    :param shape_node: Maya shape node
    :return: Map of group ids and their shading groups
    """
    gids = {}
    defaul_connections = maya.cmds.listConnections("%s.instObjGroups[0]" % shape_node, type='shadingEngine')
    if defaul_connections:
        gids[-1] = [defaul_connections[0], None]

    # if there is no default connections check for components connections
    mi = maya.cmds.getAttr("%s.instObjGroups[0].objectGroups" % shape_node, mi=1) or []
    for i in mi:
        sg_connections = maya.cmds.listConnections("%s.instObjGroups[0].objectGroups[%d]" % (shape_node, i), type='shadingEngine')
        if sg_connections:
            group_id = maya.cmds.getAttr("%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (shape_node, i))
            gids[group_id] = [sg_connections[0], "%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (shape_node, i)]
    return gids


def get_out_mesh(mash_repro_node):
    """
    Get out mesh connected to the Repro node

    :param mash_repro_node: MASH Repro node
    :return: Mesh connected to the output of the Repro node
    """
    if maya.cmds.attributeQuery("meshMessage", node=mash_repro_node, ex=True):
        return maya.cmds.listConnections("%s.meshMessage" % mash_repro_node, s=True, type="mesh", shapes=True) or []
    return maya.cmds.listConnections("%s.outMesh" % mash_repro_node, d=True, type="mesh", shapes=True) or []

def get_next_multi_index(node, attribute):
    """
    Get the next free index for the multi attribute

    :param node: Node
    :param attribute: Attribute name
    :return: Index of the first free not connected index
    """
    indices = maya.cmds.getAttr(r'%s.%s' % (node, attribute), multiIndices=True)
    return indices[-1] + 1 if indices else 0

def get_free_index_without_connections(node, attribute):
    """
    Get the first free index not connected fo the multi attribute

    :param node: Node
    :param attribute: Attribute name
    :return: Index of the first free not connected index
    """
    mi = maya.cmds.getAttr("%s.%s" % (node, attribute), mi=True) or []
    index = 0
    if mi:
        for idx in mi:
            if not maya.cmds.listConnections("%s.%s[%d]" % (node, attribute, idx)):
                index = idx
                break
        else:
            index = mi[-1] + 1
    return index

def get_free_index(node, attribute):
    """
    Get the first free index not connected fo the multi attribute

    :param node: Node
    :param attribute: Attribute name
    :return: Index of the first free not connected index
    """
    mi = maya.cmds.getAttr("%s.%s" % (node, attribute), mi=True) or []
    if not mi:
        return 0
    mi.sort()
    return mi[-1] + 1

def connect_mesh_group(mash_repro_node, group_node, index=None, new_connection=False):
    """
    Connect the mesh group node to the Repro node

    :param mash_repro_node: MASH Repro node
    :param group_node: Group node
    :param index: Attribute index, if None it use the first free available index
    :param: new_connection: Optimisations can be enabled for new connections 
    :return: Attribute index
    """
    out_meshes = get_out_mesh(mash_repro_node)
    if not out_meshes:
        return
    out_mesh = out_meshes[0]

    if maya.cmds.objectType(group_node) == "mesh":
        group_node = maya.cmds.listRelatives(group_node, p=True)[0]

    meshes_tmp = get_meshes_from_group(group_node)
    meshes = []
    for mesh in meshes_tmp:
        if mesh.split('|')[-1] != out_mesh:
            meshes.append(mesh)

    if not meshes:
        return

    with ReproUpdating(mash_repro_node):
        # remove default shading
        init_shading_connection = maya.cmds.listConnections("%s.instObjGroups[0]" % out_mesh, type="shadingEngine", d=1, p=1) or []
        for sg in init_shading_connection:
            if "initialShadingGroup" in sg:
                maya.cmds.disconnectAttr("%s.instObjGroups[0]" % out_mesh, sg)

        # clean all index created automatically by the node editor
        num_groups = maya.cmds.getAttr("%s.instancedGroup" % mash_repro_node, mi=True) or []
        for group in num_groups:
            child_ids = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh" % (mash_repro_node, group), mi=True) or []
            if not child_ids:
                clean_index(mash_repro_node, group)
                continue
            if len(child_ids) == 1:
                connections = maya.cmds.listConnections("%s.instancedGroup[%d].instancedMesh[%d].mesh" % (mash_repro_node, group, child_ids[0]), s=1) or []
                if len(connections) == 0:
                    # no connections, so it's an empty attribute, delete it
                    clean_index(mash_repro_node, group)
            else:
                # get group name
                groups_connections = maya.cmds.listConnections("%s.instancedGroup[%d].groupMessage" % (mash_repro_node, group), s=1) or []
                if len(groups_connections) == 0:
                    # no connections, so it's an empty attribute, delete it
                    clean_index(mash_repro_node, group)

        multi_attr, index = initialize_index(mash_repro_node, index)

        maya.cmds.connectAttr("%s.message" % group_node, "%s.groupMessage" % multi_attr)
        maya.cmds.connectAttr("%s.worldMatrix[0]" % group_node, "%s.groupMatrix" % multi_attr)
        for i, mesh in enumerate(meshes):
            maya.cmds.connectAttr("%s.outMesh" % mesh, "%s.instancedMesh[%d].mesh" % (multi_attr, i))
            maya.cmds.connectAttr("%s.worldMatrix" % mesh, "%s.instancedMesh[%d].matrix" % (multi_attr, i))
            gids = get_groupids_and_shaders(mesh)
            counter = 0
            for gid in list(gids.keys()):
                sg_data = gids[gid]
                group_id_node = maya.cmds.createNode("groupId", ss=True)
                if group_id_node:
                    maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (mash_repro_node, index, i, counter))
                    if gid != -1:
                        maya.cmds.connectAttr(sg_data[1], "%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (mash_repro_node, index, i, counter))
                    else:
                        maya.cmds.setAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (mash_repro_node, index, i, counter), -1)

                    # attach shaders
                    maya.cmds.getAttr("%s.instObjGroups[0]" % out_mesh, type=True)
                    maya.cmds.getAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, index), type=True)
                    obj_inst_group_id = 0
                    if new_connection:
                        obj_inst_group_id = get_next_multi_index(out_mesh, "instObjGroups[0].objectGroups")
                    else:
                        obj_inst_group_id = get_free_index_without_connections(out_mesh, "instObjGroups[0].objectGroups")
                    maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (out_mesh, obj_inst_group_id), f=True)

                    sg = sg_data[0]
                    if not sg:
                        continue
                    # connect groupId to sgs
                    group_node_index = 0
                    if new_connection:
                        group_node_index = get_next_multi_index(sg, "groupNodes")
                    else:
                        group_node_index = get_free_index_without_connections(sg, "groupNodes")
                    maya.cmds.connectAttr("%s.message" % group_id_node, "%s.groupNodes[%d]" % (sg, group_node_index))
                    dag_set_member_id = 0
                    if new_connection:
                        dag_set_member_id = get_next_multi_index(sg, "dagSetMembers")
                    else:
                        dag_set_member_id = get_free_index_without_connections(sg, "dagSetMembers")
                    
                    try:
                        maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id), f=True)
                    except:
                        dag_set_member_id = get_free_index(sg, "dagSetMembers")
                        maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id), f=True)
                    maya.cmds.connectAttr("%s.memberWireframeColor" % sg, "%s.instObjGroups[0].objectGroups[%d].objectGrpColor" % (out_mesh, obj_inst_group_id), f=True)
                    counter += 1
        hasMASHFlag = maya.cmds.objExists('%s.mashOutFilter' % (group_node))
        if not hasMASHFlag:
            maya.cmds.addAttr( group_node, longName='mashOutFilter', attributeType='bool' )
    return index


def connect_proxy_group(mash_repro_node, group_node, instance_index, index=None):
    """
    Connect the mesh group node to the Repro node as proxy obejct

    :param mash_repro_node: MASH Repro node
    :param group_node: Group node
    :param instance_index: Object index
    :param index: Attribute index, if None it use the first free available index
    :return: Attribute index
    """
    out_meshes = get_out_mesh(mash_repro_node)
    if not out_meshes:
        return
    out_mesh = out_meshes[0]

    if maya.cmds.objectType(group_node) == "mesh":
        group_node = maya.cmds.listRelatives(group_node, p=True)[0]

    meshes_tmp = get_meshes_from_group(group_node)
    meshes = []
    for mesh in meshes_tmp:
        if mesh.split('|')[-1] != out_mesh:
            meshes.append(mesh)

    if not meshes:
        return

    with ReproUpdating(mash_repro_node):
        # remove default shading
        init_shading_connection = maya.cmds.listConnections("%s.instObjGroups[0]" % out_mesh, type="shadingEngine", d=1, p=1) or []
        for sg in init_shading_connection:
            if "initialShadingGroup" in sg:
                maya.cmds.disconnectAttr("%s.instObjGroups[0]" % out_mesh, sg)

        # clean all index created automatically by the node editor
        num_groups = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (mash_repro_node, instance_index), mi=True) or []
        for group in num_groups:
            child_ids = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy" % (mash_repro_node, instance_index, group), mi=True) or []
            if not child_ids:
                clean_proxy_index(mash_repro_node, instance_index, group)
                continue
            if len(child_ids) == 1:
                connections = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyMesh" % (mash_repro_node, instance_index, group, child_ids[0]), s=1) or []
                if len(connections) == 0:
                    clean_proxy_index(mash_repro_node, instance_index, group)
            else:
                # get group name
                groups_connections = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (mash_repro_node, instance_index, group), s=1) or []
                if len(groups_connections) == 0:
                    clean_proxy_index(mash_repro_node, instance_index, group)

        multi_attr, index = initialize_proxy_index(mash_repro_node, instance_index, index)
        maya.cmds.connectAttr("%s.message" % group_node, "%s.proxyGroupMessage" % multi_attr)
        maya.cmds.connectAttr("%s.worldMatrix[0]" % group_node, "%s.proxyGroupMatrix" % multi_attr)
        for i, mesh in enumerate(meshes):
            maya.cmds.connectAttr("%s.outMesh" % mesh, "%s.proxy[%d].proxyMesh" % (multi_attr, i))
            maya.cmds.connectAttr("%s.worldMatrix" % mesh, "%s.proxy[%d].proxyMatrix" % (multi_attr, i))
            gids = get_groupids_and_shaders(mesh)
            counter = 0
            for gid in list(gids.keys()):
                sg_data = gids[gid]
                group_id_node = maya.cmds.createNode("groupId", ss=True)
                if group_id_node:
                    maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter))
                    if gid != -1:
                        maya.cmds.connectAttr(sg_data[1], "%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter))
                    else:
                        maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter), -1)

                    # attach shaders
                    maya.cmds.getAttr("%s.instObjGroups[0]" % out_mesh, type=True)
                    maya.cmds.getAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, index), type=True)
                    obj_inst_group_id = get_free_index_without_connections(out_mesh, "instObjGroups[0].objectGroups")
                    maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (out_mesh, obj_inst_group_id))

                    sg = sg_data[0]
                    if not sg:
                        continue
                    # connect groupId to sgs
                    group_node_index = get_free_index_without_connections(sg, "groupNodes")
                    maya.cmds.connectAttr("%s.message" % group_id_node, "%s.groupNodes[%d]" % (sg, group_node_index))
                    dag_set_member_id = get_free_index_without_connections(sg, "dagSetMembers")
                    try:
                        maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
                    except:
                        dag_set_member_id = get_free_index(sg, "dagSetMembers")
                        maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
                    maya.cmds.connectAttr("%s.memberWireframeColor" % sg, "%s.instObjGroups[0].objectGroups[%d].objectGrpColor" % (out_mesh, obj_inst_group_id))
                    counter += 1

        hasMASHFlag = maya.cmds.objExists('%s.mashOutFilter' % (group_node))
        if not hasMASHFlag:
            maya.cmds.addAttr( group_node, longName='mashOutFilter', attributeType='bool' )
    return index


def get_data_layout(mash_repro_node):
    """
    Get a map of all the objects and proxy objects connected to the Repro node

    :param mash_repro_node: MASH Repro node
    :return: Map af all connected object
    """
    data = {}
    group_ids = maya.cmds.getAttr("%s.instancedGroup" % mash_repro_node, mi=True) or []
    for g_id in group_ids:
        connections = maya.cmds.listConnections("%s.instancedGroup[%d].groupMessage" % (mash_repro_node, g_id), s=1) or []
        if len(connections) == 0:
            continue

        data[g_id] = {}
        data[g_id]["group"] = connections[0]
        data[g_id]["displayType"] = maya.cmds.getAttr("%s.instancedGroup[%d].displayType" % (mash_repro_node, g_id))
        p_ids = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (mash_repro_node, g_id), mi=True) or []
        data[g_id]["proxies"] = {}
        for p_id in p_ids:
            connections = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (mash_repro_node, g_id, p_id), s=1) or []
            if len(connections) == 0:
                continue
            data[g_id]["proxies"][p_id] = {}
            data[g_id]["proxies"][p_id]["group"] = connections[0]
            data[g_id]["proxies"][p_id]["proxyLod"] = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, g_id, p_id))
    return data

def remove_mesh_group(mash_repro_node, index):
    """
    Remove an object from the Repro node

    :param mash_repro_node: MASH Repro node
    :param index: Object index
    :return: None
    """
    with ReproUpdating(mash_repro_node):
        data = get_data_layout(mash_repro_node)
        indices = list(data.keys())
        indices.sort()
        if index in indices:
            position = indices.index(index)
            for i in range(position, len(indices)):
                clean_index(mash_repro_node, indices[i])
            for i in range(position + 1, len(indices)):
                new_index = connect_mesh_group(mash_repro_node, data[indices[i]]['group'])
                maya.cmds.setAttr("%s.instancedGroup[%d].displayType" % (mash_repro_node, new_index), data[indices[i]]['displayType'])
                for p_id in list(data[indices[i]]['proxies'].keys()):
                    new_p_index = connect_proxy_group(mash_repro_node, data[indices[i]]['proxies'][p_id]['group'], new_index)
                    maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, new_index, new_p_index), data[indices[i]]['proxies'][p_id]['proxyLod'])
                    hasMASHFlag = maya.cmds.objExists('%s.mashOutFilter' % (data[indices[i]]['proxies'][p_id]['group']))
                    if hasMASHFlag:
                        maya.cmds.deleteAttr( data[indices[i]]['proxies'][p_id]['group'], at='mashOutFilter' )
            hasMASHFlag = maya.cmds.objExists('%s.mashOutFilter' % (data[indices[i]]['group']))
            if hasMASHFlag:
                maya.cmds.deleteAttr( data[indices[i]]['group'], at='mashOutFilter' )

def remove_proxy_group(mash_repro_node, instance_index, index):
    """
    Remove a proxy object from the Repro node

    :param mash_repro_node: MASH Repro node
    :param instance_index: Object index
    :param index: Proxy index
    :return: None
    """
    with ReproUpdating(mash_repro_node):
        data = get_data_layout(mash_repro_node)
        indices = list(data[instance_index]['proxies'].keys())
        indices.sort()
        if index in indices:
            position = indices.index(index)
            for i in range(position, len(indices)):
                clean_proxy_index(mash_repro_node, instance_index, indices[i])
            for i in range(position + 1, len(indices)):
                if 'group' in data[instance_index]['proxies'][indices[i]]:
                    new_index = connect_proxy_group(mash_repro_node, data[instance_index]['proxies'][indices[i]]['group'], instance_index)
                    maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, instance_index, new_index), data[instance_index]['proxies'][indices[i]]['proxyLod'])
                    hasMASHFlag = maya.cmds.objExists('%s.mashOutFilter' % (data[instance_index]['proxies'][indices[i]]['group']))
                    if hasMASHFlag:
                        maya.cmds.deleteAttr( data[instance_index]['proxies'][indices[i]]['group'], at='mashOutFilter' )

def reorder_mesh_group_node(mash_repro_node, new_order):
    """
    Reorder the instanced objects

    :param mash_repro_node: MASH Repro node
    :param new_order: list with the new index order
    :return: None
    """
    with ReproUpdating(mash_repro_node):
        data = get_data_layout(mash_repro_node)
        indices = list(data.keys())
        indices.sort()
        for index in indices:
            clean_index(mash_repro_node, index)
        for i in new_order:
            new_index = connect_mesh_group(mash_repro_node, data[i]['group'])
            maya.cmds.setAttr("%s.instancedGroup[%d].displayType" % (mash_repro_node, new_index), data[i]['displayType'])
            for p_id in list(data[i]['proxies'].keys()):
                new_p_index = connect_proxy_group(mash_repro_node, data[i]['proxies'][p_id]['group'], new_index)
                maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, new_index, new_p_index), data[i]['proxies'][p_id]['proxyLod'])

def reorder_proxy_group_node(mash_repro_node, instance_index, new_order):
    """
    Reorder the proxies of an instanced object

    :param mash_repro_node: MASH Repro node
    :param instance_index: Objects index
    :param new_order: List with the new index order
    :return: None
    """
    with ReproUpdating(mash_repro_node):
        data = get_data_layout(mash_repro_node)
        indices = list(data[instance_index]['proxies'].keys())
        indices.sort()
        for index in indices:
            clean_proxy_index(mash_repro_node, instance_index, index)
        for i in new_order:
                new_index = connect_proxy_group(mash_repro_node, data[instance_index]['proxies'][i]['group'], instance_index)
                maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, instance_index, new_index), data[instance_index]['proxies'][i]['proxyLod'])

def refresh_mesh_group(mash_repro_node, index):
    """
    Refresh an instanced object, updating all the meshes and shaders

    :param mash_repro_node: MASH Repro node
    :param index: Objects index
    :return: None
    """
    data = get_data_layout(mash_repro_node)
    new_index = connect_mesh_group(mash_repro_node, data[index]['group'], index)
    maya.cmds.setAttr("%s.instancedGroup[%d].displayType" % (mash_repro_node, new_index), data[index]['displayType'])
    for p_id in list(data[index]['proxies'].keys()):
        new_p_index = connect_proxy_group(mash_repro_node, data[index]['proxies'][p_id]['group'], new_index)
        maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, new_index, new_p_index), data[index]['proxies'][p_id]['proxyLod'])

def refresh_proxy_group(mash_repro_node, instance_index, index):
    """
    Refresh an instanced object, updating all the meshes and shaders

    :param mash_repro_node: MASH Repro node
    :param instance_index: Objects index
    :param index: Proxy index
    :return: None
    """
    data = get_data_layout(mash_repro_node)
    new_index = connect_proxy_group(mash_repro_node, data[instance_index]['proxies'][index]['group'], instance_index, index)
    maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (mash_repro_node, instance_index, new_index), data[instance_index]['proxies'][index]['proxyLod'])


def get_group_index(mash_repro_node, group_node):
    """
    Return the index of the group node connected to the Repro node

    :param mash_repro_node: MASH Repro node
    :param group_node: Group node name
    :return: Object index
    """
    indices = maya.cmds.getAttr("%s.instancedGroup" % mash_repro_node, mi=True) or []
    for index in indices:
        connections = maya.cmds.listConnections("%s.instancedGroup[%d].groupMessage" % (mash_repro_node, index), p=0, s=1) or []
        if connections:
            if connections[0] == group_node:
                return index
    return None


def get_proxy_group_index(mash_repro_node, group_node, proxy_node):
    """
    Return the index of the proxy group node connected to the Repro node

    :param mash_repro_node: MASH Repro node
    :param group_node: Group node name or group index
    :param proxy_node: Proxy group node name
    :return: Object index
    """
    if isinstance(group_node, str):
        group_index = get_group_index(mash_repro_node, group_node)
    else:
        group_index = group_node
    indices = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (mash_repro_node, group_index), mi=True) or []
    for index in indices:
        connections = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (mash_repro_node, group_index, index), p=0, s=1) or []
        if connections:
            if connections[0] == proxy_node:
                return index
    return None


def move_group_node(mash_repro_node, old, new):
    """
    Move an object to a new index, the other objects are shifted

    :param mash_repro_node: MASH Repro node
    :param old: Old group index
    :param new: New group index
    :return: None
    """
    new_order = maya.cmds.getAttr("%s.instancedGroup" % mash_repro_node, mi=True) or []
    new_order.pop(old)
    new_order.insert(new, old)
    reorder_mesh_group_node(mash_repro_node, new_order)


def move_proxy_group_node(mash_repro_node, instance_index, old, new):
    """
    Move an proxy object to a new index, the other objects are shifted

    :param mash_repro_node: MASH Repro node
    :param instance_index: Instanced object index
    :param old: Old group index
    :param new: New group index
    :return: None
    """
    new_order = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (mash_repro_node, instance_index), mi=True) or []
    new_order.pop(old)
    new_order.insert(new, old)
    reorder_proxy_group_node(mash_repro_node, instance_index, new_order)

def updateSurface(mesh_node):
    """
    Force a redraw of a mesh

    :param mash_node: mesh node
    """
    sel_list = om.MSelectionList()
    sel_list.add(mesh_node)
    node = om.MObject()
    sel_list.getDependNode(0,node)
    mesh = om.MFnMesh(node)
    mesh.updateSurface()

def clean_mesh_shaders(mash_repro_node, instanced_index, mesh_index):
    """
    Remove all the shader of the object attached to the repro node

    :param mash_repro_node: Mash repro node
    :param instanced_index: Object index
    :param mesh_index: Mesh index
    """
    group_ids_mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].groupId" % (mash_repro_node, instanced_index, mesh_index), mi=True)
    #shader_ids_mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId" % (mash_repro_node, instanced_index, mesh_index), mi=True)
    for gid in group_ids_mi:
        groupId = maya.cmds.listConnections("%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (mash_repro_node, instanced_index, mesh_index, gid), s=True, t="groupId") or []
        if groupId:
            group_ids_connections = maya.cmds.listConnections("%s.groupId" % groupId[0], d=1, p=1) or []
            for groupIdConn in group_ids_connections:
                if not re.search(".instObjGroups.objectGroups\[\d\].objectGroupId", groupIdConn):
                    continue
                maya.cmds.removeMultiInstance('.'.join(groupIdConn.split('.')[:-1]), b=True)
            maya.cmds.delete(groupId)
        maya.cmds.removeMultiInstance("%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (mash_repro_node, instanced_index, mesh_index, gid), b=True)
        maya.cmds.removeMultiInstance("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (mash_repro_node, instanced_index, mesh_index, gid), b=True)

def update_mesh_shaders(mash_repro_node, instanced_index, mesh_index, mesh):
    """
    Update all the shader of the object attached to the repro node

    :param mash_repro_node: Mash repro node
    :param instanced_index: Object index
    :param mesh_index: Mesh index
    :param mesh: mesh node
    """
    out_meshes = get_out_mesh(mash_repro_node)
    if not out_meshes:
        return
    out_mesh = out_meshes[0]
    index = instanced_index
    i = mesh_index
    gids = get_groupids_and_shaders(mesh)
    counter = 0
    for gid in list(gids.keys()):
        sg_data = gids[gid]
        group_id_node = maya.cmds.createNode("groupId", ss=True)
        if group_id_node:
            maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (mash_repro_node, index, i, counter))
            if gid != -1:
                maya.cmds.connectAttr(sg_data[1], "%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (mash_repro_node, index, i, counter))
            else:
                maya.cmds.setAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (mash_repro_node, index, i, counter), -1)

            # attach shaders
            maya.cmds.getAttr("%s.instObjGroups[0]" % out_mesh, type=True)
            maya.cmds.getAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, index), type=True)
            obj_inst_group_id = get_free_index_without_connections(out_mesh, "instObjGroups[0].objectGroups")
            maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (out_mesh, obj_inst_group_id))

            sg = sg_data[0]
            if not sg:
                continue
            # connect groupId to sgs
            group_node_index = get_free_index_without_connections(sg, "groupNodes")
            maya.cmds.connectAttr("%s.message" % group_id_node, "%s.groupNodes[%d]" % (sg, group_node_index))
            dag_set_member_id = get_free_index_without_connections(sg, "dagSetMembers")
            try:
                maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
            except:
                dag_set_member_id = get_free_index(sg, "dagSetMembers")
                maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
            maya.cmds.connectAttr("%s.memberWireframeColor" % sg, "%s.instObjGroups[0].objectGroups[%d].objectGrpColor" % (out_mesh, obj_inst_group_id))
            counter += 1

def get_proxy_mesh(mash_repro_node, instance_index, proxy_index):
    conns = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (mash_repro_node, instance_index, proxy_index), s=1)
    return None if conns is None else conns[0]

def clean_proxy_mesh_shaders(mash_repro_node, instance_index, proxy_index, mesh_index):
    """
    Remove all the shader of the oproxy bject attached to the repro node

    :param mash_repro_node: Mash repro node
    :param instanced_index: Object index
    :param proxy_index: Proxy index
    :param mesh_index: Mesh index
    """
    gi_mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId" % (mash_repro_node, instance_index, proxy_index, mesh_index), mi=1) or []
    for gid in gi_mi:
        group_id = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (mash_repro_node, instance_index, proxy_index, mesh_index, gid), s=True, t="groupId") or []
        if group_id:
            group_ids_connections = maya.cmds.listConnections("%s.groupId" % group_id[0], d=1, p=1) or []
            for groupIdConn in group_ids_connections:
                if not re.search(".instObjGroups.objectGroups\[\d\].objectGroupId", groupIdConn):
                    continue
                maya.cmds.removeMultiInstance('.'.join(groupIdConn.split('.')[:-1]), b=True)
            maya.cmds.delete(group_id)
        maya.cmds.removeMultiInstance("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (mash_repro_node, instance_index, proxy_index, mesh_index, gid), b=True)
        maya.cmds.removeMultiInstance("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (mash_repro_node, instance_index, proxy_index, mesh_index, gid), b=True)

def update_proxy_mesh_shaders(mash_repro_node, instance_index, proxy_index, mesh_index, mesh):
    """
    Update all the shader of the proxy object attached to the repro node

    :param mash_repro_node: Mash repro node
    :param instanced_index: Object index
    :param proxy_index: Proxy index
    :param mesh_index: Mesh index
    :param mesh: mesh node
    """
    out_meshes = get_out_mesh(mash_repro_node)
    if not out_meshes:
        return
    out_mesh = out_meshes[0]
    index = proxy_index
    i = mesh_index
    gids = get_groupids_and_shaders(mesh)
    counter = 0
    for gid in list(gids.keys()):
        sg_data = gids[gid]
        group_id_node = maya.cmds.createNode("groupId", ss=True)
        if group_id_node:
            maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter))
            if gid != -1:
                maya.cmds.connectAttr(sg_data[1], "%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter))
            else:
                maya.cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (mash_repro_node, instance_index, index, i, counter), -1)

            # attach shaders
            maya.cmds.getAttr("%s.instObjGroups[0]" % out_mesh, type=True)
            maya.cmds.getAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, index), type=True)
            obj_inst_group_id = get_free_index_without_connections(out_mesh, "instObjGroups[0].objectGroups")
            maya.cmds.connectAttr("%s.groupId" % group_id_node, "%s.instObjGroups[0].objectGroups[%d].objectGroupId" % (out_mesh, obj_inst_group_id))

            sg = sg_data[0]
            if not sg:
                continue
            # connect groupId to sgs
            group_node_index = get_free_index_without_connections(sg, "groupNodes")
            maya.cmds.connectAttr("%s.message" % group_id_node, "%s.groupNodes[%d]" % (sg, group_node_index))
            dag_set_member_id = get_free_index_without_connections(sg, "dagSetMembers")
            try:
                maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
            except:
                dag_set_member_id = get_free_index(sg, "dagSetMembers")
                maya.cmds.connectAttr("%s.instObjGroups[0].objectGroups[%d]" % (out_mesh, obj_inst_group_id), "%s.dagSetMembers[%d]" % (sg, dag_set_member_id))
            maya.cmds.connectAttr("%s.memberWireframeColor" % sg, "%s.instObjGroups[0].objectGroups[%d].objectGrpColor" % (out_mesh, obj_inst_group_id))
            counter += 1

def refresh_shaders_connections(mesh_node):
    """
    Refresh shader connection on the repro nodes attacched to this mesh

    :param mesh_node: mesh node
    """
    if  not maya.cmds.objExists(mesh_node):
        return
    mash_repro_nodes = maya.cmds.listConnections("%s.outMesh" % mesh_node, d=True, p=True, type="MASH_Repro") or []
    for repro_plug in mash_repro_nodes:
        sgs = get_groupids_and_shaders(mesh_node)
        repro_split = repro_plug.split('.')
        repro_node = repro_split[0]
        if repro_split[-1] == "mesh":
            instanced_id = int(repro_split[1][repro_split[1].index('[')+1:repro_split[1].index(']')])
            mesh_id = int(repro_split[2][repro_split[2].index('[')+1:repro_split[2].index(']')])

            input_shader_group_ids = []
            mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].groupId" % (repro_node, instanced_id, mesh_id), mi=True) or []
            mi = maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId" % (repro_node, instanced_id, mesh_id), mi=True) or []

            #check here if jsut a new shader is attached
            mi_ids = []
            for id in mi:
                mi_ids.append(maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (repro_node, instanced_id, mesh_id, id)))

            updated_shader = False
            if list(set(mi_ids) ^ set(sgs.keys())):
                updated_shader = True
            else:
                for id in mi:
                    igid =  maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].inputShaderGroupId[%d]" % (repro_node, instanced_id, mesh_id, id))
                    gid =  maya.cmds.getAttr("%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (repro_node, instanced_id, mesh_id, id))
                    gid_connections = maya.cmds.listConnections("%s.instancedGroup[%d].instancedMesh[%d].groupId[%d]" % (repro_node, instanced_id, mesh_id, id), s=True,p=False) or []

                    if not gid_connections:
                        continue
                    sg_connected = maya.cmds.listConnections("%s.message" % gid_connections[0], d=True, p=False, type="shadingEngine") or []
                    if not sg_connected:
                        continue
                    shader = sg_connected[0]
                    # check if shader exists
                    if igid in sgs:
                        if sgs[igid][0] == shader:
                            continue

                    updated_shader = True
                    break
            if updated_shader:
                clean_mesh_shaders(repro_node, instanced_id, mesh_id)
                update_mesh_shaders(repro_node, instanced_id, mesh_id, mesh_node)
                out_meshes = get_out_mesh(repro_node)
                if out_meshes:
                    updateSurface(out_meshes[0])
                break

        if repro_split[-1] == "proxyMesh":
            instanced_id = int(repro_split[1][repro_split[1].index('[')+1:repro_split[1].index(']')])
            proxy_id = int(repro_split[2][repro_split[2].index('[')+1:repro_split[2].index(']')])
            mesh_id = int(repro_split[3][repro_split[3].index('[')+1:repro_split[3].index(']')])

            input_shader_group_ids = []
            mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId" % (repro_node, instanced_id, proxy_id, mesh_id), mi=True) or []
            mi = maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId" % (repro_node, instanced_id, proxy_id, mesh_id), mi=True) or []

            #check here if jsut a new shader is attached
            mi_ids = []
            for id in mi:
                mi_ids.append(maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (repro_node, instanced_id, proxy_id, mesh_id, id)))

            updated_shader = False
            if list(set(mi_ids) ^ set(sgs.keys())):
                updated_shader = True
            else:
                for id in mi:
                    igid =  maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyInputShaderGroupId[%d]" % (repro_node, instanced_id, proxy_id, mesh_id, id))
                    gid =  maya.cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (repro_node, instanced_id, proxy_id, mesh_id, id))
                    gid_connections = maya.cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxy[%d].proxyGroupId[%d]" % (repro_node, instanced_id, proxy_id, mesh_id, id), s=True,p=False) or []
                    if not gid_connections:
                        continue
                    sg_connected = maya.cmds.listConnections("%s.message" % gid_connections[0], d=True, p=False, type="shadingEngine") or []
                    if not sg_connected:
                        continue
                    shader = sg_connected[0]
                    # check if shader exists
                    if igid in sgs:
                        if sgs[igid][0] == shader:
                            continue

                    updated_shader = True
                    break
            if updated_shader:
                clean_proxy_mesh_shaders(repro_node, instanced_id, proxy_id, mesh_id)
                update_proxy_mesh_shaders(repro_node, instanced_id, proxy_id, mesh_id, mesh_node)
                out_meshes = get_out_mesh(repro_node)
                if out_meshes:
                    updateSurface(out_meshes[0])
                break

def set_out_mesh_display_override(mash_repro_node, value):
    out_meshes = get_out_mesh(mash_repro_node)
    if not out_meshes:
        return
    out_mesh = out_meshes[0]
    transform = maya.cmds.listRelatives(out_mesh, p=True)[0]
    if value:
        maya.cmds.setAttr("%s.overrideEnabled" % transform, 1)
        maya.cmds.setAttr("%s.overrideShading" % transform, 0)
    else:
        maya.cmds.setAttr("%s.overrideEnabled" % transform, 0)
        maya.cmds.setAttr("%s.overrideShading" % transform, 1)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
