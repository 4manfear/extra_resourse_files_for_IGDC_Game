//Maya ASCII 2017 scene
//Name: MASH_Influence.ma
//Last modified: Tue, May 31, 2016 03:23:16 PM
//Codeset: 1252
requires maya "2017";
requires -nodeType "MASH_Waiter" -nodeType "MASH_Influence" -nodeType "MASH_Distribute"
		 -nodeType "MASH_Repro" "MASH" "400";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2017";
fileInfo "version" "2017";
fileInfo "cutIdentifier" "201605302145-996578";
fileInfo "osv" "Microsoft Windows 8 Business Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "2EEAC62E-4C70-3F43-C54B-828C4867ECE8";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 45.974456146071482 42.347602211516893 18.388470534785931 ;
	setAttr ".r" -type "double3" -40.538352729603119 68.200000000000415 -8.564432287872012e-015 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "F57F50E5-40A5-FA05-A048-BAB5D67491CA";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 65.154477049551943;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".ai_translator" -type "string" "perspective";
createNode transform -s -n "top";
	rename -uid "DB1C47A3-4908-94F8-44DF-70BC83C7FD8F";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "05F35CC2-48E8-5289-369C-97837F3A922C";
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
	rename -uid "3A14CED8-4BF6-9AFC-FCBB-B49B1D3655A5";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "24802A35-4C29-C294-0254-1DB6D0B4FCC4";
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
	rename -uid "A0CAA557-4B68-035A-7F59-50949C99151E";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "4E181AC6-4EDD-6BAA-2870-8C8A330F7E5E";
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
createNode transform -n "MASH_Influence:Tree";
	rename -uid "5DCC6B12-46DB-3FF4-B9C6-04A7E41029F9";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".v" no;
createNode transform -n "MASH_Influence:pPyramid2" -p "MASH_Influence:Tree";
	rename -uid "54AC5CC8-41C6-76D8-37D8-DA90CA8BEDF6";
	setAttr ".t" -type "double3" 0 4.5320898497028557 0 ;
	setAttr ".r" -type "double3" 0 -21.831995601924376 0 ;
createNode mesh -n "MASH_Influence:pPyramidShape2" -p "MASH_Influence:pPyramid2";
	rename -uid "55B864FE-4788-40D7-22AC-158D1DE3ECF7";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:pPyramid3" -p "MASH_Influence:Tree";
	rename -uid "1C51BF4E-4EEB-844E-78B1-22B6A469E1C1";
	setAttr ".t" -type "double3" 0 3.8708525774338804 0 ;
	setAttr ".r" -type "double3" 0 23.818200693687107 0 ;
	setAttr ".s" -type "double3" 1.9477840934035067 1.9477840934035067 1.9477840934035067 ;
createNode mesh -n "MASH_Influence:pPyramidShape3" -p "MASH_Influence:pPyramid3";
	rename -uid "8A1B5C66-4104-ECFC-381C-75BF46AA415B";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.5 0.16666666 0.41666666
		 0.25 0.5 0.33333334 0.58333331 0.25 0.5 0.083333328 0.33333331 0.24999999 0.5 0.41666669
		 0.66666669 0.25 0.50000006 0 0.25 0.24999999 0.5 0.5 0.75 0.25 0.25 0.5 0.375 0.5
		 0.5 0.5 0.625 0.5 0.75 0.5 0.30000001 0.60000002 0.40000001 0.60000002 0.5 0.60000002
		 0.60000002 0.60000002 0.70000005 0.60000002 0.35000002 0.70000005 0.42500001 0.70000005
		 0.5 0.70000005 0.57499999 0.70000005 0.64999998 0.70000005 0.40000004 0.80000007
		 0.45000005 0.80000007 0.50000006 0.80000007 0.55000007 0.80000007 0.60000008 0.80000007
		 0.45000005 0.9000001 0.47500005 0.9000001 0.50000006 0.9000001 0.52500004 0.9000001
		 0.55000001 0.9000001 0.5 0.25 0.5 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 30 ".vt[0:29]"  3.0908616e-008 -0.35355338 -0.23570226 -0.23570226 -0.35355338 -2.0605746e-008
		 -1.0302873e-008 -0.35355338 0.23570226 0.23570226 -0.35355338 0 6.1817232e-008 -0.35355338 -0.47140452
		 -0.47140452 -0.35355338 -4.1211493e-008 -2.0605746e-008 -0.35355338 0.47140452 0.47140452 -0.35355338 0
		 9.2725848e-008 -0.35355338 -0.70710677 -0.70710677 -0.35355338 -6.1817239e-008 -3.090862e-008 -0.35355338 0.70710677
		 0.70710677 -0.35355338 0 7.4180676e-008 -0.21213204 -0.56568539 -0.56568539 -0.21213204 -4.9453789e-008
		 -2.4726894e-008 -0.21213204 0.56568539 0.56568539 -0.21213204 0 5.5635507e-008 -0.070710689 -0.42426404
		 -0.42426404 -0.070710689 -3.7090341e-008 -1.8545171e-008 -0.070710689 0.42426404
		 0.42426404 -0.070710689 0 3.7090338e-008 0.070710659 -0.2828427 -0.2828427 0.070710659 -2.4726894e-008
		 -1.2363447e-008 0.070710659 0.2828427 0.2828427 0.070710659 0 1.8545169e-008 0.21213201 -0.14142135
		 -0.14142135 0.21213201 -1.2363447e-008 -6.1817236e-009 0.21213201 0.14142135 0.14142135 0.21213201 0
		 0 -0.35355338 0 0 0.35355338 0;
	setAttr -s 60 ".ed[0:59]"  0 1 1 1 2 1 2 3 1 3 0 1 4 5 1 5 6 1 6 7 1
		 7 4 1 8 9 0 9 10 0 10 11 0 11 8 0 12 13 1 13 14 1 14 15 1 15 12 1 16 17 1 17 18 1
		 18 19 1 19 16 1 20 21 1 21 22 1 22 23 1 23 20 1 24 25 1 25 26 1 26 27 1 27 24 1 0 4 1
		 1 5 1 2 6 1 3 7 1 4 8 1 5 9 1 6 10 1 7 11 1 8 12 0 9 13 0 10 14 0 11 15 0 12 16 0
		 13 17 0 14 18 0 15 19 0 16 20 0 17 21 0 18 22 0 19 23 0 20 24 0 21 25 0 22 26 0 23 27 0
		 28 0 1 28 1 1 28 2 1 28 3 1 24 29 0 25 29 0 26 29 0 27 29 0;
	setAttr -s 32 -ch 120 ".fc[0:31]" -type "polyFaces" 
		f 4 0 29 -5 -29
		mu 0 4 0 1 5 4
		f 4 1 30 -6 -30
		mu 0 4 1 2 6 5
		f 4 2 31 -7 -31
		mu 0 4 2 3 7 6
		f 4 3 28 -8 -32
		mu 0 4 3 0 4 7
		f 4 4 33 -9 -33
		mu 0 4 4 5 9 8
		f 4 5 34 -10 -34
		mu 0 4 5 6 10 9
		f 4 6 35 -11 -35
		mu 0 4 6 7 11 10
		f 4 7 32 -12 -36
		mu 0 4 7 4 8 11
		f 4 8 37 -13 -37
		mu 0 4 12 13 18 17
		f 4 9 38 -14 -38
		mu 0 4 13 14 19 18
		f 4 10 39 -15 -39
		mu 0 4 14 15 20 19
		f 4 11 36 -16 -40
		mu 0 4 15 16 21 20
		f 4 12 41 -17 -41
		mu 0 4 17 18 23 22
		f 4 13 42 -18 -42
		mu 0 4 18 19 24 23
		f 4 14 43 -19 -43
		mu 0 4 19 20 25 24
		f 4 15 40 -20 -44
		mu 0 4 20 21 26 25
		f 4 16 45 -21 -45
		mu 0 4 22 23 28 27
		f 4 17 46 -22 -46
		mu 0 4 23 24 29 28
		f 4 18 47 -23 -47
		mu 0 4 24 25 30 29
		f 4 19 44 -24 -48
		mu 0 4 25 26 31 30
		f 4 20 49 -25 -49
		mu 0 4 27 28 33 32
		f 4 21 50 -26 -50
		mu 0 4 28 29 34 33
		f 4 22 51 -27 -51
		mu 0 4 29 30 35 34
		f 4 23 48 -28 -52
		mu 0 4 30 31 36 35
		f 3 -1 -53 53
		mu 0 3 1 0 37
		f 3 -2 -54 54
		mu 0 3 2 1 37
		f 3 -3 -55 55
		mu 0 3 3 2 37
		f 3 -4 -56 52
		mu 0 3 0 3 37
		f 3 24 57 -57
		mu 0 3 32 33 38
		f 3 25 58 -58
		mu 0 3 33 34 38
		f 3 26 59 -59
		mu 0 3 34 35 38
		f 3 27 56 -60
		mu 0 3 35 36 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:pPyramid4" -p "MASH_Influence:Tree";
	rename -uid "488B1296-457B-140F-CE77-9082B9FE3164";
	setAttr ".t" -type "double3" 0 2.8405932392227484 0 ;
	setAttr ".r" -type "double3" 0 -35.917090726081611 0 ;
	setAttr ".s" -type "double3" 1.9477840934035067 1.9477840934035067 1.9477840934035067 ;
