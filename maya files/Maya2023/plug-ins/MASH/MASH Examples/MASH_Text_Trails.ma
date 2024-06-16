//Maya ASCII 2017 scene
//Name: MASH_Text_Trails.ma
//Last modified: Tue, May 31, 2016 03:42:31 PM
//Codeset: 1252
requires maya "2017";
requires -nodeType "MASH_Waiter" -nodeType "MASH_Distribute" -nodeType "MASH_Trails"
		 -nodeType "MASH_Repro" "MASH" "400";
requires -nodeType "type" -nodeType "shellDeformer" -nodeType "vectorAdjust" -nodeType "vectorExtrude"
		 -nodeType "displayPoints" "Type" "019";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201605302145-996578";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "89D291F6-4CE8-2377-CFD2-4AAAEC373C93";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -41.59656795647863 51.475955233119912 99.392355440602898 ;
	setAttr ".r" -type "double3" -19.538352729602845 -36.200000000000252 -9.8535040497033336e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "280E975A-46AB-299C-AE79-B09DBF580D88";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 124.91504150558431;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "963B0385-4EC7-49FC-B27B-84A545F4AEC4";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "88D6F7A6-45A6-3BE0-4C40-E9802395E7E1";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "front";
	rename -uid "1C705CFD-4AF0-0CB1-05B1-07824210557A";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "9D8B04C9-47C1-822D-2D9A-DD82FC87D4F2";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -s -n "side";
	rename -uid "518E2BB0-422A-36F4-7857-4CA3ED83AA8F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "7635FA85-4AE0-BF55-FA19-7896EB154D28";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
	setAttr ".ai_translator" -type "string" "orthographic";
createNode transform -n "MASH_Text_Trails:typeMesh1";
	rename -uid "B36AB393-4213-CFDD-8371-A08200CDE57F";
createNode mesh -n "MASH_Text_Trails:typeMeshShape1" -p "MASH_Text_Trails:typeMesh1";
	rename -uid "8F1C84D2-4969-3ACB-F224-CCB4FD4AE162";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr -s 8 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode mesh -n "MASH_Text_Trails:typeMeshShape1Orig1" -p "MASH_Text_Trails:typeMesh1";
	rename -uid "01CE42B8-423D-FFD6-020B-AE8832FE7833";
	setAttr -k off ".v";
	setAttr ".io" yes;
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Text_Trails:transform1";
	rename -uid "6181ED52-46F5-C282-A023-A3874F1AB7AA";
	setAttr ".hio" yes;
createNode displayPoints -n "MASH_Text_Trails:displayPoints1" -p "MASH_Text_Trails:transform1";
	rename -uid "5414E493-4AF3-117F-BDAE-558A95450CF9";
	setAttr -k off ".v";
	setAttr -s 2 ".inPointPositionsPP";
	setAttr ".hio" yes;
createNode transform -n "MASH_Text_Trails:pSphere1";
	rename -uid "CEC2C0D6-4F10-78E0-EB0E-5DB8B9510ACE";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
	setAttr ".s" -type "double3" 0.15000003262751094 0.15000003262751094 0.15000003262751094 ;
createNode mesh -n "MASH_Text_Trails:pSphereShape1" -p "MASH_Text_Trails:pSphere1";
	rename -uid "0D7EBAAB-4AAA-F6F7-4A76-6D80C9F32DBA";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Text_Trails:nurbsCircle1";
	rename -uid "CF6DB082-4074-4669-B5F7-0180692E1EE8";
createNode nurbsCurve -n "MASH_Text_Trails:nurbsCircleShape1" -p "MASH_Text_Trails:nurbsCircle1";
	rename -uid "5C3E0E89-49F3-9622-381E-AE9DFE9EA0A8";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr -k off ".v";
	setAttr ".tw" yes;
createNode transform -n "MASH_Text_Trails:persp1";
	rename -uid "1A2E8273-4F23-A249-E5D0-9DAD88D09657";
	setAttr ".t" -type "double3" -21.44639276009714 42.730006464837004 84.998770411243626 ;
	setAttr ".r" -type "double3" -21.938352729602993 -29.000000000000028 6.0002252196889946e-014 ;
	setAttr ".rp" -type "double3" 3.5527136788005009e-015 1.0658141036401503e-014 1.4210854715202004e-014 ;
	setAttr ".rpt" -type "double3" -5.5796617126363031e-015 4.7034115039341031e-015 
		-4.8230408096881525e-015 ;
createNode camera -n "MASH_Text_Trails:perspShape1" -p "MASH_Text_Trails:persp1";
	rename -uid "A1D6A5D1-4270-7305-B7D0-63AA60A1B021";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".fl" 34.999999999999986;
	setAttr ".coi" 102.72365251572784;
	setAttr ".imn" -type "string" "persp1";
	setAttr ".den" -type "string" "persp1_depth";
	setAttr ".man" -type "string" "persp1_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -n "MASH_Text_Trails:areaLight1";
	rename -uid "E3D7C1F5-40BC-EA5B-1A03-629A819F6D32";
	setAttr ".t" -type "double3" -7.1701820685220046 23.53594740981498 23.29736449965668 ;
	setAttr ".r" -type "double3" -61.53624916278546 -31.884872218473106 25.307777899337388 ;
	setAttr ".s" -type "double3" 6.8910928149829562 6.8910928149829562 6.8910928149829562 ;
createNode areaLight -n "MASH_Text_Trails:areaLightShape1" -p "MASH_Text_Trails:areaLight1";
	rename -uid "D92C73B1-43B7-30E2-BA06-2D8A0F3B1B1C";
	setAttr -k off ".v";
	setAttr ".cl" -type "float3" 1 0.96842098 0.759 ;
createNode transform -n "MASH_Text_Trails:areaLight2";
	rename -uid "8B56259F-4B56-BFE6-BC7D-19908DAB9770";
	setAttr ".t" -type "double3" 26.567509337298493 27.225390732608105 40.299429527578731 ;
	setAttr ".r" -type "double3" -27.565308104222904 37.732880751004771 16.727232166158466 ;
	setAttr ".s" -type "double3" 6.8910928149829562 6.8910928149829562 6.8910928149829562 ;
createNode areaLight -n "MASH_Text_Trails:areaLightShape2" -p "MASH_Text_Trails:areaLight2";
	rename -uid "B29892DD-45D7-C3FE-F596-82BE97C577EA";
	setAttr -k off ".v";
	setAttr ".cl" -type "float3" 0.83399999 0.92787576 1 ;
	setAttr ".in" 2.7966101169586182;
createNode transform -n "MASH_Text_Trails:MASH1_ReproMesh";
	rename -uid "6B59F847-435E-3D79-1733-72B584A1B183";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
createNode mesh -n "MASH_Text_Trails:MASH1_ReproMeshShape" -p "MASH_Text_Trails:MASH1_ReproMesh";
	rename -uid "7F846D46-4E97-DE86-F62C-27B5CEBD3C99";
	setAttr -k off ".v";
	setAttr -s 2 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Text_Trails:MASH1_Trails1";
	rename -uid "F3F9C740-43FE-AE87-7DED-D682AA28390D";
createNode mesh -n "MASH_Text_Trails:MASH1_Trails_Mesh" -p "MASH_Text_Trails:MASH1_Trails1";
	rename -uid "E4849126-465A-2412-5687-BEABC6F3B1AE";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "03106B68-4E80-09B0-EF3B-80BAB312D509";
	setAttr -s 4 ".lnk";
	setAttr -s 4 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "C476A38D-43AD-3DCB-7B32-7CB0EF902C38";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "E51440B3-4AEF-2CE6-9E59-EFA3AE48C5EA";
createNode displayLayerManager -n "layerManager";
	rename -uid "BBFE811C-4934-B3DE-4B7D-40AD86CAC9DC";
createNode displayLayer -n "defaultLayer";
	rename -uid "FE59CB05-4F01-F6DB-59DA-F4A3C1CB215F";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "7BA424C2-4B21-22DC-3133-9FAE3F591A51";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "74B9E697-4D51-EFBA-F78E-C39962817ADC";
	setAttr ".g" yes;
