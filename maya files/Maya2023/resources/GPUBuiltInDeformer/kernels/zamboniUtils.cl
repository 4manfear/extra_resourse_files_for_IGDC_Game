// Helper functions
// OSX seems to be using very strict compiler setting which demand the function
// prototype be defined before the function is implemented.  It seems like we
// only need the function prototype for helper methods, not kernels that are
// used directly.

float3 multMtxPt( float16 matrix , float3 point );
float3 multMtxPtAffine( float16 matrix , float3 point );
float16 multMtx(const float16 a, const float16 b);
float3 lerp( const float3 a , const float3 b , const float factor );

float16 calculateCoordinateSystem(const float3 iNormal, const float3 iDirHint, const float3 iPos);

//------------------------------------------------------------------------------
float3 calculateVertexNormal(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs);

//------------------------------------------------------------------------------
float3 calculateVertexNormalWithAffectMap(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs);

//------------------------------------------------------------------------------
float16 calculateVertexFrame(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs);

//------------------------------------------------------------------------------
float16 calculateVertexFrameWithAffectMap(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs);

//------------------------------------------------------------------------------
float16 calculateVertexFrameWithNormal(
    unsigned int iAid,
    const float3 iNormal,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs);

//------------------------------------------------------------------------------
//
//
//
//------------------------------------------------------------------------------
float3 multMtxPt( float16 matrix , float3 point )
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
float3 multMtxPtAffine( float16 matrix , float3 point )
{
    const float4 homogeneousPoint = (float4)( point.xyz , 1.0f );
    return (float3)(dot( homogeneousPoint , matrix.s048c ) ,
                    dot( homogeneousPoint , matrix.s159d ) ,
                    dot( homogeneousPoint , matrix.s26ae ));
}

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
float3 lerp( const float3 a , const float3 b , const float factor )
{
    return a + factor * ( b - a );
}

//------------------------------------------------------------------------------
float16
calculateCoordinateSystem(const float3 iNormal, const float3 iDirHint, const float3 iPos)
{
    /*
        frame.s0123 = (float4)(1.0f, 0.0f, 0.0f, 0.0f);
        frame.s4567 = (float4)(0.0f, 1.0f, 0.0f, 0.0f);
        frame.s89ab = (float4)(0.0f, 0.0f, 1.0f, 0.0f);
        frame.scdef = (float4)(iPos, 1.0f);
    */

    float3 yvec = normalize(iDirHint);
    const float3 xvec = normalize(cross(iNormal, yvec));
    // Note: xvec and normal are orthogonal unit vectors, so their cross
    //       product will be a unit vector
    yvec = cross(xvec, iNormal);

    float16 frame;
    frame.s0123 = (float4)(xvec, 0.0f);
    frame.s4567 = (float4)(yvec, 0.0f);
    frame.s89ab = (float4)(iNormal, 0.0f);
    frame.scdef = (float4)(iPos, 1.0f);

    return frame;
}


//------------------------------------------------------------------------------
float3 calculateVertexNormal(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs)
{
    float3 normal = (float3)(0.0, 0.0, 0.0);

    const unsigned int s = iFrameIndexer[iAid];
    const unsigned int e = iFrameIndexer[iAid+1];

    if (s == e) {
        return normal;
    }

    float3 p = vload3(iAid, iVerts);

    for (unsigned int i = s; i < e; i+=2) {

        const float3 v0 = vload3(iFramePairs[i], iVerts) - p;
        const float3 v1 = vload3(iFramePairs[i+1], iVerts) - p;

        normal += cross(v0, v1); // area size influences normal (normalize to remove this)
    }

    return normalize(normal);
}

//------------------------------------------------------------------------------
float3 calculateVertexNormalWithAffectMap(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs)
{
    float3 normal = (float3)(0.0, 0.0, 0.0);

    const unsigned int s = iFrameIndexer[iAid];
    const unsigned int e = iFrameIndexer[iAid+1];

    if (s == e) {
        return normal;
    }

    if (iAffectMap) {
        float3 p = vload3(iAffectMap[iAid], iVerts);

        for (unsigned int i = s; i < e; i+=2) {
            const float3 v0 = vload3(iAffectMap[iFramePairs[i]], iVerts) - p;
            const float3 v1 = vload3(iAffectMap[iFramePairs[i+1]], iVerts) - p;

            normal += cross(v0, v1); // area size influences normal (normalize to remove this)
        }
    } else {
        float3 p = vload3(iAid, iVerts);
        for (unsigned int i = s; i < e; i+=2) {

            const float3 v0 = vload3(iFramePairs[i], iVerts) - p;
            const float3 v1 = vload3(iFramePairs[i+1], iVerts) - p;

            normal += cross(v0, v1); // area size influences normal (normalize to remove this)
        }
    }

    return normalize(normal);
}

//------------------------------------------------------------------------------
float16
calculateVertexFrame(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs)
{
    const float3 normal = calculateVertexNormal(iAid, iVerts, iFrameIndexer, iFramePairs);

    const unsigned int s = iFrameIndexer[iAid];
    const float3 vPosition = vload3(iAid, iVerts);
    const float3 nPosition = vload3(iFramePairs[s], iVerts);

    return calculateCoordinateSystem(normal, nPosition-vPosition, vPosition);
}

