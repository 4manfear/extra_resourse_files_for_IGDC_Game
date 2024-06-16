
//------------------------------------------------------------------------------
__kernel void springLengthAndDirKernel(
    __global const float* iVerts,                               // arg 0
    __global const unsigned int* iSpringAttachments,            // arg 1
    __global float* iLengths,                                   // arg 2
    __global float* iDirections,                                // arg 3
    const uint iSpringCount)                                    // arg 4
{
    const unsigned int springId = get_global_id(0);
    if ( springId >= iSpringCount ) return;

    const unsigned int p0 = iSpringAttachments[springId*2];
    const unsigned int p1 = iSpringAttachments[springId*2+1];

    const float3 v0 = vload3(p0, iVerts);
    const float3 v1 = vload3(p1, iVerts);
    const float3 dir = v1 - v0;
    const float len = length(dir);

    iLengths[springId] = len;
    const float3 ndir = normalize(dir);
    vstore3(ndir, springId, iDirections);
}

//------------------------------------------------------------------------------
__kernel void tensionVertsKernel(
    __global float* iOutPos,                                    // arg 0
    __global const float* iInPos,                               // arg 1
    __global const unsigned char* iPinned,                      // arg 2
    const float iLambda,                                        // arg 3
    const uchar iUseRelative,                                   // arg 4
    const float iRelative,                                      // arg 5
    const float iSquashConstraint,                              // arg 6
    const float iStretchConstraint,                             // arg 7
    __global const unsigned int* iSpringIndexer,                // arg 8
    __global const unsigned int* iSpringIds,                    // arg 9
    __global const unsigned int* iSpringAttachments,            // arg 10
    __global float* iDirBuffer,                                 // arg 11
    __global float* iLengthBuffer,                              // arg 12
    __global float* iRestLengthBuffer,                          // arg 13
    __global uchar* iSpringTypes,                               // arg 14
    __global float* iSpringTypeStrength,                        // arg 15
    const uint iAffectCount)                                    // arg 16
{
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    const float3 initialPos = vload3(aid, iInPos);

    if (iPinned[aid]) {
        vstore3(initialPos, aid , iOutPos);
        return;
    }

    const unsigned int s = iSpringIndexer[aid];
    const unsigned int e = iSpringIndexer[aid+1];
    if (s == e) {
        vstore3(initialPos, aid , iOutPos);
        return;
    }

    float relativeChange = 1.0;
    if (iUseRelative) {
        float lenRest = 0.0;
        float lenCur = 0.0;
        for (unsigned int c = s; c < e; ++c) {
            const unsigned int sid = iSpringIds[c];
            lenRest += iRestLengthBuffer[sid];
            lenCur += iLengthBuffer[sid];
        }
        relativeChange = lenCur/lenRest;
    }

    float3 delta = (float3)(0.0f, 0.0f, 0.0f);
    for (unsigned int c = s; c < e; ++c) {
        const unsigned int sid = iSpringIds[c];
        float d = 0.0;

        if (iUseRelative) {
            float desiredLength = iRestLengthBuffer[sid] * (1.0f + iRelative * (relativeChange - 1.0f));
            d = iLengthBuffer[sid] - desiredLength;
        } else {
            d = iLengthBuffer[sid] - iRestLengthBuffer[sid];
        }

        float k = iSpringTypeStrength[iSpringTypes[sid]];
        if (d < 0.0) {
            k *= iSquashConstraint;
        } else {
            k *= iStretchConstraint;
        }

        const float3 dir = vload3(sid, iDirBuffer);

        if (iSpringAttachments[sid*2] == aid) {
            delta += k*d*dir;
        } else {
            delta -= k*d*dir;
        }
    }
    const float r = iLambda/(float)(e-s);
    const float3 pos = initialPos + r * delta;
    vstore3(pos, aid,  iOutPos);
}