createNode renderLayerManager -n "MASH_Text_Trails:renderLayerManager";
	rename -uid "EBB4CD3A-4A47-1843-81BB-648335D91FCB";
createNode renderLayer -n "MASH_Text_Trails:defaultRenderLayer";
	rename -uid "80701F0C-42B5-A73E-7C6F-7791ECF95424";
	setAttr ".g" yes;
createNode renderLayerManager -n "MASH_Text_Trails:MASH_Text_Trails_renderLayerManager";
	rename -uid "199762EA-44B9-2C32-6401-CD97B7451FAA";
createNode renderLayer -n "MASH_Text_Trails:MASH_Text_Trails_defaultRenderLayer";
	rename -uid "08D08064-45B1-1D6E-153E-69AC82D03BF1";
	setAttr ".g" yes;
createNode type -n "MASH_Text_Trails:type1";
	rename -uid "EDA52CBF-4301-69A1-85FD-3CA05C946BE4";
	setAttr ".solidsPerCharacter" -type "doubleArray" 6 1 1 1 1 1 1 ;
	setAttr ".solidsPerWord" -type "doubleArray" 2 2 4 ;
	setAttr ".solidsPerLine" -type "doubleArray" 1 6 ;
	setAttr ".vertsPerChar" -type "doubleArray" 6 124 205 247 307 393 478 ;
	setAttr ".characterBoundingBoxesMax" -type "vectorArray" 6 8.9361702127659584
		 10.354609929078014 0 20 10.354609929078014 2.2163120567375891e-006 35.177304964539012
		 10.354609929078014 6.6489361702127667e-006 43.829787234042556 10.354609929078014
		 8.8652482269503562e-006 52.765957446808514 10.354609929078014 1.1081560283687944e-005 62.411347517730505
		 10.354609929078014 1.3297872340425533e-005 ;
	setAttr ".characterBoundingBoxesMin" -type "vectorArray" 6 0.56737588652482274
		 0 0 10.638297872340427 0 2.2163120567375891e-006 25.531914893617024 0 6.6489361702127667e-006 35.177304964539012
		 0 8.8652482269503562e-006 44.680851063829792 0 1.1081560283687944e-005 53.900709219858157
		 0 1.3297872340425533e-005 ;
	setAttr ".manipulatorPivots" -type "vectorArray" 6 0.56737588652482274 -0.14184397163120568
		 0 10.638297872340427 0 2.2163120567375891e-006 25.531914893617024 0 6.6489361702127667e-006 35.177304964539012
		 -2.9787234042553195 8.8652482269503562e-006 44.680851063829792 -2.8368794326241136
		 1.1081560283687944e-005 53.900709219858157 -0.14184397163120568 1.3297872340425533e-005 ;
	setAttr ".holeInfo" -type "Int32Array" 9 1 28 177 4 32
		 361 5 19 459 ;
	setAttr ".numberOfShells" 6;
	setAttr ".currentFont" -type "string" "Arial Black";
	setAttr ".currentStyle" -type "string" "Regular";
	setAttr ".manipulatorPositionsPP" -type "vectorArray" 20 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 ;
	setAttr ".manipulatorWordPositionsPP" -type "vectorArray" 2 0 0 0 0 0 0 ;
	setAttr ".manipulatorLinePositionsPP" -type "vectorArray" 1 0 0 0 ;
	setAttr ".manipulatorRotationsPP" -type "vectorArray" 20 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 ;
	setAttr ".manipulatorWordRotationsPP" -type "vectorArray" 2 0 0 0 0 0 0 ;
	setAttr ".manipulatorLineRotationsPP" -type "vectorArray" 1 0 0 0 ;
	setAttr ".manipulatorScalesPP" -type "vectorArray" 20 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
		 0 0 0 0 0 ;
	setAttr ".manipulatorWordScalesPP" -type "vectorArray" 2 0 0 0 0 0 0 ;
	setAttr ".manipulatorLineScalesPP" -type "vectorArray" 1 0 0 0 ;
	setAttr ".alignmentAdjustments" -type "doubleArray" 1 0 ;
	setAttr ".manipulatorMode" 0;
	setAttr ".deformableType" yes;
	setAttr ".maxEdgeLength" 1.6930817365646362;
createNode vectorExtrude -n "MASH_Text_Trails:typeExtrude1";
	rename -uid "04B570D1-48D3-2015-52EE-33A7D86255E5";
	addAttr -s false -ci true -h true -sn "typeMessage" -ln "typeMessage" -at "message";
	setAttr ".solidsPerCharacter" -type "doubleArray" 0 ;
	setAttr ".solidsPerWord" -type "doubleArray" 0 ;
	setAttr ".solidsPerLine" -type "doubleArray" 0 ;
	setAttr ".capComponents" -type "componentList" 1 "f[0:11]";
	setAttr ".extrusionComponents" -type "componentList" 1 "f[12:1923]";
	setAttr ".extrudeDistancePP" -type "doubleArray" 0 ;
	setAttr ".extrudeDistanceScalePP" -type "doubleArray" 0 ;
	setAttr -s 4 ".frontBevelCurve[0:3]"  0 1 0.5 1 1 0.5 1 0;
	setAttr -s 4 ".backBevelCurve[0:3]"  0 1 0.5 1 1 0.5 1 0;
	setAttr -s 4 ".extrudeCurve[0:3]"  0 0.5 0.333 0.5 0.667 0.5 1 0.5;
	setAttr -s 4 ".outerBevelCurve[0:3]"  0 1 0.5 1 1 0.5 1 0;
createNode groupId -n "MASH_Text_Trails:groupid1";
	rename -uid "C7DB9432-4F82-D002-F291-9A854327ECBE";
createNode groupId -n "MASH_Text_Trails:groupid2";
	rename -uid "8A9BF2E0-4849-3FCC-67E1-FFAFAC068E06";
createNode groupId -n "MASH_Text_Trails:groupid3";
	rename -uid "935A3F3C-4BF1-2ECA-5736-53AE857132FC";
createNode blinn -n "MASH_Text_Trails:typeBlinn";
	rename -uid "B52EF73F-4CF0-4F94-7736-36B1AFC899A8";
	setAttr ".c" -type "float3" 0.072580643 0.072580643 0.072580643 ;
createNode shadingEngine -n "MASH_Text_Trails:typeBlinnSG";
	rename -uid "9B34D97A-45C6-0AA5-312D-5FAEC70147E4";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "MASH_Text_Trails:materialInfo1";
	rename -uid "BA6AA010-429F-2303-09B1-A0B6C9D5C191";
createNode vectorAdjust -n "MASH_Text_Trails:vectorAdjust1";
	rename -uid "0EA3E92B-4C7C-FC1F-D330-77BFD97E7C19";
	setAttr ".extrudeDistanceScalePP" -type "doubleArray" 0 ;
createNode tweak -n "MASH_Text_Trails:tweak1";
	rename -uid "EBAF8F9E-45F9-4181-8F94-DCAFAA94E4F0";
createNode objectSet -n "MASH_Text_Trails:vectorAdjust1Set";
	rename -uid "886BA358-4B0E-EA44-9A0B-C3AB4E4BA3EA";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "MASH_Text_Trails:vectorAdjust1GroupId";
	rename -uid "9C8DF375-4F2D-9507-83FD-F5BA41827E31";
	setAttr ".ihi" 0;
createNode groupParts -n "MASH_Text_Trails:vectorAdjust1GroupParts";
	rename -uid "26D5285B-4717-0083-890A-F08A5B1085F1";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode objectSet -n "MASH_Text_Trails:tweakSet1";
	rename -uid "19488FFD-4E49-6787-2816-1EBB23E03EC1";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "MASH_Text_Trails:groupId2";
	rename -uid "CA3827E4-4534-0D06-29C3-CC8D2D70CB27";
	setAttr ".ihi" 0;
