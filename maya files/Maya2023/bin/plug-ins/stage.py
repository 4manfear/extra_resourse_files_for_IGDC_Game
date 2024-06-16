'''
Command = stage(flags)

EXAMPLES:

import cmds
cmds.loadPlugin('stage')

# Activate an existing stage name stage1
cmds.stage('stage1', a='locator1', edit=True)

#create a new stage
cmds.stage('myNewStage')

# Create a time slider bookmark and associate it with a new stage.
import maya.plugin.timeSliderBookmark.timeSliderBookmark as tsb
bm = tsb.createBookmark(name="foo", start="1",stop="10" )
s1 = cmds.stage("aStage", tsb=bm)[0]
#create a second stage after the s1 stage
cmds.stage("mySecondStage", tsb=bm2, insertAfter=s1)

# go the the stage previous to mySecondStage
cmds.stage("mySecondStage", edit=True, p=True)

'''

import maya.api.OpenMaya as om
import maya.cmds as cmds
import sys
import maya.plugin.timeSliderBookmark.timeSliderBookmark as tsb
from PySide2.QtCore import QTimer
from PySide2.QtCore import SIGNAL

kPluginNodeId = om.MTypeId(0x00080070)
kPluginNodeName = "stage"
#-------------------------------------------------------------------------------
def maya_useNewAPI():
    """
    The presence of this function tells Maya that the plugin produces, and
    expects to be passed, objects created using Maya Python API 2.0.
    """
    pass


def executePythonScript(script, name, stage):
    if script:
        try:
            code = compile(script, "%s"%name, "exec")
            exec(code, globals(), {"stage":stage, "cmds":cmds})
        except SyntaxError as s:
            print ("Syntax Error in script %s"%name)
            print(s)
        except Exception as e:
            print ("Exception in script %s"%name)
            print (e)


gActiveNode = []

