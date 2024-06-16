// Display mesh kernels

// The buffers through the deformer pipeline are standardized on float3.  But the
// buffers used for rendering can sometimes be float4 instead.  Plug-in shaders can
// ask for any arbitrary combination of formats.
// Each output buffer in this file has an associated preprocessor variable which
// controls how kernels in this file will write to that buffer.
// VertexPositionsAsFloat4
// VertexNormalsAsFloat4
// VertexTangentsAsFloat4
// VertexBitangentsAsFloat4
// All this is abstracted from the kernel writer using the LoadVertex*** / StoreVertex***
// methods.  These will automatically handle the element type of the vertex buffers for you.
// Buffers stored in Maya format (positions, normals, uvs) always have the same element size
// determined by the deformer pipeline, so there are no special access methods for them.

float4 LoadVertexPosition(const uint id, __global const float* vertexPositions);
void StoreVertexPosition(float4 position, const uint id, __global float* vertexPositions);

float4 LoadVertexNormal(const uint id, __global const float* vertexNormals);
void StoreVertexNormal(float4 position, const uint id, __global float* vertexNormals);

float4 LoadVertexTangent(const uint id, __global const float* vertexTangents);
void StoreVertexTangent(float4 position, const uint id, __global float* vertexTangents);

float4 LoadVertexBitangent(const uint id, __global const float* vertexBitangents);
void StoreVertexBitangent(float4 position, const uint id, __global float* vertexBitangents);

__kernel void displayMesh_applyTweaks(
	__global float* positions,	// float3 always
	__global float* tweaks,		// float3 always
	const uint vertexCount)
{
	unsigned int index = get_global_id(0);
	if (index >= vertexCount) return;

	float3 pos = vload3(index, positions);
	float3 tweak = vload3(index, tweaks);
	vstore3(pos + tweak, index, positions);
}

__kernel void displayMesh_computeBoundingBox(
	__global float* positions,
	const unsigned int positionCount,
	__local float* temp,
	__global float* result,
    const unsigned int resultOffset)  //offset into result buffer at which to write, in # of floats.
{
	// Phase 1: Enough serial reductions executed in parallel to fully utilize the GPU
	//
	// Each thread computes an intermediate min and max.  During phase one we work over
	// the full length of positions.  Each thread should NOT read a
	// contiguous block of memory.  When a signle thread is reading from a contiguous block of memory
	// then Each thread will be loading from a separate block of memory which reduces bandwidth.
	// Instead each thread works using a stride, so adjacent threads will access adjacent memory locations.
	unsigned int index = get_global_id(0);
	unsigned int stride = get_global_size(0);  // get_global_size is the total number of threads we have working.
	float3 minBounds = (float3)(FLT_MAX, FLT_MAX, FLT_MAX);
	float3 maxBounds = (float3)(-FLT_MAX, -FLT_MAX, -FLT_MAX);
	while (index < positionCount)
	{
		float3 position = vload3(index, positions);

		minBounds = fmin(position, minBounds);
		maxBounds = fmax(position, maxBounds);
		index += stride;
	}

	// Finish Phase 1.  This thread has completed its serial reduction over the
	// buffer.  Store the result in the local shared temporary buffer.
	int local_index = get_local_id(0);
	vstore3(minBounds, local_index * 2, temp);
	vstore3(maxBounds, local_index * 2 + 1, temp);
	barrier(CLK_LOCAL_MEM_FENCE);

	// Phase 2: Parallel reduction on all the results we computed in this work group.
	//
	// Our dataset has been reduced to a total size of get_global_size().  We can't
	// efficiently communicate between threads which are not in the same workgroup,
	// so Phase 2 does a parallel reduction within the workgroup and writes out
	// a result.
	// 
	// In order to have a good memory access pattern we DON'T add adjacent elements
	// together.  Instead use a stride so that adjacent threads access adjacent 
	// memory locations.
	//

	for(int offset = get_local_size(0) / 2; offset > 0; offset = offset/2)
	{
		if (local_index < offset) // when local_index >= offset then a different thread is going to read this value and use it
		{
			int myMinIndex = local_index * 2;
			int myMaxIndex = myMinIndex + 1;
			int otherMinIndex = (local_index + offset) * 2;
			int otherMaxIndex = otherMinIndex + 1;

			float3 myMin = vload3(myMinIndex, temp);
			float3 myMax = vload3(myMaxIndex, temp);
			float3 otherMin = vload3(otherMinIndex, temp);
			float3 otherMax = vload3(otherMaxIndex, temp);

			myMin.x = (otherMin.x < myMin.x) ? otherMin.x : myMin.x;
			myMin.y = (otherMin.y < myMin.y) ? otherMin.y : myMin.y;
			myMin.z = (otherMin.z < myMin.z) ? otherMin.z : myMin.z;

			myMax.x = (otherMax.x > myMax.x) ? otherMax.x : myMax.x;
			myMax.y = (otherMax.y > myMax.y) ? otherMax.y : myMax.y;
			myMax.z = (otherMax.z > myMax.z) ? otherMax.z : myMax.z;

			vstore3(myMin, myMinIndex, temp);
			vstore3(myMax, myMaxIndex, temp);
		}
		barrier(CLK_LOCAL_MEM_FENCE);
	}

	// Each workgroup now has a single result.  Each workgroup stores that
	// result into the result buffer, which is read back to the CPU where
	// we can do the final reduction.
	if (local_index == 0)
	{
		vstore3(vload3(0, temp), get_group_id(0)*2 + (resultOffset/3), result);
		vstore3(vload3(1, temp), get_group_id(0)*2 + 1 + (resultOffset/3), result);
	}
}

