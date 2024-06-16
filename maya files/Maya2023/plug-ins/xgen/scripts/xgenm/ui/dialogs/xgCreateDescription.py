# Copyright (C) 1997-2013 Autodesk, Inc., and/or its licensors.
# All rights reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Autodesk, Inc. ("Autodesk") and/or its licensors,
# which is protected by U.S. and Canadian federal copyright law and by
# international treaties.
#
# The Data is provided for use exclusively by You. You have the right to use,
# modify, and incorporate this Data into other products for purposes authorized 
# by the Autodesk software license agreement, without fee.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. AUTODESK
# DOES NOT MAKE AND HEREBY DISCLAIMS ANY EXPRESS OR IMPLIED WARRANTIES
# INCLUDING, BUT NOT LIMITED TO, THE WARRANTIES OF NON-INFRINGEMENT,
# MERCHANTABILITY OR FITNESS FOR A PARTICULAR PURPOSE, OR ARISING FROM A COURSE 
# OF DEALING, USAGE, OR TRADE PRACTICE. IN NO EVENT WILL AUTODESK AND/OR ITS
# LICENSORS BE LIABLE FOR ANY LOST REVENUES, DATA, OR PROFITS, OR SPECIAL,
# DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES, EVEN IF AUTODESK AND/OR ITS
# LICENSORS HAS BEEN ADVISED OF THE POSSIBILITY OR PROBABILITY OF SUCH DAMAGES.
import maya
maya.utils.loadStringResourcesForModule(__name__)


##
# @file xgCreateDescription.py
# @brief Contains the Create Description UI.

from builtins import range
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
import xgenm as xg
import xgenm.xgGlobal as xgg
import xgenm.xgLog as xglog
if xgg.Maya:
    import maya.cmds as cmds
    import maya.mel as mel
    import maya
    import maya.utils as utils

from xgenm.ui.util.xgUtil import *
from xgenm.ui.util.xgComboBox import _ComboBoxUI
import xgenm.xgUtil as xgutil
import string
import os

RB_INDEX_GROOMABLE_SPLINE = 1
RB_INDEX_GROOMING = 2
RB_INDEX_BYATTRIBUTE = 1
RB_INDEX_GENRANDOM = 0

def _createDescription(dialog):
    """Create the new description with optional patch binding."""

    try:
        success = False

        if ( dialog.getPalette()=="" or dialog.getDescription()=="" ):
            return

        if xgg.Maya:
            cmds.undoInfo( openChunk=True, cn='CreateDescription' )
        
        name = xg.createBindDescription(    dialog.getPalette(), 
                                            dialog.getDescription(),
                                            dialog.getPrimitive(), 
                                            dialog.getGenerator(),
                                            dialog.getRenderer(), 
                                            dialog.getMethod(), 
                                            dialog.getSetupForGroom() )

        xg.ui.createDescriptionEditor(False)

        if name:
            if xgg.Maya:
                if dialog.getSetupForGroom():
                    #setup the igroom UI
                    igdesc = xg.igActivateDescription( name )
                    cmds.setAttr( igdesc + '.density', 1 )
                    xg.igSetDescriptionVisibility( True )

                    #sync xgen description with igroom ptx files
                    xg.igSyncMaps( name )

                    xglog.XGTip(maya.stringTable['y_xgenm_ui_dialogs_xgCreateDescription.kGroomingTip' ] )
                elif dialog.getMethod() == "Guides":
                    xglog.XGTip(maya.stringTable['y_xgenm_ui_dialogs_xgCreateDescription.kGuideToolTip' ] )

                if xgg.DescriptionEditor and xgg.DescriptionEditor.autoCreateMR and mel.eval('exists "xgmr"'):
                    try:
                        cmds.xgmr( sgs=True, description=name, palette=dialog.getPalette() )
                        cmds.xgmr( applyShader="hair", description=name, palette=dialog.getPalette() )
                    except:
                        pass              
            success = True
    except:
        cmds.undoInfo( closeChunk=True )
        cmds.flushUndo()
        import sys
        print(sys.exc_info()[1])
        raise
    finally:
        if success and xgg.Maya:
            setPlayblast = True

            if dialog.getSetupForGroom():
                # jump to the grooming tab
                xgg.DescriptionEditor.activateTab( maya.stringTable['y_xgenm_ui_dialogs_xgCreateDescription.kGrooming' ] )
                # no playblast with grooming 
                setPlayblast = False
            else:
                # jump to the primitives tab
                xgg.DescriptionEditor.activateTab( maya.stringTable['y_xgenm_ui_dialogs_xgCreateDescription.kPrimitives' ] )
                # always set playblast to on for other descriptions
                setPlayblast = True

            # note 1: onRefreshPreviewAuto toggles the value of play blast so we need to invert it before calling
            # note 2: onRefreshPreviewAuto sets the play blast icon and installs an expression for playblast to work properly (via xgmAddExpression)
            # note 3: defer the undo chunk so xgmAddExpression can be part of it
            script = 'import maya.cmds as cmds;xgg.DescriptionEditor.setPlayblast( %d );xgg.DescriptionEditor.onRefreshPreviewAuto();xgg.DescriptionEditor.setCurrentDescription("%s");cmds.undoInfo( closeChunk=True );' % (not setPlayblast,name)
            executeDeferred( script )