//------------------------------------------------------------------------------
float16
calculateVertexFrameWithAffectMap(
    unsigned int iAid,
    __global const float* iVerts,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs)
{
    const float3 normal = calculateVertexNormalWithAffectMap(iAid, iVerts, iAffectMap, iFrameIndexer, iFramePairs);

    const unsigned int s = iFrameIndexer[iAid];
    if (iAffectMap) {
        const float3 vPosition = vload3(iAffectMap[iAid], iVerts);
        const float3 nPosition = vload3(iAffectMap[iFramePairs[s]], iVerts);
        return calculateCoordinateSystem(normal, nPosition-vPosition, vPosition);
    } else {
        const float3 vPosition = vload3(iAid, iVerts);
        const float3 nPosition = vload3(iFramePairs[s], iVerts);
        return calculateCoordinateSystem(normal, nPosition-vPosition, vPosition);
    }
}

//------------------------------------------------------------------------------
float16
calculateVertexFrameWithNormal(
    unsigned int iAid,
    const float3 iNormal,
    __global const float* iVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs)
{
    const unsigned int s = iFrameIndexer[iAid];
    const float3 vPosition = vload3(iAid, iVerts);
    const float3 nPosition = vload3(iFramePairs[s], iVerts);

    return calculateCoordinateSystem(iNormal, nPosition-vPosition, vPosition);
}

//------------------------------------------------------------------------------
__kernel void tangentConstraintKernel(
    __global float* iOutPos,                                // arg 0
    __global const float* iInPos,                           // arg 1
    __global const unsigned char* iPinned,                  // arg 2
    __global const unsigned int* iFrameIndexer,             // arg 3
    __global const unsigned int* iFramePairs,               // arg 4
    const float iInwardConstraint,                          // arg 5
    const float iOutwardConstraint,                         // arg 6
    const uint iAffectCount)                                // arg 7
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    if (iPinned && iPinned[aid])
        return;

    const float3 normal = calculateVertexNormal(aid, iInPos, iFrameIndexer, iFramePairs);

    float3 currentPos = vload3(aid, iOutPos);

    const float3 initialPos = vload3(aid, iInPos);
    const float3 displacement = currentPos-initialPos;

    const float d = dot(displacement, normal);

    if (d < 0.0) {
        const float3 offset = (iInwardConstraint*d)*normal;
        currentPos -= offset;
        vstore3(currentPos, aid, iOutPos);
    } else if (d > 0.0) {
        const float3 offset = (iOutwardConstraint*d)*normal;
        currentPos -= offset;
        vstore3(currentPos, aid, iOutPos);
    }

}

//------------------------------------------------------------------------------
__kernel void tangentConstraintWithAffectMapKernel(
    __global float* iOutPos,
    __global const float* iInPos,
    __global const unsigned int* iAffectMap,
    __global const unsigned char* iLocked,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    const float iInwardConstraint,
    const float iOutwardConstraint,
    const float iDamping,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    if (iLocked && iLocked[aid])
        return;

    const float3 normal = iAffectMap ?
                            calculateVertexNormal(aid, iInPos, iFrameIndexer, iFramePairs) :
                            calculateVertexNormalWithAffectMap(aid, iInPos, iAffectMap, iFrameIndexer, iFramePairs);

    const unsigned int vid = (iAffectMap ? iAffectMap[aid] : aid);
    float3 currentPos = vload3(vid, iOutPos);

    const float3 initialPos = vload3(vid, iInPos);
    const float3 displacement = currentPos-initialPos;

    const float d = dot(displacement, normal);
    float rConstraint = 0.0;
    if (d < 0.0) {
        rConstraint = iInwardConstraint;
    } else if (d > 0.0) {
        rConstraint = iOutwardConstraint;
    } else {
        return;
    }

    const float3 offset = (rConstraint*d)*normal;
    if (iDamping > 0.0) {
        const float3 basePos = currentPos + rConstraint*(initialPos-currentPos);
        currentPos -= offset;
        currentPos += iDamping*(basePos - currentPos);
    } else {
        currentPos -= offset;
    }
    vstore3(currentPos, vid, iOutPos);
}

//------------------------------------------------------------------------------
__kernel void averageVertKernel(
    __global float* iOutPos ,                               // arg 0
    __global const float* iInPos,                           // arg 1
    __global const unsigned char* iPinned,                  // arg 2
    const float iLambda,                                    // arg 3
    __global const unsigned int* iIndexer,                  // arg 4
    __global const unsigned int* iConnections,              // arg 5
    __global const float* iWeights,                         // arg 6
     const uint iAffectCount)                               // arg 7
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float3 initialPos = vload3(aid, iInPos);

    if (iPinned) {
        if (iPinned[aid]) {
            vstore3(initialPos, aid , iOutPos);
            return;
        }
    }

    const unsigned int s = iIndexer[aid];
    const unsigned int e = iIndexer[aid+1];
    if (s == e) {
        vstore3(initialPos, aid , iOutPos);
        return;
    }

    float3 neighborSum = (float3)(0.0f, 0.0f, 0.0f);
    if (iWeights) {
        for (unsigned int c = s; c < e; ++c) {
            float3 np = vload3(iConnections[c], iInPos);
            neighborSum = neighborSum + (iWeights[c] * np);
        }
    } else {
        for (unsigned int c = s; c < e; ++c) {
            float3 np = vload3(iConnections[c], iInPos);
            neighborSum = neighborSum + np;
        }
    }

    neighborSum /= (float)(e-s);
    const float3 pos = initialPos + iLambda * (neighborSum - initialPos);
    vstore3(pos, aid , iOutPos);
}

