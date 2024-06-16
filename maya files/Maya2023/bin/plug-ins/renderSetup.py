import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya
import maya.mel as mel


# Using the Maya Python API 2.0.
def maya_useNewAPI():
    pass


renderSetupVersion = '1.0'


# List of all available initializers
import maya.app.renderSetup.model.initialize as modelInitializer
import maya.app.renderSetup.lightEditor.model.initialize as lightEditorModelInitializer
modules = [ modelInitializer, lightEditorModelInitializer ]

# UI components  -  batch mode (i.e. Maya IO) does not need them
if not cmds.about(batch=True):
    # Add all available UI related initializers
    import maya.app.renderSetup.views.initialize as viewsInitializer
    import maya.app.renderSetup.lightEditor.views.initialize as lightEditorViewsInitializer
    modules += [ viewsInitializer, lightEditorViewsInitializer ]

def _loadPreferredPresets(renderer):
    cmds.evalDeferred("import maya.mel as mel; import maya.cmds as cmds;\nif not cmds.about(batch=True) and \"" + renderer + 
        "\" == cmds.preferredRenderer(query=True) and cmds.renderer(\"" + renderer + 
        "\", exists=True): mel.eval(\"loadPreferredRenderGlobalsPreset(\\\"" + renderer + 
        "\\\")\")")

def initializePlugin(mobject):
    """ Initialize all the needed nodes """
    mplugin = OpenMaya.MFnPlugin(mobject, "Autodesk", renderSetupVersion, "Any")

    # Does an early out if batch.
    mel.eval("loadRenderLayerFilters()")
    
    for module in modules:
        module.initialize(mplugin)
        
    if not cmds.about(batch=True):
        cmds.callbacks(addCallback=_loadPreferredPresets, hook="rendererRegistered", owner="renderSetup")
        cmds.callbacks(addCallback=_loadPreferredPresets, hook="currentRendererChanged", owner="renderSetup")

def uninitializePlugin(mobject):
    """ Uninitialize all the nodes """
    mplugin = OpenMaya.MFnPlugin(mobject, "Autodesk", renderSetupVersion, "Any")

    # Does an early out if batch.
    mel.eval("unloadRenderLayerFilters()")
    
    for module in reversed(modules):
        module.uninitialize(mplugin)

    if not cmds.about(batch=True):
        cmds.callbacks(removeCallback=_loadPreferredPresets, hook="rendererRegistered", owner="renderSetup")
        cmds.callbacks(removeCallback=_loadPreferredPresets, hook="currentRendererChanged", owner="renderSetup")
