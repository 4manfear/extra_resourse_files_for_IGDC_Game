from __future__ import division
# Copyright (C) Mainframe
# Created by Alan Stanzione on 14/09/2015.

from builtins import range
import maya.OpenMayaUI as mui
import maya.OpenMaya as om

usingPyside2 = False
try:
    import PySide2
    usingPyside2 = True
except:
    pass

from maya.app.flux.imports import *
from maya.app.flux.core import pix
import maya.app.flux.core as fx

import mash_repro_utils
from mash_repro_icons import MASH_REPRO_ICONS

from functools import partial
import MASH.undo as undo

DISABLE_UPDATE_UI = False

SCENE_OPENED = False

class LodTriStateButton(qt.QFrame):
    """ Tris tate button used for Mesh/Proxy/Lod selection """
    state_changed = qt.Signal()

    def __init__(self, index=0, parent=None, has_camera=False):
        super(LodTriStateButton, self).__init__(parent)
        self.mesh_button_annotation = mel.eval('getPluginResource("MASH", "kTriStateMeshAnnotation")')
        self.proxy_button_annotation = mel.eval('getPluginResource("MASH", "kTriStateProxyAnnotation")')
        self.lod_camera_annotation = mel.eval('getPluginResource("MASH", "kTriStateLodCameraAnnotation")')
        self.lod_no_camera_annotation = mel.eval('getPluginResource("MASH", "kTriStateLodNoCameraAnnotation")')

        self.index = index
        self._has_camera = has_camera

        self.setFixedSize(qt.QSize(pix(72), pix(26)))

        layout = qt.QHBoxLayout()
        layout.setContentsMargins(pix(3),pix(3),pix(3),pix(3))
        layout.setSpacing(pix(3))

        self._group = qt.QButtonGroup(self)

        self._mesh_button = self._build_button(MASH_REPRO_ICONS.mesh())
        self._mesh_button.setToolTip(self.mesh_button_annotation)
        layout.addWidget(self._mesh_button)

        self._proxy_button = self._build_button(MASH_REPRO_ICONS.proxy_on())
        self._proxy_button.setToolTip(self.proxy_button_annotation)
        layout.addWidget(self._proxy_button)

        self._lod_button = self._build_button(MASH_REPRO_ICONS.lod_on())
        if has_camera:
            self._lod_button.setToolTip(self.lod_camera_annotation)
        else:
            self._lod_button.setToolTip(self.lod_no_camera_annotation)
            self._lod_button.setEnabled(False)
        layout.addWidget(self._lod_button)

        self.setLayout(layout)

        self._group.addButton(self._mesh_button)
        self._group.addButton(self._proxy_button)
        self._group.addButton(self._lod_button)
        self._group.buttonClicked.connect(self.change_status)

        self.setStyleSheet("""QFrame{border: none; background-color: #444444}
                            QPushButton{border: none; icon-size: %dpx;}
                            QPushButton:checked{border: none; background-color: #5384A5}
                            QPushButton:!checked{border: none; background-color: #444444}""" % pix(20))


    def _build_button(self, icon):
        button = qt.QPushButton(self)
        button.setIcon(icon)
        button.setFixedSize(pix(20), pix(20))
        button.setCheckable(True)
        button.setFlat(True)
        return button

    def set_disabled(self, status):
        if not status:
            self._proxy_button.setIcon(MASH_REPRO_ICONS.proxy_on())
        else:
            self._proxy_button.setIcon(MASH_REPRO_ICONS.proxy_off())
        self._proxy_button.setDisabled(status)

        if not status and self._has_camera:
            self._lod_button.setIcon(MASH_REPRO_ICONS.lod_on())
        else:
            self._lod_button.setIcon(MASH_REPRO_ICONS.lod_off())
        self._lod_button.setDisabled(status or not self._has_camera)


    def camera_updated(self, value):
        #in case no camera is selected and we were in LOD mode, we switch to proxy
        if not value and self.index == 2:
            self.set_index(1)
            self.change_status()

        status = self._proxy_button.isEnabled()
        self._has_camera = value
        if value and status:
            self._lod_button.setIcon(MASH_REPRO_ICONS.lod_on())
        else:
            self._lod_button.setIcon(MASH_REPRO_ICONS.lod_off())
        self._lod_button.setEnabled(value and status)

        if value:
            self._lod_button.setToolTip(self.lod_camera_annotation )
        else:
            self._lod_button.setToolTip(self.lod_no_camera_annotation )

    def change_status(self, value=False):
        if self._mesh_button.isChecked():
            self.index = 0
        elif self._proxy_button.isChecked():
            self.index = 1
        else:
            self.index = 2
        self.state_changed.emit()

    def set_index(self, value):
        self.index = value
        if value == 0:
            self._mesh_button.setChecked(True)
        elif value == 1:
            self._proxy_button.setChecked(True)
        else:
            self._lod_button.setChecked(True)

