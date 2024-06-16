#version 330 core

layout(std140) uniform GlobalSettings
{
    vec4 lockedKeyColor;
    vec4 lockedCurveColor;
    vec4 defaultKeyColor;
    vec4 bufferCurveColor;
    vec4 breakDownKeyColor;
    vec4 keyOnBufferCurveColor;
	vec4 preSelectHighlightColor;
	vec4 primarySelectionColor;
	vec4 secondarySelectionColor;
	vec4 graphEditorBackgroundColor;
    bool displayKeysOnSelection;
    bool displayTangentsAlways;
    bool displayTangentsOnSelection;
    bool simpleKeyView;
    float keyScale;
    float keyMinScale;
    float timeMultiplier;
    bool highlightAffectedCurves;
    //uint padding[4];
}globalSettings; 

layout(std140) uniform PerFrame
{
    layout(column_major) mat4 projection;                               // transform world space into NDC space [-1,1].
    layout(column_major) mat4 projectionWithoutHorizontalTranslation;   
    layout(column_major) mat4 viewportInv;                              // transform viewport space(pixel) into NDC space [-1,1].
    layout(column_major) mat4 viewport;                                 // transform NDC [-1,1] into viewport space(pixel).
    int   projectionOffsetXSec;
    int   projectionOffsetXFrac;
    uint  displayPoint;
    float viewRegionMinX;
    float viewRegionMaxX;
    float viewRegionMinY;
    float viewRegionMaxY;  
    float viewRegionWidth;
    float keysDensity;
}perFrame;

layout(std140) uniform PerCurve
{
    layout(column_major) mat4  transformMatrix;
    vec4 color;    
    int   startTimeSec;
    int   startTimeFrac;
    float valueRange;		 
    int   timeRangeSec;		
    int   timeRangeFrac;		
    uint  preInfinityType;      
    uint  postInfinityType;  
    bool  isWeighted;
	uint  preHighlightCurvePart; 
	uint  preHighlightKeyIndex;
    bool  isBuffered;
	bool  isQuaternion;
	bool  useQuaternionKeyShape;
	bool  isPlotted;
	bool  isLocked;
	bool  isReferenced;
	bool  hasCustomTangent;
	bool  useFullStipplePattern;
}perCurve;

layout(std140) uniform PerCurveInstance
{
    layout(column_major) mat4  transformMatrix;
    uint firstVisibleKeyIndex;
}perCurveInstance;

layout(location = 0) in int   inPosXSec;
layout(location = 1) in int   inPosXFrac;
layout(location = 2) in float inPosY;
layout(location = 3) in int   inTanXSec;
layout(location = 4) in int   inTanXFrac;
layout(location = 5) in float inTanY;
layout(location = 6) in int   outTanXSec;
layout(location = 7) in int   outTanXFrac;
layout(location = 8) in float outTanY;
layout(location = 9) in uint  inFlags;

out VS_OUT
{
    vec2 inTanNDC;
    vec2 outTanNDC;
    uint flags;
}vs_output;


//
// Convert tow integers time in float
//
float decodeTime(int timeSec, int timeFraction, int offsetSec, int offsetFraction)
{
    return float(timeSec - offsetSec) + (float(timeFraction - offsetFraction) / globalSettings.timeMultiplier);
}


void main()
{  
    float keyPosX = decodeTime(inPosXSec, inPosXFrac,  perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);
    float inTanX  = decodeTime(inTanXSec, inTanXFrac,  perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);
    float outTanX = decodeTime(outTanXSec,outTanXFrac, perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);
    

    vec2 keyPos = vec2(keyPosX, inPosY);
    vec2 intTan = vec2(inTanX,  inTanY);
    vec2 outTan = vec2(outTanX, outTanY) ;
    
    // Compute the curve transformation
    mat4 curveTransform    = perCurveInstance.transformMatrix * perCurve.transformMatrix;
    
    // Transform the curve transformation in normalize device coordinate (NDC) space    
    mat4 curveTransformNDC = perFrame.projectionWithoutHorizontalTranslation * curveTransform;
    
    vs_output.inTanNDC  =  ( curveTransformNDC * vec4( intTan, 0.0f, 1.0f ) ).xy;
    vs_output.outTanNDC =  ( curveTransformNDC * vec4( outTan, 0.0f, 1.0f ) ).xy; 
    vs_output.flags     =  inFlags;
    gl_Position         =  curveTransformNDC * vec4( keyPos,  0.0f, 1.0f );
}