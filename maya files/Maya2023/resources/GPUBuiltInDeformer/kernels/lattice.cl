#if __OPENCL_VERSION__ <= CL_VERSION_1_1

#if defined(cl_khr_fp64)
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#elif defined(cl_amd_fp64)
    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif

#endif

#define LAT_DEFORM_NOT     0
#define LAT_DEFORM_FALLOFF 1
#define LAT_DEFORM_FULL    2

#define LAT_LIMIT_INSIDE   0
#define LAT_LIMIT_ALL      1
#define LAT_LIMIT_FALLOFF  2

//------------------------------------------------------------------------------
float3 mtxMul( float16 matrix , float3 point );
int gpu_checkCrd(double3 iCrd, uint iLimitMode, double iTolerance, double iFalloffDistance);
double gpu_localizeLattice(double iVal, int* iOffset, int iDivSeg, int iLocalDivSeg);
void gpu_fillPowerTable(double* iPowerTable, __global const unsigned int* iBinomials, const unsigned int iBinomialIndex, double iLocalV, int iNumSlices);
double gpu_calcFalloffStrength(double3 iCrd, double iTolerance, double iOneOverFalloffDistance);

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
void gpu_fillPowerTable(double* iPowerTable,
                        __global const unsigned int* iBinomials,
                        const unsigned int iBinomialIndex,
                        double iLocalV,
                        int iNumSlices)
{
    int ii;
    double pow_i;

    // Load the power tables that will be used in the inner loops
    //
    for ( ii = 0, pow_i = 1.0; ii < iNumSlices; ++ii, pow_i *= iLocalV )
        iPowerTable[ii] = iBinomials[iBinomialIndex+ii] * pow_i;

    for ( ii = iNumSlices-1, pow_i = 1.0; ii >= 0; --ii, pow_i *= ( 1.0 - iLocalV ) )
        iPowerTable[ii] *= pow_i;
}

//------------------------------------------------------------------------------
double gpu_localizeLattice(double iVal,
                           int* iOffset,
                           int iDivSeg,
                           int iLocalDivSeg)
{

    int closest_div = (int)(iVal*iDivSeg);
    int tStart = closest_div - (iLocalDivSeg/2);

    // clamp between 0 and iDivSeg-iLocalDivSeg
    if (tStart < 0) {
        tStart = 0;
    } else if (tStart > iDivSeg-iLocalDivSeg) {
        tStart = iDivSeg-iLocalDivSeg;
    }

    int tEnd = tStart + iLocalDivSeg;

    *iOffset = tStart;
    return (iDivSeg*iVal-tStart)/(tEnd-tStart);
}

//------------------------------------------------------------------------------
int gpu_checkCrd(double3 iCrd,
                 uint iLimitMode,
                 double iTolerance,
                 double iFalloffDistance)
{
    if (iLimitMode == LAT_LIMIT_ALL)
        return LAT_DEFORM_FULL; // we do not care whether we are inside or outside

    if (iCrd.x < -iTolerance || iCrd.x > iTolerance + 1.0 ||
        iCrd.y < -iTolerance || iCrd.y > iTolerance + 1.0 ||
        iCrd.z < -iTolerance || iCrd.z > iTolerance + 1.0) {

        // we are outside of the box, so check if we are int he falloff zone

        if (iLimitMode == LAT_LIMIT_FALLOFF) {
            if(iCrd.x < -iFalloffDistance || iCrd.x > iFalloffDistance + 1.0 ||
               iCrd.y < -iFalloffDistance || iCrd.y > iFalloffDistance + 1.0 ||
               iCrd.z < -iFalloffDistance || iCrd.z > iFalloffDistance + 1.0) {
                return LAT_DEFORM_NOT; // outside falloff zone
            } else {
                return LAT_DEFORM_FALLOFF; // inside falloff zone
            }
        } else {
            return LAT_DEFORM_NOT; // outside of box, do not care about falloff
        }
    } else {
        // we are inside the box
        return LAT_DEFORM_FULL;
    }
}

//------------------------------------------------------------------------------
double gpu_calcFalloffStrength(double3 iCrd,
                               double  iTolerance,
                               double  iOneOverFalloffDistance)
{
    double falloffStrength = 1.0;
    
    if ( iCrd.x < -iTolerance ) {
        falloffStrength = ( 1.0 + ( iCrd.x * iOneOverFalloffDistance ) );
    } else if ( iCrd.x > iTolerance + 1.0 ) {
        falloffStrength = ( 1.0 - ( iCrd.x - 1.0 ) * iOneOverFalloffDistance );
    }

    if ( iCrd.y < -iTolerance ) {
        falloffStrength *= ( 1.0 + ( iCrd.y * iOneOverFalloffDistance ) );
    } else if ( iCrd.y > iTolerance + 1.0 ) {
        falloffStrength *= ( 1.0 - ( iCrd.y - 1.0 ) * iOneOverFalloffDistance );
    }

    if ( iCrd.z < -iTolerance ) {
        falloffStrength *= ( 1.0 + ( iCrd.z * iOneOverFalloffDistance ) );
    } else if ( iCrd.z > iTolerance + 1.0 ) {
        falloffStrength *= ( 1.0 - ( iCrd.z - 1.0 ) * iOneOverFalloffDistance );
    }

    return falloffStrength;
}