createNode mesh -n "MASH_Influence:pPyramidShape4" -p "MASH_Influence:pPyramid4";
	rename -uid "052CC39C-4AD1-F3F9-4878-5DA4AE22BB84";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.5 0.16666666 0.41666666
		 0.25 0.5 0.33333334 0.58333331 0.25 0.5 0.083333328 0.33333331 0.24999999 0.5 0.41666669
		 0.66666669 0.25 0.50000006 0 0.25 0.24999999 0.5 0.5 0.75 0.25 0.25 0.5 0.375 0.5
		 0.5 0.5 0.625 0.5 0.75 0.5 0.30000001 0.60000002 0.40000001 0.60000002 0.5 0.60000002
		 0.60000002 0.60000002 0.70000005 0.60000002 0.35000002 0.70000005 0.42500001 0.70000005
		 0.5 0.70000005 0.57499999 0.70000005 0.64999998 0.70000005 0.40000004 0.80000007
		 0.45000005 0.80000007 0.50000006 0.80000007 0.55000007 0.80000007 0.60000008 0.80000007
		 0.45000005 0.9000001 0.47500005 0.9000001 0.50000006 0.9000001 0.52500004 0.9000001
		 0.55000001 0.9000001 0.5 0.25 0.5 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 30 ".vt[0:29]"  3.0908616e-008 -0.35355338 -0.23570226 -0.23570226 -0.35355338 -2.0605746e-008
		 -1.0302873e-008 -0.35355338 0.23570226 0.23570226 -0.35355338 0 6.1817232e-008 -0.35355338 -0.47140452
		 -0.47140452 -0.35355338 -4.1211493e-008 -2.0605746e-008 -0.35355338 0.47140452 0.47140452 -0.35355338 0
		 9.2725848e-008 -0.35355338 -0.70710677 -0.70710677 -0.35355338 -6.1817239e-008 -3.090862e-008 -0.35355338 0.70710677
		 0.70710677 -0.35355338 0 7.4180676e-008 -0.21213204 -0.56568539 -0.56568539 -0.21213204 -4.9453789e-008
		 -2.4726894e-008 -0.21213204 0.56568539 0.56568539 -0.21213204 0 5.5635507e-008 -0.070710689 -0.42426404
		 -0.42426404 -0.070710689 -3.7090341e-008 -1.8545171e-008 -0.070710689 0.42426404
		 0.42426404 -0.070710689 0 3.7090338e-008 0.070710659 -0.2828427 -0.2828427 0.070710659 -2.4726894e-008
		 -1.2363447e-008 0.070710659 0.2828427 0.2828427 0.070710659 0 1.8545169e-008 0.21213201 -0.14142135
		 -0.14142135 0.21213201 -1.2363447e-008 -6.1817236e-009 0.21213201 0.14142135 0.14142135 0.21213201 0
		 0 -0.35355338 0 0 0.35355338 0;
	setAttr -s 60 ".ed[0:59]"  0 1 1 1 2 1 2 3 1 3 0 1 4 5 1 5 6 1 6 7 1
		 7 4 1 8 9 0 9 10 0 10 11 0 11 8 0 12 13 1 13 14 1 14 15 1 15 12 1 16 17 1 17 18 1
		 18 19 1 19 16 1 20 21 1 21 22 1 22 23 1 23 20 1 24 25 1 25 26 1 26 27 1 27 24 1 0 4 1
		 1 5 1 2 6 1 3 7 1 4 8 1 5 9 1 6 10 1 7 11 1 8 12 0 9 13 0 10 14 0 11 15 0 12 16 0
		 13 17 0 14 18 0 15 19 0 16 20 0 17 21 0 18 22 0 19 23 0 20 24 0 21 25 0 22 26 0 23 27 0
		 28 0 1 28 1 1 28 2 1 28 3 1 24 29 0 25 29 0 26 29 0 27 29 0;
	setAttr -s 32 -ch 120 ".fc[0:31]" -type "polyFaces" 
		f 4 0 29 -5 -29
		mu 0 4 0 1 5 4
		f 4 1 30 -6 -30
		mu 0 4 1 2 6 5
		f 4 2 31 -7 -31
		mu 0 4 2 3 7 6
		f 4 3 28 -8 -32
		mu 0 4 3 0 4 7
		f 4 4 33 -9 -33
		mu 0 4 4 5 9 8
		f 4 5 34 -10 -34
		mu 0 4 5 6 10 9
		f 4 6 35 -11 -35
		mu 0 4 6 7 11 10
		f 4 7 32 -12 -36
		mu 0 4 7 4 8 11
		f 4 8 37 -13 -37
		mu 0 4 12 13 18 17
		f 4 9 38 -14 -38
		mu 0 4 13 14 19 18
		f 4 10 39 -15 -39
		mu 0 4 14 15 20 19
		f 4 11 36 -16 -40
		mu 0 4 15 16 21 20
		f 4 12 41 -17 -41
		mu 0 4 17 18 23 22
		f 4 13 42 -18 -42
		mu 0 4 18 19 24 23
		f 4 14 43 -19 -43
		mu 0 4 19 20 25 24
		f 4 15 40 -20 -44
		mu 0 4 20 21 26 25
		f 4 16 45 -21 -45
		mu 0 4 22 23 28 27
		f 4 17 46 -22 -46
		mu 0 4 23 24 29 28
		f 4 18 47 -23 -47
		mu 0 4 24 25 30 29
		f 4 19 44 -24 -48
		mu 0 4 25 26 31 30
		f 4 20 49 -25 -49
		mu 0 4 27 28 33 32
		f 4 21 50 -26 -50
		mu 0 4 28 29 34 33
		f 4 22 51 -27 -51
		mu 0 4 29 30 35 34
		f 4 23 48 -28 -52
		mu 0 4 30 31 36 35
		f 3 -1 -53 53
		mu 0 3 1 0 37
		f 3 -2 -54 54
		mu 0 3 2 1 37
		f 3 -3 -55 55
		mu 0 3 3 2 37
		f 3 -4 -56 52
		mu 0 3 0 3 37
		f 3 24 57 -57
		mu 0 3 32 33 38
		f 3 25 58 -58
		mu 0 3 33 34 38
		f 3 26 59 -59
		mu 0 3 34 35 38
		f 3 27 56 -60
		mu 0 3 35 36 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:pPyramid5" -p "MASH_Influence:Tree";
	rename -uid "F5E7C1F3-4A5A-DDE6-6B5E-C4B7ACD7F42D";
	setAttr ".t" -type "double3" 0 1.9884326151147063 0 ;
	setAttr ".s" -type "double3" 2.617497789712631 2.617497789712631 2.617497789712631 ;
