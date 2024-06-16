//Maya ASCII 2018ff06 scene
//Name: clusterNetwork.ma
//Last modified: Tue, Jun 06, 2017 10:38:53 AM
//Codeset: 1252
requires maya "2018ff06";
requires -nodeType "MASH_Waiter" -nodeType "MASH_Distribute" -nodeType "MASH_World"
		 "MASH" "450";
requires "stereoCamera" "10.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2018";
fileInfo "version" "Preview Release 80";
fileInfo "cutIdentifier" "201705291830-fd95744322";
fileInfo "osv" "Microsoft Windows 8 Enterprise Edition, 64-bit  (Build 9200)\n";
createNode transform -s -n "persp";
	rename -uid "744039FB-4772-841C-B7E8-5AB7D632AD29";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 65.110461692756942 22.50696126824198 26.93331217406741 ;
	setAttr ".r" -type "double3" -22.538352729603137 58.200000000000969 0 ;
createNode camera -s -n "perspShape" -p "persp";
	rename -uid "966D695C-456F-ED43-653B-56A9BB7F2AD9";
	setAttr -k off ".v" no;
	setAttr ".fl" 34.999999999999993;
	setAttr ".coi" 73.651584255675317;
	setAttr ".imn" -type "string" "persp";
	setAttr ".den" -type "string" "persp_depth";
	setAttr ".man" -type "string" "persp_mask";
	setAttr ".hc" -type "string" "viewSet -p %camera";
createNode transform -s -n "top";
	rename -uid "F5BFAA5F-4D7D-2518-0509-BFB28AEE4DBA";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 1000.1 0 ;
	setAttr ".r" -type "double3" -89.999999999999986 0 0 ;
createNode camera -s -n "topShape" -p "top";
	rename -uid "6341301C-4491-CA4C-4B12-8AA74A64C670";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "top";
	setAttr ".den" -type "string" "top_depth";
	setAttr ".man" -type "string" "top_mask";
	setAttr ".hc" -type "string" "viewSet -t %camera";
	setAttr ".o" yes;
createNode transform -s -n "front";
	rename -uid "DA1A74CF-4AAE-A499-454D-FAA606AFC898";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 0 0 1000.1 ;
createNode camera -s -n "frontShape" -p "front";
	rename -uid "F6F44885-4C2B-5C31-F95E-78ACCE3A25C7";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "front";
	setAttr ".den" -type "string" "front_depth";
	setAttr ".man" -type "string" "front_mask";
	setAttr ".hc" -type "string" "viewSet -f %camera";
	setAttr ".o" yes;
createNode transform -s -n "side";
	rename -uid "A1C79463-4D45-B745-13EA-94A38C0607C9";
	setAttr ".v" no;
	setAttr ".t" -type "double3" 1000.1 0 0 ;
	setAttr ".r" -type "double3" 0 89.999999999999986 0 ;
createNode camera -s -n "sideShape" -p "side";
	rename -uid "C61FCC1D-4D3F-116A-FE02-9BB470FA8935";
	setAttr -k off ".v" no;
	setAttr ".rnd" no;
	setAttr ".coi" 1000.1;
	setAttr ".ow" 30;
	setAttr ".imn" -type "string" "side";
	setAttr ".den" -type "string" "side_depth";
	setAttr ".man" -type "string" "side_mask";
	setAttr ".hc" -type "string" "viewSet -s %camera";
	setAttr ".o" yes;
createNode transform -n "pCube1";
	rename -uid "262C9881-4562-44BA-78EE-989512EDC9B2";
	setAttr ".v" no;
createNode mesh -n "pCubeShape1" -p "pCube1";
	rename -uid "74FA53D9-4FB4-C98D-2084-1BA1314E3BEB";
	setAttr -k off ".v";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
createNode instancer -n "ClusterNetwork_Instancer";
	rename -uid "A3CAEDB5-4D4F-55B4-AC8D-ADA16CA12079";
	addAttr -s false -ci true -h true -sn "instancerMessage" -ln "instancerMessage" 
		-at "message";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "03B6DA8C-4B42-EE4A-B288-3D8721FCC752";
	setAttr -s 2 ".lnk";
	setAttr -s 2 ".slnk";
createNode shapeEditorManager -n "shapeEditorManager";
	rename -uid "9B2B3211-4A47-A08F-D378-7C8F170474B4";
createNode poseInterpolatorManager -n "poseInterpolatorManager";
	rename -uid "481EAC5D-40B6-92D0-8F44-1A8248FE828D";
createNode displayLayerManager -n "layerManager";
	rename -uid "E45DE469-4298-BF2D-FA59-209AF8C67DDE";
createNode displayLayer -n "defaultLayer";
	rename -uid "CC5CFAC8-45FF-213A-12BD-A5870062F0FE";
createNode renderLayerManager -n "renderLayerManager";
	rename -uid "3EEBC43E-46D8-C42F-7972-ABB74C47F0C8";
createNode renderLayer -n "defaultRenderLayer";
	rename -uid "6E9811D1-42F2-7451-97AA-8A9334079C3A";
	setAttr ".g" yes;
createNode polyCube -n "polyCube1";
	rename -uid "892C55DF-4E71-5B09-3F29-7E938DB9894C";
