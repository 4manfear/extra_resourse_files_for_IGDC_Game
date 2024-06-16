from builtins import object
import maya.cmds as cmds
import MASH.api as mapi
import maya.mel as mel
import InViewMessageWrapper as ivm
import maya.app.flux.core as fx

class SimpleCache(object):
	def __init__(self, waiter):
		self.waiter = waiter
		self.cacheWaiter  = None # we can cache one waiter, but attach to another
		self.tmpInstancer = None
		self.startFrame = cmds.intFieldGrp('mashCacheSEFrame', q=True, v1=True)
		self.endFrame   = cmds.intFieldGrp('mashCacheSEFrame', q=True, v2=True)

		# Determine which channels the user wishes to cache from the MASH Cache Creator dialog. 
		# Based on what's checked off store a list of dictionaries with information needed later on by the createCaches method.
		#
		self.options = []
		if cmds.checkBoxGrp('mCacheTransCbox', q=True, v1=True):
			self.options.append({'attrToCache':'inPositionPP'  , 'cacheAttr':'cacheInArrayPP'   , 'enableFlag': 'enablePosCache'})
		if cmds.checkBoxGrp('mCacheTransCbox', q=True, v2=True):
			self.options.append({'attrToCache':'inRotationPP'  , 'cacheAttr':'cacheRotationPP'  , 'enableFlag': 'enableRotCache'})
		if cmds.checkBoxGrp('mCacheTransCbox', q=True, v3=True):
			self.options.append({'attrToCache':'inScalePP'     , 'cacheAttr':'cacheScalePP'     , 'enableFlag': 'enableScaleCache'})
		if cmds.checkBoxGrp('mCacheUtilsCbox', q=True, v1=True):
			self.options.append({'attrToCache':'inIdPP'        , 'cacheAttr':'cacheIdPP'        , 'enableFlag': 'enableIDCache'})
		if cmds.checkBoxGrp('mCacheUtilsCbox', q=True, v2=True):
			self.options.append({'attrToCache':'inVisibilityPP', 'cacheAttr':'cacheVisibilityPP', 'enableFlag': 'enableVisCache'})

	def createCaches(self):
		network = mapi.Network(self.waiter)
		allNodes = network.getAllNodesAndReturnList(False)

		hasDynamics = False
		dynamicsNode = None
		for node in allNodes:
			if cmds.nodeType(node) == "MASH_BulletSolver":
				hasDynamics = True
			elif cmds.nodeType(node) == "MASH_Dynamics":
				dynamicsNode = node

		# shell dynamics check
		# as we only need the inputPoints plug, we can treat the shellDeformer as the instancer
		if not network.instancer:
			conns = cmds.listConnections(self.waiter + '.outputPoints', d=True, s=False, shapes=True)
			if conns:
				solver = conns[0]
				conns = cmds.listConnections(solver + '.outputPoints', d=True, s=False, shapes=True)
				if conns:
					shellDeformer = conns[0]
					network.instancer = shellDeformer

		if hasDynamics:
			instancerInputs = cmds.listConnections(network.instancer+'.inputPoints', plugs=True, destination=False) or []
			if len(instancerInputs):
				self.cacheWaiter = cmds.createNode('MASH_Waiter')
				self.tmpInstancer = cmds.createNode('instancer')
				cmds.connectAttr(instancerInputs[0], self.cacheWaiter+'.inputPoints', force=True)
				cmds.connectAttr(self.cacheWaiter+'.outputPoints', self.tmpInstancer+'.inputPoints', force=True)

		# Cache channels one attribute at a time
		caches = []
		for channel in self.options:
			attrToCache = channel['attrToCache']
			cacheAttr   = channel['cacheAttr']
			caches.append(self.cacheChannel(attrToCache, cacheAttr))

		# Now that the cache nodes have been created, hook them up to the right plugs
		for cacheFile, plug in caches:
			source = cmds.connectionInfo(plug, sfd=True)
			if source:
				cmds.disconnectAttr(source, plug)
			cmds.cacheFile(attachFile=True, f=cacheFile, ia=plug)

		# Lastly, enable the different caches
		for channel in self.options:
			attr = "{}.{}".format(self.waiter, channel['enableFlag'])
			cmds.setAttr(attr, 1)

		msg = fx.res('kCachingComplete')
		if self.cacheWaiter:
			cmds.connectAttr(instancerInputs[0], network.instancer+'.inputPoints', force=True)
			cmds.disconnectAttr(instancerInputs[0], self.cacheWaiter+'.inputPoints')
			cmds.delete(self.cacheWaiter)
			cmds.delete(self.tmpInstancer)
			cmds.setAttr(dynamicsNode+".enable", 0)
			msg = fx.res('kDynamicsDisabled')
		ivm.MashInViewMessage(msg,'Info')
		mel.eval('updateAE("{}");'.format(self.waiter))

	def cacheChannel(self, attrToCache, cacheAttr):
		"""
		This function creates a cache file for a single attribute for values in the range (startFrame, endFrame).
		The function returns a tuple consisting of the cacheFile node that's create as well as the plug it will need to be created to.
		The process of creating the cache file and connecting it to an attribute is divided into 2 stages since we want to avoid
		graph changes during parallel evaluation.
		"""
		node = self.cacheWaiter if self.cacheWaiter else self.waiter
		outAttr  = "{}.{}".format(node, attrToCache)
		filename = "{}_{}".format(self.waiter, attrToCache)
		cacheFiles = cmds.cacheFile(fm="OneFile", f=filename, r=True, outAttr=outAttr, st=self.startFrame, et=self.endFrame)
		plug = "{}.{}".format(self.waiter,cacheAttr)
		return cacheFiles[0], plug


# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
