//Maya ASCII 7.0ff10 (Candidate) scene
//Name: NightShade.ma
//Last modified: Mon, Jul 11, 2005 07:19:06 PM
requires maya "7.0ff10 (Candidate)";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya Unlimited 7.0";
fileInfo "version" "7.0CG";
fileInfo "cutIdentifier" "200506192018-000000";
fileInfo "osv" "Microsoft Windows XP Service Pack 1 (Build 2600)\n";
createNode transform -s -n "persp";
	setAttr ".rp" -type "double3" 6.6613381477509392e-016 -2.2204460492503131e-016 
		-8.8817841970012523e-016 ;
	setAttr ".rpt" -type "double3" -1.3644860744432694e-015 -2.1022415196876547e-016 
		1.0885383121725853e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v";
	setAttr ".fl" 34.999999999999979;
	setAttr ".coi" 8.7466785366023565;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".tp" -type "double3" 3.5290715776385753 0.89499889583823411 4.4282624843976652 ;
	setAttr ".hc" -type "string" "viewSet -p %camera";
	setAttr ".col" -type "float3" 1 1 1 ;
createNode transform -s -n "top";
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v";
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "strokeTeapot1";
createNode stroke -n "strokeShapeTeapot1" -p "strokeTeapot1";
	setAttr ".cch" yes;
	setAttr -k off ".v" no;
	setAttr ".dpc" 100;
	setAttr ".mvbs" 3350;
	setAttr ".fvbs" 2400;
	setAttr ".lvbs" 1450;
	setAttr ".mpl" 100000;
	setAttr ".usn" yes;
	setAttr ".nml" -type "double3" 0 1 0 ;
	setAttr ".pcv[0].smp" 4;
	setAttr ".ps1" 0.58540000000000003;
	setAttr ".psc[0]"  0 1 1;
createNode transform -n "curveTeapot";
	setAttr ".v" no;
createNode nurbsCurve -n "curveTeapotShape" -p "curveTeapot";
	setAttr -k off ".v";
	setAttr ".cc" -type "nurbsCurve" 
		2 2 0 no 3
		5 0 0 1 2 2
		4
		3.318276 0 4.3617739999999996
		3.5035310000000002 0 4.2422880000000003
		3.7807019999999998 0 4.0635180000000002
		4.2407630000000003 0 3.766788
		;
createNode transform -n "pfxToon1";
createNode pfxToon -n "pfxToonShape1" -p "pfxToon1";
	setAttr -k off ".v";
	setAttr ".dpc" 100;
	setAttr -s 3 ".ins";
	setAttr ".iln" yes;
	setAttr ".lwd" 0.009;
	setAttr ".lop" 0.11570000000000001;
	setAttr ".clw" 0.90900000000000003;
	setAttr ".blw" 0.82640000000000002;
	setAttr ".ilw" 0.82640000000000002;
	setAttr ".lbw" 1;
	setAttr ".amn" 35.703000000000003;
	setAttr ".amx" 40.164;
	setAttr ".hco" no;
	setAttr ".cmo" yes;
	setAttr -s 2 ".cwd[0:1]"  0 1 3 0.22142857 0.60000002 3;
	setAttr ".cwm" 0.21488000000000002;
	setAttr ".bwm" 0.54544000000000004;
	setAttr ".imd" 0.099160000000000012;
	setAttr ".rpf" yes;
	setAttr ".rcr" yes;
	setAttr ".rbd" yes;
	setAttr ".rin" yes;
	setAttr ".msl" 0.01;
	setAttr ".mns" 0.00826;
	setAttr ".spw" yes;
	setAttr ".dsl" 0.23966000000000001;
	setAttr ".mpw" 0.5786;
	setAttr ".mxp" 24.800000000000001;
	setAttr ".pcl" -type "float3" 1 1 1 ;
	setAttr ".ccl" -type "float3" 1 1 1 ;
	setAttr ".bcl" -type "float3" 1 1 1 ;
	setAttr ".icl" -type "float3" 0.80992001 0.80992001 0.80992001 ;
