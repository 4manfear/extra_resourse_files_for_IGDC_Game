"""

uritemplate
===========

The URI templating library for humans.

See http://uritemplate.rtfd.org/ for documentation

:copyright: (c) 2013-2015 Ian Cordasco
:license: Modified BSD, see LICENSE for more details

"""

__title__ = 'uritemplate'
__author__ = 'Ian Cordasco'
__license__ = 'Modified BSD or Apache License, Version 2.0'
__copyright__ = 'Copyright 2013 Ian Cordasco'
__version__ = '3.0.0'
__version_info__ = tuple(int(i) for i in __version__.split('.') if i.isdigit())

from uritemplate.api import (
    URITemplate, expand, partial, variables  # noqa: E402
)

__all__ = ('URITemplate', 'expand', 'partial', 'variables')
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
