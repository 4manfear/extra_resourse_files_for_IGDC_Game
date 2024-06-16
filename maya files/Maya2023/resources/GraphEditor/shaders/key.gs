#version 330 core
#define ALLOW_STIPPLE_RANGE 1

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

bool isKeyAnySelected(uint flags)
{
    return bool(flags & kAnySelected);
}
bool isKeySelected(uint flags)
{
    return bool(flags & kIsKeyframeActive);
}
bool isInTangentActive(uint flags)
{
    return bool(flags & kIsInTangentActive);
}
bool isOutTangentActive(uint flags)
{
    return bool(flags & kIsOutTangentActive);
}
bool isKeyFixedIn(uint flags)
{
    return bool(flags & kIsFixedIn);
}
bool isKeyFixedOut(uint flags)
{
    return bool(flags & kIsFixedOut);
}
bool isNeedToDrawInTangent(uint flags)
{
    return bool(flags & kNeedToDrawInTangent);
}

bool isNeedToDrawOutTangent(uint flags)
{
    return bool(flags & kNeedToDrawOutTangent);
}
bool isKeyBreakdown(uint flags)
{
    return bool(flags & kIsBreakdown);
}

float clamp(float v, float min, float max)
{
    if (v > max) return max;
    else if (v < min) return min;
    else return v;
}

const float kKeyRadius                  = 6.0;
const float kSimpleKeyRadius            = 4.0;
const float kTangentHandleRadius        = 5.5;
const float kSimpleTangentHandleRadius  = 5.5;

const vec4 kMutedKeyColor2         = vec4(0.5098f, 0.5098f, 0.5098f, 1.0f);

const uint kPreHighlightCurveKey    = 2u;
const uint kPreHighlightCurveInTan  = 3u;
const uint kPreHighlightCurveOutTan = 4u;

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
layout(triangle_strip, max_vertices=100) out; 

in VS_OUT
{
    vec2 inTanNDC;
    vec2 outTanNDC;
    uint flags;
}gs_input[];
 
out GS_OUT
{
    vec4 color;
}gs_output;
 