class stageNode(om.MPxNode):


    aTimeSliderBookmark = om.MObject() #message connection to a time Slider Bookmark
    aOnActivateScript = om.MObject()#script to run on activate script
    aOnDeactivateScript = om.MObject()#script to run on de activate script
    aAutoPlay  = om.MObject() # boolean to automatically play on activation


    aNextState = om.MObject() #message connection to the next State
    aPreviousState = om.MObject() #message connection to the next State
    aAtEndAnimation = om.MObject() #go to next state when at the end time
    aTimeDelay = om.MObject() # activate, wait for timeDelay seconds and go to next State, 0 means not used
    aCondition = om.MObject() # When true, go to next state, start at false otherwise it will got to next automatically


    def __init__(self):
        super(stageNode, self).__init__()
        self._timer = None
        self._active = False
        self._endOfAnimCB = None
        self._conditionCB = None
        self._checkConditionTimer = None
        self._dirtyCB = None

    @staticmethod
    def nodeCreator():
        return stageNode()



    @staticmethod
    def nodeInitializer():
        tAttr = om.MFnTypedAttribute()
        nAttr = om.MFnNumericAttribute()
        mAttr = om.MFnMessageAttribute()
        stringFn = om.MFnStringData()


        stageNode.aTimeSliderBookmark = mAttr.create('timeSliderBookmark', "tsb")
        stageNode.addAttribute(stageNode.aTimeSliderBookmark)

        stageNode.aNextState = mAttr.create('nextState', "ns")
        stageNode.addAttribute(stageNode.aNextState)

        stageNode.aPreviousState = mAttr.create('previousState', "ps")
        stageNode.addAttribute(stageNode.aPreviousState)

        stageNode.aAutoPlay = nAttr.create( "autoPlay", "ap", om.MFnNumericData.kBoolean )
        nAttr.storable = True
        stageNode.addAttribute(stageNode.aAutoPlay)


        stageNode.aAtEndAnimation = nAttr.create( "endOfAnimation", "ea", om.MFnNumericData.kBoolean )
        nAttr.storable = True
        stageNode.addAttribute(stageNode.aAtEndAnimation)


        stageNode.aCondition = nAttr.create( "condition", "cd", om.MFnNumericData.kBoolean )
        nAttr.storable = True
        stageNode.addAttribute(stageNode.aCondition)


        stageNode.aTimeDelay = nAttr.create( "timeDelay", "td", om.MFnNumericData.kDouble )
        nAttr.storable = True
        stageNode.addAttribute(stageNode.aTimeDelay)


        stringAttr = stringFn.create("")
        stageNode.aOnActivateScript = tAttr.create('onActivateScript', 'oas', om.MFnData.kString, stringAttr)
        tAttr.storable = True
        stageNode.addAttribute(stageNode.aOnActivateScript)

        stageNode.aOnDeactivateScript = tAttr.create('onDeactivateScript', 'ods', om.MFnData.kString, stringAttr)
        tAttr.storable = True
        stageNode.addAttribute(stageNode.aOnDeactivateScript)



    def clear(self):
        if self._timer:
            self._timer.stop()
            self._timer = None

        if self._endOfAnimCB:
            om.MMessage.removeCallback(self._endOfAnimCB)
            self._endOfAnimCB = None

        if self._conditionCB:
            om.MMessage.removeCallback(self._conditionCB)
            self._conditionCB = None

        if self._dirtyCB:
            om.MMessage.removeCallback(self._dirtyCB)
            self._dirtyCB = None

        if self._checkConditionTimer:
            self._checkConditionTimer.stop()
            self._checkConditionTimer = None


    def aboutToDelete(self):
        self.clear()


    def _timeout(self):
        self.gotToNextState()

    def _onTimeChange(self, time):
        ct = cmds.currentTime(q=True)
        max = cmds.playbackOptions(q=True, max=True)
        if ct >= max:
            self.gotToNextState()

    def _checkConditionTimeout(self):
        self._checkConditionTimer = None
        dn = om.MFnDependencyNode(self.thisMObject())
        if dn.findPlug(stageNode.aCondition, False).asBool():
            self.gotToNextState()


    @staticmethod
    def _onDirty(node, plug, clientData):
        if plug.attribute() == stageNode.aCondition:
            if not clientData._checkConditionTimer: #setup a check at idle to see if condition is true
                clientData._checkConditionTimer =  QTimer()
                clientData._checkConditionTimer.setSingleShot(True)
                clientData._checkConditionTimer.connect(clientData._checkConditionTimer, SIGNAL("timeout()"), clientData._checkConditionTimeout)
                clientData._checkConditionTimer.start(100)#100 ms

    @staticmethod
    def _onAttrChanged(msg,plug, otherPlug, clientData):
        if msg & om.MNodeMessage.kAttributeSet and plug.attribute() == stageNode.aCondition:
             dn = om.MFnDependencyNode(clientData.thisMObject())
             if dn.findPlug(stageNode.aCondition, False).asBool():
                clientData.gotToNextState()


    def activate(self):
        if self._active:
            return
        self._active = True

        dn = om.MFnDependencyNode(self.thisMObject())

        #get time slider bookmark
        bm = dn.findPlug(stageNode.aTimeSliderBookmark, False)
        bm = bm.source()
        if  bm.node() and not bm.node().isNull():
            bm = om.MFnDependencyNode(bm.node()).name()
            if bm != "nullptr":
                tsb.frameBookmark(bm)
                currentMin = cmds.playbackOptions(q=True, min=True)
                cmds.currentTime(currentMin)


        #execute on Activate Script
        script = dn.findPlug(stageNode.aOnActivateScript, False).asString()
        executePythonScript(script, "%s.onActivateScript"%dn.name(), self)

        if not self._active: #it gotToNestState has been called in the activate script
            return

        #auto play
        autoPlay = dn.findPlug(stageNode.aAutoPlay, False).asBool()
        if autoPlay:
             cmds.play()

        #watch end condition
        #if it already the end go to next State
        if dn.findPlug(stageNode.aCondition, False).asBool():
            self.gotToNextState()
            return #done

        #time delay
        td = dn.findPlug(stageNode.aTimeDelay, False).asDouble()
        if td > 0:
            self._timer = QTimer()
            self._timer.setSingleShot(True)
            self._timer.connect(self._timer, SIGNAL("timeout()"), self._timeout)
            self._timer.start(td*1000)

        #end of Animation
        endOfAnim = dn.findPlug(stageNode.aAtEndAnimation, False).asBool()
        if endOfAnim:
            self._endOfAnimCB = om.MEventMessage.addEventCallback("timeChanged", self._onTimeChange)


        self._conditionCB = om.MNodeMessage.addAttributeChangedCallback(self.thisMObject(), self._onAttrChanged, self)
        self._dirtyCB =  om.MNodeMessage.addNodeDirtyPlugCallback(self.thisMObject(), self._onDirty, self)

    def deactivate(self):
        if not self._active:
            return

        self.clear()

        dn = om.MFnDependencyNode(self.thisMObject())
        #execute on Activate Script
        script = dn.findPlug(stageNode.aOnDeactivateScript, False).asString()
        executePythonScript(script, "%s.onDeactivateScript"%dn.name(), self)

        self._active = False

    def gotToNextState(self):
        self.deactivate()
        dn = om.MFnDependencyNode(self.thisMObject())
        nextState = dn.findPlug(stageNode.aNextState, False).destinations()
        if nextState is not None and len(nextState) > 0 :
            dn = om.MFnDependencyNode(nextState[0].node())
            if dn and dn.userNode():
                dn.userNode().activate()
                return dn.absoluteName()
        return ""

    def gotToPreviousState(self):
        self.deactivate()
        dn = om.MFnDependencyNode(self.thisMObject())
        previousState = dn.findPlug(stageNode.aPreviousState, False).source()
        if  previousState.node() and not previousState.node().isNull():
            previousStateName = om.MFnDependencyNode(previousState.node()).name()
            if previousStateName != "nullptr":
                dn = om.MFnDependencyNode(previousState.node())
                if dn and dn.userNode():
                    dn.userNode().activate()
                    return dn.absoluteName()
        return ""


