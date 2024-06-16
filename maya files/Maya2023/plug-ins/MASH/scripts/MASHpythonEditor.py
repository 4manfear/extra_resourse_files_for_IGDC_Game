from builtins import range
import maya.OpenMayaUI as mui

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import re

from MASH.syntax import PythonHighlighter

class MASHpythonEditor(qt.QWidget):
    def __init__(self, node, attr, parent=None):
        super(MASHpythonEditor, self).__init__(parent)
        self.node = node
        self.scriptEditor = MASHPythonTextEdit(node, attr)
        self.layout = qt.QVBoxLayout(self)
        self.layout.addStretch()
        self.layout.setContentsMargins(pix(5),pix(3),pix(11),pix(3))
        self.layout.setSpacing(pix(5))
        self.scriptEditor.setMinimumWidth(pix(300))
        self.scriptEditor.setMinimumHeight(pix(360))
        self.number_bar = NumberBar()
        self.number_bar.setTextEdit(self.scriptEditor)

        codeAndNumberBoxLayout = qt.QHBoxLayout()
        codeAndNumberBoxLayout.addWidget(self.number_bar)
        codeAndNumberBoxLayout.addWidget(self.scriptEditor)
        codeAndNumberBoxLayout.setContentsMargins(pix(0),pix(2),pix(2),pix(2))

        codeNumberLibraryWidget = qt.QWidget()
        codeNumberLibraryWidget.setLayout(codeAndNumberBoxLayout)

        self.layout.addWidget(codeNumberLibraryWidget)

        self.scriptEditor.installEventFilter(self)
        qt.QShortcut(qt.QKeySequence("Ctrl+]"), self.scriptEditor, self.scriptEditor.indent, context=qt.Qt.WidgetShortcut)
        qt.QShortcut(qt.QKeySequence("Ctrl+["), self.scriptEditor, self.scriptEditor.dedent, context=qt.Qt.WidgetShortcut)

    #update connections
    def set_node(self, node, attr):
        self.node = node
        self.scriptEditor.node = node
        self.scriptEditor.attr = attr
        savedScript = cmds.getAttr( node+'.'+ attr)
        self.scriptEditor.setText(savedScript)

    def eventFilter(self, object, thisEvent):
        # Update the line numbers for all events on the text edit and the viewport.
        # This is easier than connecting all necessary singals.
        if object == self.scriptEditor:
            self.number_bar.update()
            return False
        return qt.QFrame.eventFilter(object, thisEvent)

def build_qt_widget(lay, node, sourceAttr):
    widget = MASHpythonEditor(node, sourceAttr)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)
        savedScript = cmds.getAttr( node+'.'+sourceAttr)
        widget.scriptEditor.setText(savedScript)

def update_qt_widget(layout, node, sourceAttr):
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if widget.metaObject().className() == "MASHpythonEditor":
                widget.set_node(node, sourceAttr)
                break
            #isinstance DOES NOT always detect the correct class type unfortunatly
            #if isinstance(widget, MASHPythonTextEdit):
            #    widget.set_node(node, wantedType, attr, sourceAttr, postCmd)


