import maya.cmds as cmds
import maya.api.OpenMaya as OpenMaya

# Using the Maya Python API 2.0.
def maya_useNewAPI():
    pass

ufeSupportVersion = '0.1'

import maya.internal.ufeSupport.ufeCmdWrapper as ufeCmd
import maya.internal.ufeSupport.ufeSelectCmd as ufeSelectCmd

commands = [ufeCmd.UfeCmd,
            ufeSelectCmd.SelectAppendCmd, ufeSelectCmd.SelectRemoveCmd,
            ufeSelectCmd.SelectClearCmd, ufeSelectCmd.SelectReplaceWithCmd]

def initializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject, "Autodesk", ufeSupportVersion, "Any")

    for cmd in commands:
        try:
            mplugin.registerCommand(cmd.kCmdName, cmd.creator)
        except:
            OpenMaya.MGlobal.displayError('Register failed for %s' % cmd.kCmdName)
        
def uninitializePlugin(mobject):
    mplugin = OpenMaya.MFnPlugin(mobject, "Autodesk", ufeSupportVersion, "Any")

    for cmd in commands:
        try:
            mplugin.deregisterCommand(cmd.kCmdName)
        except:
            OpenMaya.MGlobal.displayError('Unregister failed for %s' % cmd.kCmdName)
