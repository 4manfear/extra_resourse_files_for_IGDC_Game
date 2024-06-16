#version 330 core
#define MAX_VERTICE 85
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

const uint kInfinityConstant      = 0u;
const uint kInfinityLinear        = 1u;
const uint kInfinityCycle         = 3u;
const uint kInfinityCycleRelative = 4u;
const uint kInfinityOscillate     = 5u;

const uint kShaderModeNormal       = 0u;
const uint kShaderModePreInfinity  = 1u;
const uint kShaderModePostInfinity = 2u;

const uint kPreHighlightCurve = 1u;

const float kDoubleEpsilon = 1e-6;
const float kOneThird      = 1.0 / 3.0;
const float kFourThirds    = 4.0 / 3.0;

const mat4 kBezierMatrix = mat4(-1,  3, -3, 1,  // first  column
                                 3, -6,  3, 0,  // second column
                                -3,  3,  0, 0,  // third  column
                                 1,  0,  0, 0); // fourth column

// Color use to blend (multiply) with the color curve when we draw the infinities
const vec4 kInfinityColorBlend = vec4(1.0f, 1.0f, 1.0f, 0.5f);

// Color use to blend (multiply) with the color curve when we draw the referenced curves
const vec4 kReferencedColorBlend = vec4(1.0f, 1.0f, 1.0f, 0.4f);

// Color use when a segment of a curve is selected
const vec4 kSelectedCurveColor = vec4(1.0f, 1.0f, 1.0f , 1.0f);

// Color use vertical stepped curve line
const vec4 kSteppedVLineCurveColor = vec4(0.5765f, 0.5843f, 0.5961f, 1.0f);


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
} globalSettings;

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
} perFrame;

layout(std140) uniform PerCurve
{
    layout(column_major) mat4  transformMatrix;
    vec4  color;
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
} perCurve;

layout(std140) uniform ShaderSettings
{
    uint mode;
} shaderSettings;

layout(lines) in;
layout(line_strip, max_vertices = MAX_VERTICE) out;

in VS_OUT
{
    vec2 pos;
    vec2 inTan;
    vec2 outTan;
    uint flags;
    flat int instanceID;
} gs_input[];

out GS_OUT
{
    flat vec4 color;
    float time;
    float stippleLineCoord;
    flat uint  useStipplePattern;
    flat uint  isInSelectionRange;
} gs_output;

// Texture buffer that containt stipple range
uniform samplerBuffer textureBuffer;


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
bool isKeyAnySelected(uint flags)
{
    return bool(flags & kAnySelected);
}
bool isInTangentActive(uint flags)
{
    return bool(flags & kIsInTangentActive);
}
bool isOutTangentActive(uint flags)
{
    return bool(flags & kIsOutTangentActive);
}

void drawSegment(vec4 pSegmentColor);
void bezierEvaluate(vec4 pSegmentColor, vec2 pStart, vec2 pEnd, vec2 pControlPoint1, vec2 pControlPoint2, int pSampleCount, bool makeMonotonic);
vec2 bezierEvaluateAt(vec2 pStart, vec2 pEnd, vec2 pControlPoint1, vec2 pControlPoint2, float pFactor);


//
// Allow to know if a given point is inside a stipple range.
//
bool isInsideStippleRange(float pTime)
{
    // the whole curve use stipple pattern
    if(perCurve.useFullStipplePattern)
        return true;

#if ALLOW_STIPPLE_RANGE
    int nbRange = int( texelFetch( textureBuffer, 0).x );
    if(nbRange == 0)
        return false;

    bool isInside = false;
    int index    = 0;
    while(!isInside && index < nbRange)
    {
        float stippleRangeStart  = ( perFrame.projection * texelFetch( textureBuffer, index * 2 + 1) ).x;
        float stippleRangeEnd    = ( perFrame.projection * texelFetch( textureBuffer, index * 2 + 2) ).x;

        isInside = (pTime >= stippleRangeStart  && pTime < stippleRangeEnd);
        ++index;
    }

    // we should inverse the boolean, this is cause by the way maya encode stipple range for mute curve.
    return !isInside;
#else
    return false;
#endif
}


