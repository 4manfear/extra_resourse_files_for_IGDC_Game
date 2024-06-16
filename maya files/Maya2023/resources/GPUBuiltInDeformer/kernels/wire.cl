#if __OPENCL_VERSION__ <= CL_VERSION_1_1

#if defined(cl_khr_fp64)
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#elif defined(cl_amd_fp64)
    #pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif

#endif

//------------------------------------------------------------------------------
// Helper functions
// OSX seems to be using very strict compiler setting which demand the function
// prototype be defined before the function is implemented.  It seems like we
// only need the function prototype for helper methods, not kernels that are
// used directly.
//------------------------------------------------------------------------------

float3 mtxMul( float16 matrix , float3 point );
float4 quaternion_conjugate( const float4 quaternion );
float4 quaternion_multiply( const float4 q1 , const float4 q2 );
float3 quaternion_transform( const float4 q , const float3 p );
float4 quaternion_angle_axis(float angle, const float3 axis);
float4 quaternion_align_axis(const float3 a, const float3 b, float angleFactor);

//------------------------------------------------------------------------------
float4 calcSplineProject(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        const float3 iPos,
        __global const float* iCached_points);

//------------------------------------------------------------------------------
float3 calcSplinePoint(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        float iU
        );

//------------------------------------------------------------------------------
float3 calcSplinePointAndDer(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        float iU,
        float3* iDer
        );

//------------------------------------------------------------------------------
float3 calcSplinePointAndPrime(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        float iU,
        float3* iDer
        );

//------------------------------------------------------------------------------
int calcDisplacementWeight(
        const float3 iDisp,
        const float iBindW,
        const float iLocal,
        const float iTension,
        int* iNodisp,
        double* iDispWeight);

//------------------------------------------------------------------------------
float calcTwist(
    const unsigned int iDriverIdx,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    float iU);


//------------------------------------------------------------------------------
void calcDropoff(
    const unsigned int iDriverIdx,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    float iU,
    float* iEnvelope,
    float* iWeight);

//------------------------------------------------------------------------------
float3 calcRotation(
    const float3 iOrgTang,
    const float3 iCurTang,
    const float iTwist,
    const float iBindW,
    const float iRotation,
    const float3 iPos);

//------------------------------------------------------------------------------
unsigned int NURBS_findSpan( __global const float* iKnots,
                             unsigned int iNbKnots,
                             unsigned int iPower,
                             const float iU);

//------------------------------------------------------------------------------
void NURBS_basisFunction(__global const float* knots,
                         unsigned int power,
                         unsigned int span,
                         const float u,
                         float* N );


//------------------------------------------------------------------------------
void NURBS_derivativeBasisFunctions(size_t P, size_t span,  __global const float* iKnots, float u, size_t n, float derivatived[8][8]);

//------------------------------------------------------------------------------
void NURBS_evaluateDerivative(__global const float* iControlPoints, 
                              __global const float* iKnots, 
                              unsigned int iPower, 
                              unsigned int iNbKnots,
                              float iU, size_t kth_derivative, float3 ders[]);

//------------------------------------------------------------------------------
bool NURBS_project_guess(
             __global const float* iControlPoints, 
             __global const float* iKnots, 
             unsigned int iPower,
             unsigned int iNbKnots,
             bool iIsClosed,
             float3 p, 
             float initialGuess, 
             float4 *convergedResult) ;

//------------------------------------------------------------------------------
float4 NURBS_project(
             __global const float* iControlPoints, 
             __global const float* iKnots, 
             unsigned int iPower,
             unsigned int iNbKnots,
             bool iIsClosed,
             const float3  iP, 
             __global const float* iCached_points,
             const size_t iNbCachePoints) ;

//------------------------------------------------------------------------------
float3 NURBS_evaluate(__global const float* iControlPoints, 
                      __global const float* iKnots, 
                      unsigned int iPower, 
                      unsigned int iNbKnots,
                      float iU); 

//------------------------------------------------------------------------------
void NURBS_sampleSpans(__global const float* iControlPoints, 
                  __global const float* iKnots, 
                  unsigned int iPower, 
                  unsigned int iNbKnots,
                  size_t numStep,
                  __global float* iSpanCachePtr);

//------------------------------------------------------------------------------
//
//
//
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
float4 quaternion_conjugate( const float4 quaternion )
{
    return (float4)( -quaternion.xyz , quaternion.w );
}

//------------------------------------------------------------------------------
float4 quaternion_multiply( const float4 q1 , const float4 q2 )
{
    return quaternion_conjugate(
        q1.zxyw*q2.yzxw - q1.ywzx*q2.zywx - q1.wyxz*q2.xwyz - q1.xzwy*q2.wxzy
        );
}

//------------------------------------------------------------------------------
float3 quaternion_transform( const float4 q , const float3 p )
{
    const float3 v = p + p;
    const float3 qv = q.xyz * v;
    const float3 result = q.w*(cross(q.xyz, v) + q.w*v) + q.xyz*(qv.xyz + qv.yzx + qv.zxy) - p;
    return result;
}

