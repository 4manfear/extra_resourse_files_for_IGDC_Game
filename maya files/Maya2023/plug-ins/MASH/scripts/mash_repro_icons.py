# Copyright (C) Mainframe
# Created by Daniele Federico on 3/12/2015.

from builtins import object
from maya.app.flux.imports import qt
from maya.utils import os_environ

class MASH_REPRO_ICONS(object):

    _vertical_drag_icon = None
    _horizontal_drag_icon = None
    _mesh_icon = None
    _proxy_on_icon = None
    _proxy_off_icon = None
    _lod_on_icon = None
    _lod_off_icon = None

    @staticmethod
    def get_icon_path(icon_name):
        #we do not use os.path.sep to join the paths as Windows "\" confuses qt stylesheets
        mash_dir = os_environ['MASH_LOCATION']
        return "/".join([mash_dir, "icons", icon_name + ".png"])

    @classmethod
    def vertical_drag(cls):
        if cls._vertical_drag_icon is None:
            cls._vertical_drag_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproDrag"))
        return cls._vertical_drag_icon

    @classmethod
    def horizontal_drag(cls):
        if cls._horizontal_drag_icon is None:
            cls._horizontal_drag_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproDrag_hor"))
        return cls._horizontal_drag_icon

    @classmethod
    def mesh(cls):
        if cls._mesh_icon is None:
            cls._mesh_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproMesh"))
        return cls._mesh_icon

    @classmethod
    def proxy_on(cls):
        if cls._proxy_on_icon is None:
            cls._proxy_on_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproProxy"))
        return cls._proxy_on_icon

    @classmethod
    def proxy_off(cls):
        if cls._proxy_off_icon is None:
            cls._proxy_off_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproProxyGrey"))
        return cls._proxy_off_icon

    @classmethod
    def lod_on(cls):
        if cls._lod_on_icon is None:
            cls._lod_on_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproLOD"))
        return cls._lod_on_icon

    @classmethod
    def lod_off(cls):
        if cls._lod_off_icon is None:
            cls._lod_off_icon = qt.QIcon(cls.get_icon_path("ae_MASH_ReproLODGrey"))
        return cls._lod_off_icon
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
