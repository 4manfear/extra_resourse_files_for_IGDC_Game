//Maya ASCII 2011 scene
//Name: meteorAutoResize.ma
//Last modified: Fri, Feb 19, 2010 11:34:09 AM
//Codeset: 1252
requires maya "2011";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya Unlimited 2011";
fileInfo "version" "2011";
fileInfo "cutIdentifier" "201002182316-769557";
fileInfo "osv" "Microsoft Windows XP Professional Service Pack 2 (Build 2600)\n";
createNode transform -s -n "persp";
	setAttr ".v" no;
	setAttr ".t" -type "double3" -7.7661101534500343 14.061888775009793 36.083198279891882 ;
	setAttr ".r" -type "double3" -4.5383527296020851 -10.599999999999977 -1.0111787502782372e-016 ;
createNode camera -s -n "perspShape" -p "persp";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 36.489422480764802;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 100.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 100.1 ;
createNode camera -s -n "frontShape" -p "front";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 100.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 100.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "fuelBurn";
	setAttr ".t" -type "double3" 0 9.8516245002628757 -0.038072587821532444 ;
createNode fluidShape -n "fuelBurnShape" -p "fuelBurn";
	addAttr -ci true -sn "nts" -ln "notes" -dt "string";
	setAttr -k off ".v";
	setAttr ".rt" 1;
	setAttr ".vf" 0;
	setAttr ".iss" yes;
	setAttr ".dw" 5;
	setAttr ".dh" 5;
	setAttr ".dd" 5;
	setAttr ".aure" yes;
	setAttr ".aurt" 0.0056506609544157982;
	setAttr -s 2 ".sd";
	setAttr -s 2 ".sd";
	setAttr -s 2 ".fce";
	setAttr -s 2 ".eml";
	setAttr ".sli" 1;
	setAttr ".vdl" 0.097120000000000012;
	setAttr ".vds" 4;
	setAttr ".opg" 0.67962002754211426;
	setAttr ".bndx" 0;
	setAttr ".bndy" 0;
	setAttr ".bndz" 0;
	setAttr ".dds" 0.24855491285874493;
	setAttr ".ddf" 0.1040462425053981;
	setAttr ".dsb" 0.72820001840591431;
	setAttr ".vmt" 0;
	setAttr ".vdp" 0.019419999793171883;
	setAttr ".tst" 0.24855491518974304;
	setAttr ".tfr" 0.81551998853683472;
	setAttr ".tbs" 0.058279998600482941;
	setAttr ".fmet" 2;
	setAttr ".fesc" 0.64079999923706055;
	setAttr ".resp" 0.0080000003799796104;
	setAttr ".fuit" -0.10000000149011612;
	setAttr ".mxrt" 0;
	setAttr ".updy" yes;
	setAttr ".ss" yes;
	setAttr ".rin" 3;
	setAttr -s 2 ".cl";
	setAttr ".cl[0].clp" 0.8928571343421936;
	setAttr ".cl[0].clc" -type "float3" 0.49000001 0.44424185 0.38416001 ;
	setAttr ".cl[0].cli" 3;
	setAttr ".cl[1].clp" 0;
	setAttr ".cl[1].clc" -type "float3" 0.049163997 0.084608153 0.102 ;
	setAttr ".cl[1].cli" 3;
	setAttr ".cib" 0.10868000239133835;
	setAttr -s 5 ".opa[2:6]"  1 0.77999997 1 0.018199233 0.054545455 
		3 0 0 3 0.032258064 0.086092718 3 0.013409962 0.0045454544 3;
	setAttr ".oib" 0.29411765933036804;
	setAttr ".t" -type "float3" 0.033905547 0.033905547 0.033905547 ;
	setAttr ".shp" 0.54802262783050537;
	setAttr ".lbrt" 0.70621466636657715;
	setAttr ".flic" -type "float3" 1 0.93620002 0.82599998 ;
	setAttr ".abrt" 0.4858756959438324;
	setAttr ".ambc" -type "float3" 0.61800003 0.8217333 1 ;
	setAttr -s 4 ".i";
	setAttr ".i[0].ip" 0.79130434989929199;
	setAttr ".i[0].ic" -type "float3" 4.9089999 2.1496513 0.96707314 ;
	setAttr ".i[0].ii" 1;
	setAttr ".i[1].ip" 0.014285714365541935;
	setAttr ".i[1].ic" -type "float3" 0.012374999 0.029318251 0.045000002 ;
	setAttr ".i[1].ii" 1;
	setAttr ".i[2].ip" 0.48571428656578064;
	setAttr ".i[2].ic" -type "float3" 0.75 0.23612496 0 ;
	setAttr ".i[2].ii" 1;
	setAttr ".i[4].ip" 0.64999997615814209;
	setAttr ".i[4].ic" -type "float3" 1 0.5628587 0.0080000162 ;
	setAttr ".i[4].ii" 1;
	setAttr ".ili" 7;
	setAttr ".iib" 0.78151261806488037;
	setAttr ".gi" 0.062146894633769989;
	setAttr ".env[0].envp" 0;
	setAttr ".env[0].envc" -type "float3" 0 0 0 ;
	setAttr ".env[0].envi" 1;
	setAttr ".dos" 0;
	setAttr ".edr" 0.29129999876022339;
	setAttr ".rl" no;
	setAttr ".dl" -type "float3" 0.60000002 0.60000002 -0.2 ;
	setAttr ".tty" 4;
	setAttr ".ctx" yes;
	setAttr ".itx" yes;
	setAttr ".itxg" 0.93203997611999512;
	setAttr ".otx" yes;
	setAttr ".a" 0.74757999181747437;
	setAttr ".ra" 0.62136000394821167;
	setAttr ".dm" 3;
	setAttr ".fq" 2.5;
	setAttr ".in" yes;
	setAttr ".cvel" no;
	setAttr ".ctmp" no;
	setAttr ".ccol" no;
	setAttr ".catc" no;
	setAttr ".nts" -type "string" "This simulates a hot cometlike object falling through the air leaving a trail of turbulence smoke. A fuel grid was used for the incandescence color. There are two nested emitters. The smaller emits density while the larger emits fuel which then reacts away a bit each timestep. Ignition temperature is below zero so that the reaction will always happen(the default temperature on the grid is zero ). Another perhaps simpler way of doing the same thing might have been to simply use the temperature grid with dissipation.\n\nThe smoke is self shadowed and animated with a little turbulence, diffusion and dissipation(note that a velocity grid is not needed for turbulence to be used, which allows the simulation to run a bit faster). Also an animated texture creates a billowing effect.\n";
