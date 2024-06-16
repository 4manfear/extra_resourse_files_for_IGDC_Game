from maya.app.flux.ae.Custom import Custom

from maya.app.flux.imports import *
import maya.app.flux.core as fx
from maya.app.flux.core import pix

import MASH.api
import MASH.editor

import MASH.deleteMashNode as dmn

# TODO: Once we're clear of 2018, move these to flux
kDeleteThisNodeQ = mel.eval('getPluginResource("MASH", "kDeleteThisNodeQ")')
kYes = mel.eval('getPluginResource("MASH", "kYes")')
kDelNo = mel.eval('getPluginResource("MASH", "kDelNo")')

class NodeHeaders(Custom):
    def buildUI(self, nodeName, title, hasDelete):
        self.pluginName = 'MASH'

        self.isWaiter = cmds.nodeType(nodeName) == 'MASH_Waiter'
        self.isConstraint = cmds.nodeType(nodeName) == 'MASH_Constraint'

        if self.isWaiter:
            self.registerExternalNode('distributeNode', self.getDistributeNode)

        icon = qt.QLabel()
        pixmap = fx.getPixmap('out_' + cmds.nodeType(nodeName))
        icon.setPixmap(pixmap)

        self.toolbar = fx.widgetWithLayout('H', pix(2), pix(5),pix(2),pix(5),pix(2))
        self.toolbar.setAutoFillBackground(True)
        self.toolbar.setFixedHeight(pix(30))
        fx.setWidgetBackgroundColor(self.toolbar, [73,73,73])
        self.toolbar.layout().addWidget(icon)
        self.toolbar.layout().addWidget(qt.QLabel(self.getRes(title)))

        if self.isWaiter:
            self.numPoints = qt.QLabel('123')
            self.numPoints.setStyleSheet('QLabel{border:0px; border-radius:%dpx; background-color: rgb(43,43,43)}' % pix(2))
            self.numPoints.setContentsMargins(pix(20),pix(2),pix(2),pix(2))
            self.numPoints.setFixedHeight(pix(18))
            self.numPoints.setFixedWidth(pix(80))

            self.pointIcon = qt.QLabel(parent=self.numPoints)
            pixmap = fx.scalePixmap(fx.getPixmap('out_MASH_Points'), 16, 16)
            self.pointIcon.move(pix(1),pix(1))
            self.pointIcon.setPixmap(pixmap)

            self.toolbar.layout().addSpacing(2)
            self.toolbar.layout().addWidget(self.numPoints, 0)

            self.createAttributeListener('pointCount', self.updatePointCount)

        self.toolbar.layout().addStretch()

        self.hasEnable = 'enable' in cmds.listAttr(self.name) or self.isWaiter or self.isConstraint

        if cmds.nodeType(self.name) == 'MASH_Python':
            self.pythonPlayBtn = fx.ImageButton('ae_MASH_PythonPlay')
            self.pythonPlayBtn.clicked.connect(self.pythonNodePlay)
            self.toolbar.layout().addWidget(self.pythonPlayBtn)

        # self.mashEditorBtn = fx.ImageButton('ae_MASH_Editor')
        # self.mashEditorBtn.setToolTip('MASH Editor')
        # self.mashEditorBtn.clicked.connect(MASH.editor.show)
        # self.toolbar.layout().addWidget(self.mashEditorBtn)

        if not self.isWaiter and cmds.nodeType(self.name) not in ['MASH_BlendDeformer', 'MASH_Deformer', 'MASH_Jiggle']:
            self.waiterShortcut = fx.ImageButton('out_MASH_Waiter')
            self.waiterShortcut.setToolTip('Waiter')
            self.waiterShortcut.clicked.connect(self.showWaiter)
            self.toolbar.layout().addWidget(self.waiterShortcut)

        if self.hasEnable:
            self.toggleBtn = fx.ImageButton('out_MASH_Enable')
            self.toggleBtn.isOn = True
            self.toggleBtn.clicked.connect(self.toggleClicked)
            self.toolbar.layout().addWidget(self.toggleBtn)

        if hasDelete:
            self.delButton = fx.ImageButton('out_MASH_Delete')
            self.delButton.clicked.connect(self.delClicked)
            self.toolbar.layout().addWidget(self.delButton)

        self.addWidget(self.toolbar)

        self.addSpacing(pix(5))

        if cmds.nodeType(nodeName) == 'MASH_Waiter':
            self.createAttributeListener('enable', self.toggleChanged, node='distributeNode')
        elif self.isConstraint:
            self.createAttributeListener('constraintEnable', self.toggleChanged)
        elif self.hasEnable:
            self.createAttributeListener('enable', self.toggleChanged)

        if self.hasEnable:
            self.toggleChanged()

        if self.isWaiter:
            self.updatePointCount()

    def pythonNodePlay(self):
        cmds.dgdirty(self.name + '.time')

    def updatePointCount(self):
        points = 0
        try: points = cmds.getAttr(self.name + '.pointCount')
        except: pass
        self.numPoints.setText(str(points))

    def showWaiter(self):
        waiter = MASH.api.getWaiterFromNode(self.name)
        if waiter:
            mel.eval('showEditorExact("%s")' % waiter)

    def getDistributeNode(self):
        conns = cmds.listConnections(self.name+'.waiterMessage', d=False, s=True)
        if conns:
            return conns[0]
        else:
            return None

    def delClicked(self):
        '''
        Delete a MASH node.
        Waiters are deleted directly as they have a delete callback which will call MASH.deleteMashNode
        The forwarding to MEL is a stable (though untidy) way to delete all other MASH nodes.
        '''
        confirm = cmds.confirmDialog( title='MASH', message=kDeleteThisNodeQ, button=[kYes,kDelNo], defaultButton=kYes, cancelButton=kDelNo, dismissString=kDelNo )
        if confirm == kDelNo:
            return

        if cmds.nodeType(self.name) == 'MASH_Waiter':
            cmds.delete(self.name)
        else:
            mel.eval('source MASHdeleteNodeButton.mel')
            mel.eval('deleteButtonCMDS("%s", 1, 1)' % self.name)

    def toggleClicked(self):
        self.toggleBtn.isOn = not self.toggleBtn.isOn
        self.updateToggleBtn()
        attribute = '.enable'

        node = self.name
        if cmds.nodeType(self.name) == 'MASH_Waiter':
            node = self.getDistributeNode()

            if not node:
                return
                
        elif self.isConstraint:
            attribute = '.constraintEnable'

        cmds.setAttr(node + attribute, self.toggleBtn.isOn)

    def updateToggleBtn(self):
        self.toggleBtn.setImage('out_MASH_Enable' if self.toggleBtn.isOn else 'out_MASH_Disable')

    def toggleChanged(self):
        node = self.name
        attribute = '.enable'
        if cmds.nodeType(self.name) == 'MASH_Waiter':
            node = self.getDistributeNode()

            if not node:
                return

        elif self.isConstraint:
            attribute = '.constraintEnable'

        new = cmds.getAttr(node + attribute)
        self.toggleBtn.isOn = new
        self.updateToggleBtn()

    def getRes(self, name):
        return self._applyLocalization(name)

    def nodeChanged(self):
        if self.hasEnable:
            self.toggleChanged()

        if self.isWaiter:
            self.updatePointCount()

def addHeader(node, title, hasDelete=True):
    import maya.app.flux.ae.api as aeAPI
    aeAPI.addCustom(NodeHeaders(node, title, hasDelete))


# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
