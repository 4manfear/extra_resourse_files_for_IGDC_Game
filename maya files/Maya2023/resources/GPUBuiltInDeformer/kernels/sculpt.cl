// Forward declaration
void flipMode(short fInsideMode, short fDropoffType, float radius, float fDropoffDistance, float fMaximalDisplacement, float3 pt[], float3 normal[]);
void projectMode(float radius, float fMaximalDisplacement, float3 pt[], float3 normal[]);
void stretchMode(short fInsideMode, short fDropoffType, short fExtendedEnd, float radius, float fDropoffDistance, float fMaximalDisplacement, float3 fStartingPosition, float16 fMatrixInverseForPoints, float3 pt[], float3 normal[]);
void handleInsidePts(short fInsideMode, float radius, float3 pt[], float3 normal[], float3 closestPt[], float3 closestNormal[], float weight);
void handleOutsidePts(short fDropoffType, float fMaximalDisplacement, float fDropoffDistance, float3 pt[], float3 closestPt, float3 closestNormal);
bool isInside(float3 localSpacePt, float3 ptOnSurface, float3 normalVect, float fraction[]);
void getClosestPtAndNormal( float radius, float3 pt, float3 normal, float3 closestPt[], float3 closestNormal[]);
float3 multiply(float3 pt, const float16 m);

// The function mirrors void TDNsculpt::deformData(...) and inlined void TsculptAlgorithm::deformPt(T4dDblPoint &pt, const T4dDblVector &normal)
__kernel void sculpt (	__global const float* inPositions,
						__global float* outPositions,
						const uint positionCount,
						const short fMode,
						const short fInsideMode,
						const short fDropoffType,
						const short fExtendedEnd,
						const float env,
						const float radius,
						const float fDropoffDistance,
						const float fMaximalDisplacement,
						const float3 fRegionOfEffectBBoxMin,
						const float3 fRegionOfEffectBBoxMax,
						const float3 fStartingPosition,
						const float16 matrixForPts,
						const float16 matrixInverseForPts,
						const float16 fMatrixInverseForPoints
						)
{
	// get the id of the position that we should be deforming:
    const unsigned int positionId = get_global_id(0);
	if ( positionId >= positionCount ) 
		// early out as we don't need to do anything
		return;

	float3 pt, localPt[1], localNormal[1];
    pt = vload3(positionId , inPositions);
	localPt[0] = multiply(pt, matrixForPts);

	// kRingMode(0)
	// kEvenMode(1)
	if (fInsideMode == 1)
	{			
		float3 startPt, endPt;
		startPt = multiply(fStartingPosition, fMatrixInverseForPoints);
		endPt.x = endPt.y = endPt.z = 0.0f;
		
		localNormal[0] = endPt - startPt;
	}

	// inlined void TsculptAlgorithm::deformPt(T4dDblPoint &pt, const T4dDblVector &normal)
	bool isPtInsideRegionOfEffect = fRegionOfEffectBBoxMin.x < localPt[0].x && localPt[0].x < fRegionOfEffectBBoxMax.y &&
									fRegionOfEffectBBoxMin.y < localPt[0].y && localPt[0].y < fRegionOfEffectBBoxMax.y &&
									fRegionOfEffectBBoxMin.z < localPt[0].z && localPt[0].z < fRegionOfEffectBBoxMax.z  ;

	// non-poly sculpt objects use this hack currently								
	if (isPtInsideRegionOfEffect || fMode == 2)
	{
		// kFlipMode(0)
		// kProjectMode(1)
		// kStretchMode(2)
		if (fMode == 0) 
			flipMode(fInsideMode, fDropoffType, radius, fDropoffDistance, fMaximalDisplacement, localPt, localNormal);
		else if (fMode == 1)
			projectMode(radius, fMaximalDisplacement, localPt, localNormal);
		else 
			stretchMode(fInsideMode, fDropoffType, fExtendedEnd, radius, fDropoffDistance, fMaximalDisplacement, fStartingPosition, fMatrixInverseForPoints, localPt, localNormal);
	}

	// Put the deformed point back into its original space
	pt = multiply(localPt[0], matrixInverseForPts);

	// Attenuate the deformation by the envelope
	if (fabs(env - 1.0f) > 0.000001f)
	{
		float3 orig;
		orig = vload3(positionId , inPositions);
		pt = (pt - orig) * env + orig;
	}

	// finally store the deformed position in the output
    vstore3(pt, positionId, outPositions);
}