__kernel void displayMesh_convertPositionsToVertexPositions(
	__global float* vertexPositions, // float3 or float4
	__global const float* positions, // float3 always
	__global const unsigned int* sharedIdxToVertex,
	const uint vertexCount)
{
	unsigned int index = get_global_id(0);
	if (index >= vertexCount) return;

	float3 pos = vload3(sharedIdxToVertex[index], positions);
	StoreVertexPosition((float4)(pos, 1.0f), index, vertexPositions);
}


__kernel void displayMesh_convertNormalsToVertexNormals(
	__global float* vertexNormals, //float3 or float4
	__global const float* normals, //float3
	__global const unsigned int* sharedIdxToNormalId,
	const unsigned int vertexCount)
{
	unsigned int vertexNormalId = get_global_id(0);
	if (vertexNormalId >= vertexCount) return;

    float3 norm = vload3(sharedIdxToNormalId[vertexNormalId], normals);
    StoreVertexNormal((float4)(norm, 0.0f), vertexNormalId, vertexNormals);
}

__kernel void displayMesh_copyDeformedUserNormals(
	__global float* vertexNormals, //float3 or float4.  Already updated with generated normals
	__global const float* normals, //float3
	__global const unsigned int* sharedIdxToNormalId,
	__global const unsigned int* hasUserNormalMap,
	const unsigned int vertexCount)
{
	unsigned int sharedId = get_global_id(0);
	if (sharedId >= vertexCount) return;
	
	if (hasUserNormalMap[sharedId])
	{
		float3 norm = vload3(sharedIdxToNormalId[sharedId], normals);
		StoreVertexNormal((float4)(norm, 0.0f), sharedId, vertexNormals);
	}
}

// Copies a contiguous range of source float[3] values to i*2 in the destination buffer
__kernel void displayMesh_remapExpandByTwo(
	__global float* dest,	   //float3
	__global const float* src, //float3
	const unsigned int count)
{
	unsigned int idx = get_global_id(0);
	if (idx >= count) return;
	
    float3 val = vload3(idx, src);
    vstore3(val, idx * 2, dest);
}

__kernel void displayMesh_copyTangentBuffer(
	__global float* dest,
	__global float* src,
	const unsigned int count)
{
	unsigned int idx = get_global_id(0);
	if (idx >= count) return;

	float4 value = LoadVertexTangent(idx, src);
	vstore3(value.xyz, idx, dest);
}

__kernel void displayMesh_copyBitangentBuffer(
	__global float* dest,
	__global float* src,
	const unsigned int count)
{
	unsigned int idx = get_global_id(0);
	if (idx >= count) return;

	float4 value = LoadVertexBitangent(idx, src);
	vstore3(value.xyz, idx, dest);
}