class ObjectsWidget(qt.QTreeWidget):
    """ Input mesh tree widget """
    obj_dropped = qt.Signal(int) # signal fired after a drop event
    obj_selected = qt.Signal(int) # signare fired after a item select event

    def __init__(self, parent=None):
        qt.QTreeWidget.__init__(self, parent)

        self.delete_annotation = mel.eval('getPluginResource("MASH", "kDeleteLabel")')
        self.refresh_annotation = mel.eval('getPluginResource("MASH", "kRefreshLabel")')
        self.reveal_annotation = mel.eval('getPluginResource("MASH", "kRevealLabel")')
        self.add_selected_objs_annotation = mel.eval('getPluginResource("MASH", "kAddSelectedObjsLabel")')

        self.font = qt.QFont()
        self.font.setPointSize(12)
        self.setFont(self.font)
        self.setDragEnabled(False)
        self.setDragDropMode(qt.QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.node = None
        self._last_selected_item = None

        self.setIndentation(pix(1))

        if usingPyside2:
            self.tree_header = self.header()
            self.tree_header.setSectionsMovable(False)
            #self.tree_header.setSectionResizeMode(0, qt.QHeaderView.Fixed)
            #self.tree_header.setSectionResizeMode(1, qt.QHeaderView.Fixed)
        else:
            self.tree_header = self.header()
            self.tree_header.setMovable(False)
            #self.tree_header.setResizeMode(0, qt.QHeaderView.Fixed)
            #self.tree_header.setResizeMode(1, qt.QHeaderView.Fixed)

        self.itemSelectionChanged.connect(self.selection_changed)

        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

        self.deleteAction = qt.QAction(self.delete_annotation, self)
        self.deleteAction.triggered.connect(self.delete_item)
        self.refreshAction = qt.QAction(self.refresh_annotation, self)
        self.refreshAction.triggered.connect(self.refresh_item)
        self.revealAction = qt.QAction(self.reveal_annotation, self)
        self.revealAction.triggered.connect(self.reveal_item_in_outliner)
        self.menu = qt.QMenu(self)
        self.menu.addAction(self.deleteAction)
        self.menu.addAction(self.refreshAction)
        self.menu.addAction(self.revealAction)

        self.addObjectsAction = qt.QAction(self.add_selected_objs_annotation, self)
        self.addObjectsAction.triggered.connect(self.add_objects)
        self.global_menu = qt.QMenu(self)
        self.global_menu.addAction(self.addObjectsAction)

    @staticmethod
    def _find_outliner():
        for panel in cmds.getPanel(vis=1):
            if 'outliner' in panel:
                return panel

    def reveal_item_in_outliner(self):
        outliner = self._find_outliner()
        if outliner is None:
            cmds.OutlinerWindow()
            outliner = cmds.getPanel(typ='outlinerPanel')[0]

        data = mash_repro_utils.get_data_layout(self.node)
        objs = [data[int(item.text(0).split(':')[0])]["group"] for item in self.selectedItems()]
        cmds.select(objs)

        cmds.evalDeferred("from maya import cmds; cmds.outlinerEditor('%s', e=1, sc=1)" % outliner)

    def refresh_item(self):
        """ Refresh an input group """

        for item in self.selectedItems():
            id = int(item.text(0).split(':')[0])
            mash_repro_utils.refresh_mesh_group(self.node, id)

        self.obj_dropped.emit(id)

    @undo.chunk('Connect Group')
    def add_objects(self):
        """ Add selected objects to the repro node """
        objs = cmds.ls(sl=True)
        self.connect_objs(objs)
        
    def connect_objs(self, objs):
        cmds.undoInfo(ock=True)

        selSize = len(objs)
        computation = None
        if selSize > 10:
            computation = om.MComputation()
            computation.beginComputation( True ) 
            computation.setProgressRange( 0, selSize )
        index = None
        cmds.flushIdleQueue()

        for i in range(0, selSize):
            obj = objs[i]
            #if it's a shape get the parent
            if cmds.objectType(obj) == "mesh":
                obj = cmds.listRelatives(obj,p=True)[0]
            if cmds.listRelatives(obj, ad=True, type="mesh"):
                index_tmp = mash_repro_utils.connect_mesh_group(self.node, obj, new_connection=True)
            if index_tmp is not None:
                index = index_tmp

            if computation:
                progress = float(i)/selSize * 100
                computation.setProgress( int(progress) )
                if computation.isInterruptRequested(): break
        
        # update the UI
        if index is not None:
            self.obj_dropped.emit(index)

        cmds.undoInfo(cck=True)

        if computation:
            computation.endComputation()

    @undo.chunk('Delete Group')
    def delete_item(self):
        """ Remove a object from the repro node """

        cmds.undoInfo(ock=True, chunkName="reproDeleteObject "+ self.node)

        ids = []
        for item in self.selectedItems():
            ids.append(int(item.text(0).split(':')[0]))

        for id in sorted(ids, reverse=True):
            mash_repro_utils.remove_mesh_group(self.node, id)

        self.obj_dropped.emit(None)

        cmds.undoInfo(cck=True)

        self._last_selected_item = None


    def show_context_menu(self, pos):
        """ Show context menu """
        item = self.itemAt( pos )
        # if the mouse is on an item show also the delete action
        if item:
            self.menu.exec_( self.mapToGlobal(pos) )
        else:
            self.global_menu.exec_( self.mapToGlobal(pos) )

    def resizeEvent(self, event):
        """ Resize event, adjust the lod button size """
        qt.QTreeWidget.resizeEvent(self, event)

        ver_sb = self.verticalScrollBar()
        first_section_offset = pix(80)
        if ver_sb.isVisible():
            first_section_offset += ver_sb.width()

        #removing two pixels to prevent horizontal scroll
        tot_width = self.size().width() - pix(2)
        self.setColumnWidth(0,tot_width - first_section_offset)
        self.setColumnWidth(1, pix(80))

    def set_node(self, node):
        """ Set the repro node """
        self.node = node

    @undo.chunk('Drop Node')
    def dropEvent(self, event):
        """ Drop event """
        bg_item = self.itemAt( event.pos() )
        # handle replace item
        dropped_index = None
        if bg_item and bg_item.treeWidget() is self:
            dropped_index = int(bg_item.text(0).split(':')[0])

        items = []
        selected_items = self.selectedItems() or []
 
        # check if the event has text data
        if event.mimeData().text():
            objs = event.mimeData().text().split("\n")
            self.connect_objs(objs)

        #caching selection before drop
        selection = [item.text(0).split(":")[-1] for item in self.selectedItems()]

        # let qt add the item widget to the tree
        qt.QTreeWidget.dropEvent(self, event)

        # if the id of every item is not in ascending order
        # it means that is a internal move event
        lastId = -1
        reorderIds = False
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            id = int(item.text(0).split(':')[0])
            if id < lastId:
                reorderIds = True
                lastId = id
                break
            lastId = id
        if reorderIds:
            new_order = []
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                id = int(item.text(0).split(':')[0])
                new_order.append(id)
            cmds.undoInfo(ock=True)
            mash_repro_utils.reorder_mesh_group_node(self.node, new_order)
            cmds.undoInfo(cck=True)
            self.obj_dropped.emit(lastId)
        elif not event.mimeData().text():
            if selected_items:
                id = int(selected_items[0].text(0).split(':')[0])
                self.obj_dropped.emit(id)
            else:
                self.obj_dropped.emit(None)

        #reapplying selection after drop
        self.selectionModel().clearSelection()
        for s in selection:
            found_items = self.findItems(':' + s, qt.Qt.MatchEndsWith)
            if not found_items:
                continue
            found_items[0].setSelected(True)


    def dragEnterEvent(self, qevent):
        """ Drag enter event """
        qevent.accept()

    def selection_changed(self):
        """ Selection changed """
        items = self.selectedItems() or []
        if items and self._last_selected_item not in [item.text(0) for item in items]:
            item = items[0]
            while item.parent():
                item = item.parent()
            id = int(item.text(0).split(':')[0])
            self.obj_selected.emit(id)

        if len(items) == 1:
            self._last_selected_item = items[0].text(0)

    def remove_last_selected(self):
        self._last_selected_item = None

    def set_display_type(self, index, button):
        """ Set display type (Mesh, Proxy, Lod) """
        cmds.setAttr("%s.instancedGroup[%d].displayType" % (self.node, index), button.index)
        selected_items = self.selectedItems()
        curret_item_is_selected = False
        for item in selected_items:
            id = int(item.text(0).split(':')[0])
            if index == id:
                curret_item_is_selected = True
        if not curret_item_is_selected:
            return

        for item in selected_items:
            id = int(item.text(0).split(':')[0])
            if index == id:
                continue
            has_proxies = len(cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (self.node, id), mi=True) or []) > 0
            if ((button.index > 0) and has_proxies) or (button.index == 0):
                cmds.setAttr("%s.instancedGroup[%d].displayType" % (self.node, id), button.index)
                # update ui
                item_button = self.itemWidget(item, 1).widget
                item_button.set_index(button.index)

    def paintEvent(self, event):
        super(ObjectsWidget, self).paintEvent(event)

        #hack for fixing a qt bug where drawing the selected row would overlap with the border
        painter = qt.QPainter(self.viewport())
        painter.fillRect(0, 0, pix(1), self.size().height(), qt.QColor(43, 43, 43))