createNode transform -n "teapot1MeshGroup";
createNode transform -n "teapot1Main" -p "teapot1MeshGroup";
createNode mesh -n "teapot1MainShape" -p "teapot1Main";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "teapot1Leaf" -p "teapot1MeshGroup";
createNode mesh -n "teapot1LeafShape" -p "teapot1Leaf";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "teapot1Flower" -p "teapot1MeshGroup";
createNode mesh -n "teapot1FlowerShape" -p "teapot1Flower";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode transform -n "annotationLocator1" -p "teapot1MeshGroup";
	setAttr ".t" -type "double3" 3.4042099714279175 0.89500065198342327 4.3800406455993652 ;
createNode locator -n "annotationLocator1Shape" -p "annotationLocator1";
	setAttr -k off ".v";
createNode transform -n "annotation1" -p "annotationLocator1";
	setAttr ".t" -type "double3" 0.41442160833648778 0.88037637586165474 0.46530488416352966 ;
createNode annotationShape -n "annotationShape1" -p "annotation1";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr -k off ".v";
	setAttr ".txt" -type "string" "Description (see attribute editor notes)";
	setAttr ".nts" -type "string" "This simulates a nighttime toon look with edge highlighting. The translucence on the ramp shader combined with the large depthmap filtersize on the spotlight allow the light boundary to be relatively simplified and smooth.\r\n\r\nThe brush assigned to the toon lines has illumination enabled, but with translucence = 1 so that the line does not look like a tube. This allows it to be dark where the line is in shadow regions. Also there is a bit of light based width on the brush so that the lines are thicker in the shadow regions as well (note that light based width attribute on the toon node is ignored when a brush is assigned to it)";
createNode transform -n "spotLight1";
	setAttr ".t" -type "double3" -0.12906336207195501 3.498262490559326 12.879807000579582 ;
	setAttr ".r" -type "double3" -16.185650105968104 -23.21303360058582 -2.3013750664151396e-013 ;
createNode spotLight -n "spotLightShape1" -p "spotLight1";
	setAttr -k off ".v";
	setAttr ".col" 9.6942633485849026;
	setAttr ".dms" yes;
	setAttr ".md" no;
	setAttr ".fs" 10;
	setAttr ".db" 0.0099999997764825821;
	setAttr ".ca" 31.244729577951308;