createNode groupParts -n "MASH_Text_Trails:groupParts2";
	rename -uid "E8D26F3B-46D6-F9A3-A83C-9AAFCA33E2E7";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode groupId -n "MASH_Text_Trails:groupId3";
	rename -uid "91466446-4277-41CD-CD33-EA9E244B6452";
createNode groupId -n "MASH_Text_Trails:groupId4";
	rename -uid "F34AC3BA-4246-8152-A962-9894E6640919";
createNode groupId -n "MASH_Text_Trails:groupId5";
	rename -uid "B149042B-4C08-C5DE-A4DB-77A0D067E61B";
createNode groupId -n "MASH_Text_Trails:groupId6";
	rename -uid "28FFFBB4-481A-E347-D905-C6A87E3D3C41";
createNode groupId -n "MASH_Text_Trails:groupId7";
	rename -uid "E136DF31-4BAB-6EBA-A126-8D9F53BE6F4A";
createNode groupId -n "MASH_Text_Trails:groupId8";
	rename -uid "AC4D02E8-4CCD-AF38-0B32-929DDA6325B8";
createNode polyRemesh -n "MASH_Text_Trails:polyRemesh1";
	rename -uid "AACDBBD0-40E4-6B0E-2067-E8B0BA5F7A0D";
	addAttr -s false -ci true -h true -sn "typeMessage" -ln "typeMessage" -at "message";
	setAttr ".nds" 1;
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".tsb" no;
	setAttr ".ipt" 0;
createNode polyAutoProj -n "MASH_Text_Trails:polyAutoProj1";
	rename -uid "E407D1DF-46CC-876D-F951-E2936F50A404";
	setAttr ".uopa" yes;
	setAttr ".ics" -type "componentList" 1 "f[*]";
	setAttr ".ix" -type "matrix" 1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1;
	setAttr ".ps" 0.20000000298023224;
	setAttr ".dl" yes;
createNode shellDeformer -n "MASH_Text_Trails:shellDeformer1";
	rename -uid "52E0FAFA-4488-A8A1-1D8F-A89D3B5FC51D";
	addAttr -s false -ci true -h true -sn "typeMessage" -ln "typeMessage" -at "message";
	setAttr ".positionInPP" -type "vectorArray" 0 ;
	setAttr ".scaleInPP" -type "vectorArray" 0 ;
	setAttr ".rotationInPP" -type "vectorArray" 0 ;
	setAttr ".enableAnimation" yes;
createNode tweak -n "MASH_Text_Trails:tweak2";
	rename -uid "9574A14C-437D-6781-077B-479233214B3B";
createNode objectSet -n "MASH_Text_Trails:shellDeformer1Set";
	rename -uid "B8CE7933-447C-A2EC-BF52-8EB2DB3F1212";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "MASH_Text_Trails:shellDeformer1GroupId";
	rename -uid "877B3A2E-453F-FE4C-A1DE-0BA27F2E5BE8";
	setAttr ".ihi" 0;
createNode groupParts -n "MASH_Text_Trails:shellDeformer1GroupParts";
	rename -uid "B90939A7-42DF-6655-0C2B-309332D37ED0";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode objectSet -n "MASH_Text_Trails:tweakSet2";
	rename -uid "42F59744-47FB-F19F-6B1A-29BC4A9CF91E";
	setAttr ".ihi" 0;
	setAttr ".vo" yes;
createNode groupId -n "MASH_Text_Trails:groupId10";
	rename -uid "A5BC5E99-4FDF-A30C-6560-8CA135BB0E50";
	setAttr ".ihi" 0;
createNode groupParts -n "MASH_Text_Trails:groupParts4";
	rename -uid "9BD91079-4EE7-7FA7-D67D-988999FA37A0";
	setAttr ".ihi" 0;
	setAttr ".ic" -type "componentList" 1 "vtx[*]";
createNode animCurveTA -n "MASH_Text_Trails:type1_animationRotationY";
	rename -uid "3B368607-4412-0AA9-9818-97BCF2959F56";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 25 360;
createNode polySphere -n "MASH_Text_Trails:polySphere1";
	rename -uid "2ABD6EE5-4698-C8C5-C4B5-E38E3C6C6403";
createNode makeNurbCircle -n "MASH_Text_Trails:makeNurbCircle1";
	rename -uid "8C5B6D82-4D40-74A0-58CA-AE996C1AA237";
	setAttr ".nr" -type "double3" 0 1 0 ;
createNode lambert -n "MASH_Text_Trails:lambert2";
	rename -uid "3E25B657-4086-8649-0BC8-80B2E0726DC9";
	setAttr ".dc" 1;
	setAttr ".c" -type "float3" 1 0 0 ;
createNode shadingEngine -n "MASH_Text_Trails:lambert2SG";
	rename -uid "E37D7E6F-4EA2-FCC1-622C-EAAEE77F847F";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "MASH_Text_Trails:materialInfo2";
	rename -uid "14E5CACC-4E6A-9BD7-EE1C-16B7E27ABFF8";
createNode nodeGraphEditorInfo -n "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo";
	rename -uid "3808999E-42E6-06D8-7F70-BA8D57E065C0";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -99.999996026357238 -1106.2081033646677 ;
	setAttr ".tgi[0].vh" -type "double2" 2479.7618062250235 203.82718684111151 ;
	setAttr -s 22 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 942.85711669921875;
	setAttr ".tgi[0].ni[0].y" -325.71429443359375;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1250;
	setAttr ".tgi[0].ni[1].y" -414.28570556640625;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 1864.2857666015625;
	setAttr ".tgi[0].ni[2].y" -310;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 21.428571701049805;
	setAttr ".tgi[0].ni[3].y" -14.285714149475098;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 2171.428466796875;
	setAttr ".tgi[0].ni[4].y" -507.14285278320312;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 942.85711669921875;
	setAttr ".tgi[0].ni[5].y" -481.42855834960937;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 2171.428466796875;
	setAttr ".tgi[0].ni[6].y" -835.71429443359375;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 328.57144165039063;
	setAttr ".tgi[0].ni[7].y" -361.42855834960937;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 21.428571701049805;
	setAttr ".tgi[0].ni[8].y" -112.85713958740234;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 328.57144165039063;
	setAttr ".tgi[0].ni[9].y" -460;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 14.285714149475098;
	setAttr ".tgi[0].ni[10].y" -214.28572082519531;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 1557.142822265625;
	setAttr ".tgi[0].ni[11].y" -325.71429443359375;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 21.428571701049805;
	setAttr ".tgi[0].ni[12].y" -312.85714721679687;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 635.71429443359375;
	setAttr ".tgi[0].ni[13].y" -268.57144165039063;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" 328.57144165039063;
	setAttr ".tgi[0].ni[14].y" -708.5714111328125;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 1557.142822265625;
	setAttr ".tgi[0].ni[15].y" -227.14285278320312;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 328.57144165039063;
	setAttr ".tgi[0].ni[16].y" -262.85714721679687;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 1864.2857666015625;
	setAttr ".tgi[0].ni[17].y" -507.14285278320312;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 1864.2857666015625;
	setAttr ".tgi[0].ni[18].y" -408.57144165039062;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 1557.142822265625;
	setAttr ".tgi[0].ni[19].y" -424.28570556640625;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 2171.428466796875;
	setAttr ".tgi[0].ni[20].y" -310;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" 328.57144165039063;
	setAttr ".tgi[0].ni[21].y" -610;
	setAttr ".tgi[0].ni[21].nvs" 18304;