//------------------------------------------------------------------------------
float4 quaternion_angle_axis(float angle, const float3 axis)
{
    const float lenSq = axis.x*axis.x +
                        axis.y*axis.y +
                        axis.z*axis.z;

    if (lenSq <= 1e-6f) { // Axis too small.
        return (float4)(0.0f, 0.0f, 0.0f, 1.0f);
    } else {
        const float theta = angle * 0.5f;
        const float commonFactor = sin(theta)/sqrt(lenSq);
        return (float4)(commonFactor * axis, cos(theta));
    }
}

//------------------------------------------------------------------------------
// Create a quaternion that will rotate vector a into vector b
// This assumes a and b are normalized
float4 quaternion_align_axis(const float3 a, const float3 b, float angleFactor)
{
    float3 rotAxis = cross(a, b);
    const float sz = dot(rotAxis,rotAxis); // squareLen
    const float d = max(min(dot(a, b), 1.0f), -1.0f);
    if (sz <  1e-6f) {
        if (d > 0.0f) { // no rotation...
            return (float4)(0.0f, 0.0f, 0.0f, 1.0f);
        } else { //get an axis orthogonal to iAxis
            rotAxis = cross(a, (float3)(a.y, a.z, a.x));
        }
    }

    return quaternion_angle_axis(acos(d)*angleFactor,  rotAxis);
}

//------------------------------------------------------------------------------
unsigned int NURBS_findSpan( __global const float* iKnots,
                             unsigned int iNbKnots,
                             unsigned int iPower,
                             const float iU)
{
	unsigned int nbSpan = iNbKnots - iPower - 1;
    unsigned int i;
	for(i = 1; i < nbSpan; ++i)
	{
		if(iKnots[i] > iU) break;
	}
	return max(iPower, i - 1) ;
}

//------------------------------------------------------------------------------
void NURBS_basisFunction(__global const float* iKnots, unsigned int iPower, unsigned int iSpan, const float iU, float* iN )
{
    iN[0] = 1.0;
	float2 lr[8]; //max_p == 7
	
	for (size_t j = 1; j <= iPower; ++j) {
		lr[j].x = iU - iKnots[iSpan + 1 - j];
		lr[j].y = iKnots[iSpan + j] - iU;
		float saved = 0.0;
		for (size_t r = 0; r < j; r++) {
			float temp = iN[r] / (lr[r + 1].y + lr[j - r].x);
			iN[r] = saved + lr[r + 1].y * temp;
			saved = lr[j - r].x * temp;
		}
		iN[j] = saved;
	}
}


//use newton-raphson method to find proper root
//return true and set result in convergedResult if the algorithm converged, otherwise it return false and do not set convergedResult
bool NURBS_project_guess(
             __global const float* iControlPoints, 
             __global const float* iKnots, 
             unsigned int iPower,
             unsigned int iNbKnots,
             bool iIsClosed,
             float3 p, 
             float initialGuess, 
             float4 *convergedResult) 
{
    
    float3 ders[3]; // I need C(u), C'(u), C''(u), in some case C' or C'' may be 0 if mPower is smaller than 2
    float u = initialGuess;
    const size_t max_iterations = 15;
    const float firstKnot = iKnots[iPower];
    const float lastKnot = iKnots[iNbKnots - iPower - 1];
    
    for (size_t i = 0; i < max_iterations; ++i) {
        NURBS_evaluateDerivative(iControlPoints, iKnots, iPower, iNbKnots, u, 2, ders);
        float3 distanceVect = ders[0] - p;
        //newton raphson equation for next estimate see Nurbs Book p 230 eq. 6.3
        float next_u = u - dot(ders[1], distanceVect) / (dot(ders[2], distanceVect) + dot(ders[1],ders[1]));

        if (next_u < firstKnot) {
            if (iIsClosed) {
	            next_u = lastKnot + next_u - firstKnot; //loop around
            }
            else {
                next_u = firstKnot;
            }
        }
        if (next_u  > lastKnot) {
            if (iIsClosed) {
                next_u = firstKnot + next_u - lastKnot; //loop around
            }
            else {
                next_u = lastKnot; //clamp if not closed
            }
        }

        float variance = fabs(next_u - u);
        u = next_u;

        if (variance < 1e-5f) {
            *convergedResult = (float4)( ders[0], u );
            return true;
        }
    }
    return false;
}