createNode fluidEmitter -n "fluidEmitter1" -p "fuelBurn";
	setAttr ".s" -type "double3" 1.2 1.2 1.2 ;
	setAttr ".emt" 4;
	setAttr -k off ".rat" 150.28901752138327;
	setAttr -k off ".sro";
	setAttr -l on -k off ".urpp";
	setAttr -k off ".npuv";
	setAttr ".max" 1;
	setAttr -k off ".dx";
	setAttr -k off ".dy";
	setAttr -k off ".dz";
	setAttr -k off ".spr";
	setAttr -k off ".spd";
	setAttr -k off ".srnd";
	setAttr -k off ".tspd";
	setAttr -k off ".nspd";
	setAttr ".vol" 1;
	setAttr -k off ".afc";
	setAttr -k off ".afa";
	setAttr -k off ".alx";
	setAttr -k off ".arx";
	setAttr -k off ".rnd";
	setAttr -k off ".drs";
	setAttr -k off ".ssz";
	setAttr -k off ".dss";
	setAttr ".fdo" 0;
	setAttr ".nzd" no;
	setAttr ".dmth" 2;
	setAttr ".fde" 0.28901734070669366;
createNode fluidEmitter -n "fuelEmitter" -p "fluidEmitter1";
	setAttr ".s" -type "double3" 1.5 1.5 1.5 ;
	setAttr ".emt" 4;
	setAttr -k off ".rat";
	setAttr -k off ".sro";
	setAttr -l on -k off ".urpp";
	setAttr -k off ".npuv";
	setAttr ".max" 1;
	setAttr -k off ".dx";
	setAttr -k off ".dy";
	setAttr -k off ".dz";
	setAttr -k off ".spr";
	setAttr -k off ".spd";
	setAttr -k off ".srnd";
	setAttr -k off ".tspd";
	setAttr -k off ".nspd";
	setAttr ".vol" 1;
	setAttr -k off ".afc";
	setAttr -k off ".afa";
	setAttr -k off ".alx";
	setAttr -k off ".arx";
	setAttr -k off ".rnd";
	setAttr -k off ".drs";
	setAttr -k off ".ssz";
	setAttr -k off ".dss";
	setAttr ".fdo" 0;
	setAttr ".nzd" no;
	setAttr ".fde" 0;
	setAttr ".ffe" 1;