//
// Tangent generations
//
void generateTangentsHandle(bool pInTangent, vec4 pOutterColor, vec4 pInnerColor, vec2 pRatio, bool simple, float keyScale );
void generateNonWeightedTangentPosition(out vec2 pInTanNDC, out vec2 pOutTanNDC, vec2 pRatio );
void drawTangentHandle(vec4 pColor, vec2 pPos, vec2 pPivot, float pHalfWidth, float pHalfHeight, vec2 pRatio);
void drawTangentSquareHandle(vec4 pColor, vec2 pPos, vec2 pPivot, float pHalfWidth, float pHalfHeight, vec2 pRatio);
//
// Key generations
//
void generateSimpleKeyShape(vec4 pOutterColor, vec4 pOutterColor2, vec4 pInnerColor, vec2 pRatio, float keyScale);
void generateKeyShape(vec4 pOutterColor, vec4 pOutterColor2, vec4 pInnerColor, vec2 pRatio, float keyScale);
void generateDiamond(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateHalfLeftDiamond(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateHalfRightDiamond(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateSquare(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateSquare(vec4 pColor, float pHalfWidth, float pHalfHeight, float pAngleInDegree);
void generateLeftSquare(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateRightSquare(vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateCircle(vec2 pPosition, vec4 pColor, float pHalfWidth, float pHalfHeight);
void generateCircle(vec2 pPosition, vec4 pColor1, vec4 pColor2, float pHalfWidth, float pHalfHeight);


void renderTangent(bool isInTangent, bool isTangentActive, bool isPreHighlight, vec2 ratio, uint keyIndex)
{    
    vec4 lColor = globalSettings.secondarySelectionColor;  
    if( isPreHighlight && keyIndex == uint(gl_PrimitiveIDIn) )
    {
        lColor = globalSettings.preSelectHighlightColor;
    }
    else if( isTangentActive )
    {
        lColor = globalSettings.primarySelectionColor;
    }
    // MAYA-75683: Inner color of tangent handle should match graph editor background
    generateTangentsHandle( isInTangent, lColor, globalSettings.graphEditorBackgroundColor, ratio, globalSettings.simpleKeyView, globalSettings.keyScale );
}

void main()
{
    //
    // Todo : ratio computation should be on the cpu side
    // Todo : Cull keys that are not visible
    // Todo : Cull tangents that are not visible
    vec4 p0 = vec4( 0,0,0,1 );
    vec4 p1 = vec4( 1,1,0,1 );
    
    vec4 p00 = perFrame.viewportInv * p0;
    vec4 p11 = perFrame.viewportInv * p1;
    vec2 ratio = (p11 - p00).xy;

    bool lIsKeySelected = isKeySelected( gs_input[0].flags );
    bool lDisplayKey = !globalSettings.displayKeysOnSelection || (globalSettings.displayKeysOnSelection && lIsKeySelected );

    uint keyIndex = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
    
    if( lDisplayKey )
    {           
        bool isPreHighlight      = (perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) );
        vec4 lOuterKeyColor      = globalSettings.defaultKeyColor;
        vec4 lOuterKeyColor2     = globalSettings.defaultKeyColor;  // only use for muted curve
        
        if(perCurve.isBuffered)
        {
            lOuterKeyColor = globalSettings.keyOnBufferCurveColor;
        }
        else if(perCurve.isLocked || perCurve.isReferenced)
        {
            lOuterKeyColor = globalSettings.lockedKeyColor;
            lOuterKeyColor2 = kMutedKeyColor2;
        } 
        else if( perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) )
        {
            lOuterKeyColor = globalSettings.preSelectHighlightColor;
        }
        else if( lIsKeySelected )
        {
            lOuterKeyColor = globalSettings.primarySelectionColor;
        }
        else if( isKeyBreakdown(gs_input[0].flags) )
        {
            lOuterKeyColor = globalSettings.breakDownKeyColor;
        }

        // MAYA-75683: Inner color of key should match graph editor background
        if (globalSettings.simpleKeyView)
            generateSimpleKeyShape(lOuterKeyColor, lOuterKeyColor2, globalSettings.graphEditorBackgroundColor, ratio, globalSettings.keyScale );
        else
            generateKeyShape(lOuterKeyColor, lOuterKeyColor2, globalSettings.graphEditorBackgroundColor, ratio, globalSettings.keyScale );
    }
        
      
    if(  !perCurve.isBuffered &&
         !perCurve.isQuaternion &&
        ( globalSettings.displayTangentsAlways ||
        ( globalSettings.displayTangentsOnSelection && isKeyAnySelected(gs_input[0].flags) ) ) 
      ) 
    {
        // render the in tangent
        if( isNeedToDrawInTangent(gs_input[0].flags) )
        {        
            renderTangent(true, isInTangentActive( gs_input[0].flags ), perCurve.preHighlightCurvePart == kPreHighlightCurveInTan, ratio, keyIndex);
        }
        
        // render the out tangent 
        if( isNeedToDrawOutTangent(gs_input[0].flags) )
        {
            renderTangent(false, isOutTangentActive( gs_input[0].flags ), perCurve.preHighlightCurvePart == kPreHighlightCurveOutTan, ratio, keyIndex);
        }
    }        
}


void generateTangentsHandle(bool pInTangent, vec4 pOutterColor, vec4 pInnerColor, vec2 pRatio, bool simple, float keyScale )
{
    // First figure out whether we want an open shape or not
    bool useTriangleShape = !simple && !perCurve.isWeighted; // use triangle in detailed mode for non-weighted tangents
    bool openShape = false;
    if (simple) {
        openShape = perCurve.isWeighted;
    } else {
        bool isTanInFixed  = isKeyFixedIn( gs_input[0].flags );
        bool isTanOutFixed = isKeyFixedOut( gs_input[0].flags );
        openShape = (pInTangent && !isTanInFixed) || (!pInTangent && !isTanOutFixed);
    }

    float baseRadius = keyScale * (simple ? kSimpleTangentHandleRadius : kTangentHandleRadius);
    if (simple && !openShape) baseRadius *= 0.7;

    float handleRadius = clamp(baseRadius / perFrame.keysDensity, 1.0, baseRadius);
    if (handleRadius < 2.0)
        openShape = false;

    float halfWidth  = (handleRadius * pRatio.x) * 0.5f;
    float halfHeight = (handleRadius * pRatio.y) * 0.5f;

    float halfInnerWidth  = halfWidth - (pRatio.x * 1.0);
    float halfInnerHeight = halfHeight- (pRatio.y * 1.0);

    vec2 lInTanNDC = gs_input[0].inTanNDC;
    vec2 lOutTanNDC = gs_input[0].outTanNDC;
    if (!perCurve.isWeighted)
        generateNonWeightedTangentPosition(lInTanNDC, lOutTanNDC, pRatio);
    vec2 tanPosNDC = pInTangent ? lInTanNDC : lOutTanNDC;

    if (useTriangleShape) {
        drawTangentHandle(pOutterColor, tanPosNDC, gl_in[0].gl_Position.xy, halfWidth, halfHeight, pRatio);
        if(openShape)
            drawTangentHandle(pInnerColor, tanPosNDC, gl_in[0].gl_Position.xy, halfInnerWidth, halfInnerHeight, pRatio);
    } else {
        drawTangentSquareHandle(pOutterColor, tanPosNDC, gl_in[0].gl_Position.xy, halfWidth, halfHeight, pRatio );
        if(openShape)
            drawTangentSquareHandle( pInnerColor, tanPosNDC, gl_in[0].gl_Position.xy, halfInnerWidth, halfInnerHeight, pRatio );
    }
}

void generateNonWeightedTangentPosition( out vec2 pInTanNDC, out vec2 pOutTanNDC, vec2 pRatio)
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

void drawTangentHandle(vec4 pColor, vec2 pPos, vec2 pPivot, float pHalfWidth, float pHalfHeight, vec2 pRatio)
{
    vec2 tangents = (pPivot - pPos) / pRatio;
    float tanLen  = sqrt( dot(tangents, tangents) );    
    float invTenLen = 1.0f / tanLen;
    
	// 2x2 RX matrix terms to position the handle in the pixel space
    float halfWidthX  = pHalfWidth *  tangents.x * invTenLen;
    float halfWidthY  = pHalfHeight*  tangents.y * invTenLen;
    float halfHeightX = pHalfWidth * (-tangents.y* invTenLen);
    float halfHeightY = pHalfHeight* (tangents.x * invTenLen);
    
    //
    // Create the in tangent handle
    //
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x-halfWidthX-halfHeightX*1.2,
                        pPos.y-halfHeightY*1.2-halfWidthY,
                        0,1
                        );
    EmitVertex();
    
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x+halfWidthX*1.4, 
                        pPos.y+halfWidthY*1.4,
                        0,1
                        );
    EmitVertex();
    
    gs_output.color = pColor;
    gl_Position = vec4( pPos.x - halfWidthX  +  halfHeightX*1.2, 
                        pPos.y + halfHeightY * 1.2 - halfWidthY,
                        0,1
                        );
    EmitVertex();
    EndPrimitive();    
} 
 
void drawTangentSquareHandle(vec4 pColor, vec2 pPos, vec2 pPivot, float pHalfWidth, float pHalfHeight, vec2 pRatio)
{
    vec2  tangents  = (pPivot - pPos) / pRatio;
    float tanLen  = sqrt( dot(tangents, tangents) );
    float invTenLen = 1.0f / tanLen;
    
	// 2x2 RX matrix terms to position the handle in the pixel space
    float halfWidthX  = pHalfWidth * tangents.x   * invTenLen;
    float halfWidthY  = pHalfHeight* tangents.y   * invTenLen;
    float halfHeightX = pHalfWidth * (-tangents.y * invTenLen);
    float halfHeightY = pHalfHeight* (tangents.x  * invTenLen);
              
    // left bottom
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x - halfWidthX - halfHeightX,
                        pPos.y - halfHeightY- halfWidthY,
                        0,1
                        );
    EmitVertex();
    
    // right bottom
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x + halfWidthX  - halfHeightX,
                        pPos.y - halfHeightY + halfWidthY,
                        0,1
                        );
    EmitVertex();
    
    // right top
    gs_output.color = pColor;
    gl_Position = vec4(  pPos.x + halfWidthX  + halfHeightX,
                         pPos.y + halfHeightY + halfWidthY,
                         0,1
                         );
    EmitVertex();    
    
    // left top
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x - halfWidthX + halfHeightX,
                        pPos.y + halfHeightY- halfWidthY,
                        0,1
                        );    
    EmitVertex(); 
    
    // left bottom
    gs_output.color = pColor;    
    gl_Position = vec4( pPos.x - halfWidthX - halfHeightX,
                        pPos.y - halfHeightY- halfWidthY,
                        0,1
                        );
    EmitVertex(); 
    EndPrimitive();                                      
} 