def deactivateAllActiveState():

    stages = cmds.ls(type="stage")
    for stageNode in stages:
        deactivateState(stageNode)

def deactivateState(state):
    slist = om.MSelectionList()
    slist.add(state)
    stageNode = om.MFnDependencyNode(slist.getDependNode(0)).userNode()
    stageNode.deactivate()

def goToNext(state):
    slist = om.MSelectionList()
    slist.add(state)
    stageNode = om.MFnDependencyNode(slist.getDependNode(0)).userNode()
    return stageNode.gotToNextState()

def goToPrevious(state):
    slist = om.MSelectionList()
    slist.add(state)
    stageNode = om.MFnDependencyNode(slist.getDependNode(0)).userNode()
    return stageNode.gotToPreviousState()

def activateState(state):
    slist = om.MSelectionList()
    slist.add(state)
    stageNode = om.MFnDependencyNode(slist.getDependNode(0)).userNode()
    stageNode.activate()



def linkTimeSliderBookmark(state, tsb):
    cmds.connectAttr("%s.message"%tsb, "%s.tsb"%state)

def linkState(previous, current):
    element = cmds.listConnections("%s.nextState"%previous)
    if element is not None:
        linkState(current, element)
    cmds.connectAttr("%s.nextState"%previous, "%s.previousState"%current, force=True)

kActivateFlag = ('-a', '-activate')
kDeactivateFlag = ('-d', '-deactivate')
kDeactivateAllFlag = ('-da', '-deactivateAll')
kNextFlag = ('-n', '-next')
kPreviousFlag = ('-p', '-previous')
kEditFlag = ('-e', '-edit')
kinsertAfterFlag = ('-ia', '-insertAfter')
kSetTimeSliderBookmarkFlag = ('-tsb', '-timeSliderBookmark')