createNode MASH_Waiter -n "ClusterNetwork";
	rename -uid "240580B3-4440-4FFD-9D41-BE941185F3BA";
	addAttr -s false -ci true -h true -sn "instancerMessage" -ln "instancerMessage" 
		-at "message";
	setAttr ".inRotPP" -type "vectorArray" 830 0 117.01444244384766 0 0 147.72166442871094
		 0 0 287.30340576171875 0 0 163.47323608398438 0 0 258.5460205078125 0 0 93.226081848144531
		 0 0 262.534912109375 0 0 66.678245544433594 0 0 84.128807067871094 0 0 59.156459808349609
		 0 0 317.04653930664063 0 0 79.179962158203125 0 0 192.54432678222656 0 0 201.38948059082031
		 0 0 129.95899963378906 0 0 263.31509399414063 0 0 275.76800537109375 0 0 115.26551818847656
		 0 0 331.14096069335938 0 0 28.153953552246094 0 0 97.202972412109375 0 0 51.486988067626953
		 0 0 91.662940979003906 0 0 216.63424682617188 0 0 286.80902099609375 0 0 302.3316650390625
		 0 0 222.70248413085938 0 0 53.433319091796875 0 0 332.52438354492188 0 0 127.67549133300781
		 0 0 104.01537322998047 0 0 275.89938354492188 0 0 322.11776733398438 0 0 143.67527770996094
		 0 0 266.82827758789063 0 0 180.89981079101563 0 0 286.87127685546875 0 0 163.97735595703125
		 0 0 99.804901123046875 0 0 161.27888488769531 0 0 112.67459106445313 0 0 279.41390991210938
		 0 0 212.6346435546875 0 0 186.63836669921875 0 0 167.59040832519531 0 0 77.406776428222656
		 0 0 256.30111694335938 0 0 53.675968170166016 0 0 46.654705047607422 0 0 55.406936645507813
		 0 0 85.493896484375 0 0 55.647724151611328 0 0 91.312767028808594 0 0 278.31298828125
		 0 0 32.068031311035156 0 0 205.42208862304688 0 0 292.85446166992188 0 0 102.303466796875
		 0 0 253.5943603515625 0 0 92.286888122558594 0 0 23.121755599975586 0 0 33.756618499755859
		 0 0 18.009946823120117 0 0 286.4478759765625 0 0 222.30958557128906 0 0 115.60003662109375
		 0 0 9.9556093215942383 0 0 174.3707275390625 0 0 73.411567687988281 0 0 52.960391998291016
		 0 0 160.31881713867188 0 0 270.33175659179688 0 0 130.18400573730469 0 0 160.03558349609375
		 0 0 267.38778686523438 0 0 178.76426696777344 0 0 143.9981689453125 0 0 226.14152526855469
		 0 0 152.23008728027344 0 0 273.29217529296875 0 0 91.957855224609375 0 0 235.41714477539063
		 0 0 282.293212890625 0 0 120.40834045410156 0 0 310.230224609375 0 0 297.1729736328125
		 0 0 124.52605438232422 0 0 170.79019165039063 0 0 94.652191162109375 0 0 270.102783203125
		 0 0 75.458000183105469 0 0 42.091503143310547 0 0 292.84945678710938 0 0 23.497640609741211
		 0 0 351.7039794921875 0 0 97.166015625 0 0 138.23118591308594 0 0 359.73446655273438
		 0 0 241.29402160644531 0 0 23.133672714233398 0 0 313.23568725585938 0 0 17.558528900146484
		 0 0 216.34602355957031 0 0 252.51425170898438 0 0 60.024032592773438 0 0 164.07388305664063
		 0 0 133.47103881835938 0 0 331.97964477539063 0 0 139.84368896484375 0 0 215.29296875
		 0 0 325.6748046875 0 0 327.57089233398438 0 0 342.06198120117188 0 0 293.65753173828125
		 0 0 295.72686767578125 0 0 42.810981750488281 0 0 225.06681823730469 0 0 60.928142547607422
		 0 0 273.40655517578125 0 0 210.941650390625 0 0 327.09786987304688 0 0 11.488971710205078
		 0 0 161.71730041503906 0 0 214.42066955566406 0 0 301.68191528320313 0 0 163.86241149902344
		 0 0 320.9921875 0 0 18.375371932983398 0 0 98.157829284667969 0 0 26.918003082275391
		 0 0 14.378274917602539 0 0 335.8743896484375 0 0 215.70939636230469 0 0 91.76361083984375
		 0 0 67.514007568359375 0 0 109.93241882324219 0 0 121.60272979736328 0 0 329.81488037109375
		 0 0 235.32115173339844 0 0 168.75242614746094 0 0 320.37948608398438 0 0 90.703170776367188
		 0 0 173.44053649902344 0 0 165.49598693847656 0 0 170.80735778808594 0 0 132.38468933105469
		 0 0 269.35623168945313 0 0 211.24588012695313 0 0 333.951171875 0 0 127.62389373779297
		 0 0 323.25030517578125 0 0 319.14999389648438 0 0 107.51554870605469 0 0 186.299560546875
		 0 0 349.24545288085938 0 0 1.6456534862518311 0 0 235.76809692382813 0 0 73.724945068359375
		 0 0 163.21351623535156 0 0 300.40338134765625 0 0 336.903076171875 0 0 185.63694763183594
		 0 0 324.49752807617188 0 0 194.85786437988281 0 0 106.81272888183594 0 0 340.04415893554688
		 0 0 319.71133422851563 0 0 255.93705749511719 0 0 83.562324523925781 0 0 4.6699891090393066
		 0 0 96.931785583496094 0 0 0.75940525531768799 0 0 314.95034790039063 0 0 125.53156280517578
		 0 0 219.21527099609375 0 0 278.07989501953125 0 0 40.124855041503906 0 0 164.3575439453125
		 0 0 150.16531372070313 0 0 93.379203796386719 0 0 99.672447204589844 0 0 10.488659858703613
		 0 0 52.973770141601563 0 0 1.4812402725219727 0 0 44.219730377197266 0 0 144.94432067871094
		 0 0 320.39352416992188 0 0 311.65679931640625 0 0 187.18270874023438 0 0 101.86396026611328
		 0 0 109.95995330810547 0 0 43.3773193359375 0 0 15.577672004699707 0 0 25.609075546264648
		 0 0 266.45916748046875 0 0 185.63838195800781 0 0 235.87136840820313 0 0 154.36540222167969
		 0 0 190.46664428710938 0 0 90.801681518554688 0 0 1.0236325263977051 0 0 152.54408264160156
		 0 0 187.42848205566406 0 0 170.14973449707031 0 0 3.3336155414581299 0 0 198.58932495117188
		 0 0 233.90122985839844 0 0 40.401401519775391 0 0 146.07847595214844 0 0 252.2232666015625
		 0 0 260.3646240234375 0 0 322.64193725585938 0 0 72.657119750976563 0 0 163.04196166992188
		 0 0 55.529010772705078 0 0 211.4766845703125 0 0 247.86299133300781 0 0 332.59564208984375
		 0 0 303.21017456054688 0 0 73.40557861328125 0 0 154.29437255859375 0 0 56.648349761962891
		 0 0 127.21225738525391 0 0 290.65695190429688 0 0 328.5340576171875 0 0 268.86212158203125
		 0 0 221.46377563476563 0 0 83.921035766601563 0 0 122.68173980712891 0 0 306.02566528320313
		 0 0 23.852249145507813 0 0 231.33683776855469 0 0 198.24726867675781 0 0 95.582679748535156
		 0 0 276.27554321289063 0 0 164.99893188476563 0 0 178.47921752929688 0 0 292.5772705078125
		 0 0 10.038901329040527 0 0 297.51937866210938 0 0 132.28976440429688 0 0 215.27236938476563
		 0 0 145.04257202148438 0 0 3.2311992645263672 0 0 307.513916015625 0 0 112.21246337890625
		 0 0 127.54515838623047 0 0 323.21170043945313 0 0 58.052692413330078 0 0 34.087554931640625
		 0 0 173.50343322753906 0 0 203.49238586425781 0 0 198.94252014160156 0 0 207.873046875
		 0 0 2.9516711235046387 0 0 188.7801513671875 0 0 71.177505493164063 0 0 350.86215209960938
		 0 0 347.74826049804688 0 0 136.84585571289063 0 0 43.490093231201172 0 0 304.0897216796875
		 0 0 9.247981071472168 0 0 237.06375122070313 0 0 155.82077026367188 0 0 173.68486022949219
		 0 0 95.827903747558594 0 0 23.341442108154297 0 0 90.016036987304688 0 0 298.17611694335938
		 0 0 119.65554046630859 0 0 200.30378723144531 0 0 106.31124114990234 0 0 60.470111846923828
		 0 0 51.524555206298828 0 0 53.38836669921875 0 0 169.18638610839844 0 0 61.042858123779297
		 0 0 157.43695068359375 0 0 71.743606567382813 0 0 335.92132568359375 0 0 52.173397064208984
		 0 0 189.52078247070313 0 0 65.183822631835938 0 0 218.86457824707031 0 0 315.93814086914063
		 0 0 237.304443359375 0 0 97.169898986816406 0 0 96.69781494140625 0 0 126.03806304931641
		 0 0 15.858590126037598 0 0 35.098979949951172 0 0 51.742511749267578 0 0 83.820487976074219
		 0 0 108.47970581054688 0 0 276.11636352539063 0 0 7.0590510368347168 0 0 10.896409034729004
		 0 0 59.915573120117188 0 0 172.69285583496094 0 0 172.39097595214844 0 0 222.19071960449219
		 0 0 158.5794677734375 0 0 291.1734619140625 0 0 47.439510345458984 0 0 272.03485107421875
		 0 0 179.45393371582031 0 0 86.199264526367188 0 0 294.29141235351563 0 0 22.87592887878418
		 0 0 165.48426818847656 0 0 91.586959838867188 0 0 38.069049835205078 0 0 77.898468017578125
		 0 0 222.94203186035156 0 0 172.67106628417969 0 0 273.2576904296875 0 0 188.91975402832031
		 0 0 243.49111938476563 0 0 185.09397888183594 0 0 345.87570190429688 0 0 193.19853210449219
		 0 0 266.85284423828125 0 0 221.63323974609375 0 0 179.54421997070313 0 0 8.0475406646728516
		 0 0 93.389686584472656 0 0 274.98965454101563 0 0 244.65434265136719 0 0 108.77561950683594
		 0 0 336.15676879882813 0 0 118.40852355957031 0 0 340.96319580078125 0 0 338.755859375
		 0 0 236.87155151367188 0 0 26.308164596557617 0 0 19.701715469360352 0 0 313.21722412109375
		 0 0 27.06294059753418 0 0 289.19631958007813 0 0 354.90451049804688 0 0 27.851842880249023
		 0 0 299.2392578125 0 0 114.20601654052734 0 0 114.14120483398438 0 0 108.15834808349609
		 0 0 245.52882385253906 0 0 298.31881713867188 0 0 0.29124832153320313 0 0 64.636184692382813
		 0 0 35.992572784423828 0 0 125.0679931640625 0 0 299.37432861328125 0 0 160.13748168945313
		 0 0 89.6407470703125 0 0 157.49650573730469 0 0 297.85498046875 0 0 138.64744567871094
		 0 0 251.43814086914063 0 0 110.51137542724609 0 0 205.31210327148438 0 0 107.86373138427734
		 0 0 66.398857116699219 0 0 98.681739807128906 0 0 63.420215606689453 0 0 231.069091796875
		 0 0 231.509033203125 0 0 176.70059204101563 0 0 4.6227192878723145 0 0 295.210693359375
		 0 0 98.301116943359375 0 0 73.183029174804688 0 0 297.49749755859375 0 0 248.427978515625
		 0 0 341.86300659179688 0 0 233.56492614746094 0 0 24.617252349853516 0 0 70.790657043457031
		 0 0 68.057662963867188 0 0 146.658447265625 0 0 281.49295043945313 0 0 244.29165649414063
		 0 0 58.19183349609375 0 0 146.34785461425781 0 0 329.08807373046875 0 0 347.12637329101563
		 0 0 27.063568115234375 0 0 218.33584594726563 0 0 277.25765991210938 0 0 208.9620361328125
		 0 0 30.401210784912109 0 0 271.48812866210938 0 0 180.59602355957031 0 0 357.57498168945313
		 0 0 91.481986999511719 0 0 129.35786437988281 0 0 248.3887939453125 0 0 219.40919494628906
		 0 0 8.6333456039428711 0 0 219.13258361816406 0 0 104.80937194824219 0 0 103.11126708984375
		 0 0 45.210926055908203 0 0 189.29876708984375 0 0 117.20982360839844 0 0 96.879631042480469
		 0 0 343.841552734375 0 0 296.73342895507813 0 0 156.81942749023438 0 0 158.73690795898438
		 0 0 194.27557373046875 0 0 167.35890197753906 0 0 237.06690979003906 0 0 174.76310729980469
		 0 0 140.0360107421875 0 0 227.32704162597656 0 0 134.34669494628906 0 0 253.14012145996094
		 0 0 191.89884948730469 0 0 69.531341552734375 0 0 266.5213623046875 0 0 203.7252197265625
		 0 0 23.665140151977539 0 0 181.12289428710938 0 0 90.780250549316406 0 0 166.50091552734375
		 0 0 304.68328857421875 0 0 231.92971801757813 0 0 198.34078979492188 0 0 135.91287231445313
		 0 0 203.81739807128906 0 0 24.218910217285156 0 0 259.65924072265625 0 0 226.938232421875
		 0 0 232.64373779296875 0 0 47.014835357666016 0 0 79.343040466308594 0 0 302.37557983398438
		 0 0 72.680915832519531 0 0 163.72932434082031 0 0 50.857387542724609 0 0 164.54966735839844
		 0 0 16.613838195800781 0 0 96.144393920898438 0 0 154.07417297363281 0 0 119.69701385498047
		 0 0 243.47734069824219 0 0 342.88442993164063 0 0 310.28170776367188 0 0 344.9755859375
		 0 0 132.58932495117188 0 0 165.70176696777344 0 0 62.3431396484375 0 0 279.24142456054688
		 0 0 303.38836669921875 0 0 7.8475246429443359 0 0 259.993896484375 0 0 346.5233154296875
		 0 0 93.772651672363281 0 0 162.96931457519531 0 0 174.80406188964844 0 0 109.76264190673828
		 0 0 265.59078979492188 0 0 32.364673614501953 0 0 174.68035888671875 0 0 42.734592437744141
		 0 0 251.49476623535156 0 0 96.819847106933594 0 0 193.0283203125 0 0 107.34556579589844
		 0 0 172.49362182617188 0 0 194.31297302246094 0 0 37.637706756591797 0 0 63.530555725097656
		 0 0 338.49526977539063 0 0 149.54270935058594 0 0 139.06466674804688 0 0 240.65643310546875
		 0 0 256.416259765625 0 0 65.3052978515625 0 0 52.644351959228516 0 0 219.73733520507813
		 0 0 227.66981506347656 0 0 230.52359008789063 0 0 294.38018798828125 0 0 94.177978515625
		 0 0 68.19073486328125 0 0 76.013214111328125 0 0 267.17578125 0 0 332.78610229492188
		 0 0 240.30657958984375 0 0 81.486099243164063 0 0 261.69967651367188 0 0 51.212192535400391
		 0 0 264.52706909179688 0 0 344.41970825195313 0 0 222.47160339355469 0 0 332.2564697265625
		 0 0 175.84857177734375 0 0 269.24896240234375 0 0 203.76658630371094 0 0 351.64627075195313
		 0 0 257.29656982421875 0 0 242.61946105957031 0 0 4.9302091598510742 0 0 226.90817260742188
		 0 0 343.28094482421875 0 0 225.984375 0 0 269.059326171875 0 0 144.98066711425781
		 0 0 323.57012939453125 0 0 263.12774658203125 0 0 243.46380615234375 0 0 52.986804962158203
		 0 0 72.943893432617188 0 0 304.32736206054688 0 0 310.71881103515625 0 0 349.0643310546875
		 0 0 284.50521850585938 0 0 119.33871459960938 0 0 139.7354736328125 0 0 244.97491455078125
		 0 0 318.64962768554688 0 0 135.83099365234375 0 0 44.271163940429688 0 0 339.6318359375
		 0 0 142.52587890625 0 0 185.54916381835938 0 0 350.34368896484375 0 0 47.680732727050781
		 0 0 201.85682678222656 0 0 113.61667633056641 0 0 286.33700561523438 0 0 68.749565124511719
		 0 0 29.0968017578125 0 0 105.57925415039063 0 0 249.7431640625 0 0 241.42538452148438
		 0 0 31.43217658996582 0 0 98.0546875 0 0 293.69549560546875 0 0 184.41024780273438
		 0 0 155.12129211425781 0 0 261.84457397460938 0 0 119.52627563476563 0 0 201.61485290527344
		 0 0 322.6680908203125 0 0 23.989620208740234 0 0 249.01986694335938 0 0 339.89187622070313
		 0 0 286.09454345703125 0 0 80.100028991699219 0 0 228.20362854003906 0 0 68.152854919433594
		 0 0 306.82815551757813 0 0 152.60690307617188 0 0 347.72137451171875 0 0 283.672607421875
		 0 0 93.196907043457031 0 0 87.288421630859375 0 0 55.078456878662109 0 0 191.74919128417969
		 0 0 18.969640731811523 0 0 183.59407043457031 0 0 32.836929321289063 0 0 280.62933349609375
		 0 0 231.46624755859375 0 0 140.35115051269531 0 0 165.69071960449219 0 0 127.14608764648438
		 0 0 218.09002685546875 0 0 89.460121154785156 0 0 301.50433349609375 0 0 30.646299362182617
		 0 0 313.2996826171875 0 0 329.34860229492188 0 0 89.434013366699219 0 0 25.211463928222656
		 0 0 338.12033081054688 0 0 182.89561462402344 0 0 50.428256988525391 0 0 281.87667846679688
		 0 0 58.490997314453125 0 0 291.4805908203125 0 0 141.26058959960938 0 0 320.23135375976563
		 0 0 225.48074340820313 0 0 233.04154968261719 0 0 32.689842224121094 0 0 223.61447143554688
		 0 0 116.80795288085938 0 0 321.59613037109375 0 0 117.74303436279297 0 0 329.95208740234375
		 0 0 205.44003295898438 0 0 21.825912475585938 0 0 298.79644775390625 0 0 306.3330078125
		 0 0 284.8531494140625 0 0 213.22091674804688 0 0 283.27297973632813 0 0 40.903701782226563
		 0 0 190.06808471679688 0 0 117.84842681884766 0 0 263.405517578125 0 0 320.49325561523438
		 0 0 198.21087646484375 0 0 351.82675170898438 0 0 347.45791625976563 0 0 182.98361206054688
		 0 0 309.26187133789063 0 0 22.060850143432617 0 0 112.45589447021484 0 0 323.14718627929688
		 0 0 270.57757568359375 0 0 282.41250610351563 0 0 213.83663940429688 0 0 271.63467407226563
		 0 0 12.313332557678223 0 0 275.51095581054688 0 0 171.93644714355469 0 0 336.52993774414063
		 0 0 291.853515625 0 0 49.478687286376953 0 0 2.7980892658233643 0 0 148.29908752441406
		 0 0 107.85243988037109 0 0 298.86941528320313 0 0 321.40042114257813 0 0 68.185600280761719
		 0 0 149.48268127441406 0 0 22.589513778686523 0 0 98.048126220703125 0 0 155.88813781738281
		 0 0 340.70382690429688 0 0 174.62936401367188 0 0 257.32415771484375 0 0 318.4525146484375
		 0 0 330.94021606445313 0 0 130.09390258789063 0 0 294.09768676757813 0 0 125.54262542724609
		 0 0 104.27728271484375 0 0 290.1478271484375 0 0 73.817306518554688 0 0 101.43076324462891
		 0 0 75.987876892089844 0 0 271.39675903320313 0 0 31.11338996887207 0 0 175.24960327148438
		 0 0 299.2337646484375 0 0 274.06344604492188 0 0 188.14753723144531 0 0 262.909912109375
		 0 0 194.88035583496094 0 0 214.18417358398438 0 0 129.10270690917969 0 0 149.35165405273438
		 0 0 118.10259246826172 0 0 208.450927734375 0 0 218.80540466308594 0 0 182.43218994140625
		 0 0 167.7728271484375 0 0 222.96685791015625 0 0 160.21298217773438 0 0 100.92827606201172
		 0 0 301.36505126953125 0 0 136.35148620605469 0 0 230.275634765625 0 0 84.503318786621094
		 0 0 229.76304626464844 0 0 355.90762329101563 0 0 238.59983825683594 0 0 344.820556640625
		 0 0 181.51239013671875 0 0 284.79171752929688 0 0 6.0767083168029785 0 0 133.69114685058594
		 0 0 170.42814636230469 0 0 323.51950073242188 0 0 222.40284729003906 0 0 244.94869995117188
		 0 0 263.9677734375 0 0 326.07199096679688 0 0 302.73922729492188 0 0 25.001398086547852
		 0 0 45.678482055664063 0 0 167.11259460449219 0 0 70.336936950683594 0 0 255.69940185546875
		 0 0 246.40852355957031 0 0 232.76997375488281 0 0 59.170684814453125 0 0 328.1710205078125
		 0 0 240.05638122558594 0 0 316.5494384765625 0 0 162.11444091796875 0 0 345.51763916015625
		 0 0 227.85163879394531 0 0 84.942184448242188 0 0 347.99432373046875 0 0 11.165382385253906
		 0 0 92.996803283691406 0 0 8.7519416809082031 0 0 164.38453674316406 0 0 75.508987426757813
		 0 0 25.832042694091797 0 0 120.04545593261719 0 0 347.04486083984375 0 0 125.98070526123047
		 0 0 320.67831420898438 0 0 271.13333129882813 0 0 311.2259521484375 0 0 349.7005615234375
		 0 0 338.17138671875 0 0 359.12155151367188 0 0 183.26518249511719 0 0 61.119472503662109
		 0 0 359.109130859375 0 0 279.22711181640625 0 0 194.38970947265625 0 0 85.997207641601563
		 0 0 239.96343994140625 0 0 14.23567008972168 0 0 283.09695434570313 0 0 0.72053080797195435
		 0 0 212.84086608886719 0 0 63.41168212890625 0 0 322.93380737304688 0 0 0.91260355710983276
		 0 0 148.69169616699219 0 0 198.08287048339844 0 0 52.191848754882813 0 0 194.34169006347656
		 0 0 289.43878173828125 0 0 228.90304565429688 0 0 29.941621780395508 0 0 17.851776123046875
		 0 0 77.079574584960938 0 0 300.83810424804688 0 0 135.95101928710938 0 0 92.993576049804688
		 0 0 96.602249145507813 0 0 66.094161987304688 0 0 151.65846252441406 0 0 53.527957916259766
		 0 0 122.95596313476563 0 0 245.44894409179688 0 0 60.788387298583984 0 0 168.23527526855469
		 0 0 120.10871124267578 0 0 301.28726196289063 0 0 2.8418900966644287 0 0 304.26324462890625
		 0 0 83.126106262207031 0 0 208.25529479980469 0 0 237.45352172851563 0 0 104.53532409667969
		 0 0 331.1014404296875 0 0 54.757785797119141 0 0 342.48895263671875 0 0 159.53378295898438
		 0 0 187.89413452148438 0 0 286.82135009765625 0 0 182.61042785644531 0 0 110.87883758544922
		 0 0 250.47572326660156 0 0 185.96395874023438 0 0 268.57513427734375 0 0 117.73119354248047
		 0 0 37.053920745849609 0 0 280.8968505859375 0 0 282.58224487304688 0 0 67.880043029785156
		 0 0 324.9766845703125 0 0 341.02688598632813 0 0 189.84681701660156 0 0 132.50538635253906
		 0 0 154.17897033691406 0 0 78.020050048828125 0 0 323.53933715820313 0 0 89.411003112792969
		 0 0 317.69757080078125 0 0 245.25932312011719 0 0 268.38092041015625 0 0 307.81707763671875
		 0 0 22.347299575805664 0 0 165.79969787597656 0 0 286.958251953125 0 0 322.63677978515625
		 0 0 310.50979614257813 0 0 176.64703369140625 0 0 93.008491516113281 0 0 104.58991241455078
		 0 0 33.937969207763672 0 0 356.2884521484375 0 0 220.75517272949219 0 0 264.63064575195313
		 0 0 166.38322448730469 0 0 168.20893859863281 0 0 54.530513763427734 0 0 204.96585083007813
		 0 0 74.852203369140625 0 0 140.64622497558594 0 0 137.15245056152344 0 0 34.965320587158203
		 0 0 260.2410888671875 0 0 305.11056518554688 0 0 151.37411499023438 0 0 197.05625915527344
		 0 0 213.55421447753906 0 0 66.916854858398438 0 0 65.285697937011719 0 0 211.92820739746094
		 0 0 109.71063995361328 0 0 119.54716491699219 0 0 71.814682006835938 0 0 90.814750671386719
		 0 0 348.8782958984375 0 0 212.1229248046875 0 0 338.0836181640625 0 0 263.15670776367188
		 0 0 159.93125915527344 0 0 262.39620971679688 0 0 308.74758911132813 0 0 202.45814514160156
		 0 0 100.10134887695313 0 0 50.877918243408203 0 0 155.59840393066406 0 0 58.219680786132813
		 0 ;
	setAttr ".cacheIdPP" -type "vectorArray" 0 ;
	setAttr ".cacheVisibilityPP" -type "vectorArray" 0 ;
	setAttr ".initSt" -type "vectorArray" 0 ;
	setAttr ".filename" -type "string" "0";