//
// Compute the stipple coordinate of a given point.
//
// point    The point for which we want the coordinate.
// refPoint The reference point from where the coordinate start.
// toViewport Transformation matrix to transform points into viewport space (Pixel)
//
float computeStippleCoord(vec2 point, vec2 refPoint, mat4 toViewport)
{
    vec2 posWinPos1 = (toViewport * vec4( refPoint, 0, 1) ).xy;
    vec2 posWinPos2 = (toViewport * vec4( point, 0, 1) ).xy;
    float coord     = length( posWinPos2 - posWinPos1 );
    return coord;
}

bool isHighlightedPart(uint firstPointFlags, uint secondPointFlags)
{
    return isOutTangentActive(firstPointFlags) || isInTangentActive(secondPointFlags)
        || (isKeyAnySelected(firstPointFlags) && !isInTangentActive(firstPointFlags))
        || (isKeyAnySelected(secondPointFlags) && !isOutTangentActive(secondPointFlags));
}

bool isBothKeysSelected(uint firstPointFlags, uint secondPointFlags)
{
    return isKeyAnySelected(firstPointFlags) && isKeyAnySelected(secondPointFlags);
}

bool useSelectionColor()
{
    return (isKeyAnySelected(gs_input[0].flags) && isKeyAnySelected(gs_input[1].flags)) || perCurve.preHighlightCurvePart == kPreHighlightCurve;
}

vec4 getSegmentColor(uint firstPointFlags, uint secondPointFlags)
{
    // MAYA-71512 Pre-Select Highlight color is distinct from selected curve color. Also takes precedence over selection.
    // MAYA-72728 If first and last key of curve segment use selected curve color. Otherwise, use the curve color

    vec4 lSegmentColor;

    if( perCurve.isBuffered )
    {
        lSegmentColor = globalSettings.bufferCurveColor;
    }
    else if (globalSettings.highlightAffectedCurves && isHighlightedPart(firstPointFlags, secondPointFlags))
    {
        lSegmentColor = kSelectedCurveColor;
    }
    else if(perCurve.isLocked && isBothKeysSelected(firstPointFlags, secondPointFlags))
    {
        lSegmentColor = kSelectedCurveColor;
    }
    else if(perCurve.isLocked)
    {
        lSegmentColor = globalSettings.lockedCurveColor;
    }
    else if (perCurve.preHighlightCurvePart == kPreHighlightCurve )
    {
        lSegmentColor = globalSettings.preSelectHighlightColor;
    }
    else if( isBothKeysSelected(firstPointFlags, secondPointFlags) )
    {
        lSegmentColor = kSelectedCurveColor;
    }
    else
    {
        lSegmentColor = perCurve.color;
        if (perCurve.isReferenced)
            lSegmentColor *= kReferencedColorBlend;
    }
    return lSegmentColor;
}

void main()
{
    if( (gs_input[0].pos.x < perFrame.viewRegionMinX && gs_input[1].pos.x < perFrame.viewRegionMinX ) ||
        (gs_input[0].pos.x > perFrame.viewRegionMaxX && gs_input[1].pos.x > perFrame.viewRegionMaxX ) )
    {
        // there is a bug here .... let see that later
        //return;
    }


    if( shaderSettings.mode == kShaderModeNormal )
    {
        vec4 lSegmentColor = getSegmentColor(gs_input[0].flags, gs_input[1].flags);
        drawSegment(lSegmentColor);
    }
    else
    {

        if( shaderSettings.mode == kShaderModePreInfinity )
        {
            vec4 preInfinityCurveColor = getSegmentColor(0u, gs_input[1].flags);
            preInfinityCurveColor *= kInfinityColorBlend;

            if( perCurve.preInfinityType == kInfinityConstant && gl_PrimitiveIDIn == 0)
            {
                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = preInfinityCurveColor;
                gl_Position = gl_in[1].gl_Position;
                gl_Position.x = -1;
                EmitVertex();

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = preInfinityCurveColor;
                gl_Position = gl_in[1].gl_Position;
                EmitVertex();
            }
            else if( perCurve.preInfinityType == kInfinityLinear )
            {
                // Find the intersection of 2 lines in projection space [-1, 1] in both axis
                // gl_in[1] is the first key of the curve and gl_in[0] is the dummy key
                vec2 lOrigin     = gl_in[1].gl_Position.xy;
                vec2 lDirection  = normalize ( gs_input[1].inTan - lOrigin );

                float t = (-1 - lOrigin.x) / lDirection.x;
                float value = lOrigin.y + lDirection.y * t;

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = preInfinityCurveColor;
                gl_Position = vec4(-1, value, 0, 1);
                EmitVertex();

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = preInfinityCurveColor;
                gl_Position = gl_in[1].gl_Position;
                EmitVertex();
            }
            else // for any other infinity type draw the normal segment
            {
                drawSegment(preInfinityCurveColor);
            }
        }
        else if( shaderSettings.mode == kShaderModePostInfinity )
        {
            vec4 postInfinityCurveColor = getSegmentColor(gs_input[0].flags, 0u);
            postInfinityCurveColor *= kInfinityColorBlend;
            if( perCurve.postInfinityType == kInfinityConstant )
            {
                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = postInfinityCurveColor;
                gl_Position = gl_in[0].gl_Position;
                EmitVertex();

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = postInfinityCurveColor;
                gl_Position = gl_in[0].gl_Position;
                gl_Position.x = 1.0f;
                EmitVertex();
            }
            else if( perCurve.postInfinityType == kInfinityLinear )
            {
                // Find the intersection of 2 lines in projection space [-1, 1] in both axis
                // gl_in[0] is the first key of the curve and gl_in[1] is the dummy key
                vec2 lOrigin     = gl_in[0].gl_Position.xy;
                vec2 lDirection  = normalize ( gs_input[0].outTan - lOrigin );

                float t = (1 - lOrigin.x) / lDirection.x;
                float value = lOrigin.y + lDirection.y * t;

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = postInfinityCurveColor;
                gl_Position = vec4(1, value, 0, 1);
                EmitVertex();

                gs_output.useStipplePattern = 0u;
                gs_output.stippleLineCoord  = 0.0f;
                gs_output.color = postInfinityCurveColor;
                gl_Position = gl_in[0].gl_Position;
                EmitVertex();
            }
            else // for any other infinity type draw the normal segment
            {
                drawSegment(postInfinityCurveColor);
            }
        }
    }
}