class MASHPythonTextEdit(qt.QTextEdit):
    def __init__(self, node, attr):
        super(MASHPythonTextEdit, self).__init__()
        self._separator = ' '
        self._addSpaceAfterCompleting = True
        pos = qt.QCursor.pos()
        self.node = node
        self.attr = attr

        self.setAcceptDrops(True)
        self.hilighter = PythonHighlighter(self.document())

        self._keysToIgnore = [qt.Qt.Key_Enter,
                              qt.Qt.Key_Return,
                              qt.Qt.Key_Escape,
                              ]
        self.textChanged.connect(self.on_text_changed)
        savedScript = cmds.getAttr( self.node+'.'+self.attr)
        self.setText(savedScript)

    #intercept tab keys
    def keyPressEvent(self, e):
        if e.key() == qt.Qt.Key_Tab:
            e.accept()
            cursor = self.textCursor()
            cursor.insertText("    ")
        elif e.matches(qt.QKeySequence.Paste):
            # brute force refresh of the syntax highlighting by rebuilding the AE
            import xml.parsers.expat
            #get the clipboard text using PySide
            cb = qt.QApplication.clipboard().text()
            cb = re.sub(r'<[^>]*>', '', cb)
            self.textCursor().beginEditBlock()
            self.textCursor().insertText(cb)
            self.textCursor().endEditBlock()
        else:
            #otherwise handle events normally
            qt.QTextEdit.keyPressEvent(self,e)

    def on_text_changed(self):
        textIn = self.document().toPlainText()
        cmds.setAttr( self.node+'.'+self.attr, textIn, type="string" )

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        cursor = self.textCursor()
        data = e.mimeData().text()
        cursor.insertText(data+' ')

    def textUnderCursor(self):
        cursor = self.textCursor()
        textIn = self.document().toPlainText()
        textUnderCursor = ''
        i = cursor.position() - 1
        while i >=0 and textIn[i] != self._separator and '.':
            textUnderCursor = textIn[i] + textUnderCursor
            i -= 1
        return textUnderCursor

    def indent(self):
        # Grab the cursor
        cursor = self.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            # Iterate over lines
            for n in range(diff + 1):
                # Move to start of each line
                cursor.movePosition(qt.QTextCursor.StartOfLine)
                # Insert tabbing
                cursor.insertText("    ")
                # And move back up
                cursor.movePosition(qt.QTextCursor.Up)
        # If there is no selection, just insert a tab
        else:
            cursor.insertText("    ")

    def dedent(self):
        cursor = self.textCursor()
        if cursor.hasSelection():
            # Store the current line/block number
            temp = cursor.blockNumber()
            # Move to the selection's last line
            cursor.setPosition(cursor.selectionEnd())
            # Calculate range of selection
            diff = cursor.blockNumber() - temp
            # Iterate over lines
            for n in range(diff + 1):
                self.handleDedent(cursor)
                # Move up
                cursor.movePosition(qt.QTextCursor.Up)
        else:
            self.handleDedent(cursor)


    def handleDedent(self,cursor):

        cursor.movePosition(qt.QTextCursor.StartOfLine)

        # Grab the current line
        line = cursor.block().text()

        # If the line starts with a tab character, delete it
        if line.startswith("    "):

            # Delete next character
            cursor.deleteChar()
            cursor.deleteChar()
            cursor.deleteChar()
            cursor.deleteChar()

        # Otherwise, delete all spaces until a non-space character is met
        else:
            for char in line[:8]:

                if char != " ":
                    break

                cursor.deleteChar()

class NumberBar(qt.QWidget):

    def __init__(self, *args):
        qt.QWidget.__init__(self, *args)
        self.edit = None
        # This is used to update the width of the control.
        # It is the highest line that is currently visibile.
        self.highest_line = 0

    def setTextEdit(self, edit):
        self.edit = edit

    def update(self, *args):
        '''
        Updates the number bar to display the current set of numbers.
        Also, adjusts the width of the number bar if necessary.
        '''
        # The + 4 is used to compensate for the current line being bold.
        width = pix(20)
        if self.width() != width:
            self.setFixedWidth(width)
        qt.QWidget.update(self, *args)

    def paintEvent(self, paintEvent):
        contents_y = self.edit.verticalScrollBar().value()
        page_bottom = contents_y + self.edit.viewport().height()
        font_metrics = self.fontMetrics()
        current_block = self.edit.document().findBlock(self.edit.textCursor().position())

        painter = qt.QPainter(self)

        line_count = 0
        # Iterate over all text blocks in the document.
        block = self.edit.document().begin()
        while block.isValid():
            line_count += 1

            # The top left position of the block in the document
            position = self.edit.document().documentLayout().blockBoundingRect(block).topLeft()

            # Check if the position of the block is out side of the visible
            # area.
            #if position.y() &gt; page_bottom:
            #    break

            # We want the line number for the selected line to be bold.
            bold = False
            if block == current_block:
                bold = True
                font = painter.font()
                penHText = qt.QPen(qt.QColor("#00e0fc"))
                painter.setPen(penHText);
                font.setBold(True)

                painter.setPen(penHText);
                painter.setFont(font)

            # Draw the line number right justified at the y position of the
            # line. 3 is a magic padding number. drawText(x, y, text).
            painter.drawText(self.width() - font_metrics.horizontalAdvance(str(line_count)) - pix(3), round(position.y()) - contents_y + font_metrics.ascent(), str(line_count))

            # Remove the bold style if it was set previously.
            if bold:
                font = painter.font()
                font.setBold(False)
                penHText = qt.QPen(qt.QColor("#CFCFCF"))
                painter.setPen(penHText);
                painter.setFont(font)

            block = block.next()

        self.highest_line = line_count
        painter.end()

        qt.QWidget.paintEvent(self, paintEvent)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
