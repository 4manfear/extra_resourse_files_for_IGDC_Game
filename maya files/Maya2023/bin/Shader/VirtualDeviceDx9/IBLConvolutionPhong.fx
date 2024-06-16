//**************************************************************************/
// Copyright 2011 Autodesk, Inc.
// All rights reserved.
//
// This computer source code and related instructions and comments are the
// unpublished confidential and proprietary information of Autodesk, Inc.
// and are protected under Federal copyright and state trade secret law.
// They may not be disclosed to, copied or used by any third party without
// the prior written consent of Autodesk, Inc.
//**************************************************************************/
// DESCRIPTION: IBL convolution.
// AUTHOR: Liming Zhang
// CREATED: Mar. 2011
//**************************************************************************/

// World-view-projection transformation.
float4x4 gWVPXf : WorldViewProjection < string UIWidget = "None"; >;

// The input direction texture.
texture gDirectionTex : InputTexture
<
string UIName = "Input Texture";
> = NULL;

// The direction texture sampler.
sampler2D DirectionSamp = sampler_state 
{
    Texture   = <gDirectionTex>;
};

// The input HDR LatLong texture.
texture gHDRLatLongTex : InputTexture
<
string UIName = "Input Texture";
> = NULL;

// The HDR LatLong texture sampler.
sampler2D gHDRLatLongSamp = sampler_state 
{
    Texture   = <gHDRLatLongTex>;
};

// Array of shininess.
float gShininess[4];

// Tile size.
float2 gTiling;

// Pixel size
float2 gPixelSize;

// Block texture offset.
float2 gBlockTexCoord0;

// Vertex shader input structure.
struct VS_INPUT
{
    float4 Pos : POSITION;
    float2 UV : TEXCOORD0;
};

// Vertex shader output structure.
struct VS_TO_PS
{
    float4 HPos : POSITION;
    float2 UV : TEXCOORD0;
    float4 SSamples : TEXCOORD1;
    float2 TSamples : TEXCOORD2;
};

// Vertex shader.
VS_TO_PS VS_IBLConvolution(VS_INPUT In)
{
    VS_TO_PS Out;

    // Transform the position from object space to clip space for output.
    Out.HPos = mul(In.Pos, gWVPXf);

    // Pass the texture coordinates unchanged.
    float2 tc = In.UV * gTiling;
    Out.UV = tc;

    float2 offset = gPixelSize * 0.5f;

    // We prepare 8 sample points here to increase the presicion.
    // Since the IBL sharp map is down sampled to a small tile.
    Out.SSamples.x = tc.x - (offset.x + gPixelSize.x);
    Out.SSamples.y = tc.x - offset.x;
    Out.SSamples.z = tc.x + offset.x;
    Out.SSamples.w = tc.x + (offset.x + gPixelSize.x);

    Out.TSamples.x = tc.y - offset.y;
    Out.TSamples.y = tc.y + offset.y;

    return Out;
}

struct pixelOutput {
    float4 oColor0 : COLOR0;

#if RENDER_TARGET_COUNT > 1
    float4 oColor1 : COLOR1;
#endif

#if RENDER_TARGET_COUNT > 2
    float4 oColor2 : COLOR2;
#endif

#if RENDER_TARGET_COUNT > 3
    float4 oColor3 : COLOR3;
#endif
};

// Pixel shader.
pixelOutput PS_IBLConvolution(VS_TO_PS In)
{
    // Look up Normal for the current tile.
    // Actually for diffuse map, this "Normal" is the real normal for sampling this map.
    // For glossy map, this "Normal" is the reflection vector of view.
    float3 N = tex2D(DirectionSamp, gBlockTexCoord0.xy + floor(In.UV) * gPixelSize.xy).xyz;

    float4 SS = frac(In.SSamples);
    float2 TS = frac(In.TSamples);

    float4 results[RENDER_TARGET_COUNT];
    for( int i = 0; i < RENDER_TARGET_COUNT; ++i)
    {
        results[i] = 0.0;
    }

    // For each sample point along the V direction.
    for( int t = 0; t < 2; ++t)
    {
        float4 rowSums[RENDER_TARGET_COUNT];
        // Initialize the variable.
        for( int i = 0; i < RENDER_TARGET_COUNT; ++i)
        {
            rowSums[i] = 0.0;
        }

        float4 L;
        // For each sample point along the U direction.
        for( int s = 0; s < 4; ++s)
        {
            float2 p1 = float2(SS[s], TS[t]);

            // Get the direction from the map.
            // which is used to get the illuminance from the HDR LatLong texture.
            L = tex2D(DirectionSamp, p1);
            float3 color = tex2D(gHDRLatLongSamp, p1).rgb;

            // For glossy map, this NdotL is actually the RdotV.
            // Since N is the reflection vector of view, and L is the reflection vector of R.
            float NdotL = max(0.0, dot( N, L.xyz));
            
            // Sum the irradiance of all sample points.
            for( int i = 0; i < RENDER_TARGET_COUNT; ++i)
            {
                // Here is the Phong mode. 
                // if gShininess = 1.0, it's identical to NdotL, and result is the diffuse map.
                float pf = pow( NdotL, gShininess[i]);
                rowSums[i] += float4( color * pf, pf);
            }
        }

        // Sum the result, L.w is the area of this pixel in the final output IBL map.
        for( int j = 0; j < RENDER_TARGET_COUNT; ++j)
        {
            results[j] += L.w * rowSums[j];
        }
    }

    // Output final result to the MRT targets.
    pixelOutput psOutput;
    psOutput.oColor0 = results[0];
#if RENDER_TARGET_COUNT > 1 
        psOutput.oColor1 = results[1];
#endif

#if RENDER_TARGET_COUNT > 2 
        psOutput.oColor2 = results[2];
#endif

#if RENDER_TARGET_COUNT > 3 
        psOutput.oColor3 = results[3];
#endif
    return psOutput;
}

// The main technique.
technique Main
{
    pass p0
    {
        VertexShader = compile vs_3_0 VS_IBLConvolution();
        PixelShader = compile ps_3_0 PS_IBLConvolution();
    }
}