/*
	This kernel calculates each vertex normal by calculating the face normal
	of each triangle which contributes to the vertex normal, then averaging the
	face normals using the area of the triangle and the angle of the vertex in the
	triangle as weights.
*/
__kernel void displayMesh_generateVertexNormalsUsingRenderTriangleMap(
	__global const float* vertexPositions,  //float3 or float4
	__global float* vertexNormals,          //float3 or float4
	__global const unsigned int* vertexIdToTriangleMap,
	__global const unsigned int* vertexIdToTriangleMapOffsets,
	const uint vertexCount)
{
	unsigned int vertexId = get_global_id(0);
	if (vertexId >= vertexCount) return;

	// loop over the faces, compute the face normals and accumulate them
	// then normalize the result and store it in vertexNormals

	float4 accumulatedNormal = (float4)(0.0f, 0.0f, 0.0f, 0.0f);

	unsigned int start = vertexIdToTriangleMapOffsets[vertexId];
	float4 vertex1 = LoadVertexPosition(vertexIdToTriangleMap[start++], vertexPositions);
	unsigned int end = vertexIdToTriangleMapOffsets[vertexId+1];
	for (unsigned int i = start; i < end; i++)
	{
		float4 vertex2 = LoadVertexPosition(vertexIdToTriangleMap[i++], vertexPositions);
		float4 vertex3 = LoadVertexPosition(vertexIdToTriangleMap[i], vertexPositions);

		// Make sure you get the winding order correct so the normal doesn't get reversed
		float4 vector1 = vertex2 - vertex1;
		float4 vector2 = vertex3 - vertex1;

		// Area of a triangle is half the length of the cross-product of two sides.
		// So to area-weight the normal contributions, don't normalize the cross product.
		float4 crossProd = cross(vector1, vector2);

		// Weight the normal by the angle of the triangle at the vertex.
		float angle = atan2( length(cross(vector1, vector2)), dot(vector1, vector2) );

		//accumulatedNormal += normalize(crossProd);
		accumulatedNormal += crossProd * angle;
	}

	accumulatedNormal = normalize(accumulatedNormal);
    StoreVertexNormal(accumulatedNormal, vertexId, vertexNormals);
}

/*
	This kernel calculates each vertex normal by calculating the face normal
	of each face which contributes to the vertex normal, then averaging the
	face normals using the area of the face and the angle of the vertex in the
	face as weights.
	We use Newell's method to calculate the face normal of a non-planar face.
*/

// vertexIdToFaceMap is laid out as
// First, one unsigned integer which is the sharedId of the vertex we are calculating the normal of.
// Next, a list of faces.  Each face is stored as:
//      First, an unsigned integer which is the number to vertices in the face (including the vertex we are calculating the normal of)
//      Next, the list of sharedIds in the face.  The vertices are stored in the correct winding order.  The vertex we are calculating the normal of comes before the first listed vertex (or after the last listed vertex).
// Example: if we have a vertex A which has vertex normal influenced by two faces (A, B, C, D) and (F, A, E) then vertexToFaceMap for A would be:
// [A, 4, B, C, D, 3, E, F]