createNode lightLinker -n "lightLinker1";
	setAttr -s 8 ".lnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode brush -n "teapot1";
	setAttr ".gsc" 4.475;
	setAttr ".dep" yes;
	setAttr ".csd" yes;
	setAttr ".lvs" yes;
	setAttr ".flw" yes;
	setAttr ".brt" 5;
	setAttr ".bwd" 0.28048800000000002;
	setAttr ".sdn" 12.8096;
	setAttr ".sft" 0;
	setAttr ".cl1" -type "float3" 0.926 0.926 0.926 ;
	setAttr ".spc" -type "float3" 1 0.94718665 0.72799999 ;
	setAttr ".spe" 0.6;
	setAttr ".spp" 206.71000000000001;
	setAttr ".trn" 0.3;
	setAttr ".glc" -type "float3" 0.53333336 0.53333336 0.53333336 ;
	setAttr ".gls" 1;
	setAttr ".dps" 0.6504;
	setAttr ".rll" yes;
	setAttr ".ldr" -type "double3" -0.5 -0.5 -0.5 ;
	setAttr ".grn" 1;
	setAttr ".tfl" no;
	setAttr ".tub" yes;
	setAttr ".tps" 0.070000000000000007;
	setAttr ".trd" 0;
	setAttr ".lnx" 0.40000000000000002;
	setAttr ".lnn" 0.40000000000000002;
	setAttr ".sgm" 66;
	setAttr ".tw1" 0.5;
	setAttr ".tw2" 0.5;
	setAttr ".wdb" -0.262;
	setAttr ".elm" 1;
	setAttr ".elx" 1;
	setAttr ".azn" 0;
	setAttr ".azx" 0;
	setAttr ".twd" 0;
	setAttr ".bnb" -0.2562;
	setAttr ".ddl" 0;
	setAttr ".wgf" 5;
	setAttr ".crf" 7.7661;
	setAttr ".nof" 1.26698;
	setAttr ".smd" 5;
	setAttr ".srd" 0.17476;
	setAttr ".spa" 26.214;
	setAttr ".ssd" 0.6602;
	setAttr ".slb" 0.00972;
	setAttr ".slt" 0.02912;
	setAttr ".nbr" 1;
	setAttr ".bdr" 0.26214;
	setAttr ".mbr" yes;
	setAttr ".mms" 0;
	setAttr ".cva" 0.204;
	setAttr ".tin" 2;
	setAttr ".tur" 0.004;
	setAttr ".trf" 0.2233;
	setAttr ".trs" 0.2233;
	setAttr ".dfm" -0.10000000000000001;
	setAttr ".dfx" 0.09708;
	setAttr ".tic" 3;
	setAttr ".ta1" 129.42;
	setAttr ".ta2" 55.923000000000002;
	setAttr ".ttw" 0.32040000000000002;
	setAttr ".twl" 0.5786;
	setAttr ".tst" 0.30578;
	setAttr ".ntc" 1;
	setAttr ".twb" 0.04958;
	setAttr ".twt" 0.42976;
	setAttr ".bat" yes;
	setAttr ".ll1" 59.505000000000003;
	setAttr ".ll2" 65.454;
	setAttr ".lbn" -0.7;
	setAttr ".lcl[0]"  0.33571428 0.5 1;
	setAttr ".ltwl" 1;
	setAttr ".lsg" 7;
	setAttr ".lst" 0.52066;
	setAttr ".nlc" 1;
	setAttr ".lft" -0.011560000000000001;
	setAttr ".lln" 0.103611;
	setAttr ".leb" 0.14050000000000001;
	setAttr ".let" 0.0909;
	setAttr ".lsd" 0.80700000000000005;
	setAttr ".ltr" 0.3;
	setAttr ".lsp" 0.6;
	setAttr ".lc1" -type "float3" 1 1 1 ;
	setAttr ".lc2" -type "float3" 1 1 1 ;
	setAttr ".lim" -type "string" "sideleaf.rgb";
	setAttr ".fw1" -58.014000000000003;
	setAttr ".fw2" -60.990000000000002;
	setAttr ".ftw" 0;
	setAttr ".pbn" -2.7272;
	setAttr ".pcl[0]"  0.11428571 0.5 1;
	setAttr ".psg" 30;
	setAttr ".fst" 0.6033;
	setAttr ".nfl" 1;
	setAttr ".pft" 0.33058;
	setAttr ".pln" 0.36364000000000002;
	setAttr ".ptb" 0.07438;
	setAttr ".ptt" 0.0909;
	setAttr ".fsd" 1;
	setAttr ".ftr" 0.3;
	setAttr ".fsp" 0.6033;
	setAttr ".pc1" -type "float3" 1 1 1 ;
	setAttr ".pc2" -type "float3" 1 0.885732 0.85299999 ;
	setAttr ".fls" 1;
	setAttr ".smp" 1;
	setAttr ".spl" 1;
	setAttr ".txt" 3;
	setAttr ".mmd" 3;
	setAttr ".dsc" 0.041320000000000003;
	setAttr ".bmi" 0.90908;
	setAttr ".bbl" 1.47108;
	setAttr ".lid" no;
	setAttr ".al1" 0;
	setAttr ".al2" 1;
	setAttr ".rpu" 0.3966;
	setAttr ".bmt" 0.9256;
	setAttr ".smr" 0.20326;
	setAttr ".imn" -type "string" "wrapBark.iff";
	setAttr ".fra" 0.52066;
	setAttr ".tbs" 50;
	setAttr ".ppl" yes;
	setAttr -s 13 ".wsc[0:12]"  0 0.001 3 0.85000002 0.31999999 3 
		0.75714284 0.54000002 3 0.40714285 0.86000001 3 0.092857145 0.77999997 3 
		1 0.003 3 0.72857141 0.41999999 1 0.72142857 0.56 1 0.87857145 0.079999998 
		3 0.9357143 0.14 3 0.97857141 0.18000001 3 0.028571429 0.46000001 3 0.6857143 
		0.60000002 3;
	setAttr -s 6 ".lws[0:5]"  0 1 3 0.60000002 0.74000001 3 1 0.5 
		1 0.97142857 0.66000003 1 0.22857143 0.89999998 3 0.80714285 0.69999999 
		3;
	setAttr -s 11 ".pws[0:10]"  0 0 0 0 0 0 0 0 0 0 0 0 0 0 
		0 0 1 3 0.26428571 0.54000002 3 0.8214286 0.69999999 3 0.042857144 0.81999999 
		3 1 0.86000001 1 0.92142856 0.94 3;
	setAttr ".tls[0]"  0 1 1;
	setAttr ".nth" 100;
	setAttr ".tln" 0.28100000000000003;
	setAttr ".tbwd" 0.14049600000000001;
	setAttr ".ttwd" 0.0082640000000000005;
	setAttr ".tel" 1.00828;
	setAttr -s 7 ".env";
	setAttr ".env[0].envp" 0;
	setAttr ".env[0].envc" -type "float3" 0.37144801 0.40200001 0.37345934 ;
	setAttr ".env[0].envi" 2;
	setAttr ".env[1].envp" 0.52857142686843872;
	setAttr ".env[1].envc" -type "float3" 0.72809201 0.73951674 0.764 ;
	setAttr ".env[1].envi" 2;
	setAttr ".env[2].envp" 1;
	setAttr ".env[2].envc" -type "float3" 0.400107 0.4425171 0.59100002 ;
	setAttr ".env[2].envi" 2;
	setAttr ".env[3].envp" 0.5;
	setAttr ".env[3].envc" -type "float3" 0.22551499 0.2326552 0.26499999 ;
	setAttr ".env[3].envi" 2;
	setAttr ".env[4].envp" 0.32857143878936768;
	setAttr ".env[4].envc" -type "float3" 0.54320502 0.63879848 0.685 ;
	setAttr ".env[4].envi" 2;
	setAttr ".env[5].envp" 0;
	setAttr ".env[5].envc" -type "float3" 0 0 0 ;
	setAttr ".env[5].envi" 0;
	setAttr ".env[6].envp" 0.71428573131561279;
	setAttr ".env[6].envc" -type "float3" 0.59761798 0.67640859 0.71399999 ;
	setAttr ".env[6].envi" 2;
	setAttr -s 4 ".rro[0:3]"  0 1 1 1 0.16 3 0.15714286 1 3 
		0.52142859 0.47999999 3;
