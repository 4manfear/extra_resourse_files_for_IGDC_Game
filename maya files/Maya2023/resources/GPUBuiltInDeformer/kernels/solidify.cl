#define INVALID_INDEX UINT_MAX

float16 multMtx(const float16 a, const float16 b);
float3 mtxMul( float16 matrix , float3 point );

float3 calcCenter(unsigned int iChunkId,
    __global const unsigned int* iChunkDataIndexer,
    __global const unsigned int* iChunkData,
    __global const float* iPoints);

float16 calcMatrix(unsigned int iChunkId,
    __global const unsigned int* iChunkDataIndexer,
    __global const unsigned int* iChunkData,
    __global const float* iPoints,
    __global const float* iStabilizationPoints,
    __global const float* iApplyScale);

double calcEdgeLength(unsigned int iChunkId,
    __global const unsigned int* iEdgeIndexer,
    __global const unsigned int* iEdgeConnections,
    __global const float* iPoints);

//------------------------------------------------------------------------------
//
//
//
//------------------------------------------------------------------------------

float16 multMtx(const float16 a, const float16 b)
{
	float16 c;

    c.s0 = dot(b.s048c, a.s0123);
    c.s1 = dot(b.s159d, a.s0123);
    c.s2 = dot(b.s26ae, a.s0123);
    c.s3 = dot(b.s37bf, a.s0123);

    c.s4 = dot(b.s048c, a.s4567);
    c.s5 = dot(b.s159d, a.s4567);
    c.s6 = dot(b.s26ae, a.s4567);
    c.s7 = dot(b.s37bf, a.s4567);

    c.s8 = dot(b.s048c, a.s89ab);
    c.s9 = dot(b.s159d, a.s89ab);
    c.sa = dot(b.s26ae, a.s89ab);
    c.sb = dot(b.s37bf, a.s89ab);

    c.sc = dot(b.s048c, a.scdef);
    c.sd = dot(b.s159d, a.scdef);
    c.se = dot(b.s26ae, a.scdef);
    c.sf = dot(b.s37bf, a.scdef);

	return c;
}

//------------------------------------------------------------------------------
float3 mtxMul( float16 matrix , float3 point )
{
    const float4 homogeneousPoint = (float4)( point.xyz , 1.0f );
    const float4 transformedPoint = (float4)(
        dot( homogeneousPoint , matrix.s048c ) ,
        dot( homogeneousPoint , matrix.s159d ) ,
        dot( homogeneousPoint , matrix.s26ae ) ,
        dot( homogeneousPoint , matrix.s37bf )
        );
    return transformedPoint.xyz / transformedPoint.w;
}

//------------------------------------------------------------------------------
float3
calcCenter(
    unsigned int iChunkId,
    __global const unsigned int* iChunkDataIndexer,
    __global const unsigned int* iChunkData,
    __global const float* iPoints)
{
    const unsigned int h = iChunkDataIndexer[iChunkId];
    const unsigned int s = h+4;
    const unsigned int e = iChunkDataIndexer[iChunkId+1];

    float3 center = (float3)(0.0, 0.0, 0.0);
    for (unsigned int c = s; c < e; ++c) {
        unsigned int vid = iChunkData[c];
        center += vload3(vid, iPoints);
    }

    unsigned int nv = (e-s);
    if (nv > 0) {
        const float w = 1.0/(float)nv;
        return w * center;
    }
    return center;
}