class ProxiesWidget(qt.QTreeWidget):
    """ Proxies tree widget """
    obj_dropped = qt.Signal(int)

    def __init__(self, parent=None):
        qt.QTreeWidget.__init__(self, parent)

        self.delete_annotation = mel.eval('getPluginResource("MASH", "kDeleteLabel")')
        self.refresh_annotation = mel.eval('getPluginResource("MASH", "kRefreshLabel")')
        self.reveal_annotation = mel.eval('getPluginResource("MASH", "kRevealLabel")')
        self.add_selected_objs_annotation = mel.eval('getPluginResource("MASH", "kAddSelectedObjsLabel")')

        self.font = qt.QFont()
        self.font.setPointSize(12)
        self.setFont(self.font)
        self.setDragEnabled(False)
        self.setDragDropMode(qt.QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        self.node = None
        self.instance_index = -1

        self.setIndentation(pix(1))

        if usingPyside2:
            self.header_tree = self.header()
            self.header_tree.setSectionsMovable(False)
            #self.header().setSectionResizeMode(0, qt.QHeaderView.Fixed)
            #self.header().setSectionResizeMode(1, qt.QHeaderView.Fixed)
        else:
            self.header_tree = self.header()
            self.header_tree.setMovable(False)
            #self.header().setResizeMode(0, qt.QHeaderView.Fixed)
            #self.header().setResizeMode(1, qt.QHeaderView.Fixed)

        # Set context menu
        self.setContextMenuPolicy(qt.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)
        self.deleteAction = qt.QAction(self.delete_annotation, self)
        self.deleteAction.triggered.connect(self.delete_item)
        self.refreshAction = qt.QAction(self.refresh_annotation, self)
        self.refreshAction.triggered.connect(self.refresh_item)
        self.revealAction = qt.QAction(self.reveal_annotation, self)
        self.revealAction.triggered.connect(self.reveal_item_in_outliner)
        self.menu = qt.QMenu(self)
        self.menu.addAction(self.deleteAction)
        self.menu.addAction(self.refreshAction)
        self.menu.addAction(self.revealAction)

        self.addObjectsAction = qt.QAction(self.add_selected_objs_annotation, self)
        self.addObjectsAction.triggered.connect(self.add_objects)
        self.global_menu = qt.QMenu(self)
        self.global_menu.addAction(self.addObjectsAction)

    def refresh_item(self):
        """ Refresh an input proxy group """
        for item in self.selectedItems():
            id = int(item.text(0).split(':')[0])
            mash_repro_utils.refresh_proxy_group(self.node, self.instance_index, id)

        self.obj_dropped.emit(self.instance_index)

    @undo.chunk('Add Group')
    def add_objects(self):
        """ Add selected objects to the repro node """
        cmds.undoInfo(ock=True)
        objs = cmds.ls(sl=True)
        for obj in objs:
            #if it's a shape get the parent
            if cmds.objectType(obj) == "mesh":
                obj = cmds.listRelatives(obj,p=True)[0]
            if cmds.listRelatives(obj, ad=True, type="mesh"):
                mash_repro_utils.connect_proxy_group(self.node, obj, self.instance_index)
        cmds.undoInfo(cck=True)
        self.obj_dropped.emit(self.instance_index)

    @staticmethod
    def _find_outliner():
        for panel in cmds.getPanel(vis=1):
            if 'outliner' in panel:
                return panel

    def reveal_item_in_outliner(self):
        outliner = self._find_outliner()
        if outliner is None:
            cmds.OutlinerWindow()
            outliner = cmds.getPanel(typ='outlinerPanel')[0]

        objs = []
        for item in self.selectedItems():
            obj = mash_repro_utils.get_proxy_mesh(self.node, self.instance_index, int(item.text(0).split(':')[0]))
            if obj is not None:
                objs.append(obj)
        cmds.select(objs)

        cmds.evalDeferred("from maya import cmds; cmds.outlinerEditor('%s', e=1, sc=1)" % outliner)

    @undo.chunk('Delete Group')
    def delete_item(self):
        """ Remove a object from the repro node """
        cmds.undoInfo(ock=True, chunkName="reproDeleteProxyGroup " + self.node + " " + str(self.instance_index))

        ids = []
        for item in self.selectedItems():
            ids.append(int(item.text(0).split(':')[0]))

        for id in sorted(ids, reverse=True):
            mash_repro_utils.remove_proxy_group(self.node, self.instance_index, id)

        self.obj_dropped.emit(self.instance_index)
        cmds.undoInfo(cck=True)

    def show_context_menu(self, pos):
        """ Show context menu """
        item = self.itemAt( pos )
        # if the mouse is on an item show also the delete action
        if item:
            self.menu.exec_( self.mapToGlobal(pos) )
        else:
            self.global_menu.exec_( self.mapToGlobal(pos) )

    def set_node(self, node):
        """ Set the repro node """
        self.node = node

    @undo.chunk('Drop Group')
    def dropEvent(self, event):
        """ Drop event """
        # check if the event has text data
        cmds.undoInfo(ock=True)
        bg_item = self.itemAt( event.pos() )
        # handle replace item
        dropped_index = None
        if bg_item and bg_item.treeWidget() is self:
            dropped_index = int(bg_item.text(0).split(':')[0])

        if event.mimeData().text():
            objs = event.mimeData().text().split("\n")
            for obj in objs:
                if mash_repro_utils.connect_proxy_group(self.node, obj, self.instance_index, dropped_index) is not None:
                    self.obj_dropped.emit(self.instance_index)
        cmds.undoInfo(cck=True)

        #caching selection before drop
        selection = [item.text(0).split(":")[-1] for item in self.selectedItems()]

        # let qt add the item widget to the tree
        qt.QTreeWidget.dropEvent(self, event)

        # if the id of every item is not in ascending order
        # it means that is a internal move event
        lastId = -1
        reorderIds = False
        for i in range(self.topLevelItemCount()):
            item = self.topLevelItem(i)
            id = int(item.text(0).split(':')[0])
            if id < lastId:
                reorderIds = True
                lastId = id
                break
            lastId = id
        if reorderIds:
            new_order = []
            for i in range(self.topLevelItemCount()):
                item = self.topLevelItem(i)
                id = int(item.text(0).split(':')[0])
                new_order.append(id)
            mash_repro_utils.reorder_proxy_group_node(self.node, self.instance_index, new_order)
            self.obj_dropped.emit(self.instance_index)
        elif not event.mimeData().text():
            self.obj_dropped.emit(self.instance_index)

        #reapplying selection after drop
        self.selectionModel().clearSelection()
        for s in selection:
            found_items = self.findItems(s, qt.Qt.MatchEndsWith)
            if not found_items:
                continue
            found_items[0].setSelected(True)

    def dragEnterEvent(self, qevent):
        """ Drag enter event """
        if self.isEnabled():
            qevent.acceptProposedAction()

    def resizeEvent(self, event):
        """ Resize event, resize to lod distance box to the correct proportion """
        qt.QTreeWidget.resizeEvent(self, event)

        ver_sb = self.verticalScrollBar()
        first_section_offset = pix(80)
        if ver_sb.isVisible():
            first_section_offset += ver_sb.width()

        #removing two pixels to prevent horizontal scroll
        tot_width = self.size().width() - pix(2)
        self.setColumnWidth(0,tot_width - first_section_offset)
        self.setColumnWidth(1, pix(80))

    def set_lod_distance(self, index, spinBox):
        """ Set lod distance """
        if self.node:
            value = cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (self.node, self.instance_index, index))
            if value != spinBox.value():
                cmds.setAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (self.node, self.instance_index, index), spinBox.value())

    def paintEvent(self, event):
        super(ProxiesWidget, self).paintEvent(event)

        #hack for fixing a qt bug where drawing the selected row would overlap with the border
        painter = qt.QPainter(self.viewport())
        painter.fillRect(0, 0, pix(1), self.size().height(), qt.QColor(43, 43, 43))


