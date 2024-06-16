'''
#Usage (in Maya):
from maya import cmds
cmds.file(new=True, force=True)
cmds.unloadPlugin('_SHADING_NODE_NAME_Override.py')
cmds.loadPlugin('_SHADING_NODE_NAME_Override.py')
'''

from string import *
import maya.api.OpenMaya as om
import maya.api.OpenMayaRender as omr

def maya_useNewAPI():
	"""
	The presence of this function tells Maya that the plugin produces, and
	expects to be passed, objects created using the Maya Python API 2.0.
	"""
	pass

################################################################################
##
## _SHADING_NODE_NAME_ Node Override
##
################################################################################
class _SHADING_NODE_NAME_Override(omr.MPx_SHADING_NODE_OVERRIDE_TYPE_Override):
	@classmethod
	def creator(cls, obj):
		return _SHADING_NODE_NAME_Override(obj)

	def __init__(self, obj):
		super(_SHADING_NODE_NAME_Override, self).__init__(obj)

	def supportedDrawAPIs(self):
		return omr.MRenderer.kOpenGLCoreProfile | omr.MRenderer.kOpenGL | omr.MRenderer.kDirectX11

	def fragmentName(self):
		return "_SHADING_NODE_NAME_"

################################################################################
##
## _SHADING_NODE_NAME_
##
##
################################################################################
class _SHADING_NODE_NAME_(om.MPxNode):

        id = om.MTypeId(_SHADING_NODE_PLUGIN_ID_)
        
	##########################################################
	##
	## Attributes
	##
	##########################################################
_SHADING_NODE_ATTRIB_DECLARATIONS_

	@staticmethod
	def creator():
		return _SHADING_NODE_NAME_()
	    
	@staticmethod
	def initialize():
		inAttrs = []
		outAttrs = []
		nAttr = om.MFnNumericAttribute()

		# attributes

_SHADING_NODE_ATTRIBS_

		# Connect the attrs
		# Note that this is necessary to have outColor show up as an output by default
		for inAttr in inAttrs:
			for outAttr in outAttrs:
				_SHADING_NODE_NAME_.attributeAffects(inAttr, outAttr)

	def __init__(self):
		om.MPxNode.__init__(self)
		
	def postConstructor(self):
		# Implementation will go here 
		pass

_SHADING_NODE_COMPUTE_METHOD_

	def compute(self, plug, block):
_SHADING_NODE_COMPUTE_IMPLEMENTATION_

##
## Plugin setup
#######################################################
sRegistrantId = "_SHADING_NODE_NAME_Plugin"

def initializePlugin(mobject):
	try:
		plugin = om.MFnPlugin(mobject, 'Autodesk', '2016', 'Any')
		userClassify = "_SHADING_NODE_CLASS_TYPE_:drawdb/shader/_SHADING_NODE_CLASS_TYPE_/_SHADING_NODE_NAME_"
		plugin.registerNode("_SHADING_NODE_NAME_", _SHADING_NODE_NAME_.id, _SHADING_NODE_NAME_.creator, _SHADING_NODE_NAME_.initialize, om.MPxNode.kDependNode, userClassify)
	except:
		sys.stderr.write("Failed to register node: _SHADING_NODE_NAME_\n")
		raise


	fragmentMgr = omr.MRenderer.getFragmentManager()
	if fragmentMgr != None:
		if not fragmentMgr.hasFragment("_SHADING_NODE_NAME_"):
			fragmentMgr.add_SHADING_NODE_FRAGMENT_TYPE_FromFile("_SHADING_NODE_NAME_.xml"_SHADING_NODE_ADD_FRAGMENT_ARGS_)

	try:
		global sRegistrantId
		omr.MDrawRegistry.register_SHADING_NODE_OVERRIDE_TYPE_OverrideCreator("drawdb/shader/_SHADING_NODE_CLASS_TYPE_/_SHADING_NODE_NAME_", sRegistrantId, _SHADING_NODE_NAME_Override.creator)
	except:
		sys.stderr.write("Failed to register shading override for _SHADING_NODE_NAME_\n")
		raise

def uninitializePlugin(mobject):
	plugin = om.MFnPlugin(mobject)
	try:
		plugin.deregisterNode(_SHADING_NODE_NAME_.id)
	except:
		sys.stderr.write("Failed to deregister node: _SHADING_NODE_NAME_\n")
		raise

	try:
		global sRegistrantId
		omr.MDrawRegistry.deregister_SHADING_NODE_OVERRIDE_TYPE_OverrideCreator("drawdb/shader/_SHADING_NODE_CLASS_TYPE_/_SHADING_NODE_NAME_", sRegistrantId)
	except:
		sys.stderr.write("Failed to deregister shading override for _SHADING_NODE_NAME_\n")
		raise