//------------------------------------------------------------------------------
float16
calcMatrix(
    unsigned int iChunkId,
    __global const unsigned int* iChunkDataIndexer,
    __global const unsigned int* iChunkData,
    __global const float* iPoints,
    __global const float* iStabilizationPoints,
    __global const float* iApplyScale)
{
    float3 center = calcCenter(iChunkId, iChunkDataIndexer, iChunkData, iPoints);

    const unsigned int h = iChunkDataIndexer[iChunkId];
    float3 yvec;
    float3 zvec;
    bool valid = false;

    if (iStabilizationPoints) {
        unsigned int sid0 = iChunkData[h+2];
        unsigned int sid1 = iChunkData[h+3];
        if (sid0 != INVALID_INDEX && sid1 != INVALID_INDEX) {
            zvec = normalize(vload3(sid0, iStabilizationPoints) - center);
            yvec = normalize(vload3(sid1, iStabilizationPoints) - center);
            valid = true;
        }
    } else {
        unsigned int vid0 = iChunkData[h+0];
        unsigned int vid1 = iChunkData[h+1];
        if (vid0 != INVALID_INDEX && vid1 != INVALID_INDEX) {
            zvec = normalize(vload3(vid0, iPoints) - center);
            yvec = normalize(vload3(vid1, iPoints) - center);
            valid = true;
        }
    }

    float16 frame;
    if (valid) {
        const float3 xvec = normalize(cross(zvec, yvec));
        yvec = cross(xvec, zvec);

        frame.s0123 = (float4)(xvec, 0.0f);
        frame.s4567 = (float4)(yvec, 0.0f);
        frame.s89ab = (float4)(zvec, 0.0f);
        frame.scdef = (float4)(center, 1.0f);

        float16 scaleMat;
        const float3 sc = vload3(iChunkId, iApplyScale);
        scaleMat.s0123 = (float4)(sc.x, 0.0f, 0.0f, 0.0f);
        scaleMat.s4567 = (float4)(0.0f, sc.y, 0.0f, 0.0f);
        scaleMat.s89ab = (float4)(0.0f, 0.0f, sc.z, 0.0f);
        scaleMat.scdef = (float4)(0.0f, 0.0f, 0.0f, 1.0f);

        return multMtx(scaleMat, frame);
    }
    else {
        frame.s0123 = (float4)(1.0f, 0.0f, 0.0f, 0.0f);
        frame.s4567 = (float4)(0.0f, 1.0f, 0.0f, 0.0f);
        frame.s89ab = (float4)(0.0f, 0.0f, 1.0f, 0.0f);
        frame.scdef = (float4)(0.0f, 0.0f, 0.0f, 1.0f);
    }
    return frame;
}

//------------------------------------------------------------------------------
double calcEdgeLength(
    unsigned int iChunkId,
    __global const unsigned int* iEdgeIndexer,
    __global const unsigned int* iEdgeConnections,
    __global const float* iPoints)
{
    const unsigned int s = iEdgeIndexer[iChunkId];
    const unsigned int e = iEdgeIndexer[iChunkId+1];
    double cel = 0.0;
    for (unsigned int c = s; c < e; c+=2) {
        const float3 p0 = vload3(iEdgeConnections[c],iPoints);
        const float3 p1 = vload3(iEdgeConnections[c+1],iPoints);
        double dx = (double)p0.x - (double)p1.x;
        double dy = (double)p0.y - (double)p1.y;
        double dz = (double)p0.z - (double)p1.z;
        cel += sqrt(dx*dx + dy*dy + dz*dz);
    }
    return cel;
}

//------------------------------------------------------------------------------
__kernel void basicScaleKernel(
    __global float* iApplyScale,
    const float iScaleEnvelope,
    const float iNormalScale,
    const float iTangentPlaneScale,
    const uint iChunkCount)
{
    unsigned int cid = get_global_id(0);
    if ( cid >= iChunkCount ) return;

    float3 sc = (float3)(iNormalScale, iTangentPlaneScale, iTangentPlaneScale);
    vstore3(sc, cid, iApplyScale);
}

//------------------------------------------------------------------------------
__kernel void edgeScaleKernel(
    __global float* iApplyScale,
    const float iScaleEnvelope,
    const float iNormalScale,
    const float iTangentPlaneScale,
    const uint iChunkCount,
    __global const unsigned int* iEdgeIndexer,
    __global const unsigned int* iEdgeConnections,
    __global const double* iOrgEdgeLengths,
    __global const float* iPoints)
{
    unsigned int cid = get_global_id(0);
    if ( cid >= iChunkCount ) return;

    const double bel = iOrgEdgeLengths[cid];
    const double cel = calcEdgeLength(cid, iEdgeIndexer, iEdgeConnections, iPoints);

    double as = cel/bel;
    as = as*iScaleEnvelope + (1.0-iScaleEnvelope);
    float3 sc = (float3)(as*iNormalScale, as*iTangentPlaneScale, as*iTangentPlaneScale);
    vstore3(sc, cid, iApplyScale);
}