void drawSegment(vec4 pSegmentColor)
{
    if( isKeyStepOut(gs_input[0].flags) )
    {
        // If the first key of the segment is stepOut, draw the segment with 2 lines.
        // The first line is a regular line and the second one use a stipple pattern

        vec2 lMiddlePoint = vec2(gl_in[1].gl_Position.x, gl_in[0].gl_Position.y);

        bool useSelectionColor = useSelectionColor();

        // Emit the first vertex
        gs_output.useStipplePattern = 0u;
        gs_output.stippleLineCoord  = 0.0f;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = pSegmentColor;
        gs_output.time = gl_in[0].gl_Position.x;
        gl_Position = gl_in[0].gl_Position;
        EmitVertex();

        // middle vertex
        gs_output.useStipplePattern = 0u;
        gs_output.stippleLineCoord  = computeStippleCoord(lMiddlePoint, gl_in[0].gl_Position.xy, perFrame.viewport);
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = pSegmentColor;
        gs_output.time   = lMiddlePoint.x;
        gl_Position.xy  = lMiddlePoint;
        EmitVertex();

        EndPrimitive();

        // Second line with stipple pattern

        vec4 verticalLineColor = kSteppedVLineCurveColor;
        if( useSelectionColor)
        {
            verticalLineColor = kSelectedCurveColor;
        }
        else if(shaderSettings.mode != kShaderModeNormal)
        {
            verticalLineColor *= kInfinityColorBlend;
        }

        // middle vertex
        gs_output.useStipplePattern  = 1u;
        gs_output.stippleLineCoord   = 0.0f;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color              = verticalLineColor;
        gs_output.time               = lMiddlePoint.x;
        gl_Position.xy               = lMiddlePoint;
        EmitVertex();

        // compute the stipple coordinate of the last vertex
        mat4 projViewport = perFrame.viewport * perFrame.projection;
        vec2 lPosWinPos0      = (projViewport * vec4( gs_input[1].pos.x, gs_input[0].pos.y, 0, 1) ).xy;
        vec2 lPosWinPos1      = (projViewport * vec4( gs_input[1].pos,   0, 1) ).xy;
        float lStipplePattern = length( lPosWinPos1 - lPosWinPos0 );

        // Emit the last vertex
        gs_output.useStipplePattern = 1u;
        gs_output.stippleLineCoord  = lStipplePattern;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = verticalLineColor;
        gs_output.time = gl_in[1].gl_Position.x;
        gl_Position = gl_in[1].gl_Position;
        EmitVertex();
    }
    else if( isKeyStepNextOut(gs_input[0].flags) )
    {
        // If the first key of the segment is stepOutNext, draw the segment with 2 lines.
        // The first line use a stipple pattern and the second one is a regular line.

        vec2 lMiddlePoint = vec2(gl_in[0].gl_Position.x, gl_in[1].gl_Position.y);

        vec4 verticalLineColor = kSteppedVLineCurveColor;
        bool useSelectionColor = useSelectionColor();

        if( useSelectionColor )
        {
            verticalLineColor = kSelectedCurveColor;
        }
        else if(shaderSettings.mode != kShaderModeNormal)
        {
            verticalLineColor *= kInfinityColorBlend;
        }

        // Emit the first vertex
        gs_output.useStipplePattern = 1u;
        gs_output.stippleLineCoord  = 0.0f;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = verticalLineColor;
        gs_output.time = gl_in[0].gl_Position.x;
        gl_Position = gl_in[0].gl_Position;
        EmitVertex();

        // compute the stipple coordinate of the last vertex of the first line
        mat4 projViewport = perFrame.viewport * perFrame.projection;
        vec2 lPosWinPos0      = (projViewport * vec4( gs_input[0].pos, 0, 1) ).xy;
        vec2 lPosWinPos1      = (projViewport * vec4( gs_input[0].pos.x, gs_input[1].pos.y, 0, 1) ).xy;
        float lStipplePattern = length( lPosWinPos1 - lPosWinPos0 );

        // middle vertex
        gs_output.useStipplePattern = 1u;
        gs_output.stippleLineCoord  = lStipplePattern;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = verticalLineColor;
        gs_output.time = lMiddlePoint.x;
        gl_Position.xy = lMiddlePoint;
        EmitVertex();

        EndPrimitive();

        // Second line

        // middle vertex
        gs_output.useStipplePattern = 0u;
        gs_output.stippleLineCoord  = 0.0f;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = pSegmentColor;
        gs_output.time = lMiddlePoint.x;
        gl_Position.xy = lMiddlePoint;
        EmitVertex();

         // Emit the last vertex
        gs_output.useStipplePattern = 0u;
        gs_output.stippleLineCoord  = computeStippleCoord(lMiddlePoint, gl_in[1].gl_Position.xy, perFrame.viewport);
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = pSegmentColor;
        gs_output.time = gl_in[1].gl_Position.x;
        gl_Position = gl_in[1].gl_Position;
        EmitVertex();
    }
    else
    {
        // Emit the first vertex
        gs_output.useStipplePattern = 0u;
        gs_output.stippleLineCoord  = 0.0f;
        gs_output.color = pSegmentColor;
        gs_output.time = gl_in[0].gl_Position.x;
        gl_Position    = gl_in[0].gl_Position;
        EmitVertex();

        // Skip the curve interpolation if both tangent (in / out) are linear
        // Quaternion curve and curve with custom tangent dont need to be sampled because they are already done on the cpu.
        if( !perCurve.isQuaternion && !perCurve.isPlotted && !perCurve.hasCustomTangent &&
            (!isKeyLinearOut(gs_input[0].flags) || !isKeyLinearIn(gs_input[1].flags) ) )
        {
            // gl_Position is in projection space [1, -1] so that means the width is 2.
            float fraction = (gl_in[1].gl_Position.x - gl_in[0].gl_Position.x) / 2;
            if(fraction < 0) {
                fraction *= -1;
            }

            int numSamples = int( clamp( fraction * perFrame.displayPoint, 0.0, MAX_VERTICE-2  ) );

            if (numSamples > 1)
            {
                bool makeMonotonic = perCurve.isWeighted;

                bezierEvaluate(pSegmentColor,
                               gl_in[0].gl_Position.xy,
                               gl_in[1].gl_Position.xy,
                               gs_input[0].outTan,
                               gs_input[1].inTan,
                               numSamples,
                               makeMonotonic);
            }
        }

        bool useSelectionColor = useSelectionColor();

        // Emit the last vertex
        gs_output.stippleLineCoord  = 0;
        gs_output.useStipplePattern = 0u;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.color = pSegmentColor;
        gs_output.time  = gl_in[1].gl_Position.x;
        gl_Position     = gl_in[1].gl_Position;
        EmitVertex();
    }
}

