from __future__ import division
from builtins import object
import re
import maya.cmds as cmds
import maya.mel as mel
import inspect, random, math
import json
import os.path
import ast
import MASH.undo as undo

'''
To get all selected channels in the channelbox, use:
import DashCommands
selectedChannels = DashCommands.getAllSelectedChannels()
'''

dashActivatingWidget = 'mainChannelBox'

class DashCommand(object):

    OPERATORS = ["+", "-", "*", "/"]

    def __init__(self, commandStr):
        self.commandStr = commandStr

        callableData = inspect.getmembers(random, callable)
        self.callableRandomCmds = [item[0] for item in callableData]
        callableData = inspect.getmembers(math, callable)
        self.callableMathCmds = [item[0] for item in callableData]

        # Custom commands are stored in a JSON file. Dash comes with some examples stored here.
        self.JSON = None
        mashPath = mel.eval('getenv("MASH_LOCATION")')
        jsonPath = mashPath+'scripts/Dash.json'
        jsonFound = os.path.isfile(jsonPath)
        if jsonFound:
            with open(jsonPath) as dataFile:
                self.JSON = json.load(dataFile)

        # delete some of the random commands
        self.callableRandomCmds = [ x for x in self.callableRandomCmds if "_" not in x ]

        self.command = None
        self.args = []

    def getCommandParts(self):
        error = False
        tolkens = re.compile("[(),=]").split(self.commandStr)
        if tolkens:
            self.command = tolkens[0]
            if len(tolkens) > 1:
                self.args = tolkens[1:]

            error = self.detectCommand()
        return error

    #
    #   First we check if the user entered an Operator
    #   Next we check if the user entered a Dash command
    #   Finally we check if the user entered a Python random command
    #
    def detectCommand(self):
        command = None
        execute = None
        dashCmd = False
        error = False
        # print help
        if self.command == "help":
            dashHelp()
            return

        # Dash specific commands
        if any(self.command in s for s in self.OPERATORS):
            eval("dashOperator('"+self.command+"', '"+str(self.args[0])+"')")
            dashCmd = True
        elif self.JSON:
            for dictionary in self.JSON :
                for key, value in list(dictionary.items()):
                    if value == self.command:
                        commandToEvaluate = dictionary['MayaEval']
                        command = self.commandStr.replace(value, commandToEvaluate)
                        execute = dictionary['MayaExec']
                        dashCmd = True

        # If no Dash command was found, check against the allowed Python commands
        if not dashCmd:
            if any(self.command in s for s in self.callableRandomCmds):
                command = 'random.'+self.commandStr
            else:
                error = True
                cmds.error ("Command not found. Type 'help' for Help")

        if command:
            #user has supplied no arguements so add () to complete the call
            if len(self.args) == 0:
                command += "()"
            self.applyResult(command, execute, dashCmd)

        return error

    @undo.chunk('Dash')
    def applyResult(self, command, execute, dashCmd):
        selectedObjs = cmds.ls(selection=True)
        selectedChannels = getAllSelectedChannels()

        if (dashCmd):
            # if we've any modules to import, do so here
            if execute:
                exec(execute)
            result = eval(command)
            if result:
                cmds.setAttr(obj+"."+chan, result)
        else:
            for obj in selectedObjs:
                for chan in selectedChannels:
                    result = eval(command)
                    if result:
                        cmds.setAttr(obj+"."+chan, result)

def dashRandom(*args):
    selectedObjs = cmds.ls(selection=True)
    selectedChannels = getAllSelectedChannels()

    numArgs = len(args)
    result = 0
    for obj in selectedObjs:
        for chan in selectedChannels:
            if numArgs == 1:
                result =  random.uniform(0,args[0])
            elif numArgs == 2:
                result =  random.uniform(args[0],args[1])
            else:
                result =  random.random()

            cmds.setAttr(obj+"."+chan, result)

