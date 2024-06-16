#version 330 core


const uint kInfinityConstant      = 0u;
const uint kInfinityLinear        = 1u;
const uint kInfinityCycle         = 3u;
const uint kInfinityCycleRelative = 4u;
const uint kInfinityOscillate     = 5u;

const uint kShaderModeNormal       = 0u;
const uint kShaderModePreInfinity  = 1u;
const uint kShaderModePostInfinity = 2u;


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
    uint displayPoint;
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


layout(std140) uniform ShaderSettings
{
    uint mode;
}shaderSettings;

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
    vec2 pos;
    vec2 inTan;
    vec2 outTan;
    uint flags;
    flat int instanceID;
}vs_output;


//
// Convert an integer time in float
//
float decodeTime(int timeSec, int timeFraction, int offsetSec, int offsetFraction)
{
    return float(timeSec - offsetSec) + (float(timeFraction - offsetFraction) / globalSettings.timeMultiplier);
}


void applayInfinityTransform(inout mat4 pOutMatrix);



void main()
{  
    float keyPosX = decodeTime(inPosXSec, inPosXFrac,  perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);
    float inTanX  = decodeTime(inTanXSec, inTanXFrac,  perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);
    float outTanX = decodeTime(outTanXSec,outTanXFrac, perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac);

    vec2 keyPos = vec2(keyPosX, inPosY);
    vec2 intTan = vec2(inTanX,  inTanY);
    vec2 outTan = vec2(outTanX, outTanY) ;
    
    mat4 lCurveMat;
    if(perCurve.isPlotted)
    {
        // plotted curve already containt per instance transform
        lCurveMat = perCurve.transformMatrix;
    }
    else
    {
        lCurveMat = perCurveInstance.transformMatrix * perCurve.transformMatrix;
    }
    
    applayInfinityTransform( lCurveMat );
    
    mat4 curveProj = perFrame.projectionWithoutHorizontalTranslation * lCurveMat;
     
    vs_output.pos        = ( lCurveMat * vec4( keyPos, 0.0f, 1.0f ) ).xy;
    vs_output.inTan      = ( curveProj * vec4( intTan, 0.0f, 1.0f ) ).xy;
    vs_output.outTan     = ( curveProj * vec4( outTan, 0.0f, 1.0f ) ).xy; 
    vs_output.flags      = inFlags;
    vs_output.instanceID = gl_InstanceID;
    gl_Position          = curveProj * vec4( keyPos, 0, 1);
}



void applayInfinityTransform(inout mat4 pOutMatrix)
{
   float curveLength = decodeTime(perCurve.timeRangeSec, perCurve.timeRangeFrac, 0, 0);
                
   if( shaderSettings.mode == kShaderModePreInfinity )   
   {
        if( perCurve.preInfinityType == kInfinityCycle ) // cycle
        {
            float lOffsetX = curveLength  * (gl_InstanceID+1);
        
            mat4 lOffsetYMatrix = mat4(1);
            lOffsetYMatrix[3].x = -lOffsetX;
            pOutMatrix *= lOffsetYMatrix;        
        }   
        else if( perCurve.preInfinityType == kInfinityCycleRelative ) // cycle offset
        {
            float lOffsetX = curveLength  * (gl_InstanceID+1);
            float lOffsetY = perCurve.valueRange * (gl_InstanceID+1);
        
            mat4 lOffsetYMatrix = mat4(1);
            lOffsetYMatrix[3].x = -lOffsetX;
            lOffsetYMatrix[3].y = -lOffsetY;
            pOutMatrix *= lOffsetYMatrix;        
        }
        else if( perCurve.preInfinityType == kInfinityOscillate ) // kOscillate
        {           
            if( bool( gl_InstanceID & 1) )
            {     
                // Compute the translation offset
                mat4 lTranslateMatrix = mat4(1);
                lTranslateMatrix[3].x = -( curveLength  * (gl_InstanceID + 1) );   
                pOutMatrix *=  lTranslateMatrix; 
            }
            else
            {
                // Compute the transformation matrix for the infinity repetition
                float curveStartTime = decodeTime(perCurve.startTimeSec, perCurve.startTimeFrac, 0, 0);
                             
                float lOffsetX = curveLength  * (gl_InstanceID);
            
                mat4 lCenterMatrix = mat4(1);
                lCenterMatrix[3].x = -curveStartTime;
            
                mat4 lCenterMatrix2 = mat4(1);
                lCenterMatrix2[3].x = curveStartTime;
                
                mat4 lScaleMatrix     = mat4(1);
                lScaleMatrix[0].x     = -1;
                
                mat4 lTranslateMatrix2 = mat4(1);
                lTranslateMatrix2[3].x = -lOffsetX;

                mat4 lTranslateMatrix3 = mat4(1);
                lTranslateMatrix3[3].x = 2.0 * -decodeTime(perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac, 0, 0);                
                
                pOutMatrix *=  lTranslateMatrix3 * lTranslateMatrix2 * lCenterMatrix2 * lScaleMatrix * lCenterMatrix;
            }                  
        }
   }
   else if( shaderSettings.mode == kShaderModePostInfinity )   
   {    
        if( perCurve.postInfinityType == kInfinityCycle ) // cycle
        {
            float lOffsetX = curveLength  * (gl_InstanceID+1);
        
            mat4 lOffsetYMatrix = mat4(1);
            lOffsetYMatrix[3].x = lOffsetX;
            pOutMatrix *= lOffsetYMatrix;        
        }   
        else if( perCurve.postInfinityType == kInfinityCycleRelative ) // cycle offset
        {   
            float lOffsetX = curveLength  * (gl_InstanceID+1);
            float lOffsetY = perCurve.valueRange * (gl_InstanceID+1);
        
            mat4 lOffsetYMatrix = mat4(1);
            lOffsetYMatrix[3].x = lOffsetX;
            lOffsetYMatrix[3].y = lOffsetY;
            pOutMatrix *= lOffsetYMatrix;  
        }
        else if( perCurve.postInfinityType == kInfinityOscillate ) // kOscillate
        {
            if( bool( gl_InstanceID & 1) )
            {              
                mat4 lTranslateMatrix = mat4(1);
                lTranslateMatrix[3].x = curveLength  * (gl_InstanceID + 1);   
                pOutMatrix *=  lTranslateMatrix; 
            }
            else
            {
                // pair
                float curveStartTime = decodeTime(perCurve.startTimeSec, perCurve.startTimeFrac, 0, 0);           
                
                float lOffsetX = curveLength  * (gl_InstanceID+2);
            
                mat4 lCenterMatrix = mat4(1);
                lCenterMatrix[3].x = -curveStartTime;
            
                mat4 lCenterMatrix2 = mat4(1);
                lCenterMatrix2[3].x = curveStartTime;
                
                mat4 lScaleMatrix     = mat4(1);
                lScaleMatrix[0].x     = -1;
                
                mat4 lTranslateMatrix2 = mat4(1);
                lTranslateMatrix2[3].x = lOffsetX;              

                mat4 lTranslateMatrix3 = mat4(1);
                lTranslateMatrix3[3].x = 2.0 * -decodeTime(perFrame.projectionOffsetXSec, perFrame.projectionOffsetXFrac, 0, 0); 
                
                pOutMatrix *=  lTranslateMatrix3 * lTranslateMatrix2 * lCenterMatrix2 * lScaleMatrix * lCenterMatrix; 
            }       
        }        
   }
}