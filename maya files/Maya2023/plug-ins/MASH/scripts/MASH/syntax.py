# source: https://wiki.python.org/moin/PyQt/Python%20syntax%20highlighting
# syntax.py

from maya.app.flux.imports import *

#from insulate.debug import debug
from MASH.textblock import TextBlock

def syFormat(syntaxColor, style=''):
    """Return a QTextCharFormat with the given attributes.
    """
    _color = qt.QColor()
    _color.setNamedColor(syntaxColor)

    _syFormat = qt.QTextCharFormat()
    _syFormat.setForeground(_color)
    if 'bold' in style:
        _syFormat.setFontWeight(qt.QFont.Bold)
    if 'italic' in style:
        _syFormat.setFontItalic(True)

    return _syFormat



class PythonHighlighter (qt.QSyntaxHighlighter):


    """Syntax highlighter for the Python language.
    """
    # Python keywords
    keywords = [
        'and', 'assert', 'break', 'class', 'continue', 'def',
        'del', 'elif', 'else', 'except', 'exec', 'finally',
        'for', 'from', 'global', 'if', 'import', 'in',
        'is', 'lambda', 'not', 'or', 'pass', 'print',
        'raise', 'return', 'try', 'while', 'yield',
        'None', 'True', 'False',
    ]

    # Python operators
    operators = [
        '=',
        # Comparison
        '==', '!=', '<', '<=', '[^>]>', '>=',
        # Arithmetic
        '\+', '-', '\*', '/', '//', '\%', '\*\*',
        # In-place
        '\+=', '-=', '\*=', '/=', '\%=',
        # Bitwise
        '\^', '\|', '\&', '\~', '[^>]>>', '<<',
    ]

    # Python braces
    braces = [
        '\{', '\}', '\(', '\)', '\[', '\]',
    ]

    mayaCmds = cmds.help( '[a-z]*', list=True, lng='Python' )

    MSG_FORMAT = syFormat('Gray')
    ERR_FORMAT = syFormat('red')

    def __init__(self, document):
        qt.QSyntaxHighlighter.__init__(self, document)

        # Syntax styles that can be shared by all languages
        self.STYLES = {
            'keyword': syFormat('DeepSkyBlue'),
            'operator': syFormat('DeepPink '),
            'brace': syFormat('darkGray'),
            'defclass': syFormat('MistyRose'),
            'string': syFormat('red'),
            'string2': syFormat('yellow'),
            'comment': syFormat('Gray'),
            'self': syFormat('Plum'),
            'numbers': syFormat('GhostWhite'),
            'maya': syFormat('SpringGreen'),
        }

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (qt.QRegExp("'''"), 1, self.STYLES['string2'])
        self.tri_double = (qt.QRegExp('"""'), 2, self.STYLES['string2'])

        rules = []

        # Keyword, operator, and brace rules
        rules += [(r'\b%s\b' % w, 0, self.STYLES['keyword'])
                  for w in PythonHighlighter.keywords]
        #rules += [(r'.%s.' % w, 0, self.STYLES['maya'])
        #          for w in PythonHighlighter.mayaCmds]
        rules += [(r'%s' % o, 0, self.STYLES['operator'])
                  for o in PythonHighlighter.operators]
        rules += [(r'%s' % b, 0, self.STYLES['brace'])
                  for b in PythonHighlighter.braces]

        # All other rules
        rules += [
            # 'self'
            (r'\bself\b', 0, self.STYLES['self']),

            # Double-quoted string, possibly containing escape sequences
            (r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.STYLES['string']),
            # Single-quoted string, possibly containing escape sequences
            (r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.STYLES['string']),

            # 'def' followed by an identifier
            (r'\bdef\b\s*(\w+)', 1, self.STYLES['defclass']),
            # 'class' followed by an identifier
            (r'\bclass\b\s*(\w+)', 1, self.STYLES['defclass']),

            # From '#' until a newline
            (r'#[^\n]*', 0, self.STYLES['comment']),

            # Numeric literals
            (r'\b[+-]?[0-9]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, self.STYLES['numbers']),
            (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, self.STYLES[
             'numbers']),
        ]

        # Build a qt.QRegExp for each pattern
        self.rules = [(qt.QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, textBlock):
        """Apply syntax highlighting to the given block of text.
        """
        data = self.currentBlockUserData()
        if data:
            try:
                if data['type'] == TextBlock.TYPE_MESSAGE:
                    self.setFormat(0, len(textBlock), self.MSG_FORMAT)
                    return
                if data['type'] == TextBlock.TYPE_OUTPUT_MSG:
                    self.setFormat(0, len(textBlock), self.ERR_FORMAT)
                    return
                if data['type'] not in TextBlock.CODE_TYPES:
                    return
            except:
                pass

        # Do other syntax syFormatting
        for expr, nth, syFormat in self.rules:
            index = expr.indexIn(textBlock, 0)

            while index >= 0:
                # We actually want the index of the nth match
                index = expr.pos(nth)
                length = len(expr.cap(nth))

                self.setFormat(index, length, syFormat)
                index = expr.indexIn(textBlock, index + length)

        self.setCurrentBlockState(0)

        # Do multi-line strings
        in_multiline = self.match_multiline(textBlock, *self.tri_single)
        if not in_multiline:
            in_multiline = self.match_multiline(textBlock, *self.tri_double)

    def match_multiline(self, textBlock, delimiter, in_state, style):
        """Do highlighting of multi-line strings. ``delimiter`` should be a
        ``qt.QRegExp`` for triple-single-quotes or triple-double-quotes, and
        ``in_state`` should be a unique integer to represent the corresponding
        state changes when inside those strings. Returns True if we're still
        inside a multi-line string when this function is finished.
        """
        # If inside triple-single quotes, start at 0
        if self.previousBlockState() == in_state:
            start = 0
            add = 0
        # Otherwise, look for the delimiter on this line
        else:
            start = delimiter.indexIn(textBlock)
            # Move past this match
            add = delimiter.matchedLength()

        # As long as there's a delimiter match on this line...
        while start >= 0:
            # Look for the ending delimiter
            end = delimiter.indexIn(textBlock, start + add)
            # Ending delimiter on this line?
            if end >= add:
                length = end - start + add + delimiter.matchedLength()
                self.setCurrentBlockState(0)
            # No; multi-line string
            else:
                self.setCurrentBlockState(in_state)
                length = textBlock.length() - start + add
            # Apply syFormatting
            self.setFormat(start, length, style)
            # Look for the next match
            start = delimiter.indexIn(textBlock, start + length)

        # Return True if still inside a multi-line string, False otherwise
        if self.currentBlockState() == in_state:
            return True
        else:
            return False
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
