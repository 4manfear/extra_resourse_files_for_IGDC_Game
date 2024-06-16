import maya.app.flux.ae.api as aeAPI
import maya.app.flux.attrUtils as attrUtils
import maya.mel as mel

DEBUG = False

def register():
    aeAPI.registerTemplate('MASHAET.MASH_Distribute.AETemplate', 'MASH_Distribute')
    aeAPI.registerTemplate('MASHAET.MASH_Repro.AETemplate', 'MASH_Repro')

    names = {
        'MASH_BaseNode':{
            'Envelope':                 res('kStrength'),
            'randEnvelope':             res('kRandStrength'),
            'StepEnvelope':             res('kStepStrength'),
            'mColour':                  res('kStrengthMap'),
            'mapDirection':             res('kMapProjAxis')
        },
        'MASH_Distribute':{
            'pointCount':               res('kNumberOfPoints'),
            'arrangement':              res('kDistType'),
            'centerLinearDistribution': res('kCenterDistribution'),
            'amplitudeX':               res('kDistanceX'),
            'amplitudeY':               res('kDistanceY'),
            'amplitudeZ':               res('kDistanceZ'),
            'rotateX':                  res('kRotateX'),
            'rotateY':                  res('kRotateY'),
            'rotateZ':                  res('kRotateZ'),
            'scaleX':                   res('kScaleX'),
            'scaleY':                   res('kScaleY'),
            'scaleZ':                   res('kScaleZ'),
            'offset':                   res('kDistOffset'),
            'radialRadius':             res('kRadius'),
            'radialAngle':              res('kAngleDegrees'),
            'amplitudeZ':               res('kZOffset'),
            'modelAxis':                res('kRadialAxis'),
            'calcRotation':             res('kCalculateRotation'),
            'ignoreRamps':              res('kIgnoreRamps'),
            'sphericalAngleX':          res('kAngleX'),
            'sphericalAngleY':          res('kAngleY'),
            'radialRadius':             res('kRadius'),
            'noiseFrequency':           res('kAnimationSpeed'),
            'animationTime':            res('kAnimationTime'),
            'ignoreRamps':              res('kIgnoreRamps'),
            'meshType':                 res('kMethod'),
            'distanceAlongNormal':      res('kPushAlingNormal'),
            'useUpVector':              res('kUseUpVector'),
            'upVector':                 res('kUpVector'),
            'calcRotation':             res('kCalculateRotation'),
            'floodMesh':                res('kFloodMesh'),
            'ignoreRamps':              res('kIgnoreRamps'),
            'areaBasedScatter':         res('kScatterUsesArea'),
            'useFaceScale':             res('kEnableScaling'),
            'faceScaleMultiplier':      res('kScaleMultiplier'),
            'edgeAlignment':            res('kEdgeAlignment'),
            'voxelDensity':             res('kVoxelSize'),
            'maxVoxels':                res('kMaxVoxels'),
            'voxelMode':                res('kFillWithVoxels'),
            'centerLinearDistribution': res('kCenterDistribution'),
            'gridAmplitudeX':           res('kDistanceX'),
            'gridAmplitudeY':           res('kDistanceY'),
            'gridAmplitudeZ':           res('kDistanceZ'),
            'gridx':                    res('kGridX'),
            'gridy':                    res('kGridY'),
            'gridz':                    res('kGridZ'),
            'enableMain':               res('kMain'),
            'enableLeaf':               res('kLeaf'),
            'enableFlowers':            res('kFlowers'),
            'floodMesh':                res('kFloodMesh'),
            'useFaceScale':             res('kEnableScaling'),
            'enablePfxRotation':        res('kCalculateRotation'),
            'pfxMode':                  res('kPfxMode'),
            'strengthPosition':         res('kPosition'),
            'strengthRotation':         res('kRotation'),
            'strengthScale':            res('kScale'),
            'zeroScale':                res('kZeroScaleDist'),
            'volumeShape':              res('kVolumeShape'),
            'volumeSize':               res('kVolumeSize'),
            'sphericalBias':            res('kSphericalBias'),
            'batchRenderMultiplier':    res('kBatchMult')
        },
        'MASH_Repro':{
            'setUVs'                    :res('kUVs'),
            'setColors'                 :res('kCPV'),
            'normalMode'                :res('kNormals'),
            'positionAttributeName'     :res('kPosition'),
            'rotationAttributeName'     :res('kRotation'),
            'scaleAttributeName'        :res('kScale'),
            'objectIndexAttributeName'  :res('kObjectIndex'),
            'visibilityAttributeName'   :res('kVisibility'),
            'colorAttributeName'        :res('kColor'),
            'uvTileAttributeName'       :res('kUvTile'),
            'animatedAttributeName'     :res('kAnimated'),
            'frameAttributeName'        :res('kFrame')
        }
    }
    if DEBUG:
        attrUtils.checkNiceNames(names)
    attrUtils.registerNiceNames(names)

def res(name):
    return mel.eval('getPluginResource("MASH", "%s")' % name)
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
