import maya.cmds as cmds

def MashInViewMessage(message, typeOfMessage):
    inViewOn = cmds.optionVar(q='inViewMessageEnable')

    if typeOfMessage == "Info":
        if inViewOn:
            cmds.inViewMessage (amg=(" <span style=\"color:#82C99A;\">MASH:</span> "+ message), fst=2000, dragKill=True, pos='topCenter', fade=True)
    elif typeOfMessage == "Warning":
        if inViewOn:
            cmds.inViewMessage (amg=("<span style=\"color:#F4FA58;\">MASH:</span> "+ message), fst=2000, dragKill=True, pos='midCenterTop', fade=True)
    elif typeOfMessage == "Error":
        if inViewOn:
            cmds.inViewMessage (amg=("<span style=\"color:#F05A5A;\">MASH:</span> "+ message), fst=2000, dragKill=True, pos='midCente', fade=True)

    print(message)



# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
