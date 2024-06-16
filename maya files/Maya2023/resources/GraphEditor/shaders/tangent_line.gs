#version 330 core

// flags for keys
const uint kInvisible                 = uint(1 << 0);
const uint kIsKeyframeActive          = uint(1 << 1);
const uint kIsInTangentActive         = uint(1 << 2);
const uint kIsOutTangentActive        = uint(1 << 3);
const uint kNeedToDrawInTangent       = uint(1 << 4);
const uint kNeedToDrawOutTangent      = uint(1 << 5);
const uint kIsStepOut                 = uint(1 << 6);
const uint kIsStepNextOut             = uint(1 << 7);
const uint kIsLinearIn                = uint(1 << 8);
const uint kIsLinearOut               = uint(1 << 9);
const uint kIsFixedIn                 = uint(1 << 10);
const uint kIsFixedOut                = uint(1 << 11);
const uint kIsTangentLocked           = uint(1 << 12);
const uint kIsWeightLocked            = uint(1 << 13);
const uint kIsBreakdown               = uint(1 << 14);
const uint kCanDisplayTangentInAngle  = uint(1 << 15);
const uint kCanDisplayTangentOutAngle = uint(1 << 16);
const uint kCanDisplayTangentLength   = uint(1 << 17);
const uint kAnySelected               = uint(1 << 18);

const vec4 kTangentColorWeightLocked = vec4(0.0f, 0.0f, 0.0f, 1.0f);


const uint kPreHighlightCurveInTan  = 3u;
const uint kPreHighlightCurveOutTan = 4u;


bool isInTangentActive(uint flags)
{
    return bool(flags & kIsInTangentActive);
}
bool isOutTangentActive(uint flags)
{
    return bool(flags & kIsOutTangentActive);
}
bool isKeyAnySelected(uint flags)
{
    return bool(flags & kAnySelected);
}
bool isKeyTangentLocked(uint flags)
{
    return bool(flags & kIsTangentLocked);
}
bool isKeyTangentWeightLocked(uint flags)
{
    return bool(flags & kIsWeightLocked);
}
bool isKeyStepOut(uint flags)
{
    return bool(flags & kIsStepOut);
}
bool isKeyStepNextOut(uint flags)
{
    return bool(flags & kIsStepNextOut);
}
bool isKeyLinearIn(uint flags)
{
    return bool(flags & kIsLinearIn);
}
bool isKeyLinearOut(uint flags)
{
    return bool(flags & kIsLinearOut);
}
bool isNeedToDrawInTangent(uint flags)
{
    return bool(flags & kNeedToDrawInTangent);
}

bool isNeedToDrawOutTangent(uint flags)
{
    return bool(flags & kNeedToDrawOutTangent);
}

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


layout(points) in;
layout(line_strip, max_vertices=4) out;

in VS_OUT
{
    vec2 inTanNDC;
    vec2 outTanNDC;
    uint flags;
}gs_input[];
 
out GS_OUT
{
    vec4  color;
    float stippleLineCoord;
    flat uint  useStipplePattern;
}gs_output;
 
void generateNonWeightedTangentPosition(out vec2 pInTanNDC, out vec2 pOutTanNDC, vec2 pRatio );
 
