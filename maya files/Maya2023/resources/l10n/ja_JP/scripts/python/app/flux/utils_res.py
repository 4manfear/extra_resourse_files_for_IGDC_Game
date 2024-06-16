import maya

identifier = 'maya.app.flux.utils'
resources = {
    'kWhite':            u'白',
    'kRed':              u'赤',
    'kBlue':             u'青',
    'kGrey':             u'グレー',
    'kOrange':           u'オレンジ',
    'kGreen':            u'緑',
    'kYellow':           u'黄',
    'kPurple':           u'紫',
    'kLabelColour':      u'ラベルのカラー',
    'kAccepting':        u'受け入れる',
    'kChooseExport':     u'書き出し先ファイルを選択:',
    'kExportCanceled':   u'書き出しがキャンセルされました',
    'kExportedTo':       u'書き出し先 ',
    'kChooseImport': u'読み込み元ファイルを選択:',
    'kImportCanceled': u'読み込みがキャンセルされました',
    'kImportFailed': u'読み込みに失敗しました: ',
    'kOpeningFileFailed': u'ファイルを開くのに失敗しました。',
    'kInvalidImportFile': u'無効な読み込みファイル',
    'kMASH_delete_error': u'MASH ノードを削除: アトリビュートが見つかりません',
    'kMASH_delete_error2': u'MASH ノードを削除: ソルバが見つかりません',
    'kMASH_delete_error3': u'MASH ネットワークの削除中にエラーが発生しました',
    'kBounce': u'バウンス',
    'kFriction': u'摩擦',
    'kDamping': u'ダンピング',
    'kMass': u'質量',
    'kCollisionShape': u'衝突シェイプ',
    'kCollisionShapeScale': u'衝突シェイプのスケール',
    'kCollisionContactMaskLayers': u'衝突接触マスク レイヤ',
    'kCollisionMaskLayers': u'衝突マスク レイヤ',
    'kCollisionGroupLayers': u'衝突グループ レイヤ',
    'kSelectSolver': u'ソルバを選択してください。',
    'kDynamicsDisabled': u'ダイナミクスは、キャッシュされたネットワークでは無効になっています。',
    'kCachingComplete': u'キャッシングが完成しました。',
    'kUVSpaceMode': u'UV 空間モードには三角化入力メッシュが必要です',
    'kFitToSelection': u'選択項目に合わせる',
    'kLoad': u'ロード',
    'kSaveAs': u'名前を付けて保存',
    'kAverageIntensity': u'平均強度:',
    'kAverageTemperature': u'平均温度:',
    'kParentLightsUnder': u'下にある親ライト ',

    'kSearchMode': u'検索',
    'kSelectMode': u'選択',
    'kSearchModeSwitch': u'検索モード: 検索、選択、MEL、Python の各モードを切り替えます([Ctrl]+[F])',
    'kSearchModeHint': u'検索ツールとコマンド',
    'kSelectModeHint': u'シーン オブジェクトを検索',
    'kMELModeHint': u'MEL コマンドを検索して実行',
    'kPythonModeHint': u'Python コマンドを検索して実行',
    'kTTF_Extract': u'TTF 抽出',
    'kExportMayaCMDS': u'maya.cmds 名を書き出し',
    'kExportMayaTools': u'ツール名を書き出し',
    'kExportMayaMenus': u'メイン メニュー項目を書き出し(TTF)',
    'kSearchFilterTagMgmt': u'検索フィルタ タグの管理',
    'kStartWithLastCommand': u'最後のコマンドを使用して開始',
    'kTTFHiddenHistory': u'非表示の履歴',
    'kTagColor': u'タグの色',
    'kData': u'データ',
    'kTags': u'タグ',
    'kChooseDataFile': u'データ ファイルを選択:',
    'kNewTag': u'新しいタグ',
    'kRenameTag': u'タグの名前を変更',
    'kDeleteTag': u'タグを削除',
    'kDelete': u'削除',
    'kImportData': u'データの読み込み',
    'kEnterTag': u'タグを入力',
    'kPreferences': u'プリファレンス',
    'kSearchPreferences': u'プリファレンス...',
    'kManageFilterTags': u'フィルタ タグを管理...',
    'kOpenExtractWindow': u'[抽出]ウィンドウを開く',
    'kCommand': u'コマンド',
    'kChooseMenusExport': u'メニューの書き出し先を選択:',
    'kChooseNamesExport': u'名前の書き出し先を選択:',
    'kFilter': u'フィルタ',
    'kSearchFilters': u'検索フィルタ',
    'kLoading': u'ロード中...',
    'kOnlineDocumentation': u'オンライン ドキュメント',
    'kTTF_Menu': u'メニュー: ',
    'kTTF_Tags': u'タグ: ',
    'kTTF_Synonyms': u'同義語: ',

    'kNew': u'新規',
    'kSelectSVG': u'操作する SVG パスを選択',
    'kSVGClipboardError': u'SVG を貼り付けられませんでした: クリップボードは空です。',
    'kNoValidSVG': u'SVG を貼り付けられませんでした: 有効な SVG が見つかりませんでした',
    'kMaterialAssignmentFailure': u'マテリアルの割り当てに失敗しました。',
    'kBevelProfile': u'ベベル プロファイル',
    'kConnectToMASH': u'MASH に接続',
    'kAddDynamics': u'ダイナミクスを追加',
    'kLocalRotatePivot': u'ローカル回転ピボット',
    'kLocalScalePivot': u'ローカル スケール ピボット',

    'kUnsupportedNodeType': u'不正なノード タイプ',
    'kNotConnected': u'接続されていない'
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