createNode transform -n "MeteorAutoResizeCam";
	setAttr ".t" -type "double3" 6.9350079330926429 21.420523178882515 -14.197360845724255 ;
	setAttr ".r" -type "double3" -33.338352729601596 156.99999999999915 0 ;
createNode camera -n "MeteorAutoResizeCamShape" -p "MeteorAutoResizeCam";
	setAttr -k off ".v";
	setAttr ".coi" 24.634183001962175;
	setAttr ".imn" -type "string" "persp1";
	setAttr ".den" -type "string" "persp1_depth";
	setAttr ".man" -type "string" "persp1_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode lightLinker -s -n "lightLinker1";
	setAttr -s 3 ".lnk";
	setAttr -s 3 ".slnk";
createNode displayLayerManager -n "layerManager";
createNode displayLayer -n "defaultLayer";
createNode renderLayerManager -n "renderLayerManager";
createNode renderLayer -n "defaultRenderLayer";
	setAttr ".g" yes;
createNode animCurveTL -n "fluidEmitter1_translateX";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  -40 14.120918607417488 0 6.7709192524639379 
		31.2 -3.3347091145335512 71.2 -0.71803662558150805 138.4 8.0211193998773052;
createNode animCurveTL -n "fluidEmitter1_translateY";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  -43.2 7.0020984337826695 0 7.2926292802676045 
		31.2 2.9989793285794164 71.2 -6.3071777928692327 138.4 -6.3071777928692327;
createNode animCurveTL -n "fluidEmitter1_translateZ";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 5 ".ktv[0:4]"  -45.6 -0.096843615494977442 0 0 31.2 2.9647312930235139 
		71.2 -0.0064122449285739513 138.4 0.90729581510087742;
createNode expression -n "expression1";
	setAttr -k on ".nds";
	setAttr ".ixp" -type "string" ".O[0]= time * .1";
createNode materialInfo -n "materialInfo1";
createNode shadingEngine -n "fluidShape1SG";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode imagePlane -n "imagePlane2";
	setAttr ".t" 1;
	setAttr ".fc" 12;
	setAttr ".s" -type "double2" 1.4173200000000001 1.4173200000000001 ;
	setAttr ".c" -type "double3" -0.55919433169014532 6.7185049687524341 4.1477424876990661 ;
	setAttr ".w" 10;
	setAttr ".h" 10;
createNode ramp -n "ramp2";
	setAttr -s 5 ".cel";
	setAttr ".cel[0].ep" 0;
	setAttr ".cel[0].ec" -type "float3" 1 0 0 ;
	setAttr ".cel[2].ep" 0.99000000953674316;
	setAttr ".cel[2].ec" -type "float3" 0.14180499 0.24102694 0.359 ;
	setAttr ".cel[4].ep" 0.46500000357627869;
	setAttr ".cel[4].ec" -type "float3" 0.51099998 0.51099998 0.51099998 ;
	setAttr ".cel[6].ep" 0.004999999888241291;
	setAttr ".cel[6].ec" -type "float3" 0.201447 0.243 0.24209967 ;
	setAttr ".cel[7].ep" 0.24500000476837158;
	setAttr ".cel[7].ec" -type "float3" 0.352 0.33418107 0.297088 ;
	setAttr ".nf" 0.29128000140190125;
createNode place2dTexture -n "place2dTexture2";
createNode script -n "sceneConfigurationScriptNode";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 100 -ast 1 -aet 100 ";
	setAttr ".st" 6;
