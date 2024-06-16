#include <XgUtils.cl>

static float calCrvLengthFromSegs(__global float* segLens, uint numCVs)
{
    // segLens[1] stands for len(P1-P0).....segLens[0] is not used
    float length = 0.0f;
    for (uint i = 1; i < numCVs; ++i) {
        length += segLens[i];
    }
    return length;
}

static float calCrvLengthFromCVs(__global float* CVs, uint numCVs)
{
    float length = 0.0f;
    for (uint i = 1; i < numCVs; ++i) {
        length += fast_length((float3)(
            CVs[i * 3] - CVs[i * 3 - 3],
            CVs[i * 3 + 1] - CVs[i * 3 - 2],
            CVs[i * 3 + 2] - CVs[i * 3 - 1]));
    }
    return length;
}

static float3 rotateBy(const float3 v, const float3 axis, float angle)
{
    float ca = cos(angle);
    float sa = sin(angle);
    float ca1 = 1.0f - ca;

    float a01 = axis.x * axis.y;
    float a02 = axis.x * axis.z;
    float a12 = axis.y * axis.z;
    float a00 = axis.x * axis.x;
    float a11 = axis.y * axis.y;
    float a22 = axis.z * axis.z;

    return (float3)(
        dot(v, (float3)(a00*ca1 + ca, a01*ca1 - axis.z * sa, a02*ca1 + axis.y * sa)),
        dot(v, (float3)(a01*ca1 + axis.z * sa, a11*ca1 + ca, a12*ca1 - axis.x * sa)),
        dot(v, (float3)(a02*ca1 - axis.y * sa, a12*ca1 + axis.x * sa, a22*ca1 + ca))
        );
}

static int hashReduceChar(int3 index)
{
    uint seed = 0;
    const int M = 1664525;
    const int C = 1013904223;
    seed = seed* M + index.x + C;
    seed = seed* M + index.y + C;
    seed = seed* M + index.z + C;

    seed = seed ^ (seed >> 11);
    seed = seed ^ ((seed << 7) & 0x9d2c5680);
    seed = seed ^ ((seed << 15) & 0xefc60000);
    seed = seed ^ (seed >> 18);

    return (((seed & 0xff0000) >> 4) + (seed & 0xff)) & 0xff;
}

static float s_curve(float t) {
    return t * t * t * mad(t, mad(6, t, - 15), 10);
}

static float noiseFn(float3 s, __global float* noiseTable)
{
    // lower and upper weights
    float3 f = floor(s);
    int3 index = (int3)((int)f.x, (int)f.y, (int)f.z);
    float3 weights[2];
    weights[0] = s - f;
    weights[1] = weights[0] - 1.0f;

    // compute function values propagated from zero from each node
    int num = 8; // 1 << 3;
    float vals[8];
    for (uint i = 0;i < 8;++i) {
        vals[i] = 0.0f;
    }
    for (int dummy = 0; dummy<num; dummy++) {
        int3 offset = (int3)((int)((dummy & 1) != 0), (int)((dummy & 2) != 0), (int)((dummy & 4) != 0));
        int3 latticeIndex = index + offset;

        // hash to get representative gradient vector
        int lookup = hashReduceChar(latticeIndex);

        // x
        float grad   = noiseTable[3 * lookup];
        float weight = weights[offset.x].x;
        vals[dummy] += grad*weight;
        // y
        grad = noiseTable[3 * lookup+1];
        weight = weights[offset.y].y;
        vals[dummy] += grad*weight;
        // z
        grad = noiseTable[3 * lookup + 2];
        weight = weights[offset.z].z;
        vals[dummy] += grad*weight;
    }
    // compute linear interpolation coefficients
    float alphas[] = { s_curve(weights[0].x), s_curve(weights[0].y), s_curve(weights[0].z) };

    // perform multilinear interpolation (i.e. linear, bilinear, trilinear, quadralinear)
    for (int newd = 3 - 1;newd >= 0;newd--) {
        int newnum = 1 << newd;
        for (int dummy = 0;dummy<newnum;dummy++) {
            int index = dummy*(1 << (3 - newd));
            int k = (3 - newd - 1);
            int otherIndex = index + (1 << k);
            vals[index] = (1 - alphas[k])*vals[index] + alphas[k] *vals[otherIndex];
        }
    }
    // return reduced version
    return mad(0.5f, vals[0], 0.5f);
}

static void blendLength(
    __global float* CVs,
    uint numCVs,
    float newLen, float curLen)
{
    if (islessequal(curLen, 0.0f))
        return;

    // If there is basically no change just return.
    if (isless(fabs(curLen - newLen), 0.0001f))
        return;

    // Now correct it by scaling all control poly segments
    const float ratio = newLen / curLen;

    //scalePoly(CVs, cvCount, ratio);
    float3 oldSeg, newSeg, vec;
    for (uint j = 0; j < numCVs - 1; j++)
    {
        oldSeg = (float3)(
            CVs[j * 3 + 3] - CVs[j * 3],
            CVs[j * 3 + 4] - CVs[j * 3 + 1],
            CVs[j * 3 + 5] - CVs[j * 3 + 2]
            );
        newSeg = oldSeg * ratio;
        vec = newSeg - oldSeg;
        for (uint k = j + 1; k < numCVs; k++)
        {
            CVs[k * 3]     += vec.x;
            CVs[k * 3 + 1] += vec.y;
            CVs[k * 3 + 2] += vec.z;
        }
    }
}

