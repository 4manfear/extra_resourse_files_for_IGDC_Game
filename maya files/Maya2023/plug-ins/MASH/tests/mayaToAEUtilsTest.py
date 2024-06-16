from builtins import range
import PythonTests.harness as harness

import maya.cmds as cmds
import maya.api.OpenMaya as om

import MayaToAE.utils as utils

class mayaToAEUtilsTest(harness.TestCase):

    def testGetTranslation(self):
        cube = cmds.polyCube()
        name = cube[0]

        context = om.MDGContext()
        uuid = cmds.ls(name, uuid=True)

        initialPos = [0, 0, 0]
        finalPos = [1, 1, 1]
        self.assertNotEqual(initialPos, finalPos)

        cmds.move(initialPos[0], initialPos[1], initialPos[2], name)
        pos = utils.getTranslateInFrame(name, context, uuid)
        self.assertEqual(pos, initialPos)

        cmds.move(finalPos[0], finalPos[1], finalPos[2], name)
        pos = utils.getTranslateInFrame(name, context, uuid)
        self.assertEqual(pos, finalPos)

    def testGetRotation(self):
        cube = cmds.polyCube()
        name = cube[0]

        context = om.MDGContext()
        uuid = cmds.ls(name, uuid=True)

        initialRot = [0, 0, 0]
        finalRot = [30, 30, 30]
        self.assertNotEqual(initialRot, finalRot)

        cmds.rotate(initialRot[0], initialRot[1], initialRot[2], name)
        rot = utils.getRotateInFrame(name, context, uuid)
        self.assertEqual(rot, initialRot)

        cmds.rotate(finalRot[0], finalRot[1], finalRot[2], name)
        rot = utils.getRotateInFrame(name, context, uuid)
        for i in range(0,3):
            self.assertAlmostEqual(rot[i], finalRot[i])

    def testGetScale(self):
        cube = cmds.polyCube()
        name = cube[0]

        context = om.MDGContext()
        uuid = cmds.ls(name, uuid=True)

        initialScale = [1, 1, 1]
        finalScale = [2, 2, 2]
        self.assertNotEqual(initialScale, finalScale)

        cmds.scale(initialScale[0], initialScale[1], initialScale[2], name)
        scale = utils.getScaleInFrame(name, context, uuid)
        self.assertEqual(scale, initialScale)

        cmds.scale(finalScale[0], finalScale[1], finalScale[2], name)
        scale = utils.getScaleInFrame(name, context, uuid)
        self.assertEqual(scale, finalScale)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