bool equivalent(float x, float y)
{
    return ((x > y) ? (x - y <= kDoubleEpsilon) : (y - x <= kDoubleEpsilon));
}

void bezierConstrainInsideBounds( inout  float x1, inout  float x2 )
//
//	Description:
//		We want to ensure that (x1, x2) is inside the ellipse
//		(x1^2 + x2^2 - 2(x1 +x2) + x1*x2 + 1) given that we know
//		x1 is within the x bounds of the ellipse.
//
{
	// (x1^2 + x2^2 - 2(x1 +x2) + x1*x2 + 1)
	//   = x2^2 + (x1 - 2)*x1 + (x1^2 - 2*x1 + 1)
	// Therefore, we solve for x2.

	float b, c;
	if ( x1 + kDoubleEpsilon < kFourThirds )
	{
		b = x1 - 2.0;
		c = x1 - 1.0;
		float	discr = sqrt( b * b - 4 * c * c );
		float	root = (-b + discr) * 0.5;
		if ( x2 + kDoubleEpsilon > root )
		{
			x2 = root - kDoubleEpsilon;
		}
		else
        {
			root = (-b - discr) * 0.5;
			if ( x2 < root + kDoubleEpsilon )
				x2 = root + kDoubleEpsilon;
		}
	}
	else
    {
		x1 = kFourThirds - kDoubleEpsilon;
		x2 = kOneThird - kDoubleEpsilon;
	}
}