void generateSimpleKeyShape(vec4 pOutterColor, vec4 pOutterColor2, vec4 pInnerColor, vec2 pRatio, float keyScale )
{
    float baseRadius = kSimpleKeyRadius*keyScale;
    float keyRadius = clamp(baseRadius / perFrame.keysDensity, 1.0, baseRadius);

    float halfWidth  = (keyRadius * pRatio.x) * 0.5f;
    float halfHeight = (keyRadius * pRatio.y) * 0.5f;

    generateSquare(pOutterColor, halfWidth, halfHeight);
}

void generateKeyShape(vec4 pOutterColor, vec4 pOutterColor2, vec4 pInnerColor, vec2 pRatio, float keyScale )
{
    float baseRadius = kKeyRadius*keyScale;
    float keyRadius = clamp(baseRadius / perFrame.keysDensity, 1.0, baseRadius);

    float halfWidth  = (keyRadius * pRatio.x) * 0.5f;
    float halfHeight = (keyRadius * pRatio.y) * 0.5f;
    
    bool isTanInFixed  = isKeyFixedIn( gs_input[0].flags );
    bool isTanOutFixed = isKeyFixedOut( gs_input[0].flags );
    
    if( !perCurve.isWeighted && !perCurve.useQuaternionKeyShape )
    {
        halfWidth  *= 1.4;
        halfHeight *= 1.4;        
    }
        
    // remove 2 pixel for the inner halft width and haft height
    float innerHalfWidth  = halfWidth -( pRatio.x * 2 );
    float innerHalfHeight = halfHeight-( pRatio.y * 2 );

    if(perCurve.useQuaternionKeyShape)
    {
        float halfWidth  = ((keyRadius) * pRatio.x) * 0.5f;
        float halfHeight = ((keyRadius) * pRatio.y) * 0.5f;    

        // remove 2 pixel for the inner halft width and haft height
        float innerHalfWidth  = halfWidth -( pRatio.x * 2 );
        float innerHalfHeight = halfHeight-( pRatio.y * 2 );
    
        generateCircle( gl_in[0].gl_Position.xy, pOutterColor, halfWidth, halfHeight );
            
        generateCircle( gl_in[0].gl_Position.xy, pInnerColor, innerHalfWidth, innerHalfHeight );
    }
    else if( !perCurve.isWeighted )
    {
        // generate and render the outter diamond first
        generateDiamond(pOutterColor, halfWidth, halfHeight);  
        
        // generate and render the inner diamond(s) if needed
        if(keyRadius > 2.0)
        {
            if( isTanInFixed == isTanOutFixed || perCurve.isBuffered )
            { 
                if( !isTanInFixed || perCurve.isBuffered )
                {
                    generateDiamond(pInnerColor, innerHalfWidth, innerHalfHeight);
                }
            }
            else if( isTanInFixed )
            {
                uint keyIndex       = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
                bool lIsKeySelected = isKeySelected( gs_input[0].flags );
                bool lIsPreSelected = (perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) );            
                             
                generateHalfLeftDiamond(pOutterColor, innerHalfWidth, innerHalfHeight);
                generateHalfRightDiamond(pInnerColor, innerHalfWidth, innerHalfHeight);
            }
            else if( isTanOutFixed )
            {
                uint keyIndex       = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
                bool lIsKeySelected = isKeySelected( gs_input[0].flags );
                bool lIsPreSelected = (perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) );            
                    
                generateHalfLeftDiamond(pInnerColor,   innerHalfWidth, innerHalfHeight);
                generateHalfRightDiamond(pOutterColor, innerHalfWidth, innerHalfHeight);
            }   
        }            
    }
    else
    {
        // generate and render the outter square first      
        generateSquare(pOutterColor, halfWidth, halfHeight);
        
        // generate and render the inner square(s) if needed
        if(keyRadius > 2.0)
        {
            if( isTanInFixed == isTanOutFixed || perCurve.isBuffered )
            {
                if( !isTanInFixed || perCurve.isBuffered )
                {
                    generateSquare(pInnerColor, innerHalfWidth, innerHalfHeight );
                }
            }  
            else if( isTanInFixed )
            {
                uint keyIndex       = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
                bool lIsKeySelected = isKeySelected( gs_input[0].flags );
                bool lIsPreSelected = (perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) );            
                
                generateLeftSquare(pOutterColor, innerHalfWidth, innerHalfHeight );
                generateRightSquare(pInnerColor, innerHalfWidth, innerHalfHeight );
            }
            else if( isTanOutFixed )
            {
                uint keyIndex       = perCurve.preHighlightKeyIndex - perCurveInstance.firstVisibleKeyIndex;
                bool lIsKeySelected = isKeySelected( gs_input[0].flags );
                bool lIsPreSelected = (perCurve.preHighlightCurvePart == kPreHighlightCurveKey && keyIndex == uint(gl_PrimitiveIDIn) );            
                    
                generateLeftSquare(pInnerColor,   innerHalfWidth, innerHalfHeight );
                generateRightSquare(pOutterColor, innerHalfWidth, innerHalfHeight );
            }
        }
    }
}
 
 
void generateDiamond(vec4 pColor2, float pHalfWidth, float pHalfHeight)
{
    // top        
    gs_output.color = pColor2 ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y += pHalfHeight;  
    EmitVertex();
    
    // left
    gs_output.color = pColor2 ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.x -= pHalfWidth;
    EmitVertex();

    // bottom        
    gs_output.color = pColor2 ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y -= pHalfHeight;
    EmitVertex();
     
    // right        
    gs_output.color = pColor2 ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.x += pHalfWidth;
    EmitVertex(); 
                                             
    // top        
    gs_output.color = pColor2 ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y += pHalfHeight;      
    EmitVertex();
 
    EndPrimitive();
}
 
 
void generateHalfLeftDiamond(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    // top        
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y += pHalfHeight;  
    EmitVertex();
    
    // left
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.x -= pHalfWidth;
    EmitVertex();

    // bottom        
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y -= pHalfHeight;
    EmitVertex();

    EndPrimitive();
}


