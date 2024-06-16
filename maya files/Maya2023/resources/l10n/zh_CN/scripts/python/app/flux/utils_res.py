import maya

identifier = 'maya.app.flux.utils'
resources = {
    'kWhite':            u'白色',
    'kRed':              u'红',
    'kBlue':             u'蓝',
    'kGrey':             u'灰色',
    'kOrange':           u'橙色',
    'kGreen':            u'绿',
    'kYellow':           u'黄色',
    'kPurple':           u'紫色',
    'kLabelColour':      u'标签颜色',
    'kAccepting':        u'接受',
    'kChooseExport':     u'选择文件以导出到:',
    'kExportCanceled':   u'导出已取消',
    'kExportedTo':       u'已导出到 ',
    'kChooseImport': u'从以下位置选择要导入的文件:',
    'kImportCanceled': u'导入已取消',
    'kImportFailed': u'无法导入: ',
    'kOpeningFileFailed': u'打开文件失败。',
    'kInvalidImportFile': u'无效的导入文件',
    'kMASH_delete_error': u'删除 MASH 节点: 找不到属性',
    'kMASH_delete_error2': u'删除 MASH 节点: 找不到解算器',
    'kMASH_delete_error3': u'删除 MASH 网络时出错',
    'kBounce': u'反弹',
    'kFriction': u'摩擦力',
    'kDamping': u'阻尼',
    'kMass': u'质量',
    'kCollisionShape': u'碰撞形状',
    'kCollisionShapeScale': u'碰撞形状比例',
    'kCollisionContactMaskLayers': u'碰撞接触遮罩层',
    'kCollisionMaskLayers': u'碰撞遮罩层',
    'kCollisionGroupLayers': u'碰撞组层',
    'kSelectSolver': u'请选择一个解算器。',
    'kDynamicsDisabled': u'已对缓存网络禁用动力学。',
    'kCachingComplete': u'缓存完成。',
    'kUVSpaceMode': u'UV 空间模式需要一个三角化的输入网格',
    'kFitToSelection': u'适应选择',
    'kLoad': u'加载',
    'kSaveAs': u'另存为',
    'kAverageIntensity': u'平均强度:',
    'kAverageTemperature': u'平均温度:',
    'kParentLightsUnder': u'将灯光设置为下面的子对象 ',

    'kSearchMode': u'搜索',
    'kSelectMode': u'选择',
    'kSearchModeSwitch': u'搜索模式: 在搜索、选择、MEL 和 Python 模式之间切换(Ctrl+F)',
    'kSearchModeHint': u'搜索工具和命令',
    'kSelectModeHint': u'搜索场景对象',
    'kMELModeHint': u'搜索并运行 MEL 命令',
    'kPythonModeHint': u'搜索并运行 Python 命令',
    'kTTF_Extract': u'TTF 提取',
    'kExportMayaCMDS': u'导出 maya.cmds 名称',
    'kExportMayaTools': u'导出工具名称',
    'kExportMayaMenus': u'导出主菜单项(TTF)',
    'kSearchFilterTagMgmt': u'搜索过滤标记管理',
    'kStartWithLastCommand': u'使用上一命令启动',
    'kTTFHiddenHistory': u'隐藏历史',
    'kTagColor': u'标记颜色',
    'kData': u'数据',
    'kTags': u'标记',
    'kChooseDataFile': u'选择数据文件:',
    'kNewTag': u'新建标记',
    'kRenameTag': u'重命名标记',
    'kDeleteTag': u'删除标记',
    'kDelete': u'删除',
    'kImportData': u'导入数据',
    'kEnterTag': u'输入标记',
    'kPreferences': u'首选项',
    'kSearchPreferences': u'首选项...',
    'kManageFilterTags': u'管理过滤标记...',
    'kOpenExtractWindow': u'打开提取窗口',
    'kCommand': u'命令',
    'kChooseMenusExport': u'选择菜单的导出位置:',
    'kChooseNamesExport': u'选择名称的导出位置:',
    'kFilter': u'过滤',
    'kSearchFilters': u'搜索过滤器',
    'kLoading': u'正在加载...',
    'kOnlineDocumentation': u'联机文档',
    'kTTF_Menu': u'菜单: ',
    'kTTF_Tags': u'标记: ',
    'kTTF_Synonyms': u'同义词: ',

    'kNew': u'新建',
    'kSelectSVG': u'选择要操纵的 SVG 路径',
    'kSVGClipboardError': u'无法粘贴 SVG: 剪贴板为空',
    'kNoValidSVG': u'无法粘贴 SVG: 找不到有效的 SVG 文件',
    'kMaterialAssignmentFailure': u'无法指定材质。',
    'kBevelProfile': u'倒角剖面',
    'kConnectToMASH': u'连接到 MASH',
    'kAddDynamics': u'添加动力学',
    'kLocalRotatePivot': u'局部旋转枢轴',
    'kLocalScalePivot': u'局部缩放枢轴',

    'kUnsupportedNodeType': u'节点类型不正确',
    'kNotConnected': u'未连接'
}

for key, value in list(resources.items()):
    maya.stringTable['y_%s.%s' % (identifier, key)] = value
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================