//------------------------------------------------------------------------------
__kernel void gpu_calcSTUKernel(
    __global const float*    iPos,          // arg 0
    __global double*         iCrds,         // arg 1
    __global const float16 * iGeomToWorld,  // arg 2
    const float16            iWorldToFfd,   // arg 3
    const double3            iCorner,       // arg 4
    const double3            iCross_x,      // arg 5
    const double3            iCross_y,      // arg 6
    const double3            iCross_z,      // arg 7
    const double3            iDivisor,      // arg 8 
    const uint               iAffectCount)  // arg 9
{
    // Determine the id of the affected vertex and bail if it's invalid
    const unsigned int aid = get_global_id(0);
    if ( aid >= iAffectCount ) return;

    // Project the vertex from world space to ffd space
    const float3 initialPos = vload3(aid, iPos);
    float3 tmp = mtxMul( *iGeomToWorld, initialPos );
    tmp = mtxMul(iWorldToFfd, tmp);

    // Compute the local position to tmp in local coordinates
    double3 p = (double3)(tmp.x, tmp.y, tmp.z) - iCorner;
    double3 crd = (double3)(
        dot(iCross_x, p) / iDivisor.x,
        dot(iCross_y, p) / iDivisor.y,
        dot(iCross_z, p) / iDivisor.z);

    // iCrds[aid] = crd
    vstore3(crd, aid, iCrds);
}

//------------------------------------------------------------------------------
__kernel void gpu_deformVertKernel(
    __global float*              iPos,                    // arg 0
    __global const double*       iLatticePos,             // arg 1
    __global const double*       iCrds,                   // arg 2
    __global const float16*      iWorldToGeom,            // arg 3
    const float16                iFfdToWorld,             // arg 4
    const float                  iEnvelope,               // arg 5
    const uint                   iLimitMode,              // arg 6
    const double                 iOutsideFalloffDistance, // arg 7
    const double                 iTolerance,              // arg 8
    const float                  iResolution,             // arg 9
    const uchar                  iLocal,                  // arg 10
    const uint3                  iLatticeDivisions,       // arg 11
    const uint3                  iLocalDivisions,         // arg 12
    __global const unsigned int* iBinomialsIndexer,       // arg 13
    __global const unsigned int* iBinomials,              // arg 14
    const uint                   iAffectCount)            // arg 15
{
    const unsigned int aid = get_global_id(0);
    if (aid >= iAffectCount) return;

    double3 initialCrd = vload3(aid, iCrds);

    int deformMode = gpu_checkCrd(initialCrd, iLimitMode, iTolerance, iOutsideFalloffDistance);

    if (deformMode == LAT_DEFORM_NOT) {
        return;
    }

    int offsetS = 0;
    int offsetT = 0;
    int offsetU = 0;
    double3 crd = initialCrd;

    if (iLocal) {
        crd.x = gpu_localizeLattice(initialCrd.x, &offsetS, iLatticeDivisions.s0-1, iLocalDivisions.s0-1);
        crd.y = gpu_localizeLattice(initialCrd.y, &offsetT, iLatticeDivisions.s1-1, iLocalDivisions.s1-1);
        crd.z = gpu_localizeLattice(initialCrd.z, &offsetU, iLatticeDivisions.s2-1, iLocalDivisions.s2-1);
    }

    int numDivS = iLocalDivisions.s0;
    int numDivT = iLocalDivisions.s1;
    int numDivU = iLocalDivisions.s2;

    double power_s[32];
    double power_t[32];
    double power_u[32];

    gpu_fillPowerTable(&power_s[0], iBinomials, iBinomialsIndexer[numDivS], crd.x, numDivS);
    gpu_fillPowerTable(&power_t[0], iBinomials, iBinomialsIndexer[numDivT], crd.y, numDivT);
    gpu_fillPowerTable(&power_u[0], iBinomials, iBinomialsIndexer[numDivU], crd.z, numDivU);

    // Transform the point by the deformed lattice using a tri-
    // variate Bernstein polynomial (see the Sederberg/Parry paper
    // for details).

    double3 sumSTU = (double3)(0.0, 0.0, 0.0);
    double3 sumST;
    double3 sumS;

    bool insideOnly = (iLimitMode == (uint)LAT_LIMIT_INSIDE);

    for (int ii = 0; ii < numDivU; ++ii ) {
        if (insideOnly && power_u[ii] < iResolution)
            continue;

        sumST = (double3)(0.0, 0.0, 0.0);

        for (int jj = 0; jj < numDivT; ++jj ) {
            double factor = power_u[ii]*power_t[jj];
            if (insideOnly && factor < iResolution)
                continue;

            sumS = (double3)(0.0, 0.0, 0.0);

            for (int kk = 0; kk < numDivS; ++kk ) {
                int index = iLatticeDivisions.s0*(iLatticeDivisions.s1*(ii+offsetU)+(jj+offsetT))+(kk+offsetS);
                const double3 latpt = vload3(index, iLatticePos);
                sumS += power_s[kk] * latpt;
            }
            sumST += power_t[jj] * sumS;
         }

        sumSTU += power_u[ii] * sumST;
    }

    // bring back to geometry space....
    float3 pt = mtxMul( iFfdToWorld, (float3)(sumSTU.x, sumSTU.y, sumSTU.z) );
    pt = mtxMul( *iWorldToGeom, pt);

    float envelope = (float)iEnvelope;
    if (deformMode == LAT_DEFORM_FALLOFF)
        envelope *= gpu_calcFalloffStrength(initialCrd, iTolerance, 1.0/iOutsideFalloffDistance);

    const float3 initialPos = vload3(aid, iPos);
    float3 delta = pt - initialPos;
    vstore3(initialPos+(envelope*delta), aid, iPos);
}