createNode mesh -n "MASH_Influence:pPyramidShape5" -p "MASH_Influence:pPyramid5";
	rename -uid "7851481E-43D1-4654-41EA-698240E35A95";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 39 ".uvst[0].uvsp[0:38]" -type "float2" 0.5 0.16666666 0.41666666
		 0.25 0.5 0.33333334 0.58333331 0.25 0.5 0.083333328 0.33333331 0.24999999 0.5 0.41666669
		 0.66666669 0.25 0.50000006 0 0.25 0.24999999 0.5 0.5 0.75 0.25 0.25 0.5 0.375 0.5
		 0.5 0.5 0.625 0.5 0.75 0.5 0.30000001 0.60000002 0.40000001 0.60000002 0.5 0.60000002
		 0.60000002 0.60000002 0.70000005 0.60000002 0.35000002 0.70000005 0.42500001 0.70000005
		 0.5 0.70000005 0.57499999 0.70000005 0.64999998 0.70000005 0.40000004 0.80000007
		 0.45000005 0.80000007 0.50000006 0.80000007 0.55000007 0.80000007 0.60000008 0.80000007
		 0.45000005 0.9000001 0.47500005 0.9000001 0.50000006 0.9000001 0.52500004 0.9000001
		 0.55000001 0.9000001 0.5 0.25 0.5 1;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr -s 30 ".vt[0:29]"  3.0908616e-008 -0.35355338 -0.23570226 -0.23570226 -0.35355338 -2.0605746e-008
		 -1.0302873e-008 -0.35355338 0.23570226 0.23570226 -0.35355338 0 6.1817232e-008 -0.35355338 -0.47140452
		 -0.47140452 -0.35355338 -4.1211493e-008 -2.0605746e-008 -0.35355338 0.47140452 0.47140452 -0.35355338 0
		 9.2725848e-008 -0.35355338 -0.70710677 -0.70710677 -0.35355338 -6.1817239e-008 -3.090862e-008 -0.35355338 0.70710677
		 0.70710677 -0.35355338 0 7.4180676e-008 -0.21213204 -0.56568539 -0.56568539 -0.21213204 -4.9453789e-008
		 -2.4726894e-008 -0.21213204 0.56568539 0.56568539 -0.21213204 0 5.5635507e-008 -0.070710689 -0.42426404
		 -0.42426404 -0.070710689 -3.7090341e-008 -1.8545171e-008 -0.070710689 0.42426404
		 0.42426404 -0.070710689 0 3.7090338e-008 0.070710659 -0.2828427 -0.2828427 0.070710659 -2.4726894e-008
		 -1.2363447e-008 0.070710659 0.2828427 0.2828427 0.070710659 0 1.8545169e-008 0.21213201 -0.14142135
		 -0.14142135 0.21213201 -1.2363447e-008 -6.1817236e-009 0.21213201 0.14142135 0.14142135 0.21213201 0
		 0 -0.35355338 0 0 0.35355338 0;
	setAttr -s 60 ".ed[0:59]"  0 1 1 1 2 1 2 3 1 3 0 1 4 5 1 5 6 1 6 7 1
		 7 4 1 8 9 0 9 10 0 10 11 0 11 8 0 12 13 1 13 14 1 14 15 1 15 12 1 16 17 1 17 18 1
		 18 19 1 19 16 1 20 21 1 21 22 1 22 23 1 23 20 1 24 25 1 25 26 1 26 27 1 27 24 1 0 4 1
		 1 5 1 2 6 1 3 7 1 4 8 1 5 9 1 6 10 1 7 11 1 8 12 0 9 13 0 10 14 0 11 15 0 12 16 0
		 13 17 0 14 18 0 15 19 0 16 20 0 17 21 0 18 22 0 19 23 0 20 24 0 21 25 0 22 26 0 23 27 0
		 28 0 1 28 1 1 28 2 1 28 3 1 24 29 0 25 29 0 26 29 0 27 29 0;
	setAttr -s 32 -ch 120 ".fc[0:31]" -type "polyFaces" 
		f 4 0 29 -5 -29
		mu 0 4 0 1 5 4
		f 4 1 30 -6 -30
		mu 0 4 1 2 6 5
		f 4 2 31 -7 -31
		mu 0 4 2 3 7 6
		f 4 3 28 -8 -32
		mu 0 4 3 0 4 7
		f 4 4 33 -9 -33
		mu 0 4 4 5 9 8
		f 4 5 34 -10 -34
		mu 0 4 5 6 10 9
		f 4 6 35 -11 -35
		mu 0 4 6 7 11 10
		f 4 7 32 -12 -36
		mu 0 4 7 4 8 11
		f 4 8 37 -13 -37
		mu 0 4 12 13 18 17
		f 4 9 38 -14 -38
		mu 0 4 13 14 19 18
		f 4 10 39 -15 -39
		mu 0 4 14 15 20 19
		f 4 11 36 -16 -40
		mu 0 4 15 16 21 20
		f 4 12 41 -17 -41
		mu 0 4 17 18 23 22
		f 4 13 42 -18 -42
		mu 0 4 18 19 24 23
		f 4 14 43 -19 -43
		mu 0 4 19 20 25 24
		f 4 15 40 -20 -44
		mu 0 4 20 21 26 25
		f 4 16 45 -21 -45
		mu 0 4 22 23 28 27
		f 4 17 46 -22 -46
		mu 0 4 23 24 29 28
		f 4 18 47 -23 -47
		mu 0 4 24 25 30 29
		f 4 19 44 -24 -48
		mu 0 4 25 26 31 30
		f 4 20 49 -25 -49
		mu 0 4 27 28 33 32
		f 4 21 50 -26 -50
		mu 0 4 28 29 34 33
		f 4 22 51 -27 -51
		mu 0 4 29 30 35 34
		f 4 23 48 -28 -52
		mu 0 4 30 31 36 35
		f 3 -1 -53 53
		mu 0 3 1 0 37
		f 3 -2 -54 54
		mu 0 3 2 1 37
		f 3 -3 -55 55
		mu 0 3 3 2 37
		f 3 -4 -56 52
		mu 0 3 0 3 37
		f 3 24 57 -57
		mu 0 3 32 33 38
		f 3 25 58 -58
		mu 0 3 33 34 38
		f 3 26 59 -59
		mu 0 3 34 35 38
		f 3 27 56 -60
		mu 0 3 35 36 38;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:pCylinder1" -p "MASH_Influence:Tree";
	rename -uid "15D00DB2-459B-A10B-8525-D7BE19B58E67";
	setAttr ".t" -type "double3" 0 1.2354076353766754 0 ;
	setAttr ".s" -type "double3" 0.34435918501068619 1.2050090088365679 0.34435918501068619 ;