createNode animCurveTL -n "persp_translateX";
	setAttr ".tan" 10;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 7.3879994934167472 12 5.1874903092294575 
		24 3.8653402225573239 30 3.5938603798564599;
	setAttr -s 4 ".kit[3]"  3;
createNode animCurveTL -n "persp_translateY";
	setAttr ".tan" 10;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 1.9379768306036602 12 2.1085950738438486 
		24 2.4334879738563031 30 2.5577347474809806;
	setAttr -s 4 ".kit[3]"  3;
createNode animCurveTL -n "persp_translateZ";
	setAttr ".tan" 10;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 5.0443318293241726 12 3.2090684857849423 
		24 2.5036030453288793 30 2.3509454803882242;
	setAttr -s 4 ".kit[3]"  3;
createNode animCurveTA -n "persp_rotateX";
	setAttr ".tan" 10;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 -14.943724091443363 12 -32.448071919730438 
		24 -44.037604386466519 30 -43.743724091444044;
	setAttr -s 4 ".kit[3]"  3;
createNode animCurveTA -n "persp_rotateY";
	setAttr ".tan" 10;
	setAttr ".wgt" no;
	setAttr -s 4 ".ktv[0:3]"  1 80.929400134846759 12 122.44244360933197 
		24 167.72940013484643 30 174.5294001348463;
	setAttr -s 4 ".kit[3]"  3;
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 40 -ast 1 -aet 48 ";
	setAttr ".st" 6;
createNode noise -n "noise2";
	setAttr ".cg" -type "float3" 0.29752001 0.29752001 0.29752001 ;
	setAttr ".co" -type "float3" 0.71073997 0.71073997 0.71073997 ;
	setAttr ".ra" 0.89256000518798828;
	setAttr ".dm" 5;
	setAttr ".fq" 57.023998260498047;
	setAttr ".fr" 2.0413999557495117;
	setAttr ".nty" 4;
createNode place2dTexture -n "place2dTexture2";
	setAttr ".re" -type "float2" 1.5 1 ;
createNode imagePlane -n "imagePlane1";
	setAttr ".t" 1;
	setAttr ".s" -type "double2" 1.4173200000000001 1.0629926294108702 ;
	setAttr ".c" -type "double3" 4.2863327718840187 1.0996688802716696 4.5491575666741584 ;
	setAttr ".w" 10;
	setAttr ".h" 10;
