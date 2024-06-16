import maya.OpenMaya as OpenMaya
import maya.OpenMayaMPx as OpenMayaMPx
import maya.cmds as cmds
import maya.app.type.svgSetup as svgSetup

class svgFileTranslator(OpenMayaMPx.MPxFileTranslator):
    kPluginTranslatorName = "SVG"

    def __init__(self):
        OpenMayaMPx.MPxFileTranslator.__init__(self)

    @staticmethod
    def translatorCreator():
        return OpenMayaMPx.asMPxPtr(svgFileTranslator())

    def haveWriteMethod(self):
        return False

    def haveReadMethod(self):
        return True

    def filter(self):
        return '*.svg'

    def defaultExtension(self):
        return '*.svg'

    def reader(self, fileObject, optionString, accessMode):
        # Make sure the Type plug-in is loaded
        #
        cmds.loadPlugin('Type', quiet=True)

        svgSetup.setUpSVGNetwork(filePath=fileObject.resolvedFullName())

    def identifyFile (self, file, buffer, size):
        filePath = file.resolvedFullName()
        
        import os.path
        extension = os.path.splitext(filePath)[1]

        if extension == ".svg":
            return OpenMayaMPx.MPxFileTranslator.kIsMyFileType
        else:
            return OpenMayaMPx.MPxFileTranslator.kNotMyFileType

# Initialize the plug-in
def initializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.registerFileTranslator(svgFileTranslator.kPluginTranslatorName, None, svgFileTranslator.translatorCreator
        )
    except:
        sys.stderr.write(
            "Failed to register translator: %s\n" % svgFileTranslator.kPluginTranslatorName
        )
        raise

# Uninitialize the plug-in
def uninitializePlugin(plugin):
    pluginFn = OpenMayaMPx.MFnPlugin(plugin)
    try:
        pluginFn.deregisterFileTranslator(svgFileTranslator.kPluginTranslatorName)
    except:
        sys.stderr.write(
            "Failed to unregister translator: %s\n" % svgFileTranslator.kPluginTranslatorName
        )
        raise