# #-------------------------------------------------------------------------------
# # The command class
# #-------------------------------------------------------------------------------
class stageCmd(om.MPxCommand):

    kPluginCmdName = 'stage'

    def __init__(self):
        om.MPxCommand.__init__(self)
        self.clear()

    def clear(self):
        self._state = []
        self._activate = False
        self._deactivate = False
        self._deactivateAll = False
        self._previousState = None
        self._tsb = None
        self._create = True
        self._name = None
        self._previous = False
        self._next = False

    # Create an instance of the command
    @staticmethod
    def cmdCreator():
        return stageCmd()

    # Make the command undoable
    def isUndoable(self):
        return True

    # Syntax creator : Builds the argument strings up for the command
    @classmethod
    def syntaxCreator(cls):
        syntax = om.MSyntax()


        syntax.addFlag(kActivateFlag[0], kActivateFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kDeactivateFlag[0], kDeactivateFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kDeactivateAllFlag[0], kDeactivateAllFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kNextFlag[0], kNextFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kPreviousFlag[0], kPreviousFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kEditFlag[0], kEditFlag[1], om.MSyntax.kNoArg)
        syntax.addFlag(kinsertAfterFlag[0], kinsertAfterFlag[1],  om.MSyntax.kString)
        syntax.addFlag(kSetTimeSliderBookmarkFlag[0], kSetTimeSliderBookmarkFlag[1],  om.MSyntax.kString)


        syntax.setObjectType(syntax.kStringObjects)
        syntax.setMinObjects(0)
        syntax.useSelectionAsDefault(True)
        syntax.enableQuery = False
        syntax.enableEdit = False

        return syntax

    def _parseFlags(self, args):
        argData = om.MArgDatabase(self.syntax(), args)

        slist = argData.getObjectStrings()

        if argData.isFlagSet(kEditFlag[0]):
            self._create = False
            if slist is not None and len(slist) == 0:
                 cmds.error('No Object to edit in cmds {}'.format(stageCmd.kPluginCmdName))
                 return False
            # Get the objects specified on the command line.
            self._state = slist[0]
        else:
            if slist is not None and len(slist) > 0:
                self._name = slist[0]

        if argData.isFlagSet(kinsertAfterFlag[0]):
            self._previousState = argData.flagArgumentString(kinsertAfterFlag[0], 0)


        if argData.isFlagSet(kSetTimeSliderBookmarkFlag[0]):
            self._tsb = argData.flagArgumentString(kSetTimeSliderBookmarkFlag[0], 0)


        if argData.isFlagSet(kActivateFlag[0]):
            self._activate = True
        elif argData.isFlagSet(kDeactivateFlag[0]):
            self._deactivate = True
        elif argData.isFlagSet(kDeactivateAllFlag[0]):
            self._create = False
            self._deactivateAll = True

        if argData.isFlagSet(kNextFlag[0]):
            self._next = True
        elif argData.isFlagSet(kPreviousFlag[0]):
            self._previous = True


        if argData.isFlagSet(kEditFlag[0]):
            self._create = False
        return True

    def doIt(self, args):
        # Check if all the flags can be parsed correctly
        if not self._parseFlags(args):
            cmds.error('Failed to parse the arguments of the {} command: See script editor for details'.format(stageCmd.kPluginCmdName))
            return

        # Check if we want to reparent to a child, because that is not allowed

        # Now go do the actual work
        self.redoIt()

    def undoIt(self):
         pass

    def redoIt(self):
        if self._create:
            if self._name:
                self._state = cmds.createNode("stage", n=self._name)
            else:
                self._state = cmds.createNode("stage")
            self.setResult(self._state)
        if self._tsb:
            linkTimeSliderBookmark(self._state, self._tsb)
        if self._previousState:
            linkState(self._previousState, self._state)
        if self._activate:
            activateState(self._state)
        elif self._deactivate:
            deactivateState(self._state)
        elif self._deactivateAll:
            deactivateAllActiveState()

        if self._next:
            self.setResult(goToNext(self._state))
        elif self._previous:
            self.setResult(goToPrevious(self._state))


#-------------------------------------------------------------------------------
# Initialize the script plug-in
#-------------------------------------------------------------------------------
def initializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', "1.0", 'Any')

    try:
        pluginFn.registerCommand( stageCmd.kPluginCmdName, stageCmd.cmdCreator, stageCmd.syntaxCreator )
        pluginFn.registerNode( kPluginNodeName, kPluginNodeId, stageNode.nodeCreator, stageNode.nodeInitializer)
    except:
        sys.stderr.write( 'Failed to register stage plugin')
        raise

#-------------------------------------------------------------------------------
# Uninitialize the script plug-in
#-------------------------------------------------------------------------------
def uninitializePlugin(pluginObject):
    pluginFn = om.MFnPlugin(pluginObject, 'Autodesk', "1.0", 'Any')

    try:
        pluginFn.deregisterCommand( stageCmd.kPluginCmdName )
        pluginFn.deregisterNode( kPluginNodeId )
    except:
        sys.stderr.write( 'Failed to unregister stage plugin \n')
        raise