void bezierCheckMonotonic( inout  float x1, inout  float x2 )
//
//	Description:
//
//		Given the bezier curve
//			 B(t) = [t^3 t^2 t 1] * | -1  3 -3  1 | * | 0  |
//									|  3 -6  3  0 |   | x1 |
//									| -3  3  0  0 |   | x2 |
//									|  1  0  0  0 |   | 1  |
//
//		We want to ensure that the B(t) is a monotonically increasing function.
//		We can do this by computing
//			 B'(t) = [3t^2 2t 1 0] * | -1  3 -3  1 | * | 0  |
//									 |  3 -6  3  0 |   | x1 |
//									 | -3  3  0  0 |   | x2 |
//									 |  1  0  0  0 |   | 1  |
//
//		and finding the roots where B'(t) = 0.  If there is at most one root
//		in the interval [0, 1], then the curve B(t) is monotonically increasing.
//
//		It is easier if we use the control vector [ 0 x1 (1-x2) 1 ] since
//		this provides more symmetry, yields better equations and constrains
//		x1 and x2 to be positive.
//
//		Therefore:
//			 B'(t) = [3t^2 2t 1 0] * | -1  3 -3  1 | * | 0    |
//									 |  3 -6  3  0 |   | x1   |
//									 | -3  3  0  0 |   | 1-x2 |
//									 |  1  0  0  0 |   | 1    |
//
//				   = [t^2 t 1 0] * | 3*(3*x1 + 3*x2 - 2)  |
//								   | 2*(-6*x1 - 3*x2 + 3) |
//								   | 3*x1                 |
//								   | 0                    |
//
//		gives t = (2*x1 + x2 -1) +/- sqrt(x1^2 + x2^2 + x1*x2 - 2*(x1 + x2) + 1)
//				  --------------------------------------------------------------
//								3*x1 + 3* x2 - 2
//
//		If the ellipse [x1^2 + x2^2 + x1*x2 - 2*(x1 + x2) + 1] <= 0, (Note
//		the symmetry) x1 and x2 are valid control values and the curve is
//		monotonic.  Otherwise, x1 and x2 are invalid and have to be projected
//		onto the ellipse.
//
//		It happens that the maximum value that x1 or x2 can be is 4/3.
//		If one of the values is less than 4/3, we can determine the
//		boundary constraints for the other value.
//
{
	// We want a control vector of [ 0 x1 (1-x2) 1 ] since this provides
	// more symmetry. (This yields better equations and constrains x1 and x2
	// to be positive.)
	//
	x2 = 1.0 - x2;

	// x1 and x2 must always be positive
	if ( x1 < 0.0 )
		x1 = 0.0;
	if ( x2 < 0.0 )
		x2 = 0.0;

	// If x1 or x2 are greater than 1.0, then they must be inside the
	// ellipse (x1^2 + x2^2 - 2(x1 +x2) + x1*x2 + 1).
	// x1 and x2 are invalid if x1^2 + x2^2 - 2(x1 +x2) + x1*x2 + 1 > 0.0
	//
	//
	if( x1 > 1.0 || x2 > 1.0 )
	{
		float	d = x1 * (x1 - 2.0 + x2) + x2 * (x2 - 2.0) + 1.0;

		if ( d + kDoubleEpsilon > 0.0 )
		{
			bezierConstrainInsideBounds( x1, x2 );
		}
	}

	// we change the control vector back to [ 0 x1 x2 1 ]
	//
	x2 = 1.0 - x2;
}

