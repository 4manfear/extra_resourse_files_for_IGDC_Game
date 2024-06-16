import PythonTests.harness as harness
import maya.cmds as cmds

class bug86630MashTest(harness.TestCase):
    """Test import MASH.api module in the batch mode"""

    def testImportMashAPI( self ):
        from MASH import api
        self.assertIsNotNone(api)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