void generateHalfRightDiamond(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    // bottom        
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y -= pHalfHeight;
    EmitVertex(); 
     
    // right        
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.x += pHalfWidth; 
    EmitVertex(); 
                                             
    // top        
    gs_output.color = pColor ;
    gl_Position = gl_in[0].gl_Position;
    gl_Position.y += pHalfHeight;      
    EmitVertex();
 
    EndPrimitive();
}


void generateSquare(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    float left   = gl_in[0].gl_Position.x - pHalfWidth;
    float right  = gl_in[0].gl_Position.x + pHalfWidth;
    float bottom = gl_in[0].gl_Position.y - pHalfHeight;
    float top    = gl_in[0].gl_Position.y + pHalfHeight;
    
    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();

    // right - bottom        
    gs_output.color = pColor ;
    gl_Position = vec4( right, bottom, 0, 1);
    EmitVertex();

    // right - top
    gs_output.color = pColor ;
    gl_Position = vec4( right, top, 0, 1);
    EmitVertex();
    
    // left - top
    gs_output.color = pColor ;
    gl_Position = vec4( left, top, 0, 1);
    EmitVertex();

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();      
    
    EndPrimitive();  
}


void generateSquare(vec4 pColor, float pHalfWidth, float pHalfHeight, float pAngleInDegree)
{
    // create a rotation matrix around the Z-axis
    float angleInRadian = radians(pAngleInDegree);
    float cosAngle = cos(angleInRadian);
    float sinAngle = sin(angleInRadian);
    mat2 rotationMatrix = mat2( cosAngle,  sinAngle,  // first column
                                -sinAngle, cosAngle); // seconds column
    
    //
    // Here we compute the rotated square.
    // Use the pHalfWidth and pHalfHeight as coordinate for the square (Square centered to origin).
    // Rotate the square then translate it by gl_in[0].gl_Position.xy
    //
    vec2 leftTop     = gl_in[0].gl_Position.xy + rotationMatrix * vec2(-pHalfWidth,  pHalfHeight);
    vec2 leftButtom  = gl_in[0].gl_Position.xy + rotationMatrix * vec2(-pHalfWidth, -pHalfHeight);
    vec2 rightTop    = gl_in[0].gl_Position.xy + rotationMatrix * vec2( pHalfWidth,  pHalfHeight);
    vec2 rightButtom = gl_in[0].gl_Position.xy + rotationMatrix * vec2( pHalfWidth, -pHalfHeight);    
    
   
    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( leftButtom, 0, 1);
    EmitVertex();

    // right - bottom        
    gs_output.color = pColor ;
    gl_Position = vec4( rightButtom, 0, 1);
    EmitVertex();

    // right - top
    gs_output.color = pColor ;
    gl_Position = vec4( rightTop, 0, 1);
    EmitVertex();
    
    // left - top
    gs_output.color = pColor ;
    gl_Position = vec4( leftTop, 0, 1);
    EmitVertex();

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( leftButtom, 0, 1);
    EmitVertex();      
    
    EndPrimitive();
}


