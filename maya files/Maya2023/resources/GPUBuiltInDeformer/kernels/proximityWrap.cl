//------------------------------------------------------------------------------
float3 mtxMul( float16 matrix , float3 point );

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
__kernel void gpu_proximityWrapOffsetKernel(
    // general kernel arguments
    __global float* iPos,
    __global const float16* iBendyCurMatInv,
    __global const unsigned int* iUseMap,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iVid,
    __global const float* iVidWeight,
    const uint iUseCount,
    __global const float16* iDriverCurMat,
    // kernel specific arguments
    __global const float* iDriverCurVerts,
    __global const float* iDriverOrgVerts)
{
    const unsigned int uid = get_global_id(0);
    if ( uid >= iUseCount ) return;

    const unsigned int aid = iUseMap[uid];
    const unsigned int s = iIndexer[uid];
    const unsigned int e = iIndexer[uid+1];

    if (s == e)
        return;

    float3 delta = (float3)(0.0f, 0.0f, 0.0f);
    for (unsigned int c = s; c < e; ++c) {
        const float3 localDriverVert = vload3(iVid[c], iDriverCurVerts);
        const float3 driverVert = mtxMul(*iBendyCurMatInv, mtxMul( *iDriverCurMat, localDriverVert));

        const float3 driverBindVert = vload3(iVid[c], iDriverOrgVerts);
        const float3 offset = driverVert - driverBindVert;
        delta = delta + (iVidWeight[c] * offset);
    }

    const float3 initialPos = vload3(aid, iPos);
    vstore3(initialPos+delta, aid , iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_proximityWrapSnapKernel(
    // general kernel arguments
    __global float* iPos,
    __global const float16* iBendyCurMatInv,
    __global const unsigned int* iUseMap,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iVid,
    __global const float* iVidWeight,
    const uint iUseCount,
    __global const float16* iDriverCurMat,
    // kernel specific arguments
    __global const float* iDriverCurVerts,
    __global const float* iBendyCurVerts,
    __global const unsigned int* iAffectMap)
{
    const unsigned int uid = get_global_id(0);
    if ( uid >= iUseCount ) return;

    const unsigned int aid = iUseMap[uid];
    const unsigned int s = iIndexer[uid];
    const unsigned int e = iIndexer[uid+1];

    if (s == e)
        return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    const float3 src = vload3(vid, iBendyCurVerts);
    float3 delta = (float3)(0.0f, 0.0f, 0.0f);
    for (unsigned int c = s; c < e; ++c) {
        const float3 ldrv = vload3(iVid[c], iDriverCurVerts);
        const float3 drv = mtxMul(*iBendyCurMatInv, mtxMul( *iDriverCurMat, ldrv));

        const float3 offset = drv - src;
        delta = delta + (iVidWeight[c] * offset);
    }

    const float3 initialPos = vload3(aid, iPos);
    vstore3(initialPos+delta, aid , iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_proximityWrapSurfaceKernel(
    // general kernel arguments
    __global float* iPos,
    __global const float16* iBendyCurMatInv,
    __global const unsigned int* iUseMap,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iVid,
    __global const float* iVidWeight,
    const uint iUseCount,
    __global const float16* iDriverCurMat,
    // kernel specific arguments
    __global const float* iVertexFrames,
    __global const float* iBendyCurVerts,
    __global const unsigned int* iAffectMap)
{
    const unsigned int uid = get_global_id(0);
    if ( uid >= iUseCount ) return;

    const unsigned int aid = iUseMap[uid];
    const unsigned int s = iIndexer[uid];
    const unsigned int e = iIndexer[uid +1];

    if (s == e)
        return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);

    const float3 src = vload3(vid, iBendyCurVerts);
    float3 delta = (float3)(0.0f, 0.0f, 0.0f);
    for (unsigned int c = s; c < e; ++c) {
        const float16 m = vload16(iVid[c], iVertexFrames);
        const float3 offset = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, mtxMul( m, src ))) - src;
        delta = delta + (iVidWeight[c] * offset);
    }

    const float3 initialPos = vload3(aid, iPos);
    vstore3(initialPos+delta, aid , iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_proximityWrapRigidKernel(
    // general kernel arguments
    __global float* iPos,
    __global const float16* iBendyCurMatInv,
    __global const unsigned int* iUseMap,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iVid,
    __global const float* iVidWeight,
    const uint iUseCount,
    __global const float16* iDriverCurMat,
    // kernel specific arguments
    __global const float16* iDriverOrgMatInv,
    __global const float* iBendyCurVerts,
    __global const unsigned int* iAffectMap)
{
    const unsigned int uid = get_global_id(0);
    if ( uid >= iUseCount ) return;

    const unsigned int aid = iUseMap[uid];
    const unsigned int s = iIndexer[uid];
    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);

    const float3 src = vload3(vid, iBendyCurVerts);
    const float3 dst = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, mtxMul( *iDriverOrgMatInv, src)));
    const float3 offset = dst - src;

    const float3 delta = (iVidWeight[s] * offset);

    const float3 initialPos = vload3(aid, iPos);
    vstore3(initialPos+delta, aid , iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_proximityWrapMatrixBindKernel(
    __global float* iPos,
    __global const float16* iBendyCurMatInv,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iDriverIds,
    __global const float* iDriverWeights,
    __global const float* iDriverCurMatrices,
    __global const float* iDriverOrgInvMatrices,
    __global const float* iBendyCurVerts,
    __global const unsigned int* iAffectMap,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int s = iIndexer[aid];
    const unsigned int e = iIndexer[aid+1];
    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);

    const float3 src = vload3(vid, iBendyCurVerts);
    float3 newPt = vload3(aid, iPos); // initialPos
    for (unsigned int c = s; c < e; ++c) {
        const unsigned int didx = iDriverIds[c];
        const float w = iDriverWeights[c];
        const float16 cm = vload16(didx, iDriverCurMatrices);
        const float16 om = vload16(didx, iDriverOrgInvMatrices);
        const float3 dst = mtxMul(*iBendyCurMatInv, mtxMul(cm, mtxMul(om, src)));
        const float3 offset = dst - src;
        newPt += w*offset;
    }

    vstore3(newPt, aid , iPos);
}