__kernel void displayMesh_generateVertexNormalsUsingFaceMap(
	__global const float* vertexPositions,  //float3
	__global float* vertexNormals,          //float3 or float4
	__global const unsigned int* vertexIdToFaceMap,
	__global const unsigned int* vertexIdToFaceMapOffsets,
	const uint vertexCount)
{
	unsigned int vertexId = get_global_id(0);
	if (vertexId >= vertexCount) return;

	// loop over the faces, compute the face normals and accumulate them
	// then normalize the result and store it in vertexNormals

	float3 accumulatedNormal = (float3)(0.0f, 0.0f, 0.0f);

	unsigned int start = vertexIdToFaceMapOffsets[vertexId];
	unsigned int end = vertexIdToFaceMapOffsets[vertexId+1];
	if (start == end) return; // If there are no faces then don't try to read the primary vertex, we might be past the end of the buffer
	float3 primaryVertexPosition = vload3(vertexIdToFaceMap[start++], vertexPositions); // position of the vertex we are calculating the normal of
	
	for (unsigned int i = start; i < end; ++i)
	{
		unsigned int faceVertexCount = vertexIdToFaceMap[i++]; // the number of vertices in the current face including the primary vertex.  This number is one more than the number of verts we have stored in the buffer for this face.
		unsigned int currFaceStart = i;
		unsigned int currFaceEnd = i + faceVertexCount - 1;  // subtract 1 because the primary vertex is not in the buffer.

		// calculate the face normal of the current face
		float3 faceNormal = (float3)(0.0f, 0.0f, 0.0f);
		float3 vertex0 = primaryVertexPosition;
		float3 vertex1;
		for (; i < currFaceEnd; ++i)
		{
			vertex1 = vload3(vertexIdToFaceMap[i], vertexPositions);

			float3 difference = vertex0 - vertex1;
			float3 sum = vertex0 + vertex1;
			faceNormal += difference.yzx * sum.zxy;

			vertex0 = vertex1;
		}
		// i is now currFaceEnd, which should also be next face start.  If we don't modify i then
		// the outer loop will increment i again, and we'll start a face in the wrong place;
		--i;

		// now handle the edge from the last vertex stored in vertexIdToFaceMap and the primary vertex
		float3 difference = vertex1 - primaryVertexPosition;
		float3 sum = vertex1 + primaryVertexPosition;
		faceNormal += difference.yzx * sum.zxy;

		// end of face.  We need to calculate the area of the face and the angle of
		// the vertex in the face, and accumulate the vertex normal.

		// In TpolyGeom::faceArea() we say the area is the length of the faceNormal / 2.
		// I'll just ignore the factor of 2 because it'll be the same everywhere, and then
		// not normalize the faceNormal.  This should be equivalent to normalizing the face
		// normal, then multiplying by the area.
		// Therefore, I only need to calculate the angle in the face at the vertex.
		// I know that the vertex we care about is stored in primaryVertexPosition.
		// I know that the last vertex in the face is stored in vertex0 and vertex1.
		// I know I need the vertex after currFaceStart.
		vertex1 = vload3(vertexIdToFaceMap[currFaceStart], vertexPositions);

		float3 vector1 = vertex1 - primaryVertexPosition;
		float3 vector2 = vertex0 - primaryVertexPosition;
		
		// Weight the normal by the angle of the triangle at the vertex.
		float angle = atan2( length(cross(vector1, vector2)), dot(vector1, vector2) );
		accumulatedNormal += faceNormal * angle;
	}

	accumulatedNormal = normalize(accumulatedNormal);
    StoreVertexNormal((float4)(accumulatedNormal, 0.0f), vertexId, vertexNormals);
}