createNode script -n "MASH_Text_Trails:uiConfigurationScriptNode";
	rename -uid "DB04C2D9-4BEB-CD7D-D295-67A7CEE321EF";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"top\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n"
		+ "                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n"
		+ "                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n"
		+ "                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n"
		+ "            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n"
		+ "            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n"
		+ "        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"side\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n"
		+ "                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n"
		+ "            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n"
		+ "            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n"
		+ "            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"front\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n"
		+ "                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n"
		+ "                -width 1\n                -height 1\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n"
		+ "            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n"
		+ "            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n"
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"MASH_Text_Trails:persp1\" \n                -useInteractiveMode 0\n                -displayLights \"all\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n"
		+ "                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 1\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n"
		+ "                -isFiltered 0\n                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n"
		+ "                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1604\n                -height 836\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"MASH_Text_Trails:persp1\" \n            -useInteractiveMode 0\n            -displayLights \"all\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 1\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n"
		+ "            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n"
		+ "            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1604\n            -height 836\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n"
		+ "        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -showShapes 0\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n"
		+ "                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -isSet 0\n                -isSetMember 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n"
		+ "                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                -renderFilterIndex 0\n                -selectionOrder \"chronological\" \n                -expandAttribute 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n"
		+ "            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n"
		+ "            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n"
		+ "            outlinerEditor -e \n                -showShapes 0\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n"
		+ "                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n"
		+ "            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n"
		+ "                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n"
		+ "                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n"
		+ "                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n"
		+ "                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n"
		+ "                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n"
		+ "                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n"
		+ "                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n"
		+ "                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n"
		+ "                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n"
		+ "                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n"
		+ "                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n"
		+ "                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"timeEditorPanel\" -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n"
		+ "                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"sequenceEditorPanel\" -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperGraphPanel\" -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n"
		+ "            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n"
		+ "                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n"
		+ "                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"visorPanel\" -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"createNodePanel\" -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"polyTexturePlacementPanel\" -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"renderWindowPanel\" -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tshapePanel -unParent -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels ;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\tposePanel -unParent -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels ;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynRelEdPanel\" -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"relationshipPanel\" -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"referenceEditorPanel\" -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"componentEditorPanel\" -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dynPaintScriptedPanelType\" -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"scriptEditorPanel\" -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\tif ($useSceneConfig) {\n\t\tscriptedPanel -e -to $panelName;\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"contentBrowserPanel\" -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels `;\n"
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"Stereo\" -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels `;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n"
		+ "                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n"
		+ "                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n"
		+ "                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n"
		+ "            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n"
		+ "                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n"
		+ "                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n"
		+ "                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"hyperShadePanel\" -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"nodeEditorPanel\" -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n"
		+ "                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n"
		+ "                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"MASH_Text_Trails:persp1\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"all\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1604\\n    -height 836\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -camera \\\"MASH_Text_Trails:persp1\\\" \\n    -useInteractiveMode 0\\n    -displayLights \\\"all\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 1\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1604\\n    -height 836\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "MASH_Text_Trails:sceneConfigurationScriptNode";
	rename -uid "FE4C4706-4BC4-A4B0-9942-589BF716FB94";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode MASH_Waiter -n "MASH_Text_Trails:MASH1";
	rename -uid "8F4AB780-4185-3029-1954-A0A8F0CEF12E";
	addAttr -s false -ci true -sn "instancerMessage" -ln "instancerMessage" -at "message";
	setAttr ".inArray" -type "vectorArray" 100 8.6558065414428711 4.5611701011657715
		 1.8749997615814209 16.341976165771484 7.2229609489440918 0.62500214576721191 56.299659729003906
		 0.089414343237876892 1.8750133514404297 44.680850982666016 3.6621534824371338 1.1081559932790697e-005 44.680850982666016
		 -0.98001289367675781 0.62501102685928345 15.137480735778809 7.7652649879455566 2.5000021457672119 48.781028747558594
		 1.7021276950836182 0.62501102685928345 41.117019653320312 7.3758864402770996 2.5000088214874268 62.411346435546875
		 3.4286346435546875 0.62501329183578491 59.179965972900391 2.1138076782226562 1.2500133514404297 8.47296142578125
		 1.5857713222503662 2.4999997615814209 49.663120269775391 -0.14184397459030151 0.62501102685928345 10.638298034667969
		 2.7852997779846191 0.62500214576721191 62.411346435546875 3.1205673217773437 1.2500133514404297 47.311614990234375
		 6.4051418304443359 1.8750109672546387 2.4960522651672363 9.9668941497802734 1.8749997615814209 13.758865356445313
		 7.8014183044433594 1.2500021457672119 8.9361705780029297 3.320035457611084 1.8749997615814209 42.209415435791016
		 3.0035951137542725 2.5000088214874268 37.115837097167969 7.3758864402770996 0.62500882148742676 17.914728164672852
		 0.5828900933265686 1.2500021457672119 31.914894104003906 0.86682426929473877 1.8750064373016357 47.517730712890625
		 -1.103723406791687 1.1081559932790697e-005 35.85943603515625 5.737785816192627 0.62500882148742676 48.081642150878906
		 7.0974621772766113 1.1081559932790697e-005 47.517730712890625 -1.9703013896942139
		 1.8750109672546387 15.010181427001953 2.4245760440826416 1.8750021457672119 5.516746997833252
		 7.7931766510009766 1.8749997615814209 37.345687866210938 -2.968888521194458 2.5000088214874268 37.732711791992188
		 -0.88541668653488159 1.2500088214874268 3.4042553901672363 3.1205673217773437 0 31.914894104003906
		 4.3341212272644043 1.2500065565109253 61.465721130371094 3.1205673217773437 1.2500133514404297 36.200504302978516
		 4.9187350273132324 8.8652486738283187e-006 38.085105895996094 7.3758864402770996
		 1.8750088214874268 40.82269287109375 6.3936171531677246 1.8750088214874268 5.5532469749450684
		 10.309453010559082 0 13.758865356445313 4.2080378532409668 1.8750021457672119 11.572251319885254
		 10.212765693664551 1.8750021457672119 52.711032867431641 2.7524518966674805 1.2500109672546387 7.6966977119445801
		 5.4945144653320313 0 47.517730712890625 -2.8368794918060303 0.62501102685928345 49.204345703125
		 5.5551862716674805 1.8750109672546387 15.96534252166748 10.189287185668945 1.8750021457672119 52.5462646484375
		 2.0004987716674805 1.8750109672546387 40.234043121337891 4.4290781021118164 1.2500088214874268 15.404199600219727
		 2.4642620086669922 2.5000021457672119 37.382534027099609 -1.0724179744720459 1.2500088214874268 5.3075132369995117
		 1.8051861524581909 2.4999997615814209 42.021278381347656 7.3758864402770996 0.62500882148742676 54.744846343994141
		 1.1571227312088013 2.5000133514404297 19.185504913330078 1.7730495929718018 0.62500214576721191 54.521553039550781
		 5.8827157020568848 2.5000133514404297 49.313358306884766 7.499722957611084 1.1081559932790697e-005 4.5681653022766113
		 6.5446310043334961 0 54.451461791992188 1.5735815763473511 0.62501329183578491 4.8515071868896484
		 -0.14184397459030151 2.4999997615814209 58.144947052001953 -0.14184397459030151 1.3297872101247776e-005 59.291057586669922
		 5.2581310272216797 1.3297872101247776e-005 48.081642150878906 7.0974621772766113
		 2.5000109672546387 40.82269287109375 6.3936171531677246 2.5000088214874268 49.313358306884766
		 7.499722957611084 0.62501102685928345 52.715538024902344 4.4072055816650391 2.5000109672546387 51.514156341552734
		 6.885042667388916 0.62501102685928345 44.680850982666016 0.87685364484786987 2.5000109672546387 59.060283660888672
		 2.0045156478881836 1.3297872101247776e-005 16.174783706665039 2.7486424446105957
		 2.2163121684570797e-006 7.1387410163879395 0.30695921182632446 1.2499998807907104 18.316987991333008
		 9.3794326782226563 0.62500214576721191 44.680850982666016 6.4474530220031738 1.2500109672546387 4.745124340057373
		 4.6808509826660156 2.4999997615814209 17.081254959106445 10.00145435333252 0.62500214576721191 47.588653564453125
		 2.7850730419158936 2.5000109672546387 50.306613922119141 -0.081657245755195618 1.1081559932790697e-005 14.374114036560059
		 10.212765693664551 0.62500214576721191 4.3195919990539551 6.5248227119445801 2.4999997615814209 14.558954238891602
		 7.8014183044433594 1.8750021457672119 13.758865356445313 6.9030733108520508 0.62500214576721191 35.177303314208984
		 7.3758864402770996 0.62500882148742676 15.96534252166748 10.189287185668945 2.2163121684570797e-006 48.490829467773438
		 5.6439080238342285 0.62501102685928345 10.638298034667969 4.6421661376953125 2.5000021457672119 1.1163287162780762
		 1.5011358261108398 0 59.574466705322266 4.5390071868896484 0.62501329183578491 48.055046081542969
		 1.9707862138748169 0.62501102685928345 16.74506950378418 6.3968305587768555 1.8750021457672119 44.680850982666016
		 5.5190200805664062 2.5000109672546387 47.517730712890625 -0.23714539408683777 1.8750109672546387 15.974069595336914
		 2.6230053901672363 1.2500021457672119 33.423599243164063 10.212765693664551 2.5000064373016357 57.683212280273437
		 3.1205673217773437 0.62501329183578491 49.907608032226563 4.1863365173339844 2.5000109672546387 26.408769607543945
		 10.212765693664551 1.2500065565109253 3.1076157093048096 0.045157358050346375 0.62499994039535522 57.849067687988281
		 1.7305241823196411 1.3297872101247776e-005 4.3500666618347168 4.6398491859436035
		 0.62499994039535522 16.556406021118164 10.118849754333496 1.8750021457672119 28.794326782226563
		 6.0677700042724609 1.8750064373016357 59.633476257324219 -0.0099734039977192879 1.2500133514404297 48.490829467773438
		 5.6439080238342285 1.1081559932790697e-005 ;
	setAttr ".inScPP" -type "vectorArray" 100 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
		 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 ;
	setAttr ".inRotPP" -type "vectorArray" 100 0 -0 -61.865653987525739 180.00000307046903
		 -0 -47.575569193992045 180.00000307046903 -0 -17.437981253906006 -45.000000767666599
		 7.5192922119616146e-005 89.999926342312392 180.00000307046903 -0 -90.000001535234517 95.798741251489361
		 46.084794384514367 -90.003919581880794 0.27997961264138949 -90.000001535234517 0 118.70285507912665
		 -47.353766750894032 -90.004391761452979 0 -0 -88.725639617707017 0 -0 44.968590986850302 51.128250282409951
		 27.175750858101697 -90.009711683047755 180.00000307046903 0 1.5790318903275895 180.00000307046903
		 -0 -90.000001535234517 180.00000307046903 0 44.999998352780729 0 53.452712833694818
		 -21.870109835384984 0 -25.900743168949031 24.748960738110302 0 31.856110271107394
		 -134.99999988801525 0 0 -90.411680596469438 48.453709214472141 19.13901968565045
		 -90.031456571877726 0 -0 -0 180.00000307046903 0 29.757922881482454 0 -0 -90.000001535234517 -135.00000230280244
		 -7.5187713525050849e-005 89.999926347520983 180.00000307046903 -0 -67.392355672572734 -66.906542653863511
		 -41.063575148268555 89.986539470828646 0 -0 -90.000001535234517 3.687472362858657
		 -90.000001535234517 0 99.402031335958938 -90.000001535234517 0 92.025299718338971
		 45.331185093604248 -89.959731460877137 0 180.00000307046903 39.66167874264022 -117.25591861381314
		 -48.920064009413579 89.982981462607938 0 -0 -90.000001535234517 180.00000307046903
		 0 0 -49.256945101657699 21.056880746459537 89.967310457184468 0 -0 -36.187801761970803 0
		 180.00000307046903 73.319783833999395 -94.519012004295689 -45.912418000090263 89.95901979368017 0
		 -0 -90.000001535234517 0 -0 -0 0 0 -98.006533250355943 -108.38948035329913 -42.791956428460416
		 89.996084719130423 180.00000307046903 0 45.000003182453774 180.00000307046903 55.454768578797861
		 -29.325876890538467 0 -0 -4.4208615372837716 0 0 -107.73044416805028 0 180.00000307046903
		 73.319710889039868 96.229845323638358 -45.583139253650515 -89.997284261488275 17.600422439661585
		 -90.000001535234517 0 107.17333122334344 -44.360141559694924 -90.00121936863961 0
		 -0 -0 116.99220090513568 -38.99954759607725 -0.02380071630042736 0 0 -124.32099778198224 65.956381478626028
		 -41.528788497676786 -0.041320493940843139 -85.811080917051953 -45.779748377315336
		 89.976398721083214 -83.041255824236828 -46.138998699821819 90.001985385262756 180.00000307046903
		 -0 -58.753406041989869 89.821234923772778 45.657203604899038 -89.968287883138103 -135.70334364469093
		 -0.13183297631040813 0.00013747819122881649 -118.20651126760004 39.366438784125542
		 -0.0084398534341845917 113.07584444165633 -41.07218528116875 -89.98648738707135 132.64808498253981
		 -15.990894737220421 -90.029183458632488 0 -0 5.8116019074329444 44.28605618878975
		 -7.9416041858282771 -89.993099302111844 0 -0 -40.751107763146656 134.999999887982
		 -6.1705860824588904e-005 -89.9999398293685 -56.030048643596572 33.158620598663212
		 0.0059330463075191082 -63.738909314998047 -40.058495814781651 90.006171511595099 180.00000307046903
		 0 26.941392110462711 0 -0 -37.524934549919529 180.00000307046903 -0 -90.000001535234517 90.509482349445392
		 46.209740640846313 -90.000524850010933 0 -0 -16.161608557203621 45.426413725381344
		 -14.460386303002386 -89.993852199842649 -98.201292356649901 46.231049920797325 89.958805731503119 0
		 -0 -0 91.050052527847569 -45.951107560582351 -89.999356142250178 -178.21206197984102
		 90.000001535234517 0 0 -0 -90.000001535234517 0 -0 56.303865820232424 -93.141644967618618
		 -45.657357640684559 89.967790332406281 166.23663213387218 90.000001535234517 0 135.0000023028517
		 2.4955635848502889e-006 -90.000004030798095 -52.57165675891715 28.948807788057898
		 90.014186185840387 0 -10.179844034384137 50.941583676331291 0 -0 -40.783988513092503 180.00000307046903
		 -0 -75.486918637413879 134.999999887982 -6.1705860824588904e-005 -89.9999398293685 0
		 -0 -90.000001535234517 0 242.98479337006191 26.238133205750305 89.911158781385623
		 -44.999931887784435 -89.874358857474462 180.00000307046903 0 0 135.69272864743752
		 5.9946724694602569 -89.996976173135906 0 -0 -0 180.00000307046903 -0 -14.999688874460654 -44.345478394196789
		 -11.526863984436801 -0.0046562110273290318 169.97614270066686 90.000001535234517
		 0 0 -0 -9.7020082769725029 180.00000307046903 -0 -90.000001535234517 180.00000307046903
		 0 11.761096974563749 -100.04117230754494 46.309421252307047 90.003559858682408 ;
	setAttr ".cacheIdPP" -type "vectorArray" 0 ;
	setAttr ".cacheVisibilityPP" -type "vectorArray" 0 ;
	setAttr ".initSt" -type "vectorArray" 0 ;
	setAttr ".filename" -type "string" "/Applications/Autodesk/maya2017/plug-ins/MASH/Presets";