void bezierEvaluate(vec4 pSegmentColor, vec2 pStart, vec2 pEnd, vec2 pControlPoint1, vec2 pControlPoint2, int pSampleCount, bool makeMonotonic)
{
    if (makeMonotonic)
    {
        float rangeX = pEnd.x - pStart.x;
        if (rangeX == 0.0) {
            return;
        }

        float dx1 = pControlPoint1.x - pStart.x;
        float dx2 = pControlPoint2.x - pStart.x;

        // normalize X control values
        //
        float nX1 = dx1 / rangeX;
        float nX2 = dx2 / rangeX;

        // save the orig normalized control values
        //
        float oldX1 = nX1;
        float oldX2 = nX2;

        // check the inside control values yield a monotonic function.
        // if they don't correct them with preference given to one of them.
        //
        // Most of the time we are monotonic, so do some simple checks first
        //
        if (nX1 < 0.0) nX1 = 0.0;
        if (nX2 > 1.0) nX2 = 1.0;

        if ((nX1 > 1.0) || (nX2 < 0.0))
        {
            bezierCheckMonotonic(nX1, nX2);
        }

        // compute the new control points
        //
        if ( nX1 != oldX1 )
        {
            pControlPoint1.x = pStart.x + nX1 * rangeX;
            if ( !equivalent(oldX1, 0.0) ) {
                pControlPoint1.y = pStart.y + (pControlPoint1.y - pStart.y) * nX1 / oldX1;
            }
        }

        if ( nX2 != oldX2 )
        {
            pControlPoint2.x = pStart.x + nX2 * rangeX;
            if ( !equivalent(oldX2, 1.0) ) {
                pControlPoint2.y = pEnd.y - (pEnd.y - pControlPoint2.y) * (1.0 - nX2) / (1.0 - oldX2);
            }
        }
    }

    float step = 1.0 / float(pSampleCount);

    for(int i = 0; i < pSampleCount; i++)
    {
        vec2 evaluatedPoint = bezierEvaluateAt(pStart, pEnd, pControlPoint1, pControlPoint2, i * step);

        if( isInsideStippleRange(evaluatedPoint.x) )
        {
            gs_output.stippleLineCoord = computeStippleCoord(evaluatedPoint, gl_in[0].gl_Position.xy, perFrame.viewport);
        }
        else
        {
            gs_output.stippleLineCoord = 0.0f;
        }

        bool useSelectionColor = useSelectionColor();

        gs_output.useStipplePattern = 0u;
        gs_output.color = pSegmentColor;
        gs_output.isInSelectionRange = useSelectionColor ? 1u : 0u;
        gs_output.time = evaluatedPoint.x;
        gl_Position = vec4(evaluatedPoint, 0, 1);
        EmitVertex();
    }
}

/**
* /brief bezier curve evaluation
* /param pStart The point where the curve start.
* /param pEnd   The point where the curve end.
* /param pControlPoint1 The first control point.
* /param pControlPoint2 The second control point.
* /param pFactor A value between 0 and 1.
* /return The point on the curve evaluated at pFactor.
*/
vec2 bezierEvaluateAt(vec2 pStart, vec2 pEnd, vec2 pControlPoint1, vec2 pControlPoint2, float pFactor)
{
    // bezier equation : P(u) = (1-u)^3 P0 + 3u(1-u)^2 P1 + 3u^2(1-u)P2 + u^3 P3
    // this code do exactly the same thing as the bezier equation but use a maxtrix / vector notation
    float factor2    = pFactor * pFactor;
    float factor3    = factor2 * pFactor;
    vec4  factorVec4 = vec4(factor3, factor2, pFactor, 1);

    vec4 blendFunctions = factorVec4 * kBezierMatrix;

    vec4 bezierInputX = vec4(pStart.x, pControlPoint1.x, pControlPoint2.x, pEnd.x);
    vec4 bezierInputY = vec4(pStart.y, pControlPoint1.y, pControlPoint2.y, pEnd.y);

    vec2 p;
    p.x = dot(blendFunctions, bezierInputX);
    p.y = dot(blendFunctions, bezierInputY);
    return p;
}