createNode MASH_Distribute -n "ClusterNetwork_Distribute";
	rename -uid "70C44850-430B-01FA-2802-D4A22E84B98F";
	setAttr ".mapDirection" 4;
	setAttr ".fArray" -type "vectorArray" 0 ;
	setAttr ".inPPP" -type "vectorArray" 0 ;
	setAttr ".centerLinearDistribution" yes;
	setAttr -s 3 ".scaleRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".rotationRamp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr -s 3 ".bRmp[0:2]"  0 0 1 0 0 1 1 1 1;
	setAttr ".bRmpX[0]"  0 1 1;
	setAttr ".bRmpY[0]"  0 1 1;
	setAttr ".bRmpZ[0]"  0 1 1;
	setAttr ".ampX" 80;
createNode MASH_World -n "ClusterNetwork_World";
	rename -uid "06B457B3-4091-676C-E421-2C945CB57201";
	setAttr ".prevousPointsMode" 4;
	setAttr -s 3 ".avoidanceRamp[0:2]"  0 1 1 1 0 2 0 1 2;
	setAttr ".clusterRadius" 0.36000001430511475;
	setAttr ".radius" 0.20000000298023224;
	setAttr ".clusterMode" 4;
createNode script -n "uiConfigurationScriptNode";
	rename -uid "28893ECA-4923-6712-FDFC-28B0ED3DC08E";
	setAttr ".b" -type "string" (
		"// Maya Mel UI Configuration File.\n//\n//  This script is machine generated.  Edit at your own risk.\n//\n//\n\nglobal string $gMainPane;\nif (`paneLayout -exists $gMainPane`) {\n\n\tglobal int $gUseScenePanelConfig;\n\tint    $useSceneConfig = $gUseScenePanelConfig;\n\tint    $menusOkayInPanels = `optionVar -q allowMenusInPanels`;\tint    $nVisPanes = `paneLayout -q -nvp $gMainPane`;\n\tint    $nPanes = 0;\n\tstring $editorName;\n\tstring $panelName;\n\tstring $itemFilterName;\n\tstring $panelConfig;\n\n\t//\n\t//  get current state of the UI\n\t//\n\tsceneUIReplacement -update $gMainPane;\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Top View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Top View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"top\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n"
		+ "            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n"
		+ "            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n"
		+ "            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Side View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Side View\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"side\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n"
		+ "            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n"
		+ "            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Front View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Front View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"front\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n"
		+ "            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n"
		+ "            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 1\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1\n            -height 1\n"
		+ "            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"modelPanel\" (localizedPanelLabel(\"Persp View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tmodelPanel -edit -l (localizedPanelLabel(\"Persp View\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        modelEditor -e \n            -camera \"persp\" \n            -useInteractiveMode 0\n            -displayLights \"default\" \n            -displayAppearance \"smoothShaded\" \n            -activeOnly 0\n            -ignorePanZoom 0\n            -wireframeOnShaded 0\n            -headsUpDisplay 1\n            -holdOuts 1\n            -selectionHiliteDisplay 1\n            -useDefaultMaterial 0\n            -bufferMode \"double\" \n            -twoSidedLighting 0\n            -backfaceCulling 0\n"
		+ "            -xray 0\n            -jointXray 0\n            -activeComponentsXray 0\n            -displayTextures 0\n            -smoothWireframe 0\n            -lineWidth 1\n            -textureAnisotropic 0\n            -textureHilight 1\n            -textureSampling 2\n            -textureDisplay \"modulate\" \n            -textureMaxSize 16384\n            -fogging 0\n            -fogSource \"fragment\" \n            -fogMode \"linear\" \n            -fogStart 0\n            -fogEnd 100\n            -fogDensity 0.1\n            -fogColor 0.5 0.5 0.5 1 \n            -depthOfFieldPreview 1\n            -maxConstantTransparency 1\n            -rendererName \"vp2Renderer\" \n            -objectFilterShowInHUD 1\n            -isFiltered 0\n            -colorResolution 256 256 \n            -bumpResolution 512 512 \n            -textureCompression 0\n            -transparencyAlgorithm \"frontAndBackCull\" \n            -transpInShadows 0\n            -cullingOverride \"none\" \n            -lowQualityLighting 0\n            -maximumNumHardwareLights 1\n            -occlusionCulling 0\n"
		+ "            -shadingModel 0\n            -useBaseRenderer 0\n            -useReducedRenderer 0\n            -smallObjectCulling 0\n            -smallObjectThreshold -1 \n            -interactiveDisableShadows 0\n            -interactiveBackFaceCull 0\n            -sortTransparent 1\n            -controllers 1\n            -nurbsCurves 1\n            -nurbsSurfaces 1\n            -polymeshes 1\n            -subdivSurfaces 1\n            -planes 1\n            -lights 1\n            -cameras 1\n            -controlVertices 1\n            -hulls 1\n            -grid 0\n            -imagePlane 1\n            -joints 1\n            -ikHandles 1\n            -deformers 1\n            -dynamics 1\n            -particleInstancers 1\n            -fluids 1\n            -hairSystems 1\n            -follicles 1\n            -nCloths 1\n            -nParticles 1\n            -nRigids 1\n            -dynamicConstraints 1\n            -locators 1\n            -manipulators 1\n            -pluginShapes 1\n            -dimensions 1\n            -handles 1\n            -pivots 1\n"
		+ "            -textures 1\n            -strokes 1\n            -motionTrails 1\n            -clipGhosts 1\n            -greasePencils 1\n            -shadows 0\n            -captureSequenceNumber -1\n            -width 1114\n            -height 824\n            -sceneRenderFilter 0\n            $editorName;\n        modelEditor -e -viewSelected 0 $editorName;\n        modelEditor -e \n            -pluginObjects \"gpuCacheDisplayFilter\" 1 \n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"ToggledOutliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\toutlinerPanel -edit -l (localizedPanelLabel(\"ToggledOutliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 1\n            -showReferenceMembers 1\n            -showAttributes 0\n"
		+ "            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -isSet 0\n            -isSetMember 0\n"
		+ "            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            -renderFilterIndex 0\n            -selectionOrder \"chronological\" \n            -expandAttribute 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"outlinerPanel\" (localizedPanelLabel(\"Outliner\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\toutlinerPanel -edit -l (localizedPanelLabel(\"Outliner\")) -mbv $menusOkayInPanels  $panelName;\n\t\t$editorName = $panelName;\n        outlinerEditor -e \n            -showShapes 0\n            -showAssignedMaterials 0\n            -showTimeEditor 1\n            -showReferenceNodes 0\n            -showReferenceMembers 0\n            -showAttributes 0\n            -showConnected 0\n            -showAnimCurvesOnly 0\n            -showMuteInfo 0\n            -organizeByLayer 1\n            -organizeByClip 1\n            -showAnimLayerWeight 1\n            -autoExpandLayers 1\n            -autoExpand 0\n            -showDagOnly 1\n            -showAssets 1\n            -showContainedOnly 1\n            -showPublishedAsConnected 0\n            -showParentContainers 0\n            -showContainerContents 1\n            -ignoreDagHierarchy 0\n            -expandConnections 0\n            -showUpstreamCurves 1\n            -showUnitlessCurves 1\n            -showCompounds 1\n            -showLeafs 1\n            -showNumericAttrsOnly 0\n            -highlightActive 1\n"
		+ "            -autoSelectNewObjects 0\n            -doNotSelectNewObjects 0\n            -dropIsParent 1\n            -transmitFilters 0\n            -setFilter \"defaultSetFilter\" \n            -showSetMembers 1\n            -allowMultiSelection 1\n            -alwaysToggleSelect 0\n            -directSelect 0\n            -displayMode \"DAG\" \n            -expandObjects 0\n            -setsIgnoreFilters 1\n            -containersIgnoreFilters 0\n            -editAttrName 0\n            -showAttrValues 0\n            -highlightSecondary 0\n            -showUVAttrsOnly 0\n            -showTextureNodesOnly 0\n            -attrAlphaOrder \"default\" \n            -animLayerFilterOptions \"allAffecting\" \n            -sortOrder \"none\" \n            -longNames 0\n            -niceNames 1\n            -showNamespace 1\n            -showPinIcons 0\n            -mapMotionTrails 0\n            -ignoreHiddenAttribute 0\n            -ignoreOutlinerColor 0\n            -renderFilterVisible 0\n            $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n"
		+ "\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"graphEditor\" (localizedPanelLabel(\"Graph Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Graph Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 1\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n"
		+ "                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 1\n                -showCompounds 0\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 1\n                -doNotSelectNewObjects 0\n                -dropIsParent 1\n                -transmitFilters 1\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n"
		+ "                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 1\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"GraphEd\");\n            animCurveEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 1\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 1\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -showResults \"off\" \n                -showBufferCurves \"off\" \n                -smoothness \"fine\" \n                -resultSamples 1\n                -resultScreenSamples 0\n                -resultUpdate \"delayed\" \n                -showUpstreamCurves 1\n                -showCurveNames 0\n"
		+ "                -showActiveCurveNames 0\n                -stackedCurves 0\n                -stackedCurvesMin -1\n                -stackedCurvesMax 1\n                -stackedCurvesSpace 0.2\n                -displayNormalized 0\n                -preSelectionHighlight 0\n                -constrainDrag 0\n                -classicMode 1\n                -valueLinesToggle 1\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dopeSheetPanel\" (localizedPanelLabel(\"Dope Sheet\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dope Sheet\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"OutlineEd\");\n            outlinerEditor -e \n                -showShapes 1\n                -showAssignedMaterials 0\n                -showTimeEditor 1\n                -showReferenceNodes 0\n                -showReferenceMembers 0\n                -showAttributes 1\n"
		+ "                -showConnected 1\n                -showAnimCurvesOnly 1\n                -showMuteInfo 0\n                -organizeByLayer 1\n                -organizeByClip 1\n                -showAnimLayerWeight 1\n                -autoExpandLayers 1\n                -autoExpand 0\n                -showDagOnly 0\n                -showAssets 1\n                -showContainedOnly 0\n                -showPublishedAsConnected 0\n                -showParentContainers 1\n                -showContainerContents 0\n                -ignoreDagHierarchy 0\n                -expandConnections 1\n                -showUpstreamCurves 1\n                -showUnitlessCurves 0\n                -showCompounds 1\n                -showLeafs 1\n                -showNumericAttrsOnly 1\n                -highlightActive 0\n                -autoSelectNewObjects 0\n                -doNotSelectNewObjects 1\n                -dropIsParent 1\n                -transmitFilters 0\n                -setFilter \"0\" \n                -showSetMembers 0\n                -allowMultiSelection 1\n"
		+ "                -alwaysToggleSelect 0\n                -directSelect 0\n                -displayMode \"DAG\" \n                -expandObjects 0\n                -setsIgnoreFilters 1\n                -containersIgnoreFilters 0\n                -editAttrName 0\n                -showAttrValues 0\n                -highlightSecondary 0\n                -showUVAttrsOnly 0\n                -showTextureNodesOnly 0\n                -attrAlphaOrder \"default\" \n                -animLayerFilterOptions \"allAffecting\" \n                -sortOrder \"none\" \n                -longNames 0\n                -niceNames 1\n                -showNamespace 1\n                -showPinIcons 0\n                -mapMotionTrails 1\n                -ignoreHiddenAttribute 0\n                -ignoreOutlinerColor 0\n                -renderFilterVisible 0\n                $editorName;\n\n\t\t\t$editorName = ($panelName+\"DopeSheetEd\");\n            dopeSheetEditor -e \n                -displayKeys 1\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n"
		+ "                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"integer\" \n                -snapValue \"none\" \n                -outliner \"dopeSheetPanel1OutlineEd\" \n                -showSummary 1\n                -showScene 0\n                -hierarchyBelow 0\n                -showTicks 1\n                -selectionWindow 0 0 0 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"timeEditorPanel\" (localizedPanelLabel(\"Time Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Time Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"clipEditorPanel\" (localizedPanelLabel(\"Trax Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Trax Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\n\t\t\t$editorName = clipEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 0 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"sequenceEditorPanel\" (localizedPanelLabel(\"Camera Sequencer\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Camera Sequencer\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = sequenceEditorNameFromPanel($panelName);\n            clipEditor -e \n                -displayKeys 0\n                -displayTangents 0\n                -displayActiveKeys 0\n"
		+ "                -displayActiveKeyTangents 0\n                -displayInfinities 0\n                -displayValues 0\n                -autoFit 0\n                -snapTime \"none\" \n                -snapValue \"none\" \n                -initialized 0\n                -manageSequencer 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperGraphPanel\" (localizedPanelLabel(\"Hypergraph Hierarchy\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypergraph Hierarchy\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"HyperGraphEd\");\n            hyperGraph -e \n                -graphLayoutStyle \"hierarchicalLayout\" \n                -orientation \"horiz\" \n                -mergeConnections 0\n                -zoom 1\n                -animateTransition 0\n                -showRelationships 1\n                -showShapes 0\n                -showDeformers 0\n"
		+ "                -showExpressions 0\n                -showConstraints 0\n                -showConnectionFromSelected 0\n                -showConnectionToSelected 0\n                -showConstraintLabels 0\n                -showUnderworld 0\n                -showInvisible 0\n                -transitionFrames 1\n                -opaqueContainers 0\n                -freeform 0\n                -imagePosition 0 0 \n                -imageScale 1\n                -imageEnabled 0\n                -graphType \"DAG\" \n                -heatMapDisplay 0\n                -updateSelection 1\n                -updateNodeAdded 1\n                -useDrawOverrideColor 0\n                -limitGraphTraversal -1\n                -range 0 0 \n                -iconSize \"smallIcons\" \n                -showCachedConnections 0\n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"visorPanel\" (localizedPanelLabel(\"Visor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Visor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"createNodePanel\" (localizedPanelLabel(\"Create Node\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Create Node\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"polyTexturePlacementPanel\" (localizedPanelLabel(\"UV Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"UV Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"renderWindowPanel\" (localizedPanelLabel(\"Render View\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n"
		+ "\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Render View\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"shapePanel\" (localizedPanelLabel(\"Shape Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tshapePanel -edit -l (localizedPanelLabel(\"Shape Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextPanel \"posePanel\" (localizedPanelLabel(\"Pose Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tposePanel -edit -l (localizedPanelLabel(\"Pose Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynRelEdPanel\" (localizedPanelLabel(\"Dynamic Relationships\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Dynamic Relationships\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"relationshipPanel\" (localizedPanelLabel(\"Relationship Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Relationship Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"referenceEditorPanel\" (localizedPanelLabel(\"Reference Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Reference Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"componentEditorPanel\" (localizedPanelLabel(\"Component Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Component Editor\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"dynPaintScriptedPanelType\" (localizedPanelLabel(\"Paint Effects\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Paint Effects\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"scriptEditorPanel\" (localizedPanelLabel(\"Script Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Script Editor\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"profilerPanel\" (localizedPanelLabel(\"Profiler Tool\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Profiler Tool\")) -mbv $menusOkayInPanels  $panelName;\n"
		+ "\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"contentBrowserPanel\" (localizedPanelLabel(\"Content Browser\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Content Browser\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"Stereo\" (localizedPanelLabel(\"Stereo\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Stereo\")) -mbv $menusOkayInPanels  $panelName;\nstring $editorName = ($panelName+\"Editor\");\n            stereoCameraView -e \n                -camera \"persp\" \n                -useInteractiveMode 0\n                -displayLights \"default\" \n                -displayAppearance \"smoothShaded\" \n                -activeOnly 0\n                -ignorePanZoom 0\n                -wireframeOnShaded 0\n"
		+ "                -headsUpDisplay 1\n                -holdOuts 1\n                -selectionHiliteDisplay 1\n                -useDefaultMaterial 0\n                -bufferMode \"double\" \n                -twoSidedLighting 0\n                -backfaceCulling 0\n                -xray 0\n                -jointXray 0\n                -activeComponentsXray 0\n                -displayTextures 0\n                -smoothWireframe 0\n                -lineWidth 1\n                -textureAnisotropic 0\n                -textureHilight 1\n                -textureSampling 2\n                -textureDisplay \"modulate\" \n                -textureMaxSize 16384\n                -fogging 0\n                -fogSource \"fragment\" \n                -fogMode \"linear\" \n                -fogStart 0\n                -fogEnd 100\n                -fogDensity 0.1\n                -fogColor 0.5 0.5 0.5 1 \n                -depthOfFieldPreview 1\n                -maxConstantTransparency 1\n                -objectFilterShowInHUD 1\n                -isFiltered 0\n                -colorResolution 4 4 \n"
		+ "                -bumpResolution 4 4 \n                -textureCompression 0\n                -transparencyAlgorithm \"frontAndBackCull\" \n                -transpInShadows 0\n                -cullingOverride \"none\" \n                -lowQualityLighting 0\n                -maximumNumHardwareLights 0\n                -occlusionCulling 0\n                -shadingModel 0\n                -useBaseRenderer 0\n                -useReducedRenderer 0\n                -smallObjectCulling 0\n                -smallObjectThreshold -1 \n                -interactiveDisableShadows 0\n                -interactiveBackFaceCull 0\n                -sortTransparent 1\n                -controllers 1\n                -nurbsCurves 1\n                -nurbsSurfaces 1\n                -polymeshes 1\n                -subdivSurfaces 1\n                -planes 1\n                -lights 1\n                -cameras 1\n                -controlVertices 1\n                -hulls 1\n                -grid 1\n                -imagePlane 1\n                -joints 1\n                -ikHandles 1\n"
		+ "                -deformers 1\n                -dynamics 1\n                -particleInstancers 1\n                -fluids 1\n                -hairSystems 1\n                -follicles 1\n                -nCloths 1\n                -nParticles 1\n                -nRigids 1\n                -dynamicConstraints 1\n                -locators 1\n                -manipulators 1\n                -pluginShapes 1\n                -dimensions 1\n                -handles 1\n                -pivots 1\n                -textures 1\n                -strokes 1\n                -motionTrails 1\n                -clipGhosts 1\n                -greasePencils 1\n                -shadows 0\n                -captureSequenceNumber -1\n                -width 0\n                -height 0\n                -sceneRenderFilter 0\n                -displayMode \"centerEye\" \n                -viewColor 0 0 0 1 \n                -useCustomBackground 1\n                $editorName;\n            stereoCameraView -e -viewSelected 0 $editorName;\n            stereoCameraView -e \n"
		+ "                -pluginObjects \"gpuCacheDisplayFilter\" 1 \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"hyperShadePanel\" (localizedPanelLabel(\"Hypershade\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Hypershade\")) -mbv $menusOkayInPanels  $panelName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\t$panelName = `sceneUIReplacement -getNextScriptedPanel \"nodeEditorPanel\" (localizedPanelLabel(\"Node Editor\")) `;\n\tif (\"\" != $panelName) {\n\t\t$label = `panel -q -label $panelName`;\n\t\tscriptedPanel -edit -l (localizedPanelLabel(\"Node Editor\")) -mbv $menusOkayInPanels  $panelName;\n\n\t\t\t$editorName = ($panelName+\"NodeEditorEd\");\n            nodeEditor -e \n                -allAttributes 0\n                -allNodes 0\n                -autoSizeNodes 1\n                -consistentNameSize 1\n                -createNodeCommand \"nodeEdCreateNodeCommand\" \n"
		+ "                -connectNodeOnCreation 0\n                -connectOnDrop 0\n                -highlightConnections \"bifrost\" 0\n                -copyConnectionsOnPaste 1\n                -defaultPinnedState 0\n                -additiveGraphingMode 0\n                -settingsChangedCallback \"nodeEdSyncControls\" \n                -traversalDepthLimit -1\n                -keyPressCommand \"nodeEdKeyPressCommand\" \n                -nodeTitleMode \"name\" \n                -gridSnap 0\n                -gridVisibility 1\n                -crosshairOnEdgeDragging 0\n                -popupMenuScript \"nodeEdBuildPanelMenus\" \n                -showNamespace 1\n                -showShapes 1\n                -showSGShapes 0\n                -showTransforms 1\n                -useAssets 1\n                -syncedSelection 1\n                -extendToShapes 1\n                -activeTab -1\n                -editorMode \"default\" \n                $editorName;\n\t\tif (!$useSceneConfig) {\n\t\t\tpanel -e -l $label $panelName;\n\t\t}\n\t}\n\n\n\tif ($useSceneConfig) {\n        string $configName = `getPanel -cwl (localizedPanelLabel(\"Current Layout\"))`;\n"
		+ "        if (\"\" != $configName) {\n\t\t\tpanelConfiguration -edit -label (localizedPanelLabel(\"Current Layout\")) \n\t\t\t\t-userCreated false\n\t\t\t\t-defaultImage \"\"\n\t\t\t\t-image \"\"\n\t\t\t\t-sc false\n\t\t\t\t-configString \"global string $gMainPane; paneLayout -e -cn \\\"single\\\" -ps 1 100 100 $gMainPane;\"\n\t\t\t\t-removeAllPanels\n\t\t\t\t-ap false\n\t\t\t\t\t(localizedPanelLabel(\"Persp View\")) \n\t\t\t\t\t\"modelPanel\"\n"
		+ "\t\t\t\t\t\"$panelName = `modelPanel -unParent -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels `;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1114\\n    -height 824\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t\t\"modelPanel -edit -l (localizedPanelLabel(\\\"Persp View\\\")) -mbv $menusOkayInPanels  $panelName;\\n$editorName = $panelName;\\nmodelEditor -e \\n    -cam `findStartUpCamera persp` \\n    -useInteractiveMode 0\\n    -displayLights \\\"default\\\" \\n    -displayAppearance \\\"smoothShaded\\\" \\n    -activeOnly 0\\n    -ignorePanZoom 0\\n    -wireframeOnShaded 0\\n    -headsUpDisplay 1\\n    -holdOuts 1\\n    -selectionHiliteDisplay 1\\n    -useDefaultMaterial 0\\n    -bufferMode \\\"double\\\" \\n    -twoSidedLighting 0\\n    -backfaceCulling 0\\n    -xray 0\\n    -jointXray 0\\n    -activeComponentsXray 0\\n    -displayTextures 0\\n    -smoothWireframe 0\\n    -lineWidth 1\\n    -textureAnisotropic 0\\n    -textureHilight 1\\n    -textureSampling 2\\n    -textureDisplay \\\"modulate\\\" \\n    -textureMaxSize 16384\\n    -fogging 0\\n    -fogSource \\\"fragment\\\" \\n    -fogMode \\\"linear\\\" \\n    -fogStart 0\\n    -fogEnd 100\\n    -fogDensity 0.1\\n    -fogColor 0.5 0.5 0.5 1 \\n    -depthOfFieldPreview 1\\n    -maxConstantTransparency 1\\n    -rendererName \\\"vp2Renderer\\\" \\n    -objectFilterShowInHUD 1\\n    -isFiltered 0\\n    -colorResolution 256 256 \\n    -bumpResolution 512 512 \\n    -textureCompression 0\\n    -transparencyAlgorithm \\\"frontAndBackCull\\\" \\n    -transpInShadows 0\\n    -cullingOverride \\\"none\\\" \\n    -lowQualityLighting 0\\n    -maximumNumHardwareLights 1\\n    -occlusionCulling 0\\n    -shadingModel 0\\n    -useBaseRenderer 0\\n    -useReducedRenderer 0\\n    -smallObjectCulling 0\\n    -smallObjectThreshold -1 \\n    -interactiveDisableShadows 0\\n    -interactiveBackFaceCull 0\\n    -sortTransparent 1\\n    -controllers 1\\n    -nurbsCurves 1\\n    -nurbsSurfaces 1\\n    -polymeshes 1\\n    -subdivSurfaces 1\\n    -planes 1\\n    -lights 1\\n    -cameras 1\\n    -controlVertices 1\\n    -hulls 1\\n    -grid 0\\n    -imagePlane 1\\n    -joints 1\\n    -ikHandles 1\\n    -deformers 1\\n    -dynamics 1\\n    -particleInstancers 1\\n    -fluids 1\\n    -hairSystems 1\\n    -follicles 1\\n    -nCloths 1\\n    -nParticles 1\\n    -nRigids 1\\n    -dynamicConstraints 1\\n    -locators 1\\n    -manipulators 1\\n    -pluginShapes 1\\n    -dimensions 1\\n    -handles 1\\n    -pivots 1\\n    -textures 1\\n    -strokes 1\\n    -motionTrails 1\\n    -clipGhosts 1\\n    -greasePencils 1\\n    -shadows 0\\n    -captureSequenceNumber -1\\n    -width 1114\\n    -height 824\\n    -sceneRenderFilter 0\\n    $editorName;\\nmodelEditor -e -viewSelected 0 $editorName;\\nmodelEditor -e \\n    -pluginObjects \\\"gpuCacheDisplayFilter\\\" 1 \\n    $editorName\"\n"
		+ "\t\t\t\t$configName;\n\n            setNamedPanelLayout (localizedPanelLabel(\"Current Layout\"));\n        }\n\n        panelHistory -e -clear mainPanelHistory;\n        sceneUIReplacement -clear;\n\t}\n\n\ngrid -spacing 5 -size 12 -divisions 5 -displayAxes yes -displayGridLines yes -displayDivisionLines yes -displayPerspectiveLabels no -displayOrthographicLabels no -displayAxesBold yes -perspectiveLabelPosition axis -orthographicLabelPosition edge;\nviewManip -drawCompass 0 -compassAngle 0 -frontParameters \"\" -homeParameters \"\" -selectionLockParameters \"\";\n}\n");
	setAttr ".st" 3;
createNode script -n "sceneConfigurationScriptNode";
	rename -uid "C0395169-474E-2A64-AD54-43A8176C3716";
	setAttr ".b" -type "string" "playbackOptions -min 1 -max 120 -ast 1 -aet 200 ";
	setAttr ".st" 6;
createNode animCurveTU -n "ClusterNetwork_World_pointsPerCluster";
	rename -uid "572A1DB4-4C3A-53CA-336A-10AC079929D9";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 120 120;
select -ne :time1;
	setAttr ".o" 76;
	setAttr ".unw" 76;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 2 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 4 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "polyCube1.out" "pCubeShape1.i";
connectAttr "ClusterNetwork.outputPoints" "ClusterNetwork_Instancer.inp";
connectAttr "ClusterNetwork.instancerMessage" "ClusterNetwork_Instancer.instancerMessage"
		;
connectAttr "pCube1.m" "ClusterNetwork_Instancer.inh[0]";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
connectAttr "layerManager.dli[0]" "defaultLayer.id";
connectAttr "renderLayerManager.rlmi[0]" "defaultRenderLayer.rlid";
connectAttr "ClusterNetwork_World.outputPoints" "ClusterNetwork.inputPoints";
connectAttr "ClusterNetwork_Distribute.waiterMessage" "ClusterNetwork.waiterMessage"
		;
connectAttr "ClusterNetwork_Distribute.outputPoints" "ClusterNetwork_World.inputPoints"
		;
connectAttr "ClusterNetwork_World_pointsPerCluster.o" "ClusterNetwork_World.pointsPerCluster"
		;
connectAttr "defaultRenderLayer.msg" ":defaultRenderingList1.r" -na;
connectAttr "pCubeShape1.iog" ":initialShadingGroup.dsm" -na;
// End of clusterNetwork.ma
