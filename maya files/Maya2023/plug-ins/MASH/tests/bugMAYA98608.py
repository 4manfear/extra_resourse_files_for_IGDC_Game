import PythonTests.harness as harness
import maya.cmds as cmds
import MASH.api as mapi

class bugMAYA98608(harness.TestCase):
    """Ensure that newly created MASH networks have the name they were given"""

    def testCreateNamedNetwork( self ):
        netName = "testMASHNetwork"
        # create a new MASH network
        cmds.polyCube()
        mashNetwork = mapi.Network()
        mashNetwork.createNetwork(name=netName)

        self.assertEqual(mashNetwork.networkName, netName)
        cmds.delete(mashNetwork.networkName)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