createNode MASH_Distribute -n "MASH_Text_Trails:MASH1_Distribute";
	rename -uid "9EBD3BDF-431E-B189-FE76-8E85C74F6C09";
	setAttr ".mapDirection" 4;
	setAttr ".pointCount" 100;
	setAttr ".fArray" -type "vectorArray" 0 ;
	setAttr ".inPPP" -type "vectorArray" 0 ;
	setAttr -s 3 ".scaleRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".rotationRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".bRmp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr ".bRmpX[0]"  0 1 1;
	setAttr ".bRmpY[0]"  0 1 1;
	setAttr ".bRmpZ[0]"  0 1 1;
	setAttr ".see" 30;
	setAttr ".meshType" 3;
	setAttr ".rt" 4;
createNode MASH_Repro -n "MASH_Text_Trails:MASH1_Repro";
	rename -uid "A1C9AB67-4DE5-8059-D0A7-0CB92CE68B31";
	addAttr -s false -ci true -sn "instancerMessage" -ln "instancerMessage" -at "message";
	setAttr ".instancedGroup[0].inMesh[0].inShGroupId[0]"  -1;
createNode groupId -n "MASH_Text_Trails:groupId11";
	rename -uid "4CD3837A-4ECF-323A-8388-8D95CA7AEFE8";
