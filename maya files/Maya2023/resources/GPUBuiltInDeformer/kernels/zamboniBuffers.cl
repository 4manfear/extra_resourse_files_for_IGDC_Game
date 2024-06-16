// Helper functions
// OSX seems to be using very strict compiler setting which demand the function
// prototype be defined before the function is implemented.  It seems like we
// only need the function prototype for helper methods, not kernels that are
// used directly.
float3 lerp( const float3 a , const float3 b , const float factor );

//------------------------------------------------------------------------------
float3 lerp( const float3 a , const float3 b , const float factor )
{
    return a + factor * ( b - a );
}

//------------------------------------------------------------------------------
__kernel void copyToAffectBuffer(
    __global float* iOutPos ,
    __global const float* iInPos,
    __global const unsigned int* iAffectMap,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 pos = vload3(vid, iInPos);
    vstore3(pos, aid, iOutPos);
}

//------------------------------------------------------------------------------
__kernel void copyFromAffectBuffer(
    __global float* iOutPos ,
    __global const float* iAffectPos,
    __global const unsigned int* iAffectMap,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 pos = vload3(aid, iAffectPos);
    vstore3(pos, vid, iOutPos);
}

//------------------------------------------------------------------------------
__kernel void mixWithAffectBuffer(
    __global float* iOutPos,
    __global const float* iInPos,
    __global const float* iAffectPos,
    __global const unsigned int* iAffectMap,
    __global const float* iWeights,
    const float iEnvelope,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);

    float3 p0 = vload3(vid, iInPos);
    float3 p1 = vload3(aid, iAffectPos);

    float w = iEnvelope;
    if (iWeights) w *= iWeights[aid];

    vstore3( lerp( p0, p1, w), vid, iOutPos);
}
