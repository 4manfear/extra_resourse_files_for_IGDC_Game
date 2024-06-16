// Helper functions from utils.cl
float3 affineMultiplyPointRowMatrix(const float3 point, const float16 m);

// R = v*M
// M must a column-major v*M conventioned matrix
// [[expect: M.s37BF==float4(0,0,0,1) ]]
float3 affineMultiplyPointRowMatrix(const float3 point, const float16 m)
{
	float4 v = (float4)(point, 1.0f);
	float3 r;
	r.x = dot(v, m.s048C);
	r.y = dot(v, m.s159D);
	r.z = dot(v, m.s26AE);
	return r;
}

enum eAnimatedTargetType {
	kStaticTarget = 0x0,
	kAnimatedTargetRegular = 0x1,
	kAnimatedTargetWorldOrigin = 0x3,
};

// TODO : create separate kernel for different code path (animatedTargetType, useTransform)
// TODO : create proper constant buffer for this kernel
__kernel void blendShape(
    // parameters common to both kernels
	__global float* finalPos,						// 0:
    __global const float* accumulatedPos,			// 1:
    __global const float* targetPosDelta,			// 2: if (animatedTargetType == 0), then this is a vec4 where xyz are the delta target and w is the target weight per vertex.  if animatedTargetType > 0 then this is a vec3 of the targetVertex
    const float inputWeight,						// 3: 
	// parameters unique to this kernel
	const uint animatedTargetType,					// 4:
	const uint useTransform,						// 5: Should we use targetMatrices
	__global const float4* targetMatrices,			// 6: 4x4, column major, v*M convention
	__global const float* targetWeightPerVertex,	// 7: if animatedTargetType > 0 then this is a vector of the target weight per vertex
	// Parameters unique to this kernel which don't change
    __global const float* originalInputPos,			// 8:
	// constant parameters which don't change
    const uint positionCount,						// 9: 
	const float3 scale,								// 10:
	__global const float16* tgm,					// 11: targetGeometryMatrix, 4x4, row major, v*M convention, affine
	__global const float16* iigm,					// 12: inverseInputGeometryMatrix, 4x4, row major, v*M convention, affine
    __global const float*        weights ,			// 13: falloff weight
    __global const unsigned int* affectMap,			// 14:
    const uint                   affectCount		// 15:
    )
{
    unsigned int id = get_global_id(0);
    if ( affectMap && id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);

    if ( positionId >= positionCount ) return;

    const float weight = inputWeight * (weights ? weights[ id ] : 1.0f);

	float3 accumulatedPosition = vload3( positionId, accumulatedPos );

	float4 targetPositionDelta;
	if (animatedTargetType)
	{
		float3 targetPosition = vload3( positionId, targetPosDelta );
		float3 originalInputPosition = vload3( positionId, originalInputPos );

		// Apply the target and reference geometry matrix if blend shape is using WorldOrigin
		if (animatedTargetType == kAnimatedTargetWorldOrigin) 
		{
			// v = v * tgm * iigm
			targetPosition = affineMultiplyPointRowMatrix(targetPosition, *tgm);
			targetPosition = affineMultiplyPointRowMatrix(targetPosition, *iigm);
		}

        targetPositionDelta = (float4)(targetPosition - originalInputPosition, targetWeightPerVertex[positionId]);
	}
	else
	{
		targetPositionDelta = vload4( positionId , targetPosDelta );
	}

	float3 deltaPost;
	if(useTransform)
	{
		deltaPost.x = dot(targetPositionDelta, targetMatrices[0]);
		deltaPost.y = dot(targetPositionDelta, targetMatrices[1]);
		deltaPost.z = dot(targetPositionDelta, targetMatrices[2]);
		deltaPost.xyz /= scale;
	}			
	else
	{
		deltaPost.x = targetPositionDelta.x;
		deltaPost.y = targetPositionDelta.y;
		deltaPost.z = targetPositionDelta.z;
	}

    float3 finalPosition = accumulatedPosition + (weight * targetPositionDelta.w) * deltaPost;
    vstore3( finalPosition , positionId , finalPos );
}


__kernel void blendShape_tangentSpace(
	// parameters common to both kernels
    __global float* finalPos ,						// 0:
    __global const float* accumulatedPos ,			// 1:
    __global const float* targetPosDelta ,			// 2: this is a vec4 where xyz are the delta target and w is the target weight per vertex
    const float inputWeight,						// 3: 
	// parameters unique to this kernel
	// parameters which don't change.
    const uint positionCount,						// 4:
	const float3 scale,								// 5:
	__global const float* normals,					// 6:
	__global const float* tangents,					// 7:
    __global const float*        weights ,			// 8: falloff weight
    __global const unsigned int* affectMap,			// 9:
    const uint                   affectCount		// 10:
    )
{
    unsigned int id = get_global_id(0);
    if ( affectMap && id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    if ( positionId >= positionCount ) return;

    const float weight = inputWeight * (weights ? weights[ id ] : 1.0f);

	float4 targetPositionDelta = vload4( positionId , targetPosDelta );
	float3 accumulatedPosition = vload3( positionId , accumulatedPos );

	// compute the tangent space matrix.
	float3 matX = vload3( positionId, normals );
	float3 matT = vload3(positionId, tangents);
	float3 matZ = cross(matX, matT);
	matZ *= scale;

	matT *= scale;
	matT = normalize(matT);

	matX = cross(matT,matZ);
	matX = normalize(matX);
	matZ = cross(matX,matT);
	float3 matY = cross(matZ, matX);

	float3 deltaPost;
	deltaPost.x = dot(targetPositionDelta, (float4)(matX.x, matY.x, matZ.x, 0.0f));
	deltaPost.y = dot(targetPositionDelta, (float4)(matX.y, matY.y, matZ.y, 0.0f));
	deltaPost.z = dot(targetPositionDelta, (float4)(matX.z, matY.z, matZ.z, 0.0f));
	deltaPost.xyz /= scale;

    float3 finalPosition = accumulatedPosition + (weight * targetPositionDelta.w) * deltaPost;
    vstore3( finalPosition , positionId , finalPos );
}