createNode MASH_Trails -n "MASH_Text_Trails:MASH1_Trails";
	rename -uid "06935775-479C-CF35-E652-EC91113E71A0";
	setAttr ".positionInPP" -type "vectorArray" 0 ;
	setAttr ".trailLength" 6;
	setAttr ".trailWidth" 0.079999998211860657;
	setAttr ".decay" yes;
	setAttr ".upVector" -type "float3" 0 0 1 ;
	setAttr -s 4 ".trailTaperCurve[1:3]"  0.333 0.33000001 0.667 0.66000003
		 1 1;
	setAttr -s 4 ".bevelCapCurve[0:3]"  0 1 0.375 1 0.667 0.33000001 1
		 0;
createNode nodeGraphEditorInfo -n "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1";
	rename -uid "49A974F8-44C9-61EB-F0BD-B0A79AE8DBA2";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" 143.94362270176643 -306.62212813366619 ;
	setAttr ".tgi[0].vh" -type "double2" 2226.6915098335621 602.51385434449867 ;
	setAttr -s 23 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 22.857143402099609;
	setAttr ".tgi[0].ni[0].y" 131.42857360839844;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 1920;
	setAttr ".tgi[0].ni[1].y" 418.57144165039062;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 330;
	setAttr ".tgi[0].ni[2].y" 177.14285278320312;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 1920;
	setAttr ".tgi[0].ni[3].y" -218.57142639160156;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" 1558.5714111328125;
	setAttr ".tgi[0].ni[4].y" 328.57144165039063;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" 637.14288330078125;
	setAttr ".tgi[0].ni[5].y" 50;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 691.4285888671875;
	setAttr ".tgi[0].ni[6].y" 431.42855834960937;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" 998.5714111328125;
	setAttr ".tgi[0].ni[7].y" 431.42855834960937;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 944.28570556640625;
	setAttr ".tgi[0].ni[8].y" 54.285713195800781;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" 1920;
	setAttr ".tgi[0].ni[9].y" -91.428573608398437;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" 2480;
	setAttr ".tgi[0].ni[10].y" 314.28570556640625;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" -291.42855834960937;
	setAttr ".tgi[0].ni[11].y" 131.42857360839844;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 1865.7142333984375;
	setAttr ".tgi[0].ni[12].y" 304.28570556640625;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" 330;
	setAttr ".tgi[0].ni[13].y" 78.571426391601562;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" 2172.857177734375;
	setAttr ".tgi[0].ni[14].y" 314.28570556640625;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 1558.5714111328125;
	setAttr ".tgi[0].ni[15].y" 71.428573608398438;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 1251.4285888671875;
	setAttr ".tgi[0].ni[16].y" 71.428573608398438;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 1865.7142333984375;
	setAttr ".tgi[0].ni[17].y" 205.71427917480469;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 2172.857177734375;
	setAttr ".tgi[0].ni[18].y" 215.71427917480469;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 1427.142822265625;
	setAttr ".tgi[0].ni[19].y" -140;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 2480;
	setAttr ".tgi[0].ni[20].y" 67.142860412597656;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" 2172.857177734375;
	setAttr ".tgi[0].ni[21].y" 117.14286041259766;
	setAttr ".tgi[0].ni[21].nvs" 18305;
	setAttr ".tgi[0].ni[22].x" 1920;
	setAttr ".tgi[0].ni[22].y" 35.714286804199219;
	setAttr ".tgi[0].ni[22].nvs" 18304;
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 4 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 6 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -s 3 ".r";
select -ne :lightList1;
	setAttr -s 2 ".l";
select -ne :initialShadingGroup;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultLightSet;
	setAttr -s 2 ".dsm";
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "MASH_Text_Trails:shellDeformer1.og[0]" "MASH_Text_Trails:typeMeshShape1.i"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1GroupId.id" "MASH_Text_Trails:typeMeshShape1.iog.og[0].gid"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1Set.mwc" "MASH_Text_Trails:typeMeshShape1.iog.og[0].gco"
		;
connectAttr "MASH_Text_Trails:groupId2.id" "MASH_Text_Trails:typeMeshShape1.iog.og[1].gid"
		;
connectAttr "MASH_Text_Trails:tweakSet1.mwc" "MASH_Text_Trails:typeMeshShape1.iog.og[1].gco"
		;
connectAttr "MASH_Text_Trails:shellDeformer1GroupId.id" "MASH_Text_Trails:typeMeshShape1.iog.og[2].gid"
		;
connectAttr "MASH_Text_Trails:shellDeformer1Set.mwc" "MASH_Text_Trails:typeMeshShape1.iog.og[2].gco"
		;
connectAttr "MASH_Text_Trails:groupId10.id" "MASH_Text_Trails:typeMeshShape1.iog.og[3].gid"
		;
connectAttr "MASH_Text_Trails:tweakSet2.mwc" "MASH_Text_Trails:typeMeshShape1.iog.og[3].gco"
		;
connectAttr "MASH_Text_Trails:tweak2.vl[0].vt[0]" "MASH_Text_Trails:typeMeshShape1.twl"
		;
connectAttr "MASH_Text_Trails:polyAutoProj1.out" "MASH_Text_Trails:typeMeshShape1Orig1.i"
		;
connectAttr "MASH_Text_Trails:shellDeformer1.rotationPivotPointsPP" "MASH_Text_Trails:displayPoints1.inPointPositionsPP[0]"
		;
connectAttr "MASH_Text_Trails:shellDeformer1.scalePivotPointsPP" "MASH_Text_Trails:displayPoints1.inPointPositionsPP[1]"
		;
connectAttr "MASH_Text_Trails:polySphere1.out" "MASH_Text_Trails:pSphereShape1.i"
		;
connectAttr "MASH_Text_Trails:makeNurbCircle1.oc" "MASH_Text_Trails:nurbsCircleShape1.cr"
		;
connectAttr "MASH_Text_Trails:MASH1_Repro.out" "MASH_Text_Trails:MASH1_ReproMeshShape.i"
		;
connectAttr "MASH_Text_Trails:groupId11.id" "MASH_Text_Trails:MASH1_ReproMeshShape.iog.og[0].gid"
		;
connectAttr ":initialShadingGroup.mwc" "MASH_Text_Trails:MASH1_ReproMeshShape.iog.og[0].gco"
		;
connectAttr "MASH_Text_Trails:MASH1_Trails.outMesh" "MASH_Text_Trails:MASH1_Trails_Mesh.i"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "MASH_Text_Trails:typeBlinnSG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "MASH_Text_Trails:lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "MASH_Text_Trails:typeBlinnSG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "MASH_Text_Trails:lambert2SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "MASH_Text_Trails:renderLayerManager.rlmi[0]" "MASH_Text_Trails:defaultRenderLayer.rlid"
		;
connectAttr "MASH_Text_Trails:MASH_Text_Trails_renderLayerManager.rlmi[0]" "MASH_Text_Trails:MASH_Text_Trails_defaultRenderLayer.rlid"
		;
connectAttr "MASH_Text_Trails:typeMesh1.msg" "MASH_Text_Trails:type1.transformMessage"
		;
