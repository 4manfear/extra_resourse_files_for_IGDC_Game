import maya.cmds as cmds
import openMASH
import MASH.api as mapi

import PythonTests.harness as harness

class mash_named_arrays_test(harness.TestCase):

    def __init__(self, testName):
        super(mash_named_arrays_test, self).__init__(testName)
        self.mashNetworkName = "testMASH"

    def setUp(self):
        super(mash_named_arrays_test, self).setUp()
        cmds.polyCube()

        # create a new MASH network
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(name=self.mashNetworkName)

        # add a Python node
        mashNetwork.addNode("MASH_Python")

    def testGetAllNamedArrays(self):
        data = openMASH.MASHData(self.mashNetworkName + "_Python")
        arrays = data.getNamedArrays()
        self.assertTrue(len(arrays) > 0)

    def testGetPositionArray(self):
        data = openMASH.MASHData(self.mashNetworkName + "_Python")
        array = data.getNamedArray("position", "vector")
        self.assertTrue(len(array) > 0)
        self.assertEqual(array[0], (0, 0, 0))
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