class CenterWidget(qt.QWidget):
    def __init__(self, parent, wrapped_widget):
        super(CenterWidget, self).__init__(parent)

        self._widget = wrapped_widget

        l = qt.QVBoxLayout()
        l.setContentsMargins(pix(0), pix(0), pix(0), pix(0))
        l.addWidget(wrapped_widget, pix(0), qt.Qt.AlignCenter)

        self.setLayout(l)

    @property
    def widget(self):
        return self._widget

def sceneChanged(data):
    """ The scene is changed, due to a new scene or open scene command """
    global SCENE_OPENED
    SCENE_OPENED = True
    refresh_all_aetemplates(force=True)



class AEMASH_ReproTemplate(qt.QWidget):
    """ MASH Repro AETeplate widget """
    camera_has_changed = qt.Signal(bool)

    TREE_STYLE_SHEET = '''
                       QTreeWidget {outline:0; border: %dpx solid #2B2B2B; border-left: %dpx solid #2B2B2B; border-top: %dpx solid #2B2B2B;  icon-size: %dpx;}
                       QHeaderView::section{min-height: %d; background: #444444; padding-left: %dpx; border: %dpx solid #2B2B2B;}
                       QHeaderView::section:first{padding-left: %dpx;}
                       QTreeView::item {height:%dpx; border: %dpx solid #2B2B2B; border-right-color:transparent; border-left: 0px solid #2B2B2B;}
                       QTreeView::item:selected {background: #5384A5}
                       QTreeView::item:!selected {background: #5D5D5D}
                       ''' % (pix(2), pix(1), pix(1), pix(20), pix(20), pix(2), pix(1), pix(22), pix(30), pix(1))

    def __init__(self, node, parent=None):
        super(AEMASH_ReproTemplate, self).__init__(parent)

        self.objects_annotation = mel.eval('getPluginResource("MASH", "kObjectsLabel")')
        self.display_annotation = mel.eval('getPluginResource("MASH", "kDisplayLabel")')
        self.proxies_annotation = mel.eval('getPluginResource("MASH", "kProxiesLabel")')
        self.lod_annotation = mel.eval('getPluginResource("MASH", "kLodLabel")')
        self.lod_spinbox_annotation = mel.eval('getPluginResource("MASH", "kLodSpinBoxAnnotation")')


        # attach callback, used to clean the widget when a new scene is created or a scene is opened
        self.openCallback = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterFileRead, sceneChanged)
        self.newCallback = om.MSceneMessage.addCallback(om.MSceneMessage.kAfterNew, sceneChanged)

        self.updating_UI = True
        self.node = node

        #GUI
        self.layout = qt.QVBoxLayout()
        self.layout.setContentsMargins(qt.QMargins(pix(9), pix(0), pix(0), pix(0)))

        splitter = qt.QSplitter(qt.Qt.Vertical)
        splitter.setStyleSheet("QSplitter::handle {image: url(%s); height: %dpx;}" % 
                               (MASH_REPRO_ICONS.get_icon_path("ae_MASH_ReproDrag_hor"), pix(20)))
        self.layout.addWidget(splitter)

        self.objs_widget = ObjectsWidget()
        self.objs_widget.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
        self.objs_widget.setColumnCount(2)
        self.objs_widget.set_node(node)
        self.font1 = qt.QFont()
        self.font1.setPointSize(9)
        self.objs_widget.headerItem().setFont(0, self.font1)
        self.objs_widget.headerItem().setFont(1, self.font1)
        self.objs_widget.headerItem().setText(0,self.objects_annotation)
        self.objs_widget.headerItem().setText(1,self.display_annotation)
        self.objs_widget.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)
        self.objs_widget.setStyleSheet(self.TREE_STYLE_SHEET)
        splitter.addWidget(self.objs_widget)

        self.proxy_widget = ProxiesWidget()

        self.proxy_widget.setColumnCount(2)
        self.proxy_widget.setHorizontalScrollBarPolicy(qt.Qt.ScrollBarAlwaysOff)
        self.proxy_widget.set_node(node)
        self.font2 = qt.QFont()
        self.font2.setPointSize(9)

        self.proxy_widget.headerItem().setFont(0, self.font2)
        self.proxy_widget.headerItem().setFont(1, self.font2)
        self.proxy_widget.headerItem().setText(0,self.proxies_annotation)
        self.proxy_widget.headerItem().setText(1,self.lod_annotation)
        self.proxy_widget.setSelectionMode(qt.QAbstractItemView.ExtendedSelection)

        self.proxy_widget.setStyleSheet(self.TREE_STYLE_SHEET)

        splitter.addWidget(self.proxy_widget)

        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)

        self.setLayout(self.layout)

        self.update_ui()

        self.objs_widget.obj_dropped.connect(self.update_ui)
        self.objs_widget.obj_selected.connect(self.update_proxies)
        self.proxy_widget.obj_dropped.connect(self.update_proxies)

        self.updating_UI = False

        self.setObjectName("AEMASH_ReproTemplate")

    def __del__(self):
        """ Destructor, remove the scene callbacks """
        om.MSceneMessage.removeCallback(self.openCallback)
        om.MSceneMessage.removeCallback(self.newCallback)

    def set_node(self, node):
        """ Set the repro node """
        self.node = node
        self.objs_widget.set_node(node)
        self.proxy_widget.set_node(node)

    def camera_changed(self, camera):
        """ Camera changed """
        if self.updating_UI:
            return

        if cmds.objExists(camera) and cmds.objectType(camera,i="camera"):
            self.camera_has_changed.emit(True)
        else:
            self.camera_has_changed.emit(False)

    def update_proxies(self, isntance_index=-1):
        """ Update the proxies list """
        self.proxy_widget.instance_index = isntance_index
        self.proxy_widget.clear()
        num_groups = cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (self.node, isntance_index), mi=True) or []
        for group in num_groups:
            child_ids = cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxy" % (self.node, isntance_index, group), mi=True) or []
            if not child_ids:
                continue
            # get group name
            groups_connections = cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (self.node, isntance_index, group),s=1) or []
            if len(groups_connections) == 0:
                continue
            group_item_name = groups_connections[0]

            group_item = qt.QTreeWidgetItem(self.proxy_widget)
            group_item.setFlags(qt.Qt.ItemIsDragEnabled | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            spinBox = qt.QDoubleSpinBox(self)
            spinBox.setStyleSheet("QDoubleSpinBox{border: none;}")
            spinBox.setToolTip(self.lod_spinbox_annotation)
            spinBox.setMaximum(100000000)
            value = cmds.getAttr("%s.instancedGroup[%d].proxyGroup[%d].proxyLod" % (self.node, isntance_index, group))
            spinBox.setValue(value)
            spinBox.setButtonSymbols(qt.QAbstractSpinBox.NoButtons)
            spinBox.editingFinished.connect(partial(self.proxy_widget.set_lod_distance, group, spinBox))
            spinBox.setFixedSize(qt.QSize(pix(72), pix(26)))
            self.proxy_widget.setItemWidget(group_item, 1, CenterWidget(self, spinBox))
            group_item.setText(0, "%d: %s" % (group, group_item_name))
            group_item.setIcon(0, qt.QIcon(MASH_REPRO_ICONS.vertical_drag()))

        self._disable_object_tree_buttons()

    def update_ui(self, index=None):
        """ Update the objects and proxies lists """
        self.proxy_widget.clear()
        self.proxy_widget.instance_index = -1
        self.objs_widget.clear()
        if self.node is None:
            return
        if not cmds.objExists(self.node):
            self.node = None
            return
        num_groups = cmds.getAttr("%s.instancedGroup" % self.node, mi=True) or []

        self.objs_widget.remove_last_selected()

        has_camera = False
        if cmds.objExists(self.node):
            cam_connections = cmds.listConnections("%s.cameraMatrix" % self.node) or []
            if len(cam_connections) > 0:
                has_camera = cmds.objExists(cam_connections[0])

        for group in num_groups:
            child_ids = cmds.getAttr("%s.instancedGroup[%d].instancedMesh" % (self.node, group), mi=True) or []
            if not child_ids:
                continue
            # get group name
            groups_connections = cmds.listConnections("%s.instancedGroup[%d].groupMessage" % (self.node, group),s=1) or []
            if len(groups_connections) == 0:
                continue
            group_item_name = groups_connections[0]

            group_item = qt.QTreeWidgetItem(self.objs_widget)
            group_item.setFlags(qt.Qt.ItemIsDragEnabled | qt.Qt.ItemIsEnabled | qt.Qt.ItemIsSelectable)
            button = LodTriStateButton(parent=self, has_camera=has_camera)
            value = cmds.getAttr("%s.instancedGroup[%d].displayType" % (self.node, group))
            button.set_index(value)
            button.state_changed.connect(partial(self.objs_widget.set_display_type, group, button))
            self.camera_has_changed.connect(button.camera_updated)
            self.objs_widget.setItemWidget(group_item, 1, CenterWidget(self, button))
            group_item.setText(0, "%d: %s" % (group, group_item_name))
            group_item.setIcon(0, qt.QIcon(MASH_REPRO_ICONS.vertical_drag()))
            if index == group:
                group_item.setSelected(True)

        # disable the proxy widget id there is no input objects
        self.proxy_widget.setDisabled(self.objs_widget.topLevelItemCount() == 0)

        # select the first one if there is no selected items
        if  len(self.objs_widget.selectedItems() or []) == 0:
            for i in range(self.objs_widget.topLevelItemCount()):
                item = self.objs_widget.topLevelItem(i)
                item.setSelected(True)
                id = int(item.text(0).split(':')[0])
                self.update_proxies(id)
                break

        self._disable_object_tree_buttons()

    def _disable_object_tree_buttons(self):
        has_camera = False
        if cmds.objExists(self.node):
            cam_connections = cmds.listConnections("%s.cameraMatrix" % self.node) or []
            if len(cam_connections) > 0:
                has_camera = cmds.objExists(cam_connections[0])


        # disable button
        for i in range(self.objs_widget.topLevelItemCount()):
            item = self.objs_widget.topLevelItem(i)
            id = int(item.text(0).split(':')[0])
            num_groups = cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (self.node, id), mi=True) or []
            center_widget = self.objs_widget.itemWidget(item, 1)
            if center_widget:
                button = center_widget.widget
                button.set_disabled(len(num_groups) == 0)
                if (len(num_groups) == 0):
                    button.set_index(0)
                    self.objs_widget.set_display_type(id, button)
                elif not has_camera and button.index == 2:
                    button.set_index(1)

    def update_data(self, node, force=False):
        """ Update the ui data """
        # This global variable is used to check if a main event happend
        # For example a new scene is created or a scene is opened, this force to refresh
        # the aetemplate widget.

        global SCENE_OPENED
        if SCENE_OPENED:
            self.set_node(node)
            self.update_ui()
            SCENE_OPENED = False

        # If the user select another repro node this refresh the ui with the right data
        if node != self.node or force:
            self.set_node(node)
            self.update_ui()