//project p onto bspline given a pre sample array of tuple (Point, u) to speed up the search for initial guess
//the initial guess is needed to get a good approximation
//return point(x,y,z) and u(w) in a float4
float4 NURBS_project(
             __global const float* iControlPoints, 
             __global const float* iKnots, 
             unsigned int iPower,
             unsigned int iNbKnots,
			 bool iIsClosed,
             const float3  iP, 
             __global const float* iCached_points,
             const size_t iNbCachePoints) 
{
    float4 spanCache = vload4(0, iCached_points);

    float3 closest = spanCache.xyz;
    float closestu = spanCache.w;
    float3 vectp = iP - closest;
    float closestmag2 = dot(vectp, vectp);
    for (size_t i = 1; i < iNbCachePoints; ++i){
        spanCache = vload4(i, iCached_points);
        vectp = iP - spanCache.xyz;
        float currentmag2 = dot(vectp, vectp);
        if (currentmag2 < closestmag2) {
            closest = spanCache.xyz;
            closestu = spanCache.w;
            closestmag2 = currentmag2;
        }
    }
    float4 convergedResult;
    bool converged = NURBS_project_guess(iControlPoints, iKnots, iPower, iNbKnots, iIsClosed, iP, closestu, &convergedResult);
    float3 delta =  iP - convergedResult.xyz;
    if (converged && dot(delta, delta) <= closestmag2)
    {
        return convergedResult;
    }
    return (float4)(closest, closestu);
}


//------------------------------------------------------------------------------
float3 NURBS_evaluate(__global const float* iControlPoints,
                      __global const float* iKnots, 
                      unsigned int iPower, 
                      unsigned int iNbKnots,
                      float iU) 
{
 	unsigned int span = NURBS_findSpan(iKnots, iNbKnots, iPower, iU);
	float N[8]; //MAXP = 7
	NURBS_basisFunction(iKnots, iPower, span, iU, N);
	float3 pt = (float3)(0.0f, 0.0f, 0.0f);
   	for (size_t i = 0; i <= iPower; ++i) {
        float3 cp = vload3(span - iPower + i, iControlPoints);
        pt = pt + (cp * N[i]);
	}   
	return pt;
}


//------------------------------------------------------------------------------
void NURBS_sampleSpans(__global const float* iControlPoints, 
                  __global const float* iKnots, 
                  unsigned int iPower, 
                  unsigned int iNbKnots,
                  size_t numStep,
                  __global float* iSpanCachePtr)
{
    size_t spancacheidx = 0;
    size_t end =  iNbKnots - iPower - 1;
    for (size_t i = iPower; i < end; ++i) {
        float deltau = iKnots[i + 1] - iKnots[i];
        float stepu = deltau / numStep;
        for (size_t j = 0; j < numStep; ++j) {
            float currentu = iKnots[i] + stepu * j;
            float3 current = NURBS_evaluate(iControlPoints, iKnots, iPower, iNbKnots, currentu);
            vstore4((float4)(current, currentu), spancacheidx++, iSpanCachePtr);
        }
    }
    float currentu = iKnots[end];
    float3 current = NURBS_evaluate(iControlPoints, iKnots, iPower, iNbKnots, currentu);
    vstore4((float4)(current, currentu), spancacheidx++, iSpanCachePtr);
    
}


//------------------------------------------------------------------------------
void NURBS_derivativeBasisFunctions(size_t P, size_t span,  __global const float* iKnots, float u, size_t n, float derivatived[8][8])
{
	float ndu[8][8];       //MAXP = 7
	float left[8];     //MAXP = 7
	float right[8];       //MAXP = 7
	ndu[0][0] = 1.0;
	for (size_t j = 1; j <= P; j++) {
		left[j] = u - iKnots[span + 1 - j];
		right[j] = iKnots[span + j] - u;
		float saved = 0.0;
		for (size_t r = 0; r < j; r++) {
			ndu[j][r] = right[r + 1] + left[j - r];
			float temp = ndu[r][j - 1] / ndu[j][r];

			ndu[r][j] = saved + right[r + 1] * temp;
			saved = left[j - r] * temp;
		}
		ndu[j][j] = saved;
	}

	for (size_t j = 0; j <= P; j++) {
		derivatived[0][j] = ndu[j][P];
	}

	for (size_t r = 0; r <= P; ++r) {
		size_t s1 = 0;
		size_t s2 = 1;
		float a[2][8]; //MAXP = 7
		a[0][0] = 1.0;
		//loop to compute kth derivative
		for (size_t k = 1; k <= n; k++) {
			float d = 0.0;
			size_t rk = r - k;
			size_t pk = P - k;
			if (r >= k) {
				a[s2][0] = a[s1][0] / ndu[pk + 1][rk];
				d = a[s2][0] * ndu[rk][pk];
			}
			size_t j1 = (r >= k - 1) ? 1 : k - r;
			size_t j2 = (r <= pk + 1) ? k - 1 : P - r;
			for (size_t j = j1; j <= j2; ++j) {
				a[s2][j] = (a[s1][j] - a[s1][j - 1]) / ndu[pk + 1][rk + j];
				d += a[s2][j] * ndu[rk + j][pk];
			}
			if (r <= pk) {
				a[s2][k] = -a[s1][k - 1] / ndu[pk + 1][r];
				d += a[s2][k] * ndu[r][pk];
			}
			derivatived[k][r] = d;
			size_t t = s1;
			s1 = s2;
			s2 = t;
		}
	}

	float r = (float)(P);
	for (size_t k = 1; k <= n; ++k) {
		for (size_t j = 0; j <= P; ++j) {
			derivatived[k][j] *= r;
		}
		r *= (float)(P - k);
	}
}


