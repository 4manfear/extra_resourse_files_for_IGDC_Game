#define INVALID_INDEX UINT_MAX

//------------------------------------------------------------------------------
float16 multMtx(const float16 a, const float16 b);
float3 mtxMul( float16 matrix , float3 point );
float3 retargetOffset(
        const uint iAid,
        const float3 iOffset,
        __global const float* iBendyFrames,
        __global const float* iTargetFrames,
        __global const float* iEdgeScaling,
        __global const float* iBoxScaling,
        float iNormalScale,
        float iTangentPlaneScale,
        float iScaleEnvelope,
        float iUniformScaleWeight);

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

//-------------------------------------------------------------------------------
 float3 retargetOffset(
         const uint iAid,
         const float3 iOffset,
         __global const float* iBendyFrames,
         __global const float* iTargetFrames,
         __global const float* iEdgeScaling,
         __global const float* iBoxScaling,
         float iNormalScale,
         float iTangentPlaneScale,
         float iScaleEnvelope,
         float iUniformScaleWeight)
 {
     const float16 tmtx = vload16(iAid, iTargetFrames);
     const float16 bmtx = vload16(iAid, iBendyFrames);

     // The inverse of a pure 3x3 rotation matrix is its transpose...
     float3 v = (float3)(dot(tmtx.s012,iOffset.s012), dot(tmtx.s456,iOffset.s012), dot(tmtx.s89a,iOffset.s012));

     // Scale adjustments
     if (iScaleEnvelope > 0.0) {
         float ru = iEdgeScaling[iAid];
         float3 s = (float3)(ru,ru,ru);
         if (iUniformScaleWeight < 1.0) {
             float3 psc = vload3(iAid, iBoxScaling);
             float rnu = 1.0 - iUniformScaleWeight;
             s.x = iUniformScaleWeight*ru + rnu*psc.x;
             s.y = iUniformScaleWeight*ru + rnu*psc.y;
             s.z = iUniformScaleWeight*ru + rnu*psc.z;
         }

         v.x *= (1.0-iScaleEnvelope + iScaleEnvelope*s.x*iTangentPlaneScale);
         v.y *= (1.0-iScaleEnvelope + iScaleEnvelope*s.y*iTangentPlaneScale);
         v.z *= (1.0-iScaleEnvelope + iScaleEnvelope*s.z*iNormalScale);
     }

     // Only multiply with the rotational part of the matrix...
     return (float3)(dot(bmtx.s048,v.s012), dot(bmtx.s159,v.s012), dot(bmtx.s26a,v.s012));
 }

//------------------------------------------------------------------------------
//
// Kernels
//
//------------------------------------------------------------------------------
__kernel void gpu_absolute_object_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (cur_mt - cur), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_absolute_world_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float16* iBendyCurMatInv,
    __global const float16* iDriverCurMat)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    const float3 cur_mt = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, vload3(vid_mt, iCurDriverVerts)));
    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (cur_mt - cur), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_relative_object_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iOrgDriverVerts,
    const uchar iUseOriginalMorphTarget)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);
    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    float3 org_mt = vload3(iUseOriginalMorphTarget ? vid_mt : aid, iOrgDriverVerts);

    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (cur_mt - org_mt), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_relative_world_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iOrgDriverVerts,
    const uchar iUseOriginalMorphTarget,
    __global const float16* iBendyCurMatInv,
    __global const float16* iDriverCurMat)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);
    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    const float3 cur_mt = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, vload3(vid_mt, iCurDriverVerts)));
    const float3 org_mt = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, vload3(iUseOriginalMorphTarget ? vid_mt : aid, iOrgDriverVerts)));
    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (cur_mt - org_mt), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_surface_object_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iDeltaFrames)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);

    const float16 delta_frame = vload16(aid, iDeltaFrames);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (p - cur), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_surface_world_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iDeltaFrames,
    __global const float16* iBendyCurMatInv,
    __global const float16* iDriverCurMat)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const float16 delta_frame = vload16(aid, iDeltaFrames);
    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
    p = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, p)); // bring it into bendy space...
    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    vstore3(cur + e * (p - cur), vid, iOutputVerts);
}

//------------------------------------------------------------------------------
__kernel void gpu_surface_neighbor_object_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iDeltaFrames,
    __global const unsigned int* iConnectionIndexer,
    __global const unsigned int* iConnections,
    __global const float* iConnectionWeights)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    const float ev = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    const unsigned int s = iConnectionIndexer[aid];
    const unsigned int e = iConnectionIndexer[aid+1];

    if (s == e) {
        const float16 delta_frame = vload16(aid, iDeltaFrames);

        float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
        vstore3(cur + ev * (p - cur), vid, iOutputVerts);
    } else {

        float3 neighborSum = (float3)(0.0f, 0.0f, 0.0f);
        for (unsigned int c = s; c < e; ++c) {
            const unsigned int naid = iConnections[c];

            const float16 delta_frame = vload16(naid, iDeltaFrames);
            float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
            neighborSum = neighborSum + (iConnectionWeights[c] * p);
        }
        neighborSum /= (float)(e-s);
        vstore3(cur + ev * (neighborSum - cur), vid, iOutputVerts);
    }
}