createNode mesh -n "MASH_Influence:pCylinderShape1" -p "MASH_Influence:pCylinder1";
	rename -uid "3931CDF1-4A05-1B7F-9BD4-768A35EE52DD";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:MASH1_ReproMesh";
	rename -uid "234F92B4-47C1-67FA-C99F-75A9664A3FFD";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
createNode mesh -n "MASH_Influence:MASH1_ReproMeshShape" -p "MASH_Influence:MASH1_ReproMesh";
	rename -uid "32940A93-462D-01BA-1326-D494D9352D33";
	setAttr -k off ".v";
	setAttr -s 10 ".iog[0].og";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode transform -n "MASH_Influence:MANUPULATE_THESE_LOCS";
	rename -uid "4AC896B9-474E-FE91-C494-88B53074FED7";
createNode transform -n "MASH_Influence:MASH1_Influence_loc3" -p "MASH_Influence:MANUPULATE_THESE_LOCS";
	rename -uid "84CC31C8-4500-3DF2-36B2-928526FD6246";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" -8.2901245268067267 3.5527136788005009e-015 -8.9855712635043261 ;
	setAttr ".s" -type "double3" 2.4261841848809458 2.4261841848809458 2.4261841848809458 ;
createNode locator -n "MASH_Influence:MASH1_Influence_loc3Shape" -p "MASH_Influence:MASH1_Influence_loc3";
	rename -uid "229D4DA4-4F16-B8E2-8D40-878660D1D200";
	setAttr -k off ".v";
createNode transform -n "MASH_Influence:MASH1_Influence_loc2" -p "MASH_Influence:MANUPULATE_THESE_LOCS";
	rename -uid "F7B66C6F-4381-209F-8F8B-8F845674C633";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" 8.444554066485928 0 8.7617892136208901 ;
	setAttr ".s" -type "double3" 2.2491989955865508 3.9922752599024318 2.2491989955865508 ;
createNode locator -n "MASH_Influence:MASH1_Influence_loc2Shape" -p "MASH_Influence:MASH1_Influence_loc2";
	rename -uid "4993ADD2-4338-8246-B201-3192ABBDD115";
	setAttr -k off ".v";
createNode transform -n "MASH_Influence:MASH1_Influence_loc1" -p "MASH_Influence:MANUPULATE_THESE_LOCS";
	rename -uid "08EC7E11-4011-5883-DF09-C193322DBA27";
	addAttr -ci true -sn "mashOutFilter" -ln "mashOutFilter" -min 0 -max 1 -at "bool";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" 9.3388567804669549 0 -10.462939947265543 ;
	setAttr ".s" -type "double3" 2.7457671684390625 2.7457671684390625 2.7457671684390625 ;
createNode locator -n "MASH_Influence:MASH1_Influence_loc1Shape" -p "MASH_Influence:MASH1_Influence_loc1";
	rename -uid "C27FAE95-4392-7F5C-4213-958A6FE59FDB";
	setAttr -k off ".v";
createNode transform -n "MASH_Influence:MASH1_Influence_loc" -p "MASH_Influence:MANUPULATE_THESE_LOCS";
	rename -uid "C8BA3BA6-4B8C-D644-E5F4-E6BEA9B651BF";
	setAttr ".ove" yes;
	setAttr ".ovc" 9;
	setAttr ".t" -type "double3" -9.6035344827435338 5.6843418860808015e-013 9.0816111079874275 ;
	setAttr ".r" -type "double3" 0 39.798076165337726 0 ;
	setAttr ".s" -type "double3" 3.8295290174142931 3.8295290174142931 3.8295290174142931 ;
createNode locator -n "MASH_Influence:MASH1_Influence_locShape" -p "MASH_Influence:MASH1_Influence_loc";
	rename -uid "B3DF0091-4BFF-A368-9074-C0A216013DEC";
	setAttr -k off ".v";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "F376F59D-4331-4AF7-AD94-929B67601AF9";
	setAttr -s 4 ".lnk";
	setAttr -s 4 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "3D6A1800-4B37-ADB7-2B00-D19D424834AB";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "21B78537-4DEB-EA2A-3F2C-69901AAF23FA";
createNode displayLayerManager -n "layerManager";
	rename -uid "57736AE2-4D49-26E4-65AD-0684EBACBE04";
createNode displayLayer -n "defaultLayer";
	rename -uid "9899238D-40CD-C60F-BCF0-2CB93BE2E64B";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "8B23AA17-4DBF-1443-4B40-36BB3B1C9C55";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "01D08607-429A-6137-1F4E-78B76EDF0FD8";
	setAttr ".g" yes;
createNode renderLayerManager -n "MASH_Influence:renderLayerManager";
	rename -uid "8A23D637-42A6-ADEF-8E78-6894EB5B3586";
createNode renderLayer -n "MASH_Influence:defaultRenderLayer";
	rename -uid "5A524911-40BB-D200-A5AC-EDB809A04F4A";
	setAttr ".g" yes;
createNode polyPyramid -n "MASH_Influence:pasted__polyPyramid1";
	rename -uid "42126DED-424E-AA21-8EF2-5AAE00F10477";
	setAttr ".sh" 5;
	setAttr ".sc" 3;
	setAttr ".cuv" 3;
createNode materialInfo -n "MASH_Influence:pasted__materialInfo1";
	rename -uid "98AF50DA-4CD1-B66E-B88C-A39C07B52F85";
