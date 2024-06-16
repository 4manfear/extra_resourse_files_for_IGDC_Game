#-------------------------------------------------------------------------#
#   CREATED: 16 VII 2020
#-------------------------------------------------------------------------#

import maya.cmds as cmds
import maya.mel as mel

import sweepUtils

#-------------------------------------------------------------------------#

g_mayaCreateMenuID = None
g_sweepMeshFromCurveMenuItemID = None

#-------------------------------------------------------------------------#

def add():
    # Get Maya 'Create' menu
    global g_mayaCreateMenuID
    if g_mayaCreateMenuID is None:
        g_mayaCreateMenuID = mel.eval("proc string _() { global string $gMainCreateMenu; return $gMainCreateMenu;} _();")

        # Since Maya doesn't build menus (their contents) on startup but rather
        # on demand (when user clicks specific menu) we need to invoke special
        # MEL procedure to make sure our menu item will be added when plugin is
        # loaded but user still haven't clicked on a specific menu (i.e. Create menu).
        # Note that we define a dummy function _() to return the value of $gMainCreateMenu"
        # while avoiding temporaries that polute the global namespace, possibly interfering with
        # user defined variables.
        mel.eval("ModCreateMenu " + g_mayaCreateMenuID) # MAYA_LOCATION/scripts/startup

    # Get insert after ID
    mayaCreateMenuItemList = cmds.menu(g_mayaCreateMenuID, query=True, itemArray=True)
    if len(mayaCreateMenuItemList) < 8:
        insertAfterID = ""
    else:
        insertAfterID = mayaCreateMenuItemList[7]

    # Add 'Sweep Mesh from Curve' menu item
    global g_sweepMeshFromCurveMenuItemID
    g_sweepMeshFromCurveMenuItemID = cmds.menuItem("sweepMeshFromCurve",
        label = sweepUtils.getRes("kSweepMeshFromCurve"),
        annotation = sweepUtils.getRes("kSweepMeshFromCurveAnn"),
        image = "shelf_sweepMeshFromCurve.png",
        sourceType = "mel",
        command = "performSweepMesh 0;",
        parent = g_mayaCreateMenuID,
        insertAfter = insertAfterID,
        version = 2022
    )

    cmds.menuItem(
        optionBox=True,
        annotation = sweepUtils.getRes("kSweepMeshFromCurveAnn"),
        sourceType = "mel",
        command="performSweepMesh 1;",
        insertAfter = g_sweepMeshFromCurveMenuItemID
    )

#-------------------------------------------------------------------------#

def remove():
    global g_sweepMeshFromCurveMenuItemID
    if g_sweepMeshFromCurveMenuItemID is not None:
        cmds.deleteUI(g_sweepMeshFromCurveMenuItemID, menuItem=True)
        g_sweepMeshFromCurveMenuItemID = None