connectAttr "MASH_Text_Trails:type1_animationRotationY.o" "MASH_Text_Trails:type1.animationRotationY"
		;
connectAttr "MASH_Text_Trails:type1.vertsPerChar" "MASH_Text_Trails:typeExtrude1.vertsPerChar"
		;
connectAttr "MASH_Text_Trails:groupid1.id" "MASH_Text_Trails:typeExtrude1.capGroupId"
		;
connectAttr "MASH_Text_Trails:groupid2.id" "MASH_Text_Trails:typeExtrude1.bevelGroupId"
		;
connectAttr "MASH_Text_Trails:groupid3.id" "MASH_Text_Trails:typeExtrude1.extrudeGroupId"
		;
connectAttr "MASH_Text_Trails:groupId3.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:groupId4.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:groupId5.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:groupId6.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:groupId7.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:groupId8.id" "MASH_Text_Trails:typeExtrude1.charGroupId"
		 -na;
connectAttr "MASH_Text_Trails:type1.outputMesh" "MASH_Text_Trails:typeExtrude1.inputMesh"
		;
connectAttr "MASH_Text_Trails:type1.extrudeMessage" "MASH_Text_Trails:typeExtrude1.typeMessage"
		;
connectAttr "MASH_Text_Trails:typeBlinn.oc" "MASH_Text_Trails:typeBlinnSG.ss";
connectAttr "MASH_Text_Trails:typeMeshShape1.iog" "MASH_Text_Trails:typeBlinnSG.dsm"
		 -na;
connectAttr "MASH_Text_Trails:typeBlinnSG.msg" "MASH_Text_Trails:materialInfo1.sg"
		;
connectAttr "MASH_Text_Trails:typeBlinn.msg" "MASH_Text_Trails:materialInfo1.m";
connectAttr "MASH_Text_Trails:vectorAdjust1GroupParts.og" "MASH_Text_Trails:vectorAdjust1.ip[0].ig"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1GroupId.id" "MASH_Text_Trails:vectorAdjust1.ip[0].gi"
		;
connectAttr "MASH_Text_Trails:type1.grouping" "MASH_Text_Trails:vectorAdjust1.grouping"
		;
connectAttr "MASH_Text_Trails:type1.manipulatorTransforms" "MASH_Text_Trails:vectorAdjust1.manipulatorTransforms"
		;
connectAttr "MASH_Text_Trails:type1.alignmentMode" "MASH_Text_Trails:vectorAdjust1.alignmentMode"
		;
connectAttr "MASH_Text_Trails:type1.vertsPerChar" "MASH_Text_Trails:vectorAdjust1.vertsPerChar"
		;
connectAttr "MASH_Text_Trails:typeExtrude1.vertexGroupIds" "MASH_Text_Trails:vectorAdjust1.vertexGroupIds"
		;
connectAttr "MASH_Text_Trails:groupParts2.og" "MASH_Text_Trails:tweak1.ip[0].ig"
		;
connectAttr "MASH_Text_Trails:groupId2.id" "MASH_Text_Trails:tweak1.ip[0].gi";
connectAttr "MASH_Text_Trails:vectorAdjust1GroupId.msg" "MASH_Text_Trails:vectorAdjust1Set.gn"
		 -na;
connectAttr "MASH_Text_Trails:typeMeshShape1.iog.og[0]" "MASH_Text_Trails:vectorAdjust1Set.dsm"
		 -na;
connectAttr "MASH_Text_Trails:vectorAdjust1.msg" "MASH_Text_Trails:vectorAdjust1Set.ub[0]"
		;
connectAttr "MASH_Text_Trails:tweak1.og[0]" "MASH_Text_Trails:vectorAdjust1GroupParts.ig"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1GroupId.id" "MASH_Text_Trails:vectorAdjust1GroupParts.gi"
		;
connectAttr "MASH_Text_Trails:groupId2.msg" "MASH_Text_Trails:tweakSet1.gn" -na;
connectAttr "MASH_Text_Trails:typeMeshShape1.iog.og[1]" "MASH_Text_Trails:tweakSet1.dsm"
		 -na;
connectAttr "MASH_Text_Trails:tweak1.msg" "MASH_Text_Trails:tweakSet1.ub[0]";
connectAttr "MASH_Text_Trails:typeExtrude1.outputMesh" "MASH_Text_Trails:groupParts2.ig"
		;
connectAttr "MASH_Text_Trails:groupId2.id" "MASH_Text_Trails:groupParts2.gi";
connectAttr "MASH_Text_Trails:vectorAdjust1.og[0]" "MASH_Text_Trails:polyRemesh1.ip"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.wm" "MASH_Text_Trails:polyRemesh1.mp"
		;
connectAttr "MASH_Text_Trails:type1.remeshMessage" "MASH_Text_Trails:polyRemesh1.typeMessage"
		;
connectAttr "MASH_Text_Trails:typeExtrude1.capComponents" "MASH_Text_Trails:polyRemesh1.ics"
		;
connectAttr "MASH_Text_Trails:polyRemesh1.out" "MASH_Text_Trails:polyAutoProj1.ip"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.wm" "MASH_Text_Trails:polyAutoProj1.mp"
		;
connectAttr "MASH_Text_Trails:shellDeformer1GroupParts.og" "MASH_Text_Trails:shellDeformer1.ip[0].ig"
		;
connectAttr "MASH_Text_Trails:shellDeformer1GroupId.id" "MASH_Text_Trails:shellDeformer1.ip[0].gi"
		;
connectAttr "MASH_Text_Trails:type1.animationPosition" "MASH_Text_Trails:shellDeformer1.animationPosition"
		;
connectAttr "MASH_Text_Trails:type1.animationPositionX" "MASH_Text_Trails:shellDeformer1.animationPositionX"
		;
connectAttr "MASH_Text_Trails:type1.animationPositionY" "MASH_Text_Trails:shellDeformer1.animationPositionY"
		;
connectAttr "MASH_Text_Trails:type1.animationPositionZ" "MASH_Text_Trails:shellDeformer1.animationPositionZ"
		;
connectAttr "MASH_Text_Trails:type1.animationRotation" "MASH_Text_Trails:shellDeformer1.animationRotation"
		;
connectAttr "MASH_Text_Trails:type1.animationRotationX" "MASH_Text_Trails:shellDeformer1.animationRotationX"
		;
connectAttr "MASH_Text_Trails:type1.animationRotationY" "MASH_Text_Trails:shellDeformer1.animationRotationY"
		;
connectAttr "MASH_Text_Trails:type1.animationRotationZ" "MASH_Text_Trails:shellDeformer1.animationRotationZ"
		;
connectAttr "MASH_Text_Trails:type1.animationScale" "MASH_Text_Trails:shellDeformer1.animationScale"
		;
connectAttr "MASH_Text_Trails:type1.animationScaleX" "MASH_Text_Trails:shellDeformer1.animationScaleX"
		;
connectAttr "MASH_Text_Trails:type1.animationScaleY" "MASH_Text_Trails:shellDeformer1.animationScaleY"
		;
connectAttr "MASH_Text_Trails:type1.animationScaleZ" "MASH_Text_Trails:shellDeformer1.animationScaleZ"
		;
connectAttr "MASH_Text_Trails:type1.vertsPerChar" "MASH_Text_Trails:shellDeformer1.vertsPerChar"
		;
connectAttr ":time1.o" "MASH_Text_Trails:shellDeformer1.ti";
connectAttr "MASH_Text_Trails:type1.grouping" "MASH_Text_Trails:shellDeformer1.grouping"
		;
connectAttr "MASH_Text_Trails:type1.animationMessage" "MASH_Text_Trails:shellDeformer1.typeMessage"
		;
connectAttr "MASH_Text_Trails:typeExtrude1.vertexGroupIds" "MASH_Text_Trails:shellDeformer1.vertexGroupIds"
		;
connectAttr "MASH_Text_Trails:groupParts4.og" "MASH_Text_Trails:tweak2.ip[0].ig"
		;
