import maya.app.flux.core as fx

moduleIdentifier = 'MASH.resources'
fx.loadStringResources(moduleIdentifier)
str_res = lambda name: fx.getStringResource(moduleIdentifier, name)# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