createNode remapValue -n "remapValue2";
	setAttr -s 2 ".vl[0:1]"  0 0 1 1 1 1;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].clc" -type "float3" 0.102168 0.27729467 0.34400001 ;
	setAttr ".cl[0].cli" 1;
	setAttr ".cl[2].clp" 0.94999998807907104;
	setAttr ".cl[2].clc" -type "float3" 0.33699 0.39870536 0.47799999 ;
	setAttr ".cl[2].cli" 1;
createNode expression -n "expression1";
	setAttr -k on ".nds";
	setAttr ".ixp" -type "string" ".O[0]=time *2";
createNode rampShader -n "rampShader2";
	setAttr ".dc" 0.85123997926712036;
	setAttr -s 3 ".clr";
	setAttr ".clr[0].clrp" 0;
	setAttr ".clr[0].clrc" -type "float3" 0.466416 0.58838177 0.65600002 ;
	setAttr ".clr[0].clri" 0;
	setAttr ".clr[1].clrp" 0.58571428060531616;
	setAttr ".clr[1].clrc" -type "float3" 0.815 0.66876334 0.426245 ;
	setAttr ".clr[1].clri" 1;
	setAttr ".clr[2].clrp" 0.57142859697341919;
	setAttr ".clr[2].clrc" -type "float3" 0.466416 0.58838201 0.65600002 ;
	setAttr ".clr[2].clri" 1;
	setAttr ".cin" 2;
	setAttr ".it[0].itp" 0;
	setAttr ".it[0].itc" -type "float3" 0 0 0 ;
	setAttr ".it[0].iti" 1;
	setAttr ".ic[0].icp" 0;
	setAttr ".ic[0].icc" -type "float3" 0 0 0 ;
	setAttr ".ic[0].ici" 1;
	setAttr ".tc" 0.86776000261306763;
	setAttr ".trsd" 5;
	setAttr ".spl" 0;
	setAttr -s 2 ".sro[0:1]"  0 1 2 0.5 0.5 2;
	setAttr ".sc[0].scp" 0;
	setAttr ".sc[0].scc" -type "float3" 0.5 0.5 0.5 ;
	setAttr ".sc[0].sci" 1;
	setAttr ".rfl[0]"  0 1 1;
	setAttr ".env[0].envp" 0;
	setAttr ".env[0].envc" -type "float3" 0 0 0 ;
	setAttr ".env[0].envi" 1;
createNode shadingEngine -n "rampShader2SG";
	setAttr ".ihi" 0;
	setAttr -s 3 ".dsm";
	setAttr ".ro" yes;
createNode materialInfo -n "materialInfo6";
createNode brush -n "brush2";
	setAttr ".dep" yes;
	setAttr ".ill" yes;
	setAttr ".lbw" 0.28926000000000002;
	setAttr ".ows" yes;
	setAttr ".trn" 1;
	setAttr ".rll" yes;
	setAttr ".lcl[0]"  0 0.5 1;
	setAttr ".pcl[0]"  0 0.5 1;
	setAttr ".wsc[0]"  0 1 1;
	setAttr ".lws[0]"  0 1 1;
	setAttr ".pws[0]"  0 1 1;
	setAttr ".tls[0]"  0 1 1;
	setAttr -s 3 ".env";
	setAttr ".env[0].envp" 0.20000000298023224;
	setAttr ".env[0].envc" -type "float3" 0 0 0.15000001 ;
	setAttr ".env[0].envi" 2;
	setAttr ".env[1].envp" 0.5;
	setAttr ".env[1].envc" -type "float3" 0.47999999 0.55000001 0.69999999 ;
	setAttr ".env[1].envi" 2;
	setAttr ".env[2].envp" 1;
	setAttr ".env[2].envc" -type "float3" 0 0.1 0.44999999 ;
	setAttr ".env[2].envi" 2;
	setAttr ".rro[0]"  0 1 1;
select -ne :time1;
	setAttr ".o" 1;
select -ne :renderPartition;
	setAttr -s 3 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 3 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 2 ".u";