void generateRectangle(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    float left   = gl_in[0].gl_Position.x - pHalfWidth;
    float right  = gl_in[0].gl_Position.x + pHalfWidth;
    float bottom = gl_in[0].gl_Position.y - pHalfHeight;
    float top    = gl_in[0].gl_Position.y + pHalfHeight;
    
    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();

    // right - bottom        
    gs_output.color = pColor ;
    gl_Position = vec4( right, bottom, 0, 1);
    EmitVertex();

    // right - top
    gs_output.color = pColor ;
    gl_Position = vec4( right, top, 0, 1);
    EmitVertex();
    
    // left - top
    gs_output.color = pColor ;
    gl_Position = vec4( left, top, 0, 1);
    EmitVertex();

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();      
    
    EndPrimitive();  
}


void generateLeftSquare(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    float left   = gl_in[0].gl_Position.x - pHalfWidth;
    float bottom = gl_in[0].gl_Position.y - pHalfHeight;
    float top    = gl_in[0].gl_Position.y + pHalfHeight;

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();

    // right - bottom        
    gs_output.color = pColor ;
    gl_Position = vec4( gl_in[0].gl_Position.x, bottom, 0, 1);
    EmitVertex();

    // right - top
    gs_output.color = pColor ;
    gl_Position = vec4( gl_in[0].gl_Position.x, top, 0, 1);
    EmitVertex();

    // left - top
    gs_output.color = pColor ;
    gl_Position = vec4( left, top, 0, 1);
    EmitVertex();

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( left, bottom, 0, 1);
    EmitVertex();      
    
    EndPrimitive();  
}