createNode shadingEngine -n "MASH_Influence:pasted__lambert2SG";
	rename -uid "4AEEAC0D-4EB8-05B0-A5A7-E1A847AC7872";
	setAttr ".ihi" 0;
	setAttr -s 8 ".dsm";
	setAttr ".ro" yes;
	setAttr -s 4 ".gn";
createNode lambert -n "MASH_Influence:pasted__lambert2";
	rename -uid "2D75745D-4FEE-600C-87FD-4AB01F2040BF";
	setAttr ".c" -type "float3" 0.029216001 0.176 0.029216001 ;
createNode polyCylinder -n "MASH_Influence:pasted__polyCylinder1";
	rename -uid "D6974A40-4853-10CC-3117-FFB168BA76B4";
	setAttr ".r" 0.43000000000000005;
	setAttr ".sc" 1;
	setAttr ".cuv" 3;
createNode materialInfo -n "MASH_Influence:pasted__materialInfo2";
	rename -uid "9BA7730C-4A38-CBEA-C386-E9BBA7CEF7AE";
createNode shadingEngine -n "MASH_Influence:pasted__lambert3SG";
	rename -uid "28B4A391-4E0F-B347-82ED-38825C1FCD49";
	setAttr ".ihi" 0;
	setAttr -s 2 ".dsm";
	setAttr ".ro" yes;
createNode lambert -n "MASH_Influence:pasted__lambert3";
	rename -uid "D799C132-4DA5-2BA7-0C74-A5AC53489132";
	setAttr ".c" -type "float3" 0.074000001 0.033682335 0 ;
createNode MASH_Waiter -n "MASH_Influence:MASH1";
	rename -uid "CD2F8994-4A7B-CA6B-3E11-7E9CB705B52F";
	addAttr -s false -ci true -sn "instancerMessage" -ln "instancerMessage" -at "message";
	setAttr ".inArray" -type "vectorArray" 25 -12.5 0 -12.5 -6.25 0 -12.5 0 0 -12.5 6.25
		 0 -12.5 12.5 0 -12.5 -12.5 0 -6.25 -6.25 0 -6.25 0 0 -6.25 6.25 0 -6.25 12.5 0 -6.25 -12.5
		 0 0 -6.25 0 0 0 0 0 6.25 0 0 12.5 0 0 -12.5 0 6.25 -6.25 0 6.25 0 0 6.25 6.25 0 6.25 12.5
		 0 6.25 -12.5 0 12.5 -6.25 0 12.5 0 0 12.5 6.25 0 12.5 12.5 0 12.5 ;
	setAttr ".inScPP" -type "vectorArray" 25 0.81419860620069517 0.81419860620069517
		 0.81419860620069517 1.1334162855288019 1.1334162855288019 1.1334162855288019 0.61597057412353395
		 0.61597057412353395 0.61597057412353395 1.3898144664560406 1.3898144664560406 1.3898144664560406 1.3504066401087709
		 1.3504066401087709 1.3504066401087709 0.9281774608235781 0.9281774608235781 0.9281774608235781 1.3131333698430772
		 1.3131333698430772 1.3131333698430772 0.58559718116211201 0.58768400664918785 0.58559718116211201 1.0213796583548542
		 1.0351363997704144 1.0213796583548542 0.98265945906821506 0.99307559810276413 0.98265945906821506 0.65665926415626641
		 0.65665926415626641 0.65665926415626641 0.70105764781429947 0.70345538683334552 0.70105764781429947 0.33017185041057628
		 0.40162011300520228 0.33017185041057628 0.48183552388732326 0.70693151279509048 0.48183552388732326 0.42365236489857688
		 0.60812250428198578 0.42365236489857688 1.7831195132254456 1.7831195132254456 1.7831195132254456 1.6842976708698119
		 1.7007862017099216 1.6842976708698119 0.67307707920158755 0.91409595654515885 0.67307707920158755 1.2268583966567492
		 2.1630414731525578 1.2268583966567492 0.89313344728469324 1.5820073457104959 0.89313344728469324 1.6138344519522945
		 1.6138344519522945 1.6138344519522945 1.5250939909762702 1.5389359523888619 1.5250939909762702 0.61032890294060893
		 0.82157518376725036 0.61032890294060893 0.99166998067506507 1.7500006839687821 0.99166998067506507 0.74923675147439317
		 1.3298775931299249 0.74923675147439317 ;
	setAttr ".inRotPP" -type "vectorArray" 25 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0.22833094455671837
		 0 0 0.21258240811395929 0 0 0.013302763117595422 0 0 0 0 0 0 0 0 4.384191391871604
		 0 0 4.175632065776286 0 0 0.99953664579516044 0 0 0.0095037568367388053 0 0 0 0 0
		 18.407854855292094 0 0 17.110559398064812 0 0 3.7362910959694955 0 0 0.15112833145447332
		 0 0 0 0 0 16.771646364425518 0 0 15.663797713784579 0 0 3.5099857537687393 0 0 0.13665017293427928
		 0 0 0 0 ;
	setAttr ".cacheIdPP" -type "vectorArray" 0 ;
	setAttr ".cacheVisibilityPP" -type "vectorArray" 0 ;
	setAttr ".initSt" -type "vectorArray" 0 ;
	setAttr ".filename" -type "string" "/Applications/Autodesk/maya2017/plug-ins/MASH/Presets";
createNode MASH_Distribute -n "MASH_Influence:MASH1_Distribute";
	rename -uid "96F8FB1B-4C2D-8FA2-5991-9DB606D3F042";
	setAttr ".mapDirection" 4;
	setAttr ".fArray" -type "vectorArray" 0 ;
	setAttr ".inPPP" -type "vectorArray" 0 ;
	setAttr -s 3 ".scaleRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".rotationRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".bRmp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr ".bRmpX[0]"  0 1 1;
	setAttr ".bRmpY[0]"  0 1 1;
	setAttr ".bRmpZ[0]"  0 1 1;
	setAttr ".gridAmplitudeX" 25;
	setAttr ".gridAmplitudeZ" 25;
	setAttr ".grx" 5;
	setAttr ".grz" 5;
	setAttr ".rt" 6;
createNode MASH_Repro -n "MASH_Influence:MASH1_Repro";
	rename -uid "E12E38BB-44C0-204C-1804-3A83DFCBCF2D";
	addAttr -s false -ci true -sn "instancerMessage" -ln "instancerMessage" -at "message";
	setAttr -s 5 ".instancedGroup[0].inMesh";
	setAttr ".instancedGroup[0].inMesh[0].inShGroupId[0]"  -1;
	setAttr ".instancedGroup[0].inMesh[1].inShGroupId[0]"  -1;
	setAttr ".instancedGroup[0].inMesh[2].inShGroupId[0]"  -1;
	setAttr ".instancedGroup[0].inMesh[3].inShGroupId[0]"  -1;
	setAttr ".instancedGroup[0].inMesh[4].inShGroupId[0]"  -1;
createNode groupId -n "MASH_Influence:groupId1";
	rename -uid "DC69C3F4-467F-B10B-2579-E9AC0BAE6B2C";