//------------------------------------------------------------------------------
//Use this function if you want to evaluate few derivate per spline, will be faster than creating bspline derivate
//if you want large derivate value for a large numer of u than it is better to create the derivate bspline
void NURBS_evaluateDerivative(__global const float* iControlPoints, 
                              __global const float* iKnots, 
                              unsigned int iPower, 
                              unsigned int iNbKnots,
                              float iU, size_t kth_derivative, float3 ders[]) {

	for (size_t i = iPower + 1; i <= kth_derivative; ++i) {
		ders[i] = (float3)(0.0f,0.0f,0.0f);
	}

	size_t span = NURBS_findSpan(iKnots, iNbKnots, iPower, iU); 

	float nders[8][8];    //MAXP = 7
	NURBS_derivativeBasisFunctions(iPower, span, iKnots, iU, kth_derivative, nders);

	for (size_t k = 0; k <= kth_derivative; ++k) {
		float3 cp = (float3)(0.0f,0.0f,0.0f);
		for (size_t j = 0; j <= iPower; ++j) {
            float3 cpt = vload3(span - iPower + j, iControlPoints);
			cp += cpt * nders[k][j];
		}
		ders[k] = cp;
	}
}


//------------------------------------------------------------------------------
float4 calcSplineProject(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        const float3 iPos,
        __global const float* iCached_points)
{
    const unsigned int ps = iPointIndexer[iDriverIdx];
    const unsigned int ks = iKnotsIndexer[iDriverIdx];
    const unsigned int ke = iKnotsIndexer[iDriverIdx+1];
    const unsigned int numKnots = ke-ks;
    const unsigned int numStep = 10;
    const size_t spanCacheIndex = (ks - iKnotsIndexer[0]) * 4 * numStep;          // 10 float4 per knots

    const unsigned int degreeIndex = iDriverIdx * 2;
    const unsigned int degree = iDegree[degreeIndex];
    const bool isClosed = iDegree[degreeIndex +1]  > 0 ? true: false;

    const size_t numSpan = (numKnots - 2 *degree - 1) * numStep + 1; // +1 is for the last considerd knot 
    
    return NURBS_project(iPoints + ps * 3, iKnots + ks, degree , numKnots, isClosed, iPos, iCached_points + spanCacheIndex, numSpan); 
}

//------------------------------------------------------------------------------
float3 calcSplinePoint(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        float iU)
{
    const unsigned int ps = iPointIndexer[iDriverIdx];
    const unsigned int ks = iKnotsIndexer[iDriverIdx];
    const unsigned int ke = iKnotsIndexer[iDriverIdx+1];
    const unsigned int numKnots = ke-ks;

    const unsigned int degreeIndex = iDriverIdx * 2;
    const unsigned int degree = iDegree[degreeIndex];

    return NURBS_evaluate(iPoints + ps * 3, iKnots + ks, degree, numKnots, iU);
}

//------------------------------------------------------------------------------
float3 calcSplinePointAndPrime(
        const unsigned int iDriverIdx,
        __global const unsigned int* iPointIndexer,
        __global const unsigned int* iKnotsIndexer,
        __global const float* iPoints,
        __global const float* iKnots,
        __global const unsigned int* iDegree,
        float iU,
        float3* iDer
        )
{
    const unsigned int ps = iPointIndexer[iDriverIdx];
    //const unsigned int pe = iPointIndexer[iDriverIdx+1];

    const unsigned int ks = iKnotsIndexer[iDriverIdx];
    const unsigned int ke = iKnotsIndexer[iDriverIdx+1];
    
    //const unsigned int numPoints = pe-ps;
    const unsigned int numKnots = ke-ks;
	
	const unsigned int degreeIndex = iDriverIdx * 2;
	const unsigned int degree = iDegree[degreeIndex];

    float3 ders[2];
    NURBS_evaluateDerivative(iPoints + ps * 3, iKnots + ks, degree, numKnots, iU, 1, ders);
    (*iDer) = ders[1];
    return ders[0];
}


//------------------------------------------------------------------------------
int calcDisplacementWeight(
        const float3 iDisp,
        const float iBindW,
        const float iLocal,
        const float iTension,
        int* iNodisp,
        double* iDispWeight)
{
    *iDispWeight = 0;
    double cwt = iDisp.x*iDisp.x + iDisp.y*iDisp.y + iDisp.z*iDisp.z;
    if (fabs(cwt) < 1e-6) { // TODO: what is the right tolerance?
        if (iTension < 0.0f)
            *iNodisp = 1;
        return 0;
    }

    if (fabs(iTension - 1.0f) > 0.001f) {
        cwt = pow(cwt, (double)iTension);
    }

    *iDispWeight = iBindW*iBindW*iLocal + (1.0f - iLocal)*cwt;
    return 1;
}