__kernel void displayMesh_generateTangentsBitangentsUsingMap(
	__global const float* vertexPositions,  //float3 or float4
	__global const float* vertexNormals,    //float3 or float4
    __global const float* vertexUVs,        //float2
    __global float* vertexTangents,         //float3 or float4
    __global float* vertexBitangents,       //float3 or float4
	__global const unsigned int* vertexIdToTriangleMap,
	__global const unsigned int* vertexIdToTriangleMapOffsets,
    __global const unsigned int* bitanFlippedBitfield,  
	const uint vertexCount)
{
	unsigned int vertexId = get_global_id(0);
	if (vertexId >= vertexCount) return;

	// loop over the faces, compute the face normals and accumulate them
	// then normalize the result and store it in vertexNormals

	float4 accumulatedTangent = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
    float4 surfNormal = LoadVertexNormal(vertexId, vertexNormals);

	// read the position and UV of the vertex we are working on.
	unsigned int start = vertexIdToTriangleMapOffsets[vertexId];
	unsigned int triMap0 = vertexIdToTriangleMap[start++];
	float4 pos0 = LoadVertexPosition(triMap0, vertexPositions);
	float2 uv0 = vload2(triMap0, vertexUVs);
	unsigned int end = vertexIdToTriangleMapOffsets[vertexId+1];
	for (unsigned int i = start; i < end; i++)
	{
		unsigned int triMap1 = vertexIdToTriangleMap[i++];
		unsigned int triMap2 = vertexIdToTriangleMap[i];

		float4 pos1 = LoadVertexPosition(triMap1, vertexPositions);
		float4 pos2 = LoadVertexPosition(triMap2, vertexPositions);

        float2 uv1 = vload2(triMap1, vertexUVs);
        float2 uv2 = vload2(triMap2, vertexUVs);

        float2 uvDelta1 = uv1 - uv0;
        float2 uvDelta2 = uv2 - uv0;

        float4 posDelta1 = pos1 - pos0;
        float4 posDelta2 = pos2 - pos0;

        // x,s,t.  s and t vectors are re-used.
        float4 edge1 = (float4)(posDelta1.x, uvDelta1, 0.0f);
        float4 edge2 = (float4)(posDelta2.x, uvDelta2, 0.0f);
        float4 crossP = normalize(cross(edge1, edge2));
        if (fabs(crossP.x) < 0.0001f)  //check for degen
            crossP.x = 1.0f;
        float4 tangent;
        tangent.x = -crossP.y/crossP.x;

        // y,s,t
        edge1.x = posDelta1.y;
        edge2.x = posDelta2.y;
        crossP = normalize(cross(edge1, edge2));
        if (fabs(crossP.x) < 0.0001f)  //check for degen
            crossP.x = 1.0f;
        tangent.y = -crossP.y/crossP.x;

        //z,s,t
        edge1.x = posDelta1.z;
        edge2.x = posDelta2.z;
        crossP = normalize(cross(edge1, edge2));
        if (fabs(crossP.x) < 0.0001f)  //check for degen
            crossP.x = 1.0f;
        tangent.z = -crossP.y/crossP.x;
        tangent.w = 0.0f;

        // Project it into the correct plane and renormalize
        tangent = normalize(tangent - surfNormal * dot(tangent, surfNormal));

		accumulatedTangent += tangent;
	}

	float4 finalTangent = normalize(accumulatedTangent);

    unsigned int bitfieldChunk = bitanFlippedBitfield[vertexId / 32];
    unsigned int flippedRem = vertexId % 32;
    unsigned int flipped = bitfieldChunk & (1 << flippedRem);
    float flippedFactor = (flipped != 0) ? -1.0f : 1.0f;

    float4 bitangent = cross(surfNormal, finalTangent) * flippedFactor;

    // write the output
    StoreVertexTangent(finalTangent, vertexId, vertexTangents);
	StoreVertexBitangent(bitangent, vertexId, vertexBitangents);
}

float4 LoadVertexPosition(const uint id, __global const float* vertexPositions)
{
#ifdef VertexPositionsAsFloat4
	return vload4(id, vertexPositions);
#else
	return (float4)(vload3(id, vertexPositions), 1.0f);
#endif
}

void StoreVertexPosition(float4 position, const uint id, __global float* vertexPositions)
{
#ifdef VertexPositionsAsFloat4
	vstore4(position, id, vertexPositions);
#else
	vstore3(position.xyz, id, vertexPositions);
#endif
}

float4 LoadVertexNormal(const uint id, __global const float* vertexNormals)
{
#ifdef VertexNormalsAsFloat4
	return vload4(id, vertexNormals);
#else
	return (float4)(vload3(id, vertexNormals), 0.0f);
#endif
}

void StoreVertexNormal(float4 normal, const uint id, __global float* vertexNormals)
{
#ifdef VertexNormalsAsFloat4
	vstore4(normal, id, vertexNormals);
#else
	vstore3(normal.xyz, id, vertexNormals);
#endif
}

float4 LoadVertexTangent(const uint id, __global const float* vertexTangents)
{
#ifdef VertexTangentsAsFloat4
	return vload4(id, vertexTangents);
#else
	return (float4)(vload3(id, vertexTangents), 0.0f);
#endif
}

void StoreVertexTangent(float4 Tangent, const uint id, __global float* vertexTangents)
{
#ifdef VertexTangentsAsFloat4
	vstore4(Tangent, id, vertexTangents);
#else
	vstore3(Tangent.xyz, id, vertexTangents);
#endif
}

float4 LoadVertexBitangent(const uint id, __global const float* vertexBitangents)
{
#ifdef VertexBitangentsAsFloat4
	return vload4(id, vertexBitangents);
#else
	return (float4)(vload3(id, vertexBitangents), 0.0f);
#endif
}

void StoreVertexBitangent(float4 Bitangent, const uint id, __global float* vertexBitangents)
{
#ifdef VertexBitangentsAsFloat4
	vstore4(Bitangent, id, vertexBitangents);
#else
	vstore3(Bitangent.xyz, id, vertexBitangents);
#endif
}