//------------------------------------------------------------------------------
__kernel void applyDisplacementKernel(
    __global float* iResultVerts,                           // arg 0
    __global const float* iSourceVerts,                     // arg 1
    __global float* iDisplacements,                         // arg 2
    const float3 iWeightedScale,                            // arg 3
    __global const unsigned int* iFrameIndexer,             // arg 4
    __global const unsigned int* iFramePairs,               // arg 5
    const uint iAffectCount)                                // arg 6
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float3 displacement = vload3(aid, iDisplacements);

    const float3 dir = (float3)(displacement.x * iWeightedScale.x,
                                displacement.y * iWeightedScale.y,
                                displacement.z * iWeightedScale.z);

    const float16 frame = calculateVertexFrame(aid, iSourceVerts, iFrameIndexer, iFramePairs);
    vstore3(multMtxPtAffine( frame, dir ), aid, iResultVerts);
}

//------------------------------------------------------------------------------
__kernel void calculateVertexNormalsKernel(
    __global float* iNormals,
    __global const float* iInPos,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    vstore3(calculateVertexNormal(aid, iInPos, iFrameIndexer, iFramePairs), aid, iNormals);
}

//------------------------------------------------------------------------------
__kernel void averageNormalsKernel(
    __global float* iOutNormals,
    __global const float* iInNormals,
    __global const unsigned int* iIndexer,
    __global const unsigned int* iConnections,
    __global const float* iWeights,
     const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float3 initialNormal = vload3(aid, iInNormals);
    const unsigned int s = iIndexer[aid];
    const unsigned int e = iIndexer[aid+1];
    if (s == e) {
        vstore3(initialNormal, aid, iOutNormals);
        return;
    }

    float3 normal = initialNormal;
    for (unsigned int c = s; c < e; ++c) {
        float3 np = vload3(iConnections[c], iInNormals);
        normal = normal + ( iWeights[c] * np);
    }

    vstore3(normalize(normal), aid , iOutNormals);
}

//------------------------------------------------------------------------------
__kernel void calculateVertexFramesKernel(
    __global float* iResultFrames,
    __global const float* iSourceVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float16 frame = calculateVertexFrame(aid, iSourceVerts, iFrameIndexer, iFramePairs);
    vstore16(frame, aid, iResultFrames);
}

//------------------------------------------------------------------------------
__kernel void multMatricesKernel(
    __global float* iResultFrames,
    __global const float* iA,
    __global const float* iB,
    const uint iCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iCount ) return;

    const float16 a = vload16(aid, iA);
    const float16 b = vload16(aid, iB);
    const float16 frame = multMtx(a, b);

    vstore16(frame, aid, iResultFrames);
}

//------------------------------------------------------------------------------
__kernel void calculateVertexFramesDeltaKernel(
    __global float* iResultFrames,
    __global const float* iRelativeFramesInv,
    __global const float* iSourceVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float16 bindFrameInv = vload16(aid, iRelativeFramesInv);
    const float16 frame = multMtx(bindFrameInv, calculateVertexFrame(aid, iSourceVerts, iFrameIndexer, iFramePairs));

    vstore16(frame, aid, iResultFrames);
}

//------------------------------------------------------------------------------
__kernel void calculateVertexFramesDeltaWithAffectMapKernel(
    __global float* iResultFrames,
    __global const float* iRelativeFramesInv,
    __global const float* iSourceVerts,
    __global const unsigned int* iAffectMap,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float16 bindFrameInv = vload16(aid, iRelativeFramesInv);
    const float16 frame = multMtx(bindFrameInv, calculateVertexFrameWithAffectMap(aid, iSourceVerts, iAffectMap, iFrameIndexer, iFramePairs));

    vstore16(frame, aid, iResultFrames);
}

//------------------------------------------------------------------------------
__kernel void calculateVertexFramesDeltaWithNormalKernel(
    __global float* iResultFrames,
    __global const float* iRelativeFramesInv,
    __global const float* iSourceVerts,
    __global const unsigned int* iFrameIndexer,
    __global const unsigned int* iFramePairs,
    __global const float* iNormals,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float3 normal = vload3(aid, iNormals);
    const float16 bindFrameInv = vload16(aid, iRelativeFramesInv);
    const float16 frame = multMtx(bindFrameInv, calculateVertexFrameWithNormal(aid, normal, iSourceVerts, iFrameIndexer, iFramePairs));

    vstore16(frame, aid, iResultFrames);
}

//------------------------------------------------------------------------------
__kernel void offsetDebugKernel(
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
