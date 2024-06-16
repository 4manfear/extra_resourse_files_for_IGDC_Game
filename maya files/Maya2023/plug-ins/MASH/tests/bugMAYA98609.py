import PythonTests.harness as harness
import maya.cmds as cmds
import MASH.api as mapi
import re

class bugMAYA98609(harness.TestCase):
    """Ensure that Python MASH network objects store the correct names"""

    # MASH tries to access the Maya window, so skip if there's no GUI
    @harness.skipUnlessGUI
    def testDefaultNameNetwork(self):
        # create a new MASH network
        cmds.polyCube()
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(geometry = "Repro")

        self.assertNotEqual(mashNetwork.networkName, "MASH#")

        # should have a name in the form "MASH[next available number]"
        match = re.match("MASH\d{1,}", mashNetwork.networkName)
        self.assertIsNotNone(match)

        # should find network nodes based on stored network name
        self.assertIsNotNone(mashNetwork.getAllNodesInNetwork())

        # cleanup
        cmds.delete(mashNetwork.networkName)

    @harness.skipUnlessGUI
    def testNetworkRename(self):
        newName = "testMASHNetwork"

        # create a new MASH network
        cmds.polyCube()
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(geometry = "Repro")

        oldName = mashNetwork.networkName
        self.assertNotEqual(newName, oldName) # otherwise test is pointless

        mashNetwork.rename(newName)

        # check that the stored node names were updated
        self.assertEqual(mashNetwork.networkName, newName)
        self.assertEqual(mashNetwork.waiter, newName)
        self.assertEqual(mashNetwork.distribute, newName + "_Distribute")
        self.assertEqual(mashNetwork.instancer, newName + "_Repro")

        # check that the nodes were renamed properly
        nodes = mashNetwork.getAllNodesInNetwork()
        self.assertIsNotNone(nodes)
        for node in nodes:
            match = re.match("^" + newName, node)
            self.assertIsNotNone(match)

        # cleanup
        cmds.delete(mashNetwork.networkName)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