@undo.chunk('Dash Ease')
def dashEase(*args):
    numArgs = len(args)

    selectedObjs = cmds.ls(selection=True)
    selectedChannels = getAllSelectedChannels()

    for obj in selectedObjs:
        for chan in selectedChannels:
            animCrvs = cmds.keyframe (obj, attribute=chan, q=True)

            if not animCrvs:
                cmds.error("No keyframes in channel. "+chan)
                return None

            for timeToCheck in animCrvs:
                # get the long name for the attribute (required for the keyTangent command)
                longName = cmds.listAttr(obj+"."+chan)
                tangentObject = (obj+"_"+longName[0])
                cmds.selectKey(clear=True)
                cmds.selectKey(tangentObject, k=True, t=(timeToCheck,timeToCheck))

                # prepare the tangents
                cmds.keyTangent(edit=True, weightedTangents=True)
                cmds.keyTangent(weightLock=False)
                cmds.keyTangent(lock=False)  # fixes tangent lock if present.
                cmds.keyTangent(itt='flat',ott='flat')

                # get the total length of the tangents
                outWeight = cmds.keyTangent(tangentObject, t=(timeToCheck,timeToCheck),q=True ,outWeight=True)
                inWeight = cmds.keyTangent(tangentObject, t=(timeToCheck,timeToCheck),q=True ,inWeight=True)

                multiplier = 0.5
                if numArgs:
                    multiplier = float(args[0])

                if multiplier > 1.0:
                    multiplier = 1.0
                elif multiplier < -1.0:
                    multiplier = -1.0

                # new weights based on the ease value
                # > 0 means faster acceleration and slower deceleration
                # < 0 is the opposite
                if multiplier >= 0:
                    newOutWeight = outWeight[0]*(1.0-(multiplier*0.5))
                    newInWeight = inWeight[0]+(inWeight[0]*(multiplier*2))
                    cmds.keyTangent(tangentObject, e=True,a=True, t=(timeToCheck,timeToCheck), outAngle=0, outWeight=newOutWeight)
                    cmds.keyTangent(tangentObject, e=True,a=True, t=(timeToCheck,timeToCheck), inAngle=0, inWeight=newInWeight)
                else:
                    newInWeight = outWeight[0]*(1.0-(abs(multiplier)*0.5))
                    newOutWeight = inWeight[0]+(inWeight[0]*(abs(multiplier)*2))

                    cmds.keyTangent(tangentObject, e=True,a=True, t=(timeToCheck,timeToCheck), outAngle=0, outWeight=newOutWeight)
                    cmds.keyTangent(tangentObject, e=True,a=True, t=(timeToCheck,timeToCheck), inAngle=0, inWeight=newInWeight)


    return None

def dashHelp(*args):
    print("Operators: + - * /")
    print("rand [r]: 0 to 2 arguements")
    print("ease [e]: 1 arguement")
    print("timeStep [ts]: 1 arguement")
    print("linear [l]: 1 arguement")
    print("Anything from the Python Random module")

@undo.chunk('Dash Linear')
def dashLinear(*args):
    selectedObjs = cmds.ls(selection=True)
    selectedChannels = getAllSelectedChannels()
    getAllSelectedChannels()
    numArgs = len(args)
    numSelectedObjs = len(selectedObjs)
    idx = 0
    for obj in selectedObjs:
        for chan in selectedChannels:
            if (numArgs == 1):
                step = args[0]/(numSelectedObjs-1)
                result = step*idx
                cmds.setAttr(obj+"."+chan, result)
            if (numArgs == 2):
                step = (args[1]-args[0])/(numSelectedObjs-1)
                result = step*idx+args[0]
                cmds.setAttr(obj+"."+chan, result)
        idx += 1
    return None

@undo.chunk('Dash Time Step')
def dashTimeStep(*args):
    numArgs = len(args)
    if numArgs == 0:
        return None
    selectedObjs = cmds.ls(selection=True)
    selectedChannels = getAllSelectedChannels()
    idx = 0
    for obj in selectedObjs:
        for chan in selectedChannels:
            animCrvs = cmds.keyframe (obj, attribute=chan, q=True)

            if not animCrvs:
                cmds.error("No keyframes in channel. "+chan)
                return None

            reversedAnimCrv = animCrvs[::-1]
            if args[0] < 0:
                reversedAnimCrv = animCrvs
            for timeToCheck in reversedAnimCrv:
                offset = 0
                offset = args[0]*idx
                cmds.keyframe(obj, e=True, t=(timeToCheck,timeToCheck), relative=True, timeChange=offset)
        idx += 1
    return None

@undo.chunk('Dash Operator')
# Operators require some hackery as we're not operating on variables.
def dashOperator(operator, number):
    selectedObjs = cmds.ls(selection=True)
    selectedChannels = cmds.channelBox('mainChannelBox', q=True, sma=True)
    for obj in selectedObjs:
        for chan in selectedChannels:
            currentValue = cmds.getAttr(obj+"."+chan)
            strToEval = str(currentValue)+operator+number
            result = eval(strToEval)
            cmds.setAttr(obj+"."+chan, result)
    return None

def getAllSelectedChannels():
    allAttrs = []

    if dashActivatingWidget == 'mainChannelBox':
        #channel box
        selectedMainAttributes = cmds.channelBox('mainChannelBox', q=True, sma=True)
        selectedShapeAttributes = cmds.channelBox('mainChannelBox', q=True, ssa=True)
        selectedHistoryAttributes = cmds.channelBox('mainChannelBox', q=True, sha=True)
        selectedOutputAttributes = cmds.channelBox('mainChannelBox', q=True, soa=True)

        if selectedMainAttributes:
            allAttrs += selectedMainAttributes
        if selectedShapeAttributes:
            allAttrs += selectedShapeAttributes
        if selectedHistoryAttributes:
            allAttrs += selectedHistoryAttributes
        if selectedOutputAttributes:
            allAttrs += selectedOutputAttributes
    elif dashActivatingWidget == 'SSEd':
        #attribute spreadsheet editor
        cmds.spreadSheetEditor('SSEd',  e=True, niceNames=False)
        allAttrs = cmds.spreadSheetEditor('SSEd',  q=True, selectedAttr=True)

    return allAttrs
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