createNode groupId -n "MASH_Influence:groupId2";
	rename -uid "07F16364-4381-202E-6342-60BFF5ECCA52";
createNode groupId -n "MASH_Influence:groupId3";
	rename -uid "63E42323-4166-A415-D2E7-E2B44DE435D1";
createNode groupId -n "MASH_Influence:groupId4";
	rename -uid "3F28B6D9-45A1-3FA2-6619-99854BCC70FC";
createNode groupId -n "MASH_Influence:groupId5";
	rename -uid "3D522208-4E66-FC72-237D-988413FEE41A";
createNode MASH_Influence -n "MASH_Influence:MASH1_Influence";
	rename -uid "51A308E4-4FF0-51E0-8336-AD9673C5E9E9";
	setAttr ".fArray" -type "vectorArray" 0 ;
	setAttr -s 4 ".guideMatrices";
	setAttr ".positionInPP" -type "vectorArray" 0 ;
	setAttr ".scaleInPP" -type "vectorArray" 0 ;
	setAttr ".rotationInPP" -type "vectorArray" 0 ;
	setAttr ".positionOutPP" -type "vectorArray" 0 ;
	setAttr ".scaleOutPP" -type "vectorArray" 0 ;
	setAttr ".rotationOutPP" -type "vectorArray" 0 ;
	setAttr ".falloffPower" 3.406976748084606;