//------------------------------------------------------------------------------
float calcTwist(
    const unsigned int iDriverIdx,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    float iU)
{
    // data = { u0, u1, ..., un-1,
    //          p0, p1, ..., pn-1,
    //          e0, e1, ..., en-1,
    //          t0, t1, ..., tn-1 }

    const unsigned int s = iLocatorIndexer[iDriverIdx];
    const unsigned int e = iLocatorIndexer[iDriverIdx+1];
    if (e == s)
        return 0.0f;

    const unsigned int n = (e-s)/4;  // storing 4 parameters
    const unsigned int twistOffset = n*3;

    if (iU <= iLocatorData[0])
        return iLocatorData[twistOffset];
    else if (iU >= iLocatorData[n-1])
        return iLocatorData[twistOffset+n-1];

    size_t j = 0;
    while (j < n-1 && iU >= iLocatorData[j+1])
        j++;

    // it is now between j and j+1
    const float r = (iU - iLocatorData[j])/(iLocatorData[j+1] - iLocatorData[j]);
    const float interp = (r-1)*(r-1)*(r+1)*(r+1);
    return iLocatorData[j+twistOffset]*interp + iLocatorData[j+1+twistOffset]*(1.0f-interp);
}

//------------------------------------------------------------------------------
void calcDropoff(
    const unsigned int iDriverIdx,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    float iU,
    float* iEnvelope,
    float* iWeight)
{
    // data = { u0, u1, ..., un-1,
    //          w0, w1, ..., wn-1,
    //          e0, e1, ..., en-1,
    //          t0, t1, ..., tn-1 }

    const unsigned int s = iLocatorIndexer[iDriverIdx];
    const unsigned int e = iLocatorIndexer[iDriverIdx+1];
    if (e == s) {
        *iEnvelope = 1.0f;
        *iWeight = 1.0f;
        return;
    }

    const unsigned int n = (e-s)/4;  // storing 4 parameters
    const unsigned int wtOffset = n*1;
    const unsigned int enOffset = n*2;

    if (iU <= iLocatorData[0]) {
        *iEnvelope = iLocatorData[enOffset];
        *iWeight = iLocatorData[wtOffset];
        return;
    } else if (iU >= iLocatorData[n-1]) {
        *iEnvelope = iLocatorData[enOffset+n-1];
        *iWeight = iLocatorData[wtOffset+n-1];
        return;
    }

    size_t j = 0;
    while (j < n-1 && iU >= iLocatorData[j+1])
        j++;

    // it is now between j and j+1
    const float r = (iU - iLocatorData[j])/(iLocatorData[j+1] - iLocatorData[j]);
    const float interp = (r-1)*(r-1)*(r+1)*(r+1);

    *iEnvelope = iLocatorData[j+enOffset]*interp + iLocatorData[j+1+enOffset]*(1.0f-interp);
    *iWeight = iLocatorData[j+wtOffset]*interp + iLocatorData[j+1+wtOffset]*(1.0f-interp);
}