connectAttr "MASH_Text_Trails:groupId10.id" "MASH_Text_Trails:tweak2.ip[0].gi";
connectAttr "MASH_Text_Trails:shellDeformer1GroupId.msg" "MASH_Text_Trails:shellDeformer1Set.gn"
		 -na;
connectAttr "MASH_Text_Trails:typeMeshShape1.iog.og[2]" "MASH_Text_Trails:shellDeformer1Set.dsm"
		 -na;
connectAttr "MASH_Text_Trails:shellDeformer1.msg" "MASH_Text_Trails:shellDeformer1Set.ub[0]"
		;
connectAttr "MASH_Text_Trails:tweak2.og[0]" "MASH_Text_Trails:shellDeformer1GroupParts.ig"
		;
connectAttr "MASH_Text_Trails:shellDeformer1GroupId.id" "MASH_Text_Trails:shellDeformer1GroupParts.gi"
		;
connectAttr "MASH_Text_Trails:groupId10.msg" "MASH_Text_Trails:tweakSet2.gn" -na
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.iog.og[3]" "MASH_Text_Trails:tweakSet2.dsm"
		 -na;
connectAttr "MASH_Text_Trails:tweak2.msg" "MASH_Text_Trails:tweakSet2.ub[0]";
connectAttr "MASH_Text_Trails:typeMeshShape1Orig1.w" "MASH_Text_Trails:groupParts4.ig"
		;
connectAttr "MASH_Text_Trails:groupId10.id" "MASH_Text_Trails:groupParts4.gi";
connectAttr "MASH_Text_Trails:lambert2.oc" "MASH_Text_Trails:lambert2SG.ss";
connectAttr "MASH_Text_Trails:MASH1_Trails_Mesh.iog" "MASH_Text_Trails:lambert2SG.dsm"
		 -na;
connectAttr "MASH_Text_Trails:lambert2SG.msg" "MASH_Text_Trails:materialInfo2.sg"
		;
connectAttr "MASH_Text_Trails:lambert2.msg" "MASH_Text_Trails:materialInfo2.m";
connectAttr "MASH_Text_Trails:shellDeformer1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "MASH_Text_Trails:polyAutoProj1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "MASH_Text_Trails:tweak2.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "MASH_Text_Trails:tweak1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "MASH_Text_Trails:shellDeformer1Set.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr ":time1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1Set.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "MASH_Text_Trails:type1_animationRotationY.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "MASH_Text_Trails:typeBlinnSG.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "MASH_Text_Trails:typeMesh1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "MASH_Text_Trails:typeExtrude1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "MASH_Text_Trails:tweakSet2.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "MASH_Text_Trails:polyRemesh1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "MASH_Text_Trails:type1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1Orig1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "MASH_Text_Trails:tweakSet1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Distribute.outputPoints" "MASH_Text_Trails:MASH1.inputPoints"
		;
connectAttr "MASH_Text_Trails:MASH1_Distribute.waiterMessage" "MASH_Text_Trails:MASH1.waiterMessage"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.w" "MASH_Text_Trails:MASH1_Distribute.inM"
		;
connectAttr "MASH_Text_Trails:MASH1_ReproMeshShape.wim" "MASH_Text_Trails:MASH1_Repro.mmtx"
		;
connectAttr "MASH_Text_Trails:MASH1_ReproMeshShape.msg" "MASH_Text_Trails:MASH1_Repro.meshmessage"
		;
connectAttr "MASH_Text_Trails:MASH1.outputPoints" "MASH_Text_Trails:MASH1_Repro.inputPoints"
		;
connectAttr "MASH_Text_Trails:MASH1.instancerMessage" "MASH_Text_Trails:MASH1_Repro.instancerMessage"
		;
connectAttr "MASH_Text_Trails:pSphere1.msg" "MASH_Text_Trails:MASH1_Repro.instancedGroup[0].gmsg"
		;
connectAttr "MASH_Text_Trails:pSphere1.wm" "MASH_Text_Trails:MASH1_Repro.instancedGroup[0].gmtx"
		;
connectAttr "MASH_Text_Trails:pSphereShape1.o" "MASH_Text_Trails:MASH1_Repro.instancedGroup[0].inMesh[0].mesh"
		;
connectAttr "MASH_Text_Trails:pSphereShape1.wm" "MASH_Text_Trails:MASH1_Repro.instancedGroup[0].inMesh[0].matrix"
		;
connectAttr "MASH_Text_Trails:groupId11.id" "MASH_Text_Trails:MASH1_Repro.instancedGroup[0].inMesh[0].groupId[0]"
		;
connectAttr ":time1.o" "MASH_Text_Trails:MASH1_Trails.tm";
connectAttr "MASH_Text_Trails:MASH1.outputPoints" "MASH_Text_Trails:MASH1_Trails.inputPoints"
		;
connectAttr "MASH_Text_Trails:nurbsCircleShape1.ws" "MASH_Text_Trails:MASH1_Trails.inputCurve"
		;
connectAttr "MASH_Text_Trails:type1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[0].dn"
		;
connectAttr "MASH_Text_Trails:lambert2SG.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[1].dn"
		;
connectAttr "MASH_Text_Trails:typeExtrude1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[2].dn"
		;
connectAttr "MASH_Text_Trails:tweak1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[3].dn"
		;
connectAttr "MASH_Text_Trails:vectorAdjust1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[4].dn"
		;
connectAttr "MASH_Text_Trails:shellDeformer1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[5].dn"
		;
connectAttr "MASH_Text_Trails:makeNurbCircle1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[6].dn"
		;
connectAttr "MASH_Text_Trails:nurbsCircleShape1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[7].dn"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[8].dn"
		;
connectAttr "MASH_Text_Trails:tweak2.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[9].dn"
		;
connectAttr "MASH_Text_Trails:typeMeshShape1Orig1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[10].dn"
		;
connectAttr "MASH_Text_Trails:type1_animationRotationY.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[11].dn"
		;
connectAttr "MASH_Text_Trails:polyRemesh1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[12].dn"
		;
connectAttr ":time1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[13].dn"
		;
connectAttr "MASH_Text_Trails:polyAutoProj1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[14].dn"
		;
connectAttr "MASH_Text_Trails:MASH1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[15].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Distribute.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[16].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Repro.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[17].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_ReproMeshShape.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[18].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_ReproMesh.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[19].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Trails_Mesh.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[20].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Trails.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[21].dn"
		;
connectAttr "MASH_Text_Trails:MASH1_Trails1.msg" "MASH_Text_Trails:MayaNodeEditorSavedTabsInfo1.tgi[0].ni[22].dn"
		;
connectAttr "MASH_Text_Trails:typeBlinnSG.pa" ":renderPartition.st" -na;
connectAttr "MASH_Text_Trails:lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "MASH_Text_Trails:typeBlinn.msg" ":defaultShaderList1.s" -na;
connectAttr "MASH_Text_Trails:lambert2.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "MASH_Text_Trails:defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "MASH_Text_Trails:MASH_Text_Trails_defaultRenderLayer.msg" ":defaultRenderingList1.r"
		 -na;
connectAttr "MASH_Text_Trails:areaLightShape1.ltd" ":lightList1.l" -na;
connectAttr "MASH_Text_Trails:areaLightShape2.ltd" ":lightList1.l" -na;
connectAttr "MASH_Text_Trails:pSphereShape1.iog" ":initialShadingGroup.dsm" -na;
connectAttr "MASH_Text_Trails:MASH1_ReproMeshShape.iog.og[0]" ":initialShadingGroup.dsm"
		 -na;
connectAttr "MASH_Text_Trails:groupId11.msg" ":initialShadingGroup.gn" -na;
connectAttr "MASH_Text_Trails:areaLight1.iog" ":defaultLightSet.dsm" -na;
connectAttr "MASH_Text_Trails:areaLight2.iog" ":defaultLightSet.dsm" -na;
// End of MASH_Text_Trails.ma