//------------------------------------------------------------------------------
__kernel void edgeGlobalScaleKernel(
    __global float* iApplyScale,
    const float iScaleEnvelope,
    const float iNormalScale,
    const float iTangentPlaneScale,
    const uint iChunkCount,
    __global const unsigned int* iEdgeIndexer,
    __global const unsigned int* iEdgeConnections,
    __global const double* iOrgEdgeLengths,
    __global const float* iPoints,
    const uint iNum)
{
    unsigned int n = get_global_id(0);
    if ( n >= iNum ) return;

    double totalScale = 0.0;
    for (uint cid = 0; cid < iChunkCount; ++cid) {
        const double bel = iOrgEdgeLengths[cid];
        const double cel = calcEdgeLength(cid, iEdgeIndexer, iEdgeConnections, iPoints);
        totalScale += cel/bel;
    }

    double as = totalScale/iChunkCount;
    as = as*iScaleEnvelope + (1.0-iScaleEnvelope);

    float3 sc = (float3)(as*iNormalScale, as*iTangentPlaneScale, as*iTangentPlaneScale);
    for (uint cid = 0; cid < iChunkCount; ++cid)
        vstore3(sc, cid, iApplyScale);
}

//------------------------------------------------------------------------------
__kernel void deltaMatrixKernel(
    __global float* iDeltaMatrices,
    __global const float* iBindMatrices,
    __global const unsigned int* iChunkDataIndexer,
    __global const unsigned int* iChunkData,
    __global const float* iPoints,
    __global const float* iStabilizationPoints,
    __global const float* iApplyScale,
    const uint iChunkCount)
{
    unsigned int cid = get_global_id(0);
    if ( cid >= iChunkCount ) return;

    const float16 cm = calcMatrix(cid, iChunkDataIndexer, iChunkData, iPoints, iStabilizationPoints, iApplyScale);
    const float16 bm = vload16(cid, iBindMatrices);
    vstore16(multMtx(bm, cm), cid, iDeltaMatrices);
}

//------------------------------------------------------------------------------
__kernel void moveChunksKernel(
    __global float* iOutPos ,
    __global const float* iCurPos,
    __global const float* iOrgPos,
    __global const float* iDeltaMatrices,
    __global const unsigned int* iChunkIds,
    __global const float* iBorderFalloffWeights,
    __global const unsigned int* iAffectMap,
    __global const float* iWeights,
    const float iEnvelope,
    const uint iNumChunks,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    const float3 cp = vload3(vid, iCurPos);

    const unsigned int cid = iChunkIds[aid];
    if (cid >= iNumChunks) {
        vstore3(cp, vid , iOutPos);
        return;
    }

    const float e = iEnvelope * (iBorderFalloffWeights ? iBorderFalloffWeights[aid] : 1.0) * (iWeights ? iWeights[ aid ] : 1.0f);
    const float16 dm = vload16(cid, iDeltaMatrices);
    const float3 op = vload3(vid, iOrgPos);
    float3 pos = cp + e * (mtxMul(dm, op) - cp);
    vstore3(pos, vid, iOutPos);
}

//------------------------------------------------------------------------------
__kernel void replaceTestKernel(
    __global float* iOutPos ,
    __global const float* iInPos,
    __global const unsigned int* iAffectMap,
    __global const float* iPoints,
    const float iEnvelope,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 np  = vload3(aid, iPoints);
    float3 cp = vload3(vid, iInPos);
    vstore3(cp + iEnvelope * (np - cp), vid, iOutPos);
}

//------------------------------------------------------------------------------
__kernel void exampleKernel(
    __global float* iOutPos ,
    __global const float* iInPos,
    __global const unsigned int* iAffectMap,
    const float iEnvelope,
    const float3 iOffset,
    const uint iAffectCount)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);

    float3 pos = vload3(vid, iInPos) + iEnvelope * iOffset;
    vstore3(pos, vid, iOutPos);
}