// The function mirrors void TsculptAlgorithm::flipMode(T4dDblPoint &pt, const T4dDblVector &normal)
void flipMode(short fInsideMode, short fDropoffType, float radius, float fDropoffDistance, float fMaximalDisplacement, float3 pt[], float3 normal[])
{
	float  insideness[1];
	float3 closestPt[1];
	float3 closestNormal[1];
	getClosestPtAndNormal(radius, pt[0], normal[0], closestPt, closestNormal);

	if (isInside(pt[0], closestPt[0], closestNormal[0], insideness))
		handleInsidePts(fInsideMode, radius, pt, normal, closestPt, closestNormal, insideness[0]);
	handleOutsidePts(fDropoffType, fMaximalDisplacement, fDropoffDistance, pt, closestPt[0], closestNormal[0]);	
}

// The function mirrors void TsculptAlgorithm::projectMode(T4dDblPoint &pt, const T4dDblVector &normal)
void projectMode(float radius, float fMaximalDisplacement, float3 pt[], float3 normal[])
{
	float3 closestPt[1];
	float3 closestNormal[1];
	getClosestPtAndNormal(radius, pt[0], normal[0], closestPt, closestNormal);
	float3 diff = closestPt[0] - pt[0];
	pt[0] += fMaximalDisplacement * diff;
}

// The function mirrors void TsculptAlgorithm::stretchMode(T4dDblPoint &pt, const T4dDblVector &normal)
void stretchMode(short fInsideMode, short fDropoffType, short fExtendedEnd, float radius, float fDropoffDistance, float fMaximalDisplacement, float3 fStartingPosition, float16 fMatrixInverseForPoints, float3 pt[], float3 normal[])
{
	float3 startPt = multiply(fStartingPosition, fMatrixInverseForPoints);
	float3 endPt = (float3)(0.0f, 0.0f, 0.0f);
	float3 vectSE = endPt - startPt;
	float3 vectSP = pt[0] - startPt;

	float lengthSE = length(vectSE);
	float lengthSP = length(vectSP);

	float3 unitVectSE = normalize(vectSE);
	float magnitude = dot(vectSP, unitVectSE);
	if ((magnitude < 0.0f &&
		(fExtendedEnd == 0 || 
			lengthSP > (fDropoffDistance + 1.0f) ||
			lengthSE < 0.0001f)) ||
		magnitude > lengthSE)
	{
		flipMode(fInsideMode, fDropoffType, radius, fDropoffDistance, fMaximalDisplacement, pt, normal);
		return;
	}

	float3 projPt = startPt + unitVectSE * magnitude; 
	float3 stretchVector = endPt - projPt;
	float3 testPt[1];
	testPt[0] = pt[0] + stretchVector;

	float  insideness[1];
	float3 closestPt[1];
	float3 closestNormal[1];
	getClosestPtAndNormal(radius, testPt[0], normal[0], closestPt, closestNormal);

	if (isInside(testPt[0], closestPt[0], closestNormal[0], insideness))
	{
		handleInsidePts(fInsideMode, radius, testPt, normal, closestPt, closestNormal, insideness[0]);
		handleOutsidePts(fDropoffType, fMaximalDisplacement, fDropoffDistance, testPt, closestPt[0], closestNormal[0]);
		pt[0] = testPt[0];
		return;
	}

	float3 diff = testPt[0] - closestPt[0];
	float dist = length(diff);

	if (fabs(fDropoffDistance) > 0.00001f)
		dist /= fDropoffDistance;
	else
		dist = 1000000.0f;
	float fraction;
	if (dist < 1.0f)
		fraction = 1.0f - dist;
	else
		fraction = 0.0f;

	if (fabs(fraction) < 0.000001f)
		return;

	float3 stretchedPt[1];
	float3 stretchVectorTmp = stretchVector * fraction;
	stretchedPt[0] = pt[0] + stretchVectorTmp;

	flipMode(fInsideMode, fDropoffType, radius, fDropoffDistance, fMaximalDisplacement, stretchedPt, normal);

	pt[0] = stretchedPt[0];
}