void generateRightSquare(vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    float right  = gl_in[0].gl_Position.x + pHalfWidth;
    float bottom = gl_in[0].gl_Position.y - pHalfHeight;
    float top    = gl_in[0].gl_Position.y + pHalfHeight;
    
    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( gl_in[0].gl_Position.x, bottom, 0, 1);
    EmitVertex();

    // right - bottom        
    gs_output.color = pColor ;
    gl_Position = vec4( right, bottom, 0, 1);
    EmitVertex();

    // right - top
    gs_output.color = pColor ;
    gl_Position = vec4(right, top, 0, 1);
    EmitVertex();
    
    // left - top
    gs_output.color = pColor ;
    gl_Position = vec4( gl_in[0].gl_Position.x, top, 0, 1);
    EmitVertex();

    // left - bottom
    gs_output.color = pColor ;
    gl_Position = vec4( gl_in[0].gl_Position.x, bottom, 0, 1);
    EmitVertex();      
    
    EndPrimitive(); 
}



void generateCircle(vec2 pPosition, vec4 pColor, float pHalfWidth, float pHalfHeight)
{
    //
    // Generate a circle with 10 triangle, so this function output 30 vertices
    //
    uint numTriangle = 10u;
    float twicePiOverUnit = 2.0f * 3.14159265f / numTriangle;
    float angle     = 0;
    float nextAngle = 0;
    
    for(uint i = 0u; i <= numTriangle;i++) 
    { 
        angle = i * twicePiOverUnit;
        nextAngle = (i+1u) * twicePiOverUnit;
         
        gs_output.color = pColor ;
        gl_Position = vec4( pPosition, 0, 1);
        EmitVertex();           

        gs_output.color = pColor ;
        gl_Position = vec4(pPosition, 0, 0) + vec4( cos(angle) * pHalfWidth, sin(angle) * pHalfHeight, 0, 1) ;
        EmitVertex();           
        
        gs_output.color = pColor ;
        gl_Position = vec4(pPosition, 0, 0) + vec4( cos(nextAngle) * pHalfWidth, sin(nextAngle) * pHalfHeight, 0, 1);
        EmitVertex(); 
           
        EndPrimitive();         
    }    
}