__kernel void updateNoiseCache(
    __global const  uint* visIndices,
             const  uint  visCount,
    __global uint* info,
    __global float* segLens,
    __global float* P0,
    __global float* magScales,
    __global float* noiseTable,
    uint infoStride,
    uint primitiveCount,
    float mask,
    float frequency,
    float magnitude,
    float correlation,
    __global float* noiseCache
    )
{
    uint gid = get_global_id(0);
    if (gid >= visCount) return;

    gid = visIndices[gid];
    if (gid >= primitiveCount) return;

    const uint flag = info[gid * infoStride + 2];
    if (isPrimCulled(flag))
        return;

    // curve start cv offset
    const uint primitiveOffset = info[gid * infoStride];
    // curve cv count
    const uint numCVs = info[gid * infoStride + 1];

    // bias data to this curve
    segLens    += primitiveOffset;
    P0         += 3 * gid;
    noiseCache += 3 * primitiveOffset;

    const float inCrvLen = calCrvLengthFromSegs(segLens, numCVs);

    float3 P = (float3)(P0[0], P0[1], P0[2]);
    P += (float3)(0.419276f, 0.184247f, 0.805721f);
    P *= correlation;

    frequency = inCrvLen>0.0f ? fmax(0.5f / inCrvLen, frequency) : frequency;

    // Cal offsets
    float len = 0.0f;
    noiseCache[0] = 0.0f;
    noiseCache[1] = 0.0f;
    noiseCache[2] = 0.0f;
    for (uint i = 1; i < numCVs; i++) {
        len += segLens[i];

        float magScale = mask * magScales[i] * magnitude;
        float dist = len*frequency;
        float3 offset = (float3)(
            noiseFn((float3)(P.x + dist, P.y, P.z), noiseTable),
            noiseFn((float3)(P.x, P.y + dist, P.z), noiseTable),
            noiseFn((float3)(P.x, P.y, P.z + dist), noiseTable));
        offset = (offset - 0.5f) * magScale;

        noiseCache[i * 3]     = offset.x;
        noiseCache[i * 3 + 1] = offset.y;
        noiseCache[i * 3 + 2] = offset.z;
    }
}

__kernel void applyNoise(
    __global const  uint* visIndices,
             const  uint  visCount,
    __global uint* info,
    __global float* srcCVs,
    __global float* dstCVs,
    __global float* noiseCache,
    __global float* segLens,
    __global float* meshN,
    __global float* meshU,
    uint infoStride,
    uint primitiveCount,
    float presLen
    )
{
    uint gid = get_global_id(0);
    if (gid >= visCount) return;

    gid = visIndices[gid];
    if (gid >= primitiveCount) return;

    const uint flag = info[gid * infoStride + 2];
    if (isPrimCulled(flag))
        return;

    // curve start cv offset
    const uint primitiveOffset = info[gid * infoStride];
    // curve cv count
    const uint numCVs = info[gid * infoStride + 1];

    // bias data to this curve
    srcCVs     += 3 * primitiveOffset;
    dstCVs     += 3 * primitiveOffset;
    noiseCache += 3 * primitiveOffset;
    segLens    += primitiveOffset;
    meshN      += 3 * gid;
    meshU      += 3 * gid;

    float inCrvLen = 0.0f;
    if (isgreater(presLen, 0.001f)) {
        inCrvLen = calCrvLengthFromSegs(segLens, numCVs);
    }

    const float3 N = fast_normalize((float3)(meshN[0], meshN[1], meshN[2]));
    const float3 U = fast_normalize((float3)(meshU[0], meshU[1], meshU[2]));

    // cv normal, binormal related
    float3 norm, bnorm;
    float3 tan0 = N, tan1, nrml = U;
    for (uint i = 0; i<numCVs; i++) {

        // update cv normal/binormal
        {
            if (i < numCVs - 1) {
                tan1 = (float3)(
                    srcCVs[i * 3 + 3] - srcCVs[i * 3],
                    srcCVs[i * 3 + 4] - srcCVs[i * 3 + 1],
                    srcCVs[i * 3 + 5] - srcCVs[i * 3 + 2]);

                if (isequal(fast_length(tan1), 0.0f)) {
                    tan1 = tan0;
                }
            }
            else {
                tan1 = tan0;
            }
            tan1 = fast_normalize(tan1);

            float angle = acos(clamp(dot(tan0, tan1), -1.0f, 1.0f));
            float3 axis = cross(tan0, tan1);
            if (isgreater(fast_length(axis), 0.0f)) {
                nrml = rotateBy(nrml, axis, angle);
                nrml = fast_normalize(nrml);
            }

            norm = nrml;
            bnorm = cross(nrml, tan1);
            tan0 = tan1;
        }

        if (i > 0) {
            float3 offset = (float3)(noiseCache[i * 3], noiseCache[i * 3 + 1], noiseCache[i * 3 + 2]);
            float3 tan3 = cross(bnorm, norm);
            float3 duvn = norm * offset.x + bnorm * offset.y + tan3 * offset.z;

            dstCVs[i * 3]     = srcCVs[i * 3] + duvn.x;
            dstCVs[i * 3 + 1] = srcCVs[i * 3 + 1] + duvn.y;
            dstCVs[i * 3 + 2] = srcCVs[i * 3 + 2] + duvn.z;
        }
    }

    // Fill root point
    vstore3(vload3(0, srcCVs), 0, dstCVs);

    // blend the new and origin length
    if (isgreater(presLen, 0.001f)) {
        float newCrvLen = calCrvLengthFromCVs(dstCVs, numCVs);
        blendLength(dstCVs, numCVs, inCrvLen*presLen + newCrvLen*(1.0f - presLen), newCrvLen);
    }
}