def build_qt_widget(lay, node):
    """ Build the Repro AETemplate """
    widget = AEMASH_ReproTemplate(node)
    ptr = mui.MQtUtil.findLayout(lay)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        maya_layout.addWidget(widget)

def update_qt_widget(layout, node):
    """ Update the Repro AETemplate """
    ptr = mui.MQtUtil.findLayout(layout)
    if ptr is not None:
        maya_widget = wrapInstance(int(ptr), qt.QWidget)
        maya_layout = maya_widget.layout()
        for c in range(maya_layout.count()):
            widget = maya_layout.itemAt(c).widget()
            if isinstance(widget, AEMASH_ReproTemplate):
                widget.update_data(node)
                break

def get_maya_window():
    ptr = mui.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(int(ptr), qt.QMainWindow)

def refresh_all_aetemplates(force=False):
    """ Refresh all the repro aetemplates"""
    widgets = get_maya_window().findChildren(AEMASH_ReproTemplate) or []
    for widget in widgets:
        global SCENE_OPENED
        SCENE_OPENED = True
        widget.update_data(widget.node, force=force)
        SCENE_OPENED = False

def refresh_camera_aetemplates(node, camera):
    """ Refresh camera attr repro aetemplates"""
    widgets = get_maya_window().findChildren(AEMASH_ReproTemplate) or []
    for widget in widgets:
        if widget.node == node:
            widget.camera_changed(camera)