select -ne :time1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".st";
	setAttr -cb on ".an";
	setAttr -cb on ".pt";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -av -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".mwc";
	setAttr -cb on ".an";
	setAttr -cb on ".il";
	setAttr -cb on ".vo";
	setAttr -cb on ".eo";
	setAttr -cb on ".fo";
	setAttr -cb on ".epo";
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 3 ".s";
select -ne :defaultTextureList1;
select -ne :lambert1;
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
select -ne :defaultRenderGlobals;
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -k on ".mwc";
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
	setAttr -k off -cb on ".ehql";
	setAttr -k off -cb on ".eams";
	setAttr -k off ".eeaa";
	setAttr -k off ".engm";
	setAttr -k off ".mes";
	setAttr -k off ".emb";
	setAttr -k off ".mbbf";
	setAttr -k off ".mbs";
	setAttr -k off ".trm";
	setAttr -k off -cb on ".tshc";
	setAttr -k off ".clmt";
	setAttr -k off -cb on ".tcov";
	setAttr -k off -cb on ".lith";
	setAttr -k off -cb on ".sobc";
	setAttr -k off -cb on ".cuth";
	setAttr -k off -cb on ".mgcs";
	setAttr -k off ".twa";
	setAttr -k off ".twz";
	setAttr -k on ".hwcc";
	setAttr -k on ".hwdp";
	setAttr -k on ".hwql";
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -cb on ".ihi";
	setAttr -k on ".nds";
	setAttr -cb on ".bnm";
	setAttr -k on ".rp";
	setAttr -k on ".cai";
	setAttr -k on ".coi";
	setAttr -cb on ".bc";
	setAttr -av -k on ".bcb";
	setAttr -av -k on ".bcg";
	setAttr -av -k on ".bcr";
	setAttr -k on ".ei";
	setAttr -k on ".ex";
	setAttr -k on ".es";
	setAttr -av -k on ".ef";
	setAttr -cb on ".bf";
	setAttr -k on ".fii";
	setAttr -cb on ".sf";
	setAttr -k on ".gr";
	setAttr -k on ".li";
	setAttr -k on ".ls";
	setAttr -k on ".mb";
	setAttr -k on ".ti";
	setAttr -k on ".txt";
	setAttr -k on ".mpr";
	setAttr -k on ".wzd";
	setAttr ".fn" -type "string" "im";
	setAttr -k on ".if";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
	setAttr -k on ".as";
	setAttr -k on ".ds";
	setAttr -k on ".lm";
	setAttr -k on ".fir";
	setAttr -k on ".aap";
	setAttr -k on ".gh";
	setAttr -cb on ".sd";
connectAttr ":time1.o" "fuelBurnShape.cti";
connectAttr "fuelEmitter.ef" "fuelBurnShape.eml[0].emfr";
connectAttr "fluidEmitter1.ef" "fuelBurnShape.eml[1].emfr";
connectAttr "fuelEmitter.efc" "fuelBurnShape.fce[5]";
connectAttr "fluidEmitter1.efc" "fuelBurnShape.fce[6]";
connectAttr "expression1.out[0]" "fuelBurnShape.tti";
connectAttr ":time1.o" "fluidEmitter1.ct";
connectAttr "fuelBurnShape.ifl" "fluidEmitter1.full[1]";
connectAttr "fuelBurnShape.ots" "fluidEmitter1.dt[1]";
connectAttr "fuelBurnShape.inh" "fluidEmitter1.inh[1]";
connectAttr "fuelBurnShape.sti" "fluidEmitter1.stt[1]";
connectAttr "fuelBurnShape.sd[6]" "fluidEmitter1.sd[1]";
connectAttr "fluidEmitter1_translateX.o" "fluidEmitter1.tx";
connectAttr "fluidEmitter1_translateY.o" "fluidEmitter1.ty";
connectAttr "fluidEmitter1_translateZ.o" "fluidEmitter1.tz";
connectAttr ":time1.o" "fuelEmitter.ct";
connectAttr "fuelBurnShape.ifl" "fuelEmitter.full[2]";
connectAttr "fuelBurnShape.ots" "fuelEmitter.dt[2]";
connectAttr "fuelBurnShape.inh" "fuelEmitter.inh[2]";
connectAttr "fuelBurnShape.sti" "fuelEmitter.stt[2]";
connectAttr "fuelBurnShape.sd[5]" "fuelEmitter.sd[2]";
connectAttr "imagePlane2.msg" "MeteorAutoResizeCamShape.ip" -na;
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "fluidShape1SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "fluidShape1SG.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr ":time1.o" "expression1.tim";
connectAttr "fluidShape1SG.msg" "materialInfo1.sg";
connectAttr "fuelBurnShape.ocl" "fluidShape1SG.vs";
connectAttr "fuelBurnShape.iog" "fluidShape1SG.dsm" -na;
connectAttr "ramp2.oc" "imagePlane2.stx";
connectAttr "place2dTexture2.o" "ramp2.uv";
connectAttr "place2dTexture2.ofs" "ramp2.fs";
connectAttr "fluidShape1SG.pa" ":renderPartition.st" -na;
connectAttr "fuelBurnShape.msg" ":defaultShaderList1.s" -na;
connectAttr "ramp2.msg" ":defaultTextureList1.tx" -na;
connectAttr "place2dTexture2.msg" ":defaultRenderUtilityList1.u" -na;
// End of meteorAutoResize.ma