//
// Generate a circle with 10 triangle, so this function output 30 vertices
// This function use 2 color to draw the cercle. This allow to simulate a stipple pattern
//
void generateCircle(vec2 pPosition, vec4 pColor1, vec4 pColor2, float pHalfWidth, float pHalfHeight)
{
    uint numTriangle = 10u;
    float twicePiOverUnit = 2.0f * 3.14159265f / numTriangle;
    float angle     = 0;
    float nextAngle = 0;
    
    for(uint i = 0u; i <= numTriangle;i++) 
    { 
        vec4 color = bool((i & 1u) == 1u ) ? pColor1 : pColor2;
        angle = i * twicePiOverUnit;
        nextAngle = (i+1u) * twicePiOverUnit;
         
        gs_output.color = color ;
        gl_Position = vec4( pPosition, 0, 1);
        EmitVertex();           

        gs_output.color = color ;
        gl_Position = vec4(pPosition, 0, 0) + vec4( cos(angle) * pHalfWidth, sin(angle) * pHalfHeight, 0, 1) ;
        EmitVertex();           
        
        gs_output.color = color ;
        gl_Position = vec4(pPosition, 0, 0) + vec4( cos(nextAngle) * pHalfWidth, sin(nextAngle) * pHalfHeight, 0, 1);
        EmitVertex(); 
           
        EndPrimitive();         
    }    
}