void main()
{
    if( globalSettings.displayTangentsAlways || 
      ( globalSettings.displayTangentsOnSelection && isKeyAnySelected( gs_input[0].flags) ) )
    {
	
		//
		// Todo : ratio computation should be on the cpu side
		vec4 p0 = vec4( 0,0,0,1 );
		vec4 p1 = vec4( 1,1,0,1 );
    
		vec4 p00 = perFrame.viewportInv * p0;
		vec4 p11 = perFrame.viewportInv * p1;
		vec2 ratio = (p11 - p00).xy;
	
	
        bool lUseStipplePattern = !isKeyTangentLocked(gs_input[0].flags);

		vec2 lInTanNDC, lOutTanNDC;
		lInTanNDC = gs_input[0].inTanNDC;
		lOutTanNDC = gs_input[0].outTanNDC;

		// Compute position of tangents as 1/7th of window if curve is not weighted
		if(!perCurve.isWeighted)
        {
            generateNonWeightedTangentPosition(lInTanNDC, lOutTanNDC, ratio );
        }
        // compute the key and tangents position in window space (pixel space)
        vec2 lInTanWinPos  = (perFrame.viewport * vec4( lInTanNDC, 0, 1) ).xy;
        vec2 lPosWinPos    = (perFrame.viewport * gl_in[0].gl_Position ).xy;
        vec2 lOutTanWinPos = (perFrame.viewport * vec4( lOutTanNDC,0, 1) ).xy;

        vec4 lTangentColor;
        
        uint keyIndex = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
		    
        //
        // In tangent line
        //
        if( isNeedToDrawInTangent(gs_input[0].flags) )
        {
            if( (perCurve.preHighlightCurvePart == kPreHighlightCurveInTan && keyIndex == uint(gl_PrimitiveIDIn) ) )
            {
                lTangentColor = globalSettings.preSelectHighlightColor;
            }
            else if (isInTangentActive(gs_input[0].flags))
            {
                lTangentColor = globalSettings.primarySelectionColor;
            }
            else
            {
                lTangentColor = globalSettings.secondarySelectionColor;
            }

            // Tangent should be black in color if weight is locked. Handles
            // remain unchanged. (MAYA-72729)
            if(isKeyTangentWeightLocked(gs_input[0].flags))
            {
                lTangentColor = kTangentColorWeightLocked;
            }

            gs_output.useStipplePattern = uint( lUseStipplePattern );
            gs_output.stippleLineCoord  = length( lInTanWinPos - lPosWinPos );
            gs_output.color = lTangentColor; 
            gl_Position = vec4( lInTanNDC, 0, 1);
            EmitVertex();  
            
            gs_output.useStipplePattern = uint( lUseStipplePattern );
            gs_output.stippleLineCoord = 0.0f;
            gs_output.color = lTangentColor; 
            gl_Position = gl_in[0].gl_Position;
            EmitVertex(); 
        }
 
       

        
        //
        // Out tangent line
        //
        if( isNeedToDrawOutTangent(gs_input[0].flags) )
        {
            if( (perCurve.preHighlightCurvePart == kPreHighlightCurveOutTan && keyIndex == uint(gl_PrimitiveIDIn) ) )
            {
                lTangentColor = globalSettings.preSelectHighlightColor;
            }
            else if (isOutTangentActive(gs_input[0].flags))
            {
                lTangentColor = globalSettings.primarySelectionColor;
            }
            else
            {
                lTangentColor = globalSettings.secondarySelectionColor;
            }

            if(isKeyTangentWeightLocked(gs_input[0].flags))
            {
                lTangentColor = kTangentColorWeightLocked;
            }
            
           
            gs_output.useStipplePattern = uint( lUseStipplePattern );
            gs_output.stippleLineCoord = 0.0f;
            gs_output.color = lTangentColor; 
            gl_Position = gl_in[0].gl_Position;
            EmitVertex();  
            
            gs_output.useStipplePattern = uint( lUseStipplePattern );
            gs_output.stippleLineCoord = length( lOutTanWinPos - lPosWinPos);
            gs_output.color = lTangentColor; 
            gl_Position = vec4( lOutTanNDC, 0, 1);                                            
            EmitVertex();     
        }
    }   
}

void generateNonWeightedTangentPosition( out vec2 pInTanNDC, out vec2 pOutTanNDC, vec2 pRatio )
{
	// MAYA-77496 - NonWeighted tangents should have total tangent length = 1/7th of port size
	// In and Out tangents each are 1/14th of port size
	// In NDC width is always 2 units. We apply to each tangent a scale to 1/14th the port size
	// Each tangent length should then be 2/14 = approx 0.143

	float lTanLengthNDC, tangentRatio;
	vec2 tempVector;

	// to center tangents at key, the scale factor differs based on their original length
	lTanLengthNDC = length((gs_input[0].inTanNDC - gl_in[0].gl_Position.xy)/(pRatio/pRatio.x));
	tangentRatio = 0.143/lTanLengthNDC;
	tempVector = gs_input[0].inTanNDC - gl_in[0].gl_Position.xy;
	pInTanNDC = tangentRatio*tempVector + gl_in[0].gl_Position.xy;

	lTanLengthNDC = length((gl_in[0].gl_Position.xy - gs_input[0].outTanNDC)/(pRatio/pRatio.x));
	tangentRatio = 0.143/lTanLengthNDC;
	tempVector = gs_input[0].outTanNDC - gl_in[0].gl_Position.xy;
	pOutTanNDC = tangentRatio*tempVector + gl_in[0].gl_Position.xy;
}