def refresh_all_nodes_and_templates():
    nodes = cmds.ls(type="MASH_Repro")

    groups_to_delete = []
    proxies_to_delete = []

    for n in nodes:
        group_ids = cmds.getAttr("%s.instancedGroup" % n, mi=True) or []
        for g_id in sorted(group_ids, reverse=True):
            connections = cmds.listConnections("%s.instancedGroup[%d].groupMessage" % (n, g_id), s=1) or []
            if not connections:
                groups_to_delete.append((n, g_id))
                continue

            p_ids = cmds.getAttr("%s.instancedGroup[%d].proxyGroup" % (n, g_id), mi=True) or []
            for p_id in sorted(p_ids, reverse=True):
                connections = cmds.listConnections("%s.instancedGroup[%d].proxyGroup[%d].proxyGroupMessage" % (n, g_id, p_id), s=1) or []
                if not connections:
                    proxies_to_delete.append((n, g_id, p_id))
                    continue

    if groups_to_delete or proxies_to_delete:
        cmds.undoInfo(ock=True)
        for p in proxies_to_delete:
            cmds.removeMultiInstance("%s.instancedGroup[%d].proxyGroup[%d]" % (p[0], p[1], p[2]), b=True)

        for g in groups_to_delete:
            cmds.removeMultiInstance("%s.instancedGroup[%d]" % (g[0], g[1]), b=True)

        refresh_all_aetemplates(force=True)
        cmds.undoInfo(cck=True)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
