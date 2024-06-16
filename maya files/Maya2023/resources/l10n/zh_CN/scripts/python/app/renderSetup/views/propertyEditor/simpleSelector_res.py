import maya

maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kAdd'] = u'添加'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kAddToCollection'] = u'添加到集合'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kBasicSelectorDisplayType'] = u'DAG 和非 DAG 对象'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kBasicSelectorUsage'] = u'旧版对象选择器。选择 DAG 和非 DAG 对象。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kByTypeFilter'] = u'类型'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kCollectionFilters'] = u'集合过滤器'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kCreateExpression'] = u'创建表达式'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kDragDropFilter'] = u'将节点拖动到此处以便按类型过滤'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionSelectTooltipStr'] = u'选择场景中使用该表达式包括的对象。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr'] = u'要填充集合，请使用表达式包括或排除节点，并使用 * 作为通配符。\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr1'] = u'使用空格、逗号或分号分隔表达式。\n不能使用连字符。\n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr10'] = u'C aaa:bbb:ccc:pSphere1\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr11'] = u'D bbb:aaa:pSphere1\n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr12'] = u'也支持递归和非递归搜索的组合。\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr13'] = u'例如:\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr14'] = u'aaa:bbb::pSphere* 将返回节点 B 和 C。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr2'] = u'例如: \n要包括除 RobotB_shader5 以外的所有 RobotA 和 RobotB 着色器:\n\tRobotA_shad* RobotB_shad* -RobotB_shader5 \n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr3'] = u'对每个名称空间使用一个通配符。\n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr4'] = u'例如: \n要包括 livingRoom:couchB: \n\tlivingRoom:c* \n要包括 livingRoom:chairB_v08:chairB:\n\tlivingRoom:*:c*\n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr5'] = u'对于具有许多名称空间的场景，使用 :: 语法来表示递归名称空间搜索。\n\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr6'] = u'例如:\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr7'] = u'aaa::pSphere* 将返回节点 A、B 和 C。\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr8'] = u'A aaa:pSphere1\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kExpressionTooltipStr9'] = u'B aaa:bbb:pSphere1\n'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kFiltersToolTip'] = u'选择一个过滤器以便按节点类型隔离该集合'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kInclude'] = u'包含'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kIncludeAllLightsOption'] = u'每个渲染层默认包含所有灯光'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kIncludeAllLightsOptionStr'] = u'禁用手动添加灯光的选项'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kIncludeHierarchy'] = u'包括层级'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kIncludeHierarchyTooltipStr'] = u'包括所有 DAG 子对象、着色网络和几何体生成器。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kInverse'] = u'反向选择'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kRemove'] = u'移除'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kSelect'] = u'选择'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kSelectAll'] = u'全选'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kStaticAddTooltipStr'] = u'将当前场景选择添加到该集合。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kStaticRemoveTooltipStr'] = u'从该集合移除当前选定的节点。'
maya.stringTable['y_maya_app_renderSetup_views_propertyEditor_simpleSelector.kStaticSelectTooltipStr'] = u'在场景中选择通过该选择包括的节点。'
# ===========================================================================
# Copyright 2022 Autodesk, Inc. All rights reserved.
#
# Use of this software is subject to the terms of the Autodesk license
# agreement provided at the time of installation or download, or which
# otherwise accompanies this software in either electronic or hard copy form.
# ===========================================================================
