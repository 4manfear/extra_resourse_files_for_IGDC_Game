from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

class ItemStyle(qt.QCommonStyle):
    """ This class defines the view item style and is only used when style sheets and the delegate are not sufficient. """

    # Constants
    DROP_INDICATOR_COLOR = qt.QColor(255, 255, 255)
    DROP_INDICATOR_WIDTH = pix(3)
    DROP_INDICATOR_LEFT_OFFSET = pix(-25)

    def __init__(self):
        super(ItemStyle, self).__init__()

    def drawComplexControl(self, control, option, painter, widget = None):
        return qt.QApplication.style().drawComplexControl(control, option, painter, widget)

    def drawControl(self, element, option, painter, widget = None):
        return qt.QApplication.style().drawControl(element, option, painter, widget)

    def drawItemPixmap(self, painter, rectangle, alignment, pixmap):
        return qt.QApplication.style().drawItemPixmap(painter, rectangle, alignment, pixmap)

    def drawItemText(self, painter, rectangle, alignment, palette, enabled, text, textRole = qt.QPalette.NoRole):
        return qt.QApplication.style().drawItemText(painter, rectangle, alignment, palette, enabled, text, textRole)

    def drawPrimitive(self, element, option, painter, widget = None):
        """ Draws the given primitive element with the provided painter using the style options specified by option. """
        # Changes the way the drop indicator is drawn
        if element == qt.QStyle.PE_IndicatorItemViewItemDrop and not option.rect.isNull():
            painter.save()
            painter.setRenderHint(qt.QPainter.Antialiasing, True)
            oldPen = painter.pen()
            painter.setPen(qt.QPen(self.DROP_INDICATOR_COLOR, self.DROP_INDICATOR_WIDTH))
            rect = option.rect
            rect.setLeft(self.DROP_INDICATOR_WIDTH)
            rect.setRight(widget.width()-self.DROP_INDICATOR_WIDTH*2)
            if option.rect.height() == 0:
                painter.drawLine(rect.topLeft(), option.rect.topRight())
            else:
                painter.drawRect(rect);
            painter.setPen(oldPen)
            painter.restore()


    def generatedIconPixmap(self, iconMode, pixmap, option):
        return qt.QApplication.style().generatedIconPixmap(iconMode, pixmap, option)

    def hitTestComplexControl(self, control, option, position, widget = None):
        return qt.QApplication.style().hitTestComplexControl(control, option, position, widget)

    def itemPixmapRect(self, rectangle, alignment, pixmap):
        return qt.QApplication.style().itemPixmapRect(rectangle, alignment, pixmap)

    def itemTextRect(self, metrics, rectangle, alignment, enabled, text):
        return qt.QApplication.style().itemTextRect(metrics, rectangle, alignment, enabled, text)

    def pixelMetric(self, metric, option = None, widget = None):
        return qt.QApplication.style().pixelMetric(metric, option, widget)

    def polish(self, *args, **kwargs):
        return qt.QApplication.style().polish(*args, **kwargs)

    def styleHint(self, hint, option=None, widget=None, returnData=None):
        if hint == qt.QStyle.SH_Slider_AbsoluteSetButtons:
            return qt.Qt.LeftButton | qt.Qt.MidButton | qt.Qt.RightButton
        return qt.QApplication.style().styleHint(hint, option, widget, returnData)

    def subControlRect(self, control, option, subControl, widget = None):
        return qt.QApplication.style().subControlRect(control, option, subControl, widget)

    def subElementRect(self, element, option, widget = None):
        return qt.QApplication.style().subElementRect(element, option, widget)

    def unpolish(self, *args, **kwargs):
        return qt.QApplication.style().unpolish(*args, **kwargs)

    def sizeFromContents(self, ct, opt, contentsSize, widget = None):
        return qt.QApplication.style().sizeFromContents(ct, opt, contentsSize, widget)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