createNode script -n "MASH_Influence:uiConfigurationScriptNode";
	rename -uid "A8673692-4C0C-3B70-9144-DEB33FEAEB6C";
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
		+ "            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `modelPanel -unParent -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            modelEditor -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n                -headsUpDisplay 1\n"
		+ "                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -rendererName \"vp2Renderer\" \n                -objectFilterShowInHUD 1\n                -isFiltered 0\n"
		+ "                -colorResolution 256 256 \n                -bumpResolution 512 512 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 1\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n"
		+ "                -ikHandles 1\n                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 1604\n                -height 836\n                -sceneRenderFilter 0\n                $editorName;\n            modelEditor -e -viewSelected 0 $editorName;\n            modelEditor -e \n                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\t}\n\t} else {\n"
		+ "\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n"
		+ "            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n"
		+ "            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1604\n            -height 836\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n"
		+ "            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n                -showShapes 0\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n"
		+ "                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -isSet 0\n                -isSetMember 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n"
		+ "                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                -renderFilterIndex 0\n                -selectionOrder \"chronological\" \n                -expandAttribute 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n"
		+ "            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n"
		+ "            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `outlinerPanel -unParent -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels `;\n\t\t\t$editorName = $panelName;\n            outlinerEditor -e \n"
		+ "                -showShapes 0\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 0\n                -showConnected 0\n                -showAnimCurvesOnly 0\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 1\n                -showAssets 1\n                -showContainedOnly 1\n                -showPublishedAsConnected 0\n                -showContainerContents 1\n                -ignoreDagHierarchy 0\n                -expandConnections 0\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 0\n                -highlightActive 1\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n"
		+ "                -transmitFilters 0\n                -setFilter \"defaultSetFilter\" \n                -showSetMembers 1\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 0\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n"
		+ "            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n"
		+ "\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"graphEditor\" -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n"
		+ "                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n"
		+ "                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n"
		+ "                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n"
		+ "                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n"
		+ "                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"dopeSheetPanel\" -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels `;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n"
		+ "                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n"
		+ "                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n"
		+ "                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n"
		+ "                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n"
		+ "                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n"
		+ "                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"timeEditorPanel\" -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"clipEditorPanel\" -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels `;\n"
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
		+ "\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"profilerPanel\" -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels `;\n\t\t}\n\t} else {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" == $panelName) {\n\t\tif ($useSceneConfig) {\n\t\t\t$panelName = `scriptedPanel -unParent  -type \"contentBrowserPanel\" -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels `;\n"
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
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1604\\n    -height 836\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 1\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1604\\n    -height 836\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        setFocus `paneLayout -q -p1 $gMainPane`;\n        sceneUIReplacement -deleteRemaining;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "MASH_Influence:sceneConfigurationScriptNode";
	rename -uid "D04B39E1-4D34-10A3-B4DD-45BD64AF9E08";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode nodeGraphEditorInfo -n "MASH_Influence:MayaNodeEditorSavedTabsInfo";
	rename -uid "2F657D8A-4BBB-AAB1-2A4C-10AC347AF899";
	setAttr ".def" no;
	setAttr ".tgi[0].tn" -type "string" "Untitled_1";
	setAttr ".tgi[0].vl" -type "double2" -677.38092546425287 -297.61903579272968 ;
	setAttr ".tgi[0].vh" -type "double2" 677.38092546425287 296.42855964955879 ;
	setAttr -s 32 ".tgi[0].ni";
	setAttr ".tgi[0].ni[0].x" 215.71427917480469;
	setAttr ".tgi[0].ni[0].y" -724.28570556640625;
	setAttr ".tgi[0].ni[0].nvs" 18304;
	setAttr ".tgi[0].ni[1].x" 215.71427917480469;
	setAttr ".tgi[0].ni[1].y" -597.14288330078125;
	setAttr ".tgi[0].ni[1].nvs" 18304;
	setAttr ".tgi[0].ni[2].x" 271.42855834960937;
	setAttr ".tgi[0].ni[2].y" 54.285713195800781;
	setAttr ".tgi[0].ni[2].nvs" 18304;
	setAttr ".tgi[0].ni[3].x" 834.28570556640625;
	setAttr ".tgi[0].ni[3].y" -352.85714721679687;
	setAttr ".tgi[0].ni[3].nvs" 18304;
	setAttr ".tgi[0].ni[4].x" -35.714286804199219;
	setAttr ".tgi[0].ni[4].y" 241.42857360839844;
	setAttr ".tgi[0].ni[4].nvs" 18304;
	setAttr ".tgi[0].ni[5].x" -35.714286804199219;
	setAttr ".tgi[0].ni[5].y" 350;
	setAttr ".tgi[0].ni[5].nvs" 18304;
	setAttr ".tgi[0].ni[6].x" 271.42855834960937;
	setAttr ".tgi[0].ni[6].y" -142.85714721679687;
	setAttr ".tgi[0].ni[6].nvs" 18304;
	setAttr ".tgi[0].ni[7].x" -35.714286804199219;
	setAttr ".tgi[0].ni[7].y" 54.285713195800781;
	setAttr ".tgi[0].ni[7].nvs" 18304;
	setAttr ".tgi[0].ni[8].x" 271.42855834960937;
	setAttr ".tgi[0].ni[8].y" 251.42857360839844;
	setAttr ".tgi[0].ni[8].nvs" 18304;
	setAttr ".tgi[0].ni[9].x" -1380;
	setAttr ".tgi[0].ni[9].y" 34.285713195800781;
	setAttr ".tgi[0].ni[9].nvs" 18304;
	setAttr ".tgi[0].ni[10].x" -740;
	setAttr ".tgi[0].ni[10].y" 428.57144165039062;
	setAttr ".tgi[0].ni[10].nvs" 18304;
	setAttr ".tgi[0].ni[11].x" 578.5714111328125;
	setAttr ".tgi[0].ni[11].y" 132.85714721679687;
	setAttr ".tgi[0].ni[11].nvs" 18304;
	setAttr ".tgi[0].ni[12].x" 885.71429443359375;
	setAttr ".tgi[0].ni[12].y" 182.85714721679687;
	setAttr ".tgi[0].ni[12].nvs" 18304;
	setAttr ".tgi[0].ni[13].x" -11.428571701049805;
	setAttr ".tgi[0].ni[13].y" -132.85714721679687;
	setAttr ".tgi[0].ni[13].nvs" 18304;
	setAttr ".tgi[0].ni[14].x" 885.71429443359375;
	setAttr ".tgi[0].ni[14].y" 84.285713195800781;
	setAttr ".tgi[0].ni[14].nvs" 18304;
	setAttr ".tgi[0].ni[15].x" 1192.857177734375;
	setAttr ".tgi[0].ni[15].y" 218.57142639160156;
	setAttr ".tgi[0].ni[15].nvs" 18304;
	setAttr ".tgi[0].ni[16].x" 271.42855834960937;
	setAttr ".tgi[0].ni[16].y" -44.285713195800781;
	setAttr ".tgi[0].ni[16].nvs" 18304;
	setAttr ".tgi[0].ni[17].x" 271.42855834960937;
	setAttr ".tgi[0].ni[17].y" 350;
	setAttr ".tgi[0].ni[17].nvs" 18304;
	setAttr ".tgi[0].ni[18].x" 1192.857177734375;
	setAttr ".tgi[0].ni[18].y" 120;
	setAttr ".tgi[0].ni[18].nvs" 18304;
	setAttr ".tgi[0].ni[19].x" 215.71427917480469;
	setAttr ".tgi[0].ni[19].y" -342.85714721679687;
	setAttr ".tgi[0].ni[19].nvs" 18304;
	setAttr ".tgi[0].ni[20].x" 885.71429443359375;
	setAttr ".tgi[0].ni[20].y" 338.57144165039062;
	setAttr ".tgi[0].ni[20].nvs" 18304;
	setAttr ".tgi[0].ni[21].x" 215.71427917480469;
	setAttr ".tgi[0].ni[21].y" -215.71427917480469;
	setAttr ".tgi[0].ni[21].nvs" 18304;
	setAttr ".tgi[0].ni[22].x" 271.42855834960937;
	setAttr ".tgi[0].ni[22].y" 152.85714721679687;
	setAttr ".tgi[0].ni[22].nvs" 18304;
	setAttr ".tgi[0].ni[23].x" 215.71427917480469;
	setAttr ".tgi[0].ni[23].y" 38.571430206298828;
	setAttr ".tgi[0].ni[23].nvs" 18304;
	setAttr ".tgi[0].ni[24].x" 271.42855834960937;
	setAttr ".tgi[0].ni[24].y" -241.42857360839844;
	setAttr ".tgi[0].ni[24].nvs" 18304;
	setAttr ".tgi[0].ni[25].x" 1021.4285888671875;
	setAttr ".tgi[0].ni[25].y" -345.71429443359375;
	setAttr ".tgi[0].ni[25].nvs" 18304;
	setAttr ".tgi[0].ni[26].x" -345.71429443359375;
	setAttr ".tgi[0].ni[26].y" 330;
	setAttr ".tgi[0].ni[26].nvs" 18304;
	setAttr ".tgi[0].ni[27].x" 1120;
	setAttr ".tgi[0].ni[27].y" -354.28570556640625;
	setAttr ".tgi[0].ni[27].nvs" 18304;
	setAttr ".tgi[0].ni[28].x" -148.57142639160156;
	setAttr ".tgi[0].ni[28].y" 231.42857360839844;
	setAttr ".tgi[0].ni[28].nvs" 18304;
	setAttr ".tgi[0].ni[29].x" 1168.5714111328125;
	setAttr ".tgi[0].ni[29].y" -368.57144165039063;
	setAttr ".tgi[0].ni[29].nvs" 18304;
	setAttr ".tgi[0].ni[30].x" -50;
	setAttr ".tgi[0].ni[30].y" 132.85714721679687;
	setAttr ".tgi[0].ni[30].nvs" 18304;
	setAttr ".tgi[0].ni[31].x" -508.57144165039062;
	setAttr ".tgi[0].ni[31].y" 12.857142448425293;
	setAttr ".tgi[0].ni[31].nvs" 18304;
select -ne :time1;
	setAttr ".o" 53;
	setAttr ".unw" 53;
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
	setAttr -s 2 ".r";
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".ren" -type "string" "arnold";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "MASH_Influence:pasted__polyPyramid1.out" "MASH_Influence:pPyramidShape2.i"
		;
connectAttr "MASH_Influence:pasted__polyCylinder1.out" "MASH_Influence:pCylinderShape1.i"
		;
connectAttr "MASH_Influence:MASH1_Repro.out" "MASH_Influence:MASH1_ReproMeshShape.i"
		;
connectAttr "MASH_Influence:groupId1.id" "MASH_Influence:MASH1_ReproMeshShape.iog.og[0].gid"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.mwc" "MASH_Influence:MASH1_ReproMeshShape.iog.og[0].gco"
		;
connectAttr "MASH_Influence:groupId2.id" "MASH_Influence:MASH1_ReproMeshShape.iog.og[1].gid"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.mwc" "MASH_Influence:MASH1_ReproMeshShape.iog.og[1].gco"
		;
connectAttr "MASH_Influence:groupId3.id" "MASH_Influence:MASH1_ReproMeshShape.iog.og[2].gid"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.mwc" "MASH_Influence:MASH1_ReproMeshShape.iog.og[2].gco"
		;
connectAttr "MASH_Influence:groupId4.id" "MASH_Influence:MASH1_ReproMeshShape.iog.og[3].gid"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.mwc" "MASH_Influence:MASH1_ReproMeshShape.iog.og[3].gco"
		;
connectAttr "MASH_Influence:groupId5.id" "MASH_Influence:MASH1_ReproMeshShape.iog.og[4].gid"
		;
connectAttr "MASH_Influence:pasted__lambert3SG.mwc" "MASH_Influence:MASH1_ReproMeshShape.iog.og[4].gco"
		;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "MASH_Influence:pasted__lambert2SG.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "MASH_Influence:pasted__lambert3SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "MASH_Influence:pasted__lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "MASH_Influence:pasted__lambert3SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "MASH_Influence:renderLayerManager.rlmi[0]" "MASH_Influence:defaultRenderLayer.rlid"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.msg" "MASH_Influence:pasted__materialInfo1.sg"
		;
connectAttr "MASH_Influence:pasted__lambert2.msg" "MASH_Influence:pasted__materialInfo1.m"
		;
connectAttr "MASH_Influence:pasted__lambert2.oc" "MASH_Influence:pasted__lambert2SG.ss"
		;
connectAttr "MASH_Influence:pPyramidShape2.iog" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:pPyramidShape3.iog" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:pPyramidShape4.iog" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:pPyramidShape5.iog" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.iog.og[0]" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.iog.og[1]" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.iog.og[2]" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.iog.og[3]" "MASH_Influence:pasted__lambert2SG.dsm"
		 -na;
connectAttr "MASH_Influence:groupId1.msg" "MASH_Influence:pasted__lambert2SG.gn"
		 -na;
connectAttr "MASH_Influence:groupId2.msg" "MASH_Influence:pasted__lambert2SG.gn"
		 -na;
connectAttr "MASH_Influence:groupId3.msg" "MASH_Influence:pasted__lambert2SG.gn"
		 -na;
connectAttr "MASH_Influence:groupId4.msg" "MASH_Influence:pasted__lambert2SG.gn"
		 -na;
connectAttr "MASH_Influence:pasted__lambert3SG.msg" "MASH_Influence:pasted__materialInfo2.sg"
		;
connectAttr "MASH_Influence:pasted__lambert3.msg" "MASH_Influence:pasted__materialInfo2.m"
		;
connectAttr "MASH_Influence:pasted__lambert3.oc" "MASH_Influence:pasted__lambert3SG.ss"
		;
connectAttr "MASH_Influence:pCylinderShape1.iog" "MASH_Influence:pasted__lambert3SG.dsm"
		 -na;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.iog.og[4]" "MASH_Influence:pasted__lambert3SG.dsm"
		 -na;
connectAttr "MASH_Influence:groupId5.msg" "MASH_Influence:pasted__lambert3SG.gn"
		 -na;
connectAttr "MASH_Influence:MASH1_Influence.outputPoints" "MASH_Influence:MASH1.inputPoints"
		;
connectAttr "MASH_Influence:MASH1_Distribute.waiterMessage" "MASH_Influence:MASH1.waiterMessage"
		;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.wim" "MASH_Influence:MASH1_Repro.mmtx"
		;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.msg" "MASH_Influence:MASH1_Repro.meshmessage"
		;
connectAttr "MASH_Influence:MASH1.outputPoints" "MASH_Influence:MASH1_Repro.inputPoints"
		;
connectAttr "MASH_Influence:MASH1.instancerMessage" "MASH_Influence:MASH1_Repro.instancerMessage"
		;
connectAttr "MASH_Influence:Tree.msg" "MASH_Influence:MASH1_Repro.instancedGroup[0].gmsg"
		;
connectAttr "MASH_Influence:Tree.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].gmtx"
		;
connectAttr "MASH_Influence:pPyramidShape2.o" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[0].mesh"
		;
connectAttr "MASH_Influence:pPyramidShape2.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[0].matrix"
		;
connectAttr "MASH_Influence:groupId1.id" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[0].groupId[0]"
		;
connectAttr "MASH_Influence:pPyramidShape3.o" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[1].mesh"
		;
connectAttr "MASH_Influence:pPyramidShape3.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[1].matrix"
		;
connectAttr "MASH_Influence:groupId2.id" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[1].groupId[0]"
		;
connectAttr "MASH_Influence:pPyramidShape4.o" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[2].mesh"
		;
connectAttr "MASH_Influence:pPyramidShape4.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[2].matrix"
		;
connectAttr "MASH_Influence:groupId3.id" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[2].groupId[0]"
		;
connectAttr "MASH_Influence:pPyramidShape5.o" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[3].mesh"
		;
connectAttr "MASH_Influence:pPyramidShape5.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[3].matrix"
		;
connectAttr "MASH_Influence:groupId4.id" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[3].groupId[0]"
		;
connectAttr "MASH_Influence:pCylinderShape1.o" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[4].mesh"
		;
connectAttr "MASH_Influence:pCylinderShape1.wm" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[4].matrix"
		;
connectAttr "MASH_Influence:groupId5.id" "MASH_Influence:MASH1_Repro.instancedGroup[0].inMesh[4].groupId[0]"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc.wm" "MASH_Influence:MASH1_Influence.guideMatrices[0]"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc1.wm" "MASH_Influence:MASH1_Influence.guideMatrices[1]"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc2.wm" "MASH_Influence:MASH1_Influence.guideMatrices[2]"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc3.wm" "MASH_Influence:MASH1_Influence.guideMatrices[3]"
		;
connectAttr "MASH_Influence:MASH1_Distribute.outputPoints" "MASH_Influence:MASH1_Influence.inputPoints"
		;
connectAttr "MASH_Influence:pPyramid5.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[0].dn"
		;
connectAttr "MASH_Influence:pPyramid3.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[1].dn"
		;
connectAttr "MASH_Influence:pPyramidShape2.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[2].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_locShape.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[3].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[4].dn"
		;
connectAttr "MASH_Influence:pasted__polyCylinder1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[5].dn"
		;
connectAttr "MASH_Influence:pPyramidShape4.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[6].dn"
		;
connectAttr "MASH_Influence:pasted__polyPyramid1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[7].dn"
		;
connectAttr "MASH_Influence:MASH1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[8].dn"
		;
connectAttr "MASH_Influence:MASH1_Distribute.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[9].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[10].dn"
		;
connectAttr "MASH_Influence:MASH1_Repro.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[11].dn"
		;
connectAttr "MASH_Influence:MASH1_ReproMeshShape.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[12].dn"
		;
connectAttr "MASH_Influence:MASH1_ReproMesh.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[13].dn"
		;
connectAttr "MASH_Influence:pasted__lambert2.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[14].dn"
		;
connectAttr "MASH_Influence:pasted__lambert3SG.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[15].dn"
		;
connectAttr "MASH_Influence:pPyramidShape3.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[16].dn"
		;
connectAttr "MASH_Influence:pCylinderShape1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[17].dn"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[18].dn"
		;
connectAttr "MASH_Influence:pPyramid2.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[19].dn"
		;
connectAttr "MASH_Influence:pasted__lambert3.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[20].dn"
		;
connectAttr "MASH_Influence:pCylinder1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[21].dn"
		;
connectAttr "MASH_Influence:Tree.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[22].dn"
		;
connectAttr "MASH_Influence:pPyramid4.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[23].dn"
		;
connectAttr "MASH_Influence:pPyramidShape5.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[24].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc1Shape.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[25].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc1.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[26].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc2Shape.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[27].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc2.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[28].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc3Shape.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[29].dn"
		;
connectAttr "MASH_Influence:MASH1_Influence_loc3.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[30].dn"
		;
connectAttr "MASH_Influence:MANUPULATE_THESE_LOCS.msg" "MASH_Influence:MayaNodeEditorSavedTabsInfo.tgi[0].ni[31].dn"
		;
connectAttr "MASH_Influence:pasted__lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "MASH_Influence:pasted__lambert3SG.pa" ":renderPartition.st" -na;
connectAttr "MASH_Influence:pasted__lambert2.msg" ":defaultShaderList1.s" -na;
connectAttr "MASH_Influence:pasted__lambert3.msg" ":defaultShaderList1.s" -na;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "MASH_Influence:defaultRenderLayer.msg" ":defaultRenderingList1.r" -na
		;
// End of MASH_Influence.ma