// This function mirrors void TsculptAlgorithm::handleInsidePts(pt, normal, closestPt, closestNormal, weight)
void handleInsidePts(short fInsideMode, float radius, float3 pt[], float3 normal[], float3 closestPt[], float3 closestNormal[], float weight)
{
	// kRingMode(0)
	// kEvenMode(1)
	if (fInsideMode == 0)
		pt[0] = closestPt[0];
	else {
		float3 weightedTmp;
		weightedTmp = normal[0] * weight + closestNormal[0] * (1.0f - weight);
		pt[0] += weightedTmp;
		getClosestPtAndNormal(radius, pt[0], normal[0], closestPt, closestNormal);
		pt[0] = closestPt[0];
	}
}

// This function mirrors void TsculptAlgorithm::handleOutsidePts(pt, closestPt, closestNormal)
void handleOutsidePts(short fDropoffType, float fMaximalDisplacement, float fDropoffDistance, float3 pt[], float3 closestPt, float3 closestNormal)
{
	float3 diff = pt[0] - closestPt;
	float dist = length(diff);

    if (fabs(fDropoffDistance) > 0.00001f)
    	dist /= fDropoffDistance;
	else
		dist = 1000000;

	float fraction = 0.0f;
	if (dist < 1.0f)
	{
		// kNoDropoff(0)
		// kLinearDropoff(1)
		if (fDropoffType == 0)
			fraction = 1.0f;
		else 
			fraction = 1.0f - dist;
	}

	float disp = fraction * fMaximalDisplacement;

	pt[0] += disp * closestNormal;
}

// This function mirrors bool TsculptAlgorithm::isInside(...)
bool isInside(float3 localSpacePt, float3 ptOnSurface, float3 normal, float fraction[])
{
	bool inside = false;
	fraction[0] = 0.0f;
	float3 diffVect = localSpacePt - ptOnSurface;
	if (dot(normal, diffVect) < 0.0f)
	{
		inside = true;
		float3 localPtVect = localSpacePt;
		float3 ptOnSurfaceVect = ptOnSurface;
		fraction[0] = 1.0f - length(localPtVect) / length(ptOnSurfaceVect);		
	}
	return inside;
}

// This function mirrors a comination of 
// 	    bool TsculptAlgorithm::getClosestPtAndNormal(pt, norm, maxDist, closestPt, closestNormal)
//      bool TsculptAlgorithm::getClosestPtAndNormal(sphere, pt, /* maxDist */, closestPt, closestNormal)
void getClosestPtAndNormal(float radius, float3 pt, float3 normal, float3 closestPt[], float3 closestNormal[])
{
	float3 tmpPt = pt;
	float approxDist = fabs(pt.x) + fabs(pt.y) + fabs(pt.z);
	if (approxDist < 0.001f)
		tmpPt.x = 0.001f;
	closestNormal[0] = normalize(tmpPt);
    closestPt[0] = closestNormal[0] * radius;
}

float3 multiply(float3 pt, const float16 m)
//
//  Description:
//
//      Transform the specified position by the specified matrix
//
//  Parameters:
//
//      pt   - the point to transform
//      m   - the matrix to transform the point by
{
    float4 result;
    float4 tmp;// = (pt, 1.0f);
    tmp.xyz = pt.xyz;
    tmp.w = 1.0f;
    result.x = dot(tmp.xyzw, m.s0123);
    result.y = dot(tmp.xyzw, m.s4567);
    result.z = dot(tmp.xyzw, m.s89ab);
    return result.xyz;
}