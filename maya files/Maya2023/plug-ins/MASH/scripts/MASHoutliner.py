'''
Forwarder to new API
'''

import MASH.editor

def mashOutlinerWindowClosed(obj=None):
    MASH.editor.mashEditorWindowClosed(obj)

def mashOutlinerWindowDestroyed(obj=None):
    MASH.editor.mashEditorWindowDestroyed(obj)

def showMASHOutliner(restore=False):
    MASH.editor.show(restore)

def updateMASHOutliner():
    MASH.editor.updateMASHEditor()# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