select -ne :lightList1;
select -ne :defaultTextureList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultRenderGlobals;
	setAttr ".an" yes;
	setAttr ".ef" 40;
	setAttr ".ofc" 1;
	setAttr ".ope" yes;
	setAttr ".oppf" yes;
select -ne :defaultRenderQuality;
	setAttr ".rfl" 10;
	setAttr ".rfr" 10;
	setAttr ".sl" 10;
	setAttr ".eaa" 0;
	setAttr ".ufil" yes;
	setAttr ".ss" 2;
	setAttr ".rct" 0.20000000298023224;
	setAttr ".gct" 0.15000000596046448;
	setAttr ".bct" 0.30000001192092896;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :defaultLightSet;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :defaultHardwareRenderGlobals;
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
select -ne :ikSystem;
	setAttr -s 4 ".sol";
connectAttr "persp_translateX.o" ":persp.tx";
connectAttr "persp_translateY.o" ":persp.ty";
connectAttr "persp_translateZ.o" ":persp.tz";
connectAttr "persp_rotateX.o" ":persp.rx";
connectAttr "persp_rotateY.o" ":persp.ry";
connectAttr "imagePlane1.msg" ":perspShape.ip" -na;
connectAttr "teapot1.obr" "strokeShapeTeapot1.brs";
connectAttr "curveTeapotShape.ws" "strokeShapeTeapot1.pcv[0].crv";
connectAttr "strokeShapeTeapot1.omm" "pfxToonShape1.ins[0].srf";
connectAttr "strokeShapeTeapot1.wm" "pfxToonShape1.ins[0].iwm";
connectAttr "strokeShapeTeapot1.olm" "pfxToonShape1.ins[1].srf";
connectAttr "strokeShapeTeapot1.wm" "pfxToonShape1.ins[1].iwm";
connectAttr "strokeShapeTeapot1.ofm" "pfxToonShape1.ins[2].srf";
connectAttr "strokeShapeTeapot1.wm" "pfxToonShape1.ins[2].iwm";
connectAttr "brush2.obr" "pfxToonShape1.brs";
connectAttr "strokeShapeTeapot1.wmm" "teapot1MainShape.i";
connectAttr "strokeShapeTeapot1.wlm" "teapot1LeafShape.i";
connectAttr "strokeShapeTeapot1.wfm" "teapot1FlowerShape.i";
connectAttr "annotationLocator1Shape.wm" "annotationShape1.dom" -na;
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[0].llnk";
connectAttr ":initialShadingGroup.msg" "lightLinker1.lnk[0].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[1].llnk";
connectAttr ":initialParticleSE.msg" "lightLinker1.lnk[1].olnk";
connectAttr ":defaultLightSet.msg" "lightLinker1.lnk[7].llnk";
connectAttr "rampShader2SG.msg" "lightLinker1.lnk[7].olnk";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":time1.o" "teapot1.tim";
connectAttr "place2dTexture2.o" "noise2.uv";
connectAttr "place2dTexture2.ofs" "noise2.fs";
connectAttr "expression1.out[0]" "noise2.ti";
connectAttr "remapValue2.oc" "imagePlane1.stx";
connectAttr "noise2.ocr" "remapValue2.i";
connectAttr ":time1.o" "expression1.tim";
connectAttr "rampShader2.oc" "rampShader2SG.ss";
connectAttr "teapot1MainShape.iog" "rampShader2SG.dsm" -na;
connectAttr "teapot1FlowerShape.iog" "rampShader2SG.dsm" -na;
connectAttr "teapot1LeafShape.iog" "rampShader2SG.dsm" -na;
connectAttr "rampShader2SG.msg" "materialInfo6.sg";
connectAttr "rampShader2.msg" "materialInfo6.m";
connectAttr "rampShader2.msg" "materialInfo6.t" -na;
connectAttr ":time1.o" "brush2.tim";
connectAttr "rampShader2SG.pa" ":renderPartition.st" -na;
connectAttr "rampShader2.msg" ":defaultShaderList1.s" -na;
connectAttr "place2dTexture2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "remapValue2.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "lightLinker1.msg" ":lightList1.ln" -na;
connectAttr "spotLightShape1.ltd" ":lightList1.l" -na;
connectAttr "noise2.msg" ":defaultTextureList1.tx" -na;
connectAttr "spotLight1.iog" ":defaultLightSet.dsm" -na;
// End of NightShade.ma