//------------------------------------------------------------------------------
float3 calcRotation(
    const float3 iOrgTang,
    const float3 iCurTang,
    const float iTwist,
    const float iBindW,
    const float iRotation,
    const float3 iPos)
{
    const float4 q1 = quaternion_angle_axis(iTwist*iBindW, iOrgTang);
    const float4 qq = quaternion_align_axis(iOrgTang, iCurTang, iRotation*iBindW);
    const float4 qf = quaternion_multiply(q1, qq);

    return quaternion_transform( qf, iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_wireFullKernel(
    __global float* iPos,
    const float iEnvelope,
    const float iConvolve,
    const float iTension,
    const float iLocal,
    const float iRotation,
    __global const float16* iGeomMat,
    __global const float16* iGeomMatInv,
    const unsigned int iNumDrivers,
    __global const float* iBindU,
    __global const float* iBindW,
    __global const float* iDriverScales,
    __global const unsigned int* iCurPointsIndexer,
    __global const unsigned int* iCurKnotsIndexer,
    __global const float* iCurPoints,
    __global const float* iCurKnots,
    __global const unsigned int* iOrgPointsIndexer,
    __global const unsigned int* iOrgKnotsIndexer,
    __global const float* iOrgPoints,
    __global const float* iOrgKnots,
    __global const unsigned int* iDegree,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    __global const float* iEnvelopeWeights,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if (aid >= iAffectCount) return;

/*
    if (aid == 0) {
        printf("Drivers = %d\n", iNumDrivers);
        for (unsigned int i = 0; i < iNumDrivers; ++i) {
            printf("Driver %d\n", i);
            printf("  sc %2.3f\n", iDriverScales[i]);
            printf("  op [%d, %d]\n", iOrgPointsIndexer[i], iOrgPointsIndexer[i+1]);
            printf("  ok [%d, %d]\n", iOrgKnotsIndexer[i], iOrgKnotsIndexer[i+1]);
            printf("  cp [%d, %d]\n", iCurPointsIndexer[i], iCurPointsIndexer[i+1]);
            printf("  ck [%d, %d]\n", iCurKnotsIndexer[i], iCurKnotsIndexer[i+1]);
            printf("  ld [%d, %d]\n", iLocatorIndexer[i], iLocatorIndexer[i+1]);
        }
    }
*/

    const bool useRotation = (fabs(iRotation) > 1e-6f);

    float3 pos = vload3(aid, iPos);
    double totDispWeight = 0.0;
    float3 totDisp = (float3)(0.0f, 0.0f, 0.0f);
    float3 totStable = (float3)(0.0f, 0.0f, 0.0f);

    pos = mtxMul( *iGeomMat, pos );

    int nodisp = 0;
    for (unsigned int driverIdx = 0; driverIdx < iNumDrivers; ++driverIdx) {
        // Add the influence of a specific spline to the point
        const unsigned int bid = iAffectCount*driverIdx + aid;

        const float bind_w = iBindW[bid];
        const float bind_u = iBindU[bid];
        //printf("gpu full bid: %d u: %f w: %f\n", bid, bind_u, bind_w);
        if (fabs(bind_w) >= 1e-6f) {

            const float scl = 1.0f + (iDriverScales[driverIdx] - 1.0f)*bind_w;

            float3 orgPos, curPos, tmpPos;
            if (useRotation) {
                float3 orgPrimePos, curPrimePos;
                orgPos = calcSplinePointAndPrime(driverIdx, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree, bind_u, &orgPrimePos);
                curPos = calcSplinePointAndPrime(driverIdx, iCurPointsIndexer, iCurKnotsIndexer, iCurPoints, iCurKnots, iDegree, bind_u, &curPrimePos);
                tmpPos = (pos - orgPos)*scl;
                // Rotations...
                const float tw = calcTwist(driverIdx, iLocatorIndexer, iLocatorData, bind_u);
                tmpPos = calcRotation(normalize(orgPrimePos), normalize(curPrimePos), tw, bind_w, iRotation, tmpPos);

            } else {
                orgPos = calcSplinePoint(driverIdx, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree, bind_u);
                curPos = calcSplinePoint(driverIdx, iCurPointsIndexer, iCurKnotsIndexer, iCurPoints, iCurKnots, iDegree, bind_u);
                tmpPos = (pos - orgPos)*scl;
            }

            // Displacement...
            const float3 disp = orgPos + tmpPos - pos + (bind_w * (curPos - orgPos));

            // Displacement weight...
            double dispWeight = 0.0;
            if (calcDisplacementWeight(disp, bind_w, iLocal, iTension, &nodisp, &dispWeight)) {
                totDispWeight += dispWeight;
                totDisp += ((float)dispWeight*disp);
                totStable += disp;
            }
        } else {
            if (iTension < 0.0f)
                nodisp = true;
        }
    }

    if (fabs(totDispWeight) < 1e-6 || nodisp) // TODO: what is the right tolerance?
        return;

    float w = 1.0f;
    if (iEnvelopeWeights)
        w = iEnvelopeWeights[aid];

    float dw = w*(1.0f - iConvolve) / (float)totDispWeight;
    pos += iEnvelope * ( (iConvolve*totStable) + (dw*totDisp) );

    pos = mtxMul( *iGeomMatInv, pos );

    vstore3(pos, aid, iPos);
}

//------------------------------------------------------------------------------
__kernel void gpu_wirePartialKernel(
    __global float* iPos,
    const float iEnvelope,
    const float iConvolve,
    const float iTension,
    const float iLocal,
    const float iRotation,
    __global const float16* iGeomMat,
    __global const float16* iGeomMatInv,
    const unsigned int iNumDrivers,
    __global const float* iBindU,
    __global const float* iBindW,
    __global const float* iDriverScales,
    __global const unsigned int* iCurPointsIndexer,
    __global const unsigned int* iCurKnotsIndexer,
    __global const float* iCurPoints,
    __global const float* iCurKnots,
    __global const unsigned int* iOrgPointsIndexer,
    __global const unsigned int* iOrgKnotsIndexer,
    __global const float* iOrgPoints,
    __global const float* iOrgKnots,
    __global const unsigned int* iDegree,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    __global const float* iEnvelopeWeights,
    const uint iAffectCount,
    __global const unsigned int* iDriverBindId,
    __global const unsigned int* iDriverVertUse,
    __global const unsigned int* iDriverIndexer,
    const uint iUseCount)
{
    const unsigned int uid = get_global_id(0);
    if (uid >= iUseCount) return;

/*
    if (uid == 0) {
        printf("Drivers = %d\n", iNumDrivers);
        for (unsigned int i = 0; i < iNumDrivers; ++i) {
            printf("Driver %d\n", i);
            printf("  sc %2.3f\n", iDriverScales[i]);
            printf("  op [%d, %d]\n", iOrgPointsIndexer[i], iOrgPointsIndexer[i+1]);
            printf("  ok [%d, %d]\n", iOrgKnotsIndexer[i], iOrgKnotsIndexer[i+1]);
            printf("  cp [%d, %d]\n", iCurPointsIndexer[i], iCurPointsIndexer[i+1]);
            printf("  ck [%d, %d]\n", iCurKnotsIndexer[i], iCurKnotsIndexer[i+1]);
            printf("  ld [%d, %d]\n", iLocatorIndexer[i], iLocatorIndexer[i+1]);
        }
    }
*/
    const unsigned int aid = iDriverVertUse[uid];

    const unsigned int s = iDriverIndexer[uid];
    const unsigned int e = iDriverIndexer[uid+1];

    const size_t numUsedDrivers = e-s;
    if (numUsedDrivers == 0 ||
        (iTension < 0.0f && numUsedDrivers != iNumDrivers))
        return;

    const bool useRotation = (fabs(iRotation) > 1e-6f);

    float3 pos = vload3(aid, iPos);
    double totDispWeight = 0.0;
    float3 totDisp = (float3)(0.0f, 0.0f, 0.0f);
    float3 totStable = (float3)(0.0f, 0.0f, 0.0f);

    pos = mtxMul( *iGeomMat, pos );

    int nodisp = 0;
    for (unsigned int c = s; c < e; ++c) {
        // Add the influence of a specific spline to the point
        const unsigned int bid = iDriverBindId[c];

        const unsigned int driverIdx = bid/iAffectCount;

        const float bind_w = iBindW[bid];
        const float bind_u = iBindU[bid];

        const float scl = 1.0f + (iDriverScales[driverIdx] - 1.0f)*bind_w;

        float3 orgPos, curPos, tmpPos;
        if (useRotation) {
            float3 orgPrimePos, curPrimePos;
            orgPos = calcSplinePointAndPrime(driverIdx, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree, bind_u, &orgPrimePos);
            curPos = calcSplinePointAndPrime(driverIdx, iCurPointsIndexer, iCurKnotsIndexer, iCurPoints, iCurKnots, iDegree, bind_u, &curPrimePos);
            tmpPos = (pos - orgPos)*scl;
            // Rotations...
            const float tw = calcTwist(driverIdx, iLocatorIndexer, iLocatorData, bind_u);
            tmpPos = calcRotation(normalize(orgPrimePos), normalize(curPrimePos), tw, bind_w, iRotation, tmpPos);

        } else {
            orgPos = calcSplinePoint(driverIdx, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree, bind_u);
            curPos = calcSplinePoint(driverIdx, iCurPointsIndexer, iCurKnotsIndexer, iCurPoints, iCurKnots, iDegree, bind_u);
            tmpPos = (pos - orgPos)*scl;
        }

        // Displacement...
        const float3 disp = orgPos + tmpPos - pos + (bind_w * (curPos - orgPos));

        // Displacement weight...
        double dispWeight = 0.0;
        if (calcDisplacementWeight(disp, bind_w, iLocal, iTension, &nodisp, &dispWeight)) {
            totDispWeight += dispWeight;
            totDisp += ((float)dispWeight*disp);
            totStable += disp;
        }
    }       
          
    if (fabs(totDispWeight) < 1e-6 || nodisp) // TODO: what is the right tolerance?
        return;
          
    float w = 1.0f;
    if (iEnvelopeWeights)
        w = iEnvelopeWeights[aid];

    float dw = w*(1.0f - iConvolve) / (float)totDispWeight;
    pos += iEnvelope * ( (iConvolve*totStable) + (dw*totDisp) );

    pos = mtxMul( *iGeomMatInv, pos );

    vstore3(pos, aid, iPos);
}


//------------------------------------------------------------------------------
__kernel void gpu_wireSpanCacheKernel(
    const unsigned int iNumDrivers,
    __global const unsigned int* iOrgPointsIndexer,
    __global const unsigned int* iOrgKnotsIndexer,
    __global const float* iOrgPoints,
    __global const float* iOrgKnots,
    __global const unsigned int* iDegree,
    __global float* iSpanCache)
{
    __global float* currentSpanCachePtr = iSpanCache;
    for(size_t i = 0; i < iNumDrivers; ++i)
    {
        const unsigned int ps = iOrgPointsIndexer[i];
        const unsigned int ks = iOrgKnotsIndexer[i];
        const unsigned int ke = iOrgKnotsIndexer[i+1];
        const unsigned int numKnots = ke-ks;
        const size_t numStep = 10;              // 10 is arbitraty, but must match everywher spancache is used

		const unsigned int degreeIndex = i * 2;
		const unsigned int degree = iDegree[degreeIndex];

        NURBS_sampleSpans(iOrgPoints + ps * 3, iOrgKnots + ks, degree, numKnots, numStep, currentSpanCachePtr);
        currentSpanCachePtr += numKnots * 4 * numStep; // 4 for 4 float (point & u)
    }
}


//------------------------------------------------------------------------------
__kernel void gpu_wireRebindKernel(
    __global float* iPos,
    __global const float16* iGeomMat,
    const unsigned int iDriverIndex,
    __global float* iBindU,
    __global const unsigned int* iOrgPointsIndexer,
    __global const unsigned int* iOrgKnotsIndexer,
    __global const float* iOrgPoints,
    __global const float* iOrgKnots,
    __global const unsigned int* iDegree,
    const uint iAffectCount,
    __global const float* iSpanCache
    )
{
    const unsigned int aid = get_global_id(0);
    if (aid >= iAffectCount) return;

    const unsigned int offset = iDriverIndex*iAffectCount;

    float3 pos = vload3(aid, iPos);
    pos = mtxMul( *iGeomMat, pos );

    const float4 result = calcSplineProject(iDriverIndex, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree,  pos, iSpanCache);

    //if (aid == 0) {
    //    printf("aid %d, p = %2.2v3hlf, u = %2.3f\n", aid, result.xyz, result.w);
    //}   
    //if(fabs(iBindU[aid+offset] - result.w) > 1e-5f){
    //   printf("diff %d, %f : %f \n", aid, iBindU[aid+offset], result.w);
    //} 

    iBindU[aid+offset] = result.w;
}

//------------------------------------------------------------------------------
__kernel void gpu_wireInfluenceKernel(
    __global float* iPos,
    __global const float16* iGeomMat,
    const unsigned int iDriverIndex,
    const float iDropoffDistance,
    __global const float* iBindU,
    __global float* iBindW,
    __global const unsigned int* iOrgPointsIndexer,
    __global const unsigned int* iOrgKnotsIndexer,
    __global const float* iOrgPoints,
    __global const float* iOrgKnots,
    __global const unsigned int* iDegree,
    __global const unsigned int* iLocatorIndexer,
    __global const float* iLocatorData,
    const uint iAffectCount)
{
    const unsigned int aid = get_global_id(0);
    if (aid >= iAffectCount) return;

    const unsigned int offset = iDriverIndex*iAffectCount;
      
    float3 pos = vload3(aid, iPos);
    pos = mtxMul( *iGeomMat, pos );
   
    const float bind_u = iBindU[aid+offset];
   
  

    const float3 orgPos = calcSplinePoint(iDriverIndex, iOrgPointsIndexer, iOrgKnotsIndexer, iOrgPoints, iOrgKnots, iDegree, bind_u);
     
    const float3 diff = pos - orgPos;

    const float norm = dot(diff, diff); // sqrLen
        
    // get dropoff at param as interpolant
    float envelope = 1.0f;
    float dropoffInterp = 1.0f;
    calcDropoff(iDriverIndex, iLocatorIndexer, iLocatorData, bind_u, &envelope, &dropoffInterp);

    dropoffInterp *= iDropoffDistance;

    float ww = 0.0;
    if (fabs(dropoffInterp) >= 1e-6f) {
        const float ratio = norm / (dropoffInterp * dropoffInterp);
        if (ratio < 1.0f)
            ww = envelope * (1.0f - ratio);
    }

    iBindW[aid+offset] = ww;         
}

//------------------------------------------------------------------------------
__kernel void gpu_packBindDataKernel(
    __global const float* iBindW,
    __global unsigned int* iDriverBindId,
    __global unsigned int* iDriverVertUse,
    __global unsigned int* iDriverIndexer,
    __global unsigned int* iPackInfo,
    const uint iNumVerts,
    const uint iAffectCount,
    const uint iNumDrivers)
{
    uint numUse = 0;
    uint numBnd = 0;

    for (size_t aid = 0; aid < iAffectCount; ++aid) {
        bool isMoving = false;
        for (size_t driverIndex = 0; driverIndex < iNumDrivers; ++driverIndex) {
            const uint offset = driverIndex*iAffectCount;
            const uint xid = aid + offset;

            if (fabs(iBindW[xid]) >= 1e-6f) {
                if (!isMoving) {
                    iDriverIndexer[numUse] = numBnd;
                    iDriverVertUse[numUse] = aid;
                    numUse++;
                    isMoving = true;
                }

                iDriverBindId[numBnd] = xid;
                numBnd++;
            }
        }
    }

    iDriverIndexer[numUse] = numBnd; // end marker...
    iPackInfo[0] = numUse;
}