class CreateDescriptionUI(QDialog):
    """A dialog for creating new descriptions and palettes.

    This provides a list of available palettes with the ability to
    specify a new palette name. The description name is filled in
    automatically. A few predefined types are provided to ease creation.
    """
 
    def __init__(self,parent):
        QDialog.__init__(self,parent)

        self._creating = False

        self.radioValues = ["Spline","Spline","Archive","Sphere", "Card"]

        self.primImagesValues = ["descript_spline.png","descript_iGroom.png","descript_custom.png","descript_sphere.png", "descript_card.png"]

        self.randomImagesValues = ["descript_splineRandom.png","descript_iGroom.png","descript_customRandom.png","descript_sphereRandom.png", "descript_cardRandom.png"]
        self.uniformImagesValues = ["descript_splineUniform.png","descript_iGroom.png","descript_customUniform.png","descript_sphereUniform.png", "descript_cardUniform.png"]
        self.specifyImagesValues = ["descript_splineSpecify.png","descript_iGroom.png","descript_customSpecify.png","descript_sphereSpecify.png", "descript_cardSpecify.png"]        

        self.guidesImagesValues = ["descript_splineGuides.png","descript_iGroom.png","descript_customGuides.png","descript_sphereGuides.png", "descript_cardGuides.png"]
        self.expressImagesValues = ["descript_splineExpressn.png","descript_iGroom.png","descript_customExpressn.png","descript_sphereExpressn.png", "descript_cardExpressn.png"]

        self.setWindowTitle(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateXgenDescription'  ])
        self.setSizeGripEnabled(True)
        layout = QVBoxLayout()
        layout.setContentsMargins(DpiScale(24),DpiScale(16),DpiScale(24),DpiScale(16))
        self.setLayout(layout)

        # get info on folders
        (self.descFolderNames,self.descPathMaps) = xg.descriptionFolderNames( )        
        (self.palFolderNames,self.palPathMaps) = xg.paletteFolderNames( )               

        # setup the dialog widgets
        self.addDescription()
        self.addPalette()
        self.addPrim()
        self.addGen()
        self.addMethod()
        # set default to By Attribute
        self.onTogglePrimitiveSplineRadio(False)
        self.updateMethodImages()

        self.updateMethodImages()

        layout.addSpacing(DpiScale(10))
        self.addButtons()

        # populate palette list and setup radio buttons
        palettes = xg.palettes()
        if palettes:
            for pal in palettes:
                if not pal.startswith("XG_RENDER_"):
                    self.palettes.addItem(pal)

        if self.palettes.count() > 0:
            self.addDescriptionToRadio.setChecked(True)
            self.newPaletteName.setEnabled(False)
            self.setCurrentPalette( xgg.DescriptionEditor.currentPalette() )        
        else:
            self.addDescriptionToRadio.setEnabled(False)
            self.createNewPaletteRadio.setChecked(True)

        # set the  palette text edit
        palName = xg.buildPaletteName( str(self.newPaletteName.text()), self.loadedPalettes(), self.palFolderNames )
        self.newPaletteName.setText( palName )

        # set description text edit
        descName = xg.buildDescriptionName( self.getDescription(), self.loadedDescriptions(palName), self.descFolderNames )
        self.description.setText( descName )

    def _createRowLayout(self):
        row = QWidget()
        hbox = QHBoxLayout()
        hbox.setContentsMargins(DpiScale(0),DpiScale(0),DpiScale(0),DpiScale(0))
        row.setLayout(hbox)
        self.layout().addWidget(row)
        return hbox

    def _createVerticalGroupLayout(self, parentRowLayout ):
        radioButtonGroupWidget = QWidget()
        radioButtonGroup = QVBoxLayout()
        radioButtonGroup.setContentsMargins(DpiScale(0),DpiScale(0),DpiScale(0),DpiScale(0))
        radioButtonGroupWidget.setLayout(radioButtonGroup)
        parentRowLayout.layout().addWidget( radioButtonGroupWidget )
        return radioButtonGroup

    def _createGridGroupLayout(self, parent):
        gridGroupWidget = QWidget()
        gridGroupLayout = QGridLayout()
        gridGroupWidget.setLayout(gridGroupLayout)
        parent.addWidget(gridGroupWidget)
        return gridGroupLayout

    def _addSectionLabel(self,text):
        self.layout().addSpacing(DpiScale(10))
        label = QLabel("<b>"+text+"</b>")
        self.layout().addWidget(label)
        return label

    def _createRadioButtonArray(self,rowLayout,texts):
        radioButtonGroup = self._createVerticalGroupLayout(rowLayout)

        buttonList = []
        for index, item in enumerate(texts):
            buttonList.append( QRadioButton(texts[index]) )
            radioButtonGroup.addWidget(buttonList[index])
        buttonList[0].setChecked(True)
        return buttonList   

    def _createPreviewImageArea(self,rowLayout):
        ''' Create QFrame and a QLabel to show an image '''

        # QLabel to hold the image
        imageWidget = QLabel()

        # QFrame layout
        imageLayout = QVBoxLayout()
        imageLayout.setSpacing(DpiScale(0))
        imageLayout.setContentsMargins(DpiScale(0),DpiScale(0),DpiScale(0),DpiScale(0))
        imageLayout.addWidget(imageWidget)

        # QFrame to hold the QLabel image widget
        frame = QFrame()
        frame.setFrameShadow(QFrame.Plain)
        frame.setFrameShape(QFrame.StyledPanel)        
        frame.setFixedSize(DpiScale(72),DpiScale(72))
        frame.setLayout(imageLayout)

        # Add to the parent layout
        rowLayout.addWidget(frame)
        return imageWidget

    def addPalette(self):
        self.collectionSectionLabel = self._addSectionLabel(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kEachDescriptionMustBeStoredInACollection'  ])

        rowLayout = self._createRowLayout()
        radioButtonGroup = self._createVerticalGroupLayout(rowLayout)
        
        self.addDescriptionToRadio = QRadioButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kAddDescriptionToExistingCollection'  ])
        self.addDescriptionToRadio.connect(self.addDescriptionToRadio, QtCore.SIGNAL('clicked()'), self.onClickAddDescriptionToRadio)
        radioButtonGroup.addWidget(self.addDescriptionToRadio)

        self.createNewPaletteRadio = QRadioButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateNewCollectionNamed'  ])
        self.createNewPaletteRadio.connect(self.createNewPaletteRadio, QtCore.SIGNAL('clicked()'), self.onClickCreateNewPaletteRadio)
        radioButtonGroup.addWidget(self.createNewPaletteRadio)

        paletteNamesGroup = self._createVerticalGroupLayout(rowLayout)

        self.palettes = _ComboBoxUI()
        paletteNamesGroup.addWidget(self.palettes)
        
        self.newPaletteName = QLineEdit()
        rx = QRegExp("[A-Za-z]+[A-Za-z0-9_:]*")
        self.newPaletteName.setValidator(QRegExpValidator(rx,self))
        paletteNamesGroup.addWidget(self.newPaletteName)

    def setCurrentPalette(self,palette):
        for i in range(self.palettes.count()):
            pal = self.palettes.itemText(i)
            if pal == palette:
                self.palettes.setCurrentIndex(i)
                break
            i+=1
        
    def onClickCreateNewPaletteRadio(self):
        self.newPaletteName.setEnabled(True)
        self.palettes.setEnabled(False)

    def onClickAddDescriptionToRadio(self):
        self.newPaletteName.setEnabled(False)
        self.palettes.setEnabled(True)

    def addDescription(self):
        hbox = self._createRowLayout()
        label = QLabel(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kNewDescriptionName'  ])
        label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        label.setIndent(DpiScale(10))
        hbox.addWidget(label)
        self.description = QLineEdit()
        rx = QRegExp("[A-Za-z]+[A-Za-z0-9_]*")
        self.description.setValidator(QRegExpValidator(rx,self))
        hbox.addWidget(self.description)

    def addPrim(self):
        self._addSectionLabel(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kWhatKindOfPrimitivesAreMadeByThisDescription'  ])
        rowLayout = self._createRowLayout()

        radioTexts = [maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kSplinesDescription'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kGroomableSplinesDescription'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCustomGeometryArchives'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kSpheresDescription'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCardsDescription'  ]]

        self.primTypeRadioButtons = self._createRadioButtonArray(rowLayout,radioTexts)

        splineRadio = self.primTypeRadioButtons[RB_INDEX_GROOMABLE_SPLINE]
        splineRadio.toggled.connect(self.onTogglePrimitiveSplineRadio)

        self.primTypeImage = self._createPreviewImageArea(rowLayout)        
        for i in range(len(radioTexts)):
            self.primTypeRadioButtons[i].clicked.connect(self.updatePrimImages)
            self.primTypeRadioButtons[i].clicked.connect(self.updateGenImages)
            self.primTypeRadioButtons[i].clicked.connect(self.updateMethodImages)

        self.updatePrimImages()            

    def updatePrimImages(self):

        imageName = self.primImagesValues[self.getPrimitiveIndex()]
        self.primTypeImage.setPixmap(CreateIcon(imageName).pixmap(DpiScale(72),DpiScale(72)))

    def onTogglePrimitiveSplineRadio(self,isGroomable):
        # goomable spline: disabled everything except Random method and groomable tools
        # enable Grooming option for groomable splines only  

        for index, item in enumerate(self.groomRadioButtons):
            if index == RB_INDEX_GROOMING:
                item.setEnabled(isGroomable)
            else:
                item.setEnabled(False if isGroomable else True)

        for index, item in enumerate(self.generatorRadioButtons):
            if index != RB_INDEX_GENRANDOM:
                item.setEnabled(not isGroomable)                
                
        if isGroomable:
            self.groomRadioButtons[RB_INDEX_GROOMING].setChecked(True)
            self.generatorRadioButtons[RB_INDEX_GENRANDOM].setChecked(True)
        else:
            self.groomRadioButtons[RB_INDEX_BYATTRIBUTE].setChecked(True)

    def addGen(self):
        self._addSectionLabel(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kGenerateThePrimitives'  ])
        rowLayout = self._createRowLayout()

        radioTexts = [maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kRandomlyAcrossTheSurface'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kInUniformRowsAndColumns'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kAtPointsYouSpecify'  ]]
        
        self.generatorRadioButtons = self._createRadioButtonArray(rowLayout,radioTexts)

        self.generatorImage = self._createPreviewImageArea(rowLayout)        
        for i in range(len(radioTexts)):
            self.generatorRadioButtons[i].clicked.connect(self.updateGenImages)

        self.updateGenImages()            

    def updateGenImages(self):

        imageName = self.randomImagesValues[self.getPrimitiveIndex()]
        if self.getGenerator() == "Uniform":
            imageName = self.uniformImagesValues[self.getPrimitiveIndex()]
        elif self.getGenerator() == "Point":
            imageName = self.specifyImagesValues[self.getPrimitiveIndex()]

        self.generatorImage.setPixmap(CreateIcon(imageName).pixmap(DpiScale(72),DpiScale(72)))
                      
    def addMethod(self):
        self._addSectionLabel(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kGroomThePrimitivesBy'  ])
        rowLayout = self._createRowLayout()

        radioTexts = [maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kPlacingGuides'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kUsingAttributesControlledByExpressions'  ],
                      maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kUsingGroomingTools'  ]]
        
        self.groomRadioButtons = self._createRadioButtonArray(rowLayout,radioTexts)
        self.methodImage = self._createPreviewImageArea(rowLayout)        
        for i in range(len(radioTexts)):
            self.groomRadioButtons[i].clicked.connect(self.updateMethodImages)

        self.updateMethodImages()            

    def updateMethodImages(self):

        imageName = self.expressImagesValues[self.getPrimitiveIndex()]
        if self.getMethod() == "Guides":
            imageName = self.guidesImagesValues[self.getPrimitiveIndex()]

        self.methodImage.setPixmap(CreateIcon(imageName).pixmap(DpiScale(72),DpiScale(72)))

    def addButtons(self):
        row = QWidget()
        hbox = QHBoxLayout()
        QLayoutItem.setAlignment(hbox, QtCore.Qt.AlignRight)
        hbox.setSpacing(DpiScale(3))
        hbox.setContentsMargins(DpiScale(1),DpiScale(1),DpiScale(1),DpiScale(1))
        self.createButton = QPushButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreate'  ])
        self.createButton.setFixedWidth(DpiScale(110))
        self.createButton.setAutoRepeat(False)
        self.connect(self.createButton, QtCore.SIGNAL("clicked()"), self.createCB)
        self.createButton.setDefault(True)
        hbox.addWidget(self.createButton)
        self.cancelButton = QPushButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCancel'  ])
        self.cancelButton.setFixedWidth(DpiScale(110))
        self.cancelButton.setAutoRepeat(False)
        self.connect(self.cancelButton, QtCore.SIGNAL("clicked()"), self.reject)
        hbox.addWidget(self.cancelButton)
        row.setLayout(hbox)
        self.layout().addWidget(row)

    def loadedDescriptions( self, palName ):
        """ return list of all loaded description names in xgen """

        # get all descriptions in the scene
        names = list(xg.descriptions( ))

        # we want to make sure there is no clash with the palette 
        names.append(palName)

        return names

    def loadedPalettes(self):
        return [str(self.palettes.itemText(i)) for i in range(self.palettes.count())]

    def onCollidePalette( uiParent, newPalette, palette, palettePath ):
        """
        Called by xgen.validateDescription when a new palette collides with an existing one. Gives user a 
        choice to create the new one or overwrite current.
        """
        if not uiParent:
            raise
        title = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateXgenDescriptionOverwrite'  ]
        text = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCollectionAlreadyExistsOnDisk'  ] % (palette,palettePath)
        mbox = QMessageBox( QMessageBox.NoIcon, title, text, QMessageBox.NoButton, uiParent )
        newPalNameBtn = QPushButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateInstead'  ] % newPalette)
        mbox.addButton( newPalNameBtn, QMessageBox.YesRole )
        overPalNameBtn = QPushButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kOverwrite'  ] % palette)
        mbox.addButton( overPalNameBtn, QMessageBox.AcceptRole )
        mbox.addButton( QMessageBox.Cancel )
        mbox.setDefaultButton( newPalNameBtn )
        mbox.exec_()
        if mbox.clickedButton() == newPalNameBtn:
            validPalette = newPalette
        elif mbox.clickedButton() == overPalNameBtn:
            validPalette = palette
        else:
            return (False, '')
        return (True,validPalette)

    def onCollideDescription( uiParent, newDesc, desc, descPath ):
        """
        Called by xgen.validateDescription when a new description collides with an existing one. Gives user a 
        choice to create the new one or overwrite current.
        """
        if not uiParent:
            raise
        title = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateXgenDescriptionDescriptionClash'  ]
        text = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kDescriptionAlreadyExistsOnDisk'  ] % (desc, descPath )                
        mbox = QMessageBox( QMessageBox.NoIcon, title, text, QMessageBox.NoButton, uiParent )
        newDescNameBtn = QPushButton(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateInstead2'  ] % newDesc)
        mbox.addButton( newDescNameBtn, QMessageBox.YesRole )
        mbox.addButton( QMessageBox.Cancel )
        mbox.setDefaultButton( newDescNameBtn )
        mbox.exec_()
        if mbox.clickedButton() == newDescNameBtn:
            validDesc = newDesc
        else:
            return (False, '', '')
        return (True, validDesc)

    def createCB(self):
        if self._creating:
            return
        self._creating = True

        action = xg.ADD_TO_NEW_PALETTE if self.createNewPaletteRadio.isChecked() else xg.ADD_TO_EXISTING_PALETTE
        palInfo = (self.getPalette(), self.loadedPalettes(), self.palFolderNames, self.palPathMaps, CreateDescriptionUI.onCollidePalette)
        descInfo = (self.getDescription(), self.loadedDescriptions(self.getPalette()), self.descFolderNames, self.descPathMaps, CreateDescriptionUI.onCollideDescription)	      

        (result,descName,palName) = xg.validateDescription( action, palInfo, descInfo, self )
        if result:
            self.description.setText( descName )
            if action == xg.ADD_TO_NEW_PALETTE:
                self.newPaletteName.setText( palName )
            try:
                _createDescription(self)
                self.accept()
            except:
                xglog.XGError( maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kErrorCreatingDescription'  ] % descName )
                pass
                self.reject()
        
    def getPalette(self):
        if self.addDescriptionToRadio.isChecked():
            return str(self.palettes.currentText())
        else:
            return str(self.newPaletteName.text())

    def getDescription(self):
        return str(self.description.text())

    def getPrimitive(self):
        for i in range(len(self.radioValues)):
            if self.primTypeRadioButtons[i].isChecked():
                return self.radioValues[i]

    def getPrimitiveIndex(self):
        for i in range(len(self.radioValues)):
            if self.primTypeRadioButtons[i].isChecked():
                return i

    def getGenerator(self):
        radioValues = ["Random", "Uniform", "Point"]
        for i in range((len(radioValues))):
            if self.generatorRadioButtons[i].isChecked():
                return radioValues[i]
        
    def getRenderer(self):
        return "Renderman"

    def getMethod(self):
        radioValues = ["Guides","Attribute", "Attribute"]
        for i in range((len(radioValues))):
            if self.groomRadioButtons[i].isChecked():
                return radioValues[i]

    def getSetupForGroom(self):
        return self.primTypeRadioButtons[RB_INDEX_GROOMABLE_SPLINE].isChecked()

def createDescription():
    """Function to create a description using a dialog.

    This provides a simple dialog to accept the various parameters required
    for creating a new description.
    """
    if xgg.Maya:

        # check if selection is appropriate (we require to bind to selection in Maya)
        geometries = cmds.ls(dag=True,type=['mesh','nurbsSurface'],sl=True)
        faces = cmds.filterExpand(selectionMask=34)
        if len(geometries) == 0 and faces == None:
            xglog.XGTip(maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kPleaseSelectAPolygonSurfaceTip'  ] )
            return

        # check for namespace issues
        selNSpaces = xg.selectionNameSpaces()        
        if len(selNSpaces) > 1:            
            title = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kCreateXgenDescriptionNamespace'  ]
            text = maya.stringTable[ 'y_xgenm_ui_dialogs_xgCreateDescription.kNamespaceIssueError'  ]
            mbox = QMessageBox(QMessageBox.NoIcon, title, text )
            mbox.exec_()
            return 

    dialog = CreateDescriptionUI(xgg.DescriptionEditor)

    result = dialog.exec_()
    
    return result