//------------------------------------------------------------------------------
__kernel void gpu_surface_neighbor_world_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iDeltaFrames,
    __global const unsigned int* iConnectionIndexer,
    __global const unsigned int* iConnections,
    __global const float* iConnectionWeights,
    __global const float16* iBendyCurMatInv,
    __global const float16* iDriverCurMat)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }


    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    const float ev = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    const unsigned int s = iConnectionIndexer[aid];
    const unsigned int e = iConnectionIndexer[aid+1];

    if (s == e) {
        const float16 delta_frame = vload16(aid, iDeltaFrames);

        float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
        p = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, p)); // bring it into bendy space...
        vstore3(cur + ev * (p - cur), vid, iOutputVerts);
    } else {

        float3 neighborSum = (float3)(0.0f, 0.0f, 0.0f);
        for (unsigned int c = s; c < e; ++c) {
            const unsigned int naid = iConnections[c];

            const float16 delta_frame = vload16(naid, iDeltaFrames);
            float3 p = mtxMul(delta_frame, cur_mt); // get the surface point
            neighborSum = neighborSum + (iConnectionWeights[c] * p);
        }
        neighborSum /= (float)(e-s);

        float3 p = mtxMul(*iBendyCurMatInv, mtxMul(*iDriverCurMat, neighborSum)); // bring it into bendy space...
        vstore3(cur + ev * (p - cur), vid, iOutputVerts);
    }
}


//------------------------------------------------------------------------------
__kernel void gpu_retarget_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iOrgDriverVerts,

    __global const float* iBendyFrames,
    __global const float* iTargetFrames,
    __global const float* iEdgeScaling,
    __global const float* iBoxScaling,
    const float iNormalScale,
    const float iTangentPlaneScale,
    const float iScaleEnvelope,
    const float iUniformScaleWeight)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 cur_mt = vload3(vid_mt, iCurDriverVerts);
    float3 org_mt = vload3(vid_mt, iOrgDriverVerts);

    float3 offset = retargetOffset(aid, cur_mt-org_mt,
                                iBendyFrames, iTargetFrames,
                                iEdgeScaling, iBoxScaling,
                                iNormalScale, iTangentPlaneScale,
                                iScaleEnvelope, iUniformScaleWeight);

    const float e = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);
    vstore3(cur + e * offset, vid, iOutputVerts);
}

 //------------------------------------------------------------------------------
__kernel void gpu_retarget_neighbor_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iCustomMap,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights,
    __global const float* iCurDriverVerts,
    __global const float* iOrgDriverVerts,
    __global const float* iBendyFrames,
    __global const float* iTargetFrames,
    __global const float* iEdgeScaling,
    __global const float* iBoxScaling,
    const float iNormalScale,
    const float iTangentPlaneScale,
    const float iScaleEnvelope,
    const float iUniformScaleWeight,
    __global const unsigned int* iConnectionIndexer,
    __global const unsigned int* iConnections,
    __global const float* iConnectionWeights)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int vid_mt = (iCustomMap ? iCustomMap[aid] : vid);
    float3 v = vload3(vid_mt, iCurDriverVerts) - vload3(vid_mt, iOrgDriverVerts);
    const float ev = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);

    const unsigned int s = iConnectionIndexer[aid];
    const unsigned int e = iConnectionIndexer[aid+1];

    if (s == e) {
        float3 offset = retargetOffset(aid, v,
                                iBendyFrames, iTargetFrames,
                                iEdgeScaling, iBoxScaling,
                                iNormalScale, iTangentPlaneScale,
                                iScaleEnvelope, iUniformScaleWeight);
        vstore3(cur + ev * offset, vid, iOutputVerts);
    } else {
        float3 neighborSum = (float3)(0.0f, 0.0f, 0.0f);
        for (unsigned int c = s; c < e; ++c) {
            float3 offset = retargetOffset(iConnections[c], v,
                                            iBendyFrames, iTargetFrames,
                                            iEdgeScaling, iBoxScaling,
                                            iNormalScale, iTangentPlaneScale,
                                            iScaleEnvelope, iUniformScaleWeight);
            neighborSum = neighborSum + (iConnectionWeights[c] * offset);
        }
        neighborSum /= (float)(e-s);
        vstore3(cur + ev * neighborSum, vid, iOutputVerts);
    }
}

//------------------------------------------------------------------------------
__kernel void gpu_mirror_kernel(
    __global float* iOutputVerts,
    __global const float* iInputVerts,
    const uint iAffectCount,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iMirrorMap,
    const uint iMirAxis,
    __global const unsigned char* iLocked,
    const float iEnvelope,
    __global const float* iWeights)
{
    unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 cur = vload3(vid, iInputVerts);

    if (iLocked && iLocked[aid]) {
        vstore3(cur, vid, iOutputVerts);
        return;
    }

    const unsigned int mirAid = iMirrorMap[aid];

    if (mirAid > iAffectCount) {
        vstore3(cur, vid, iOutputVerts);
    } else {
        const unsigned int mirVid = (iAffectMap ? iAffectMap[mirAid] : mirAid);
        const float ev = iEnvelope * (iWeights ? iWeights[ aid ] : 1.0f);
        float3 p = vload3(mirVid, iInputVerts);

        if (iMirAxis == 0)
            p.x *= -1.0;
        else if (iMirAxis == 1)
            p.y *= -1.0;
        else if (iMirAxis == 2)
            p.z *= -1.0;

        vstore3(cur + ev * (p-cur), vid, iOutputVerts);
    }
}
