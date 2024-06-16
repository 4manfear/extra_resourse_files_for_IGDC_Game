// OPTME: We could optimize this kernel by using __constant keyword
// for kernel parameter:
// - const struct TransformationMatrix* matrices
//
// This was done because of a bug with __constant on older hardware 
// that could be detected at run-time instead, but that would require
// inelegant tricks to do so.

// Helper functions
// OSX seems to be using very strict compiler setting which demand the function
// prototype be defined before the function is implemented.  It seems like we
// only need the function prototype for helper methods, not kernels that are
// used directly.
float3 mul( float16 matrix , float3 point );
float3 lerp( const float3 a , const float3 b , const float factor );
float4 quaternion_conjugate( const float4 quaternion );
float4 quaternion_multiply( const float4 q1 , const float4 q2 );
float3 quaternion_transform( const float4 q , const float3 p );
float4 quaternion_lerp( const float4 a , const float4 b , const float factor );
float4 quaternion_slerp( const float4 q1 , const float4 q2 , const float factor );
float4 core_slerp( const float4 p,
                   const float4 q,
                   const float alpha,
                   const int numSpins,
                   const int spinOn);

float3 mul( float16 matrix , float3 point )
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


__kernel void clusterRigidTransform(
    __global float* finalPos ,
    __global const float* initialPos ,
    const float16 rigidTransform ,
    __global const unsigned int* affectMap,
    const uint affectCount
    )
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);

    float3 initialPosition = vload3( positionId , initialPos );
    float3 finalPosition = mul( rigidTransform , initialPosition );
    vstore3( finalPosition , positionId , finalPos );
}

// Utility functions to manipulate vectors and quaternions.
float3 lerp( const float3 a , const float3 b , const float factor )
{
    return a + factor * ( b - a );
}

float4 quaternion_conjugate( const float4 quaternion )
{
    return (float4)( -quaternion.xyz , quaternion.w );
}

float4 quaternion_multiply( const float4 q1 , const float4 q2 )
{
    return quaternion_conjugate(
        q1.zxyw*q2.yzxw - q1.ywzx*q2.zywx - q1.wyxz*q2.xwyz - q1.xzwy*q2.wxzy
        );
}

float3 quaternion_transform( const float4 q , const float3 p )
{
    const float3 v = p + p;
    const float3 qv = q.xyz * v;
    const float3 result = q.w*(cross(q.xyz, v) + q.w*v) + q.xyz*(qv.xyz + qv.yzx + qv.zxy) - p;
    return result;
}

float4 quaternion_lerp( const float4 a , const float4 b , const float factor )
{
    return normalize( a + factor * ( b - a ) );
}

// OPTME: Other slerp implementations might be more optimal.
float4 quaternion_slerp( const float4 q1 , const float4 q2 , const float factor )
{
    float2 weights = (float2)( 1.0f - factor , factor );

    const float cosTheta = dot( q1 , q2 );

    // Perform linear interpolation if quaternions are too close to each other.
    // Hard-coded threshold is kind of arbitrary.
    if ( fabs( cosTheta ) < ( 1.0f - 0.00001f ) )
    {
        // No need for inverseSinTheta if we normalize at the end.
        // const float inverseSinTheta = rsqrt( 1.0f - cosTheta * cosTheta );
        const float theta = acos( cosTheta );

        weights = sin( weights * theta ); // * inverseSinTheta;
    }

    return normalize( weights.x * q1 + weights.y * q2 );
}

float4 core_slerp( const float4 p,
                   const float4 q,
                   const float alpha,
                   const int numSpins,
                   const int spinOn)
{
    float4 tmp = q;
    float cosTheta = dot( p, q );
    int spins = numSpins;
    if (cosTheta < 0.0)
    {
        cosTheta = -cosTheta;
        tmp = -tmp;

        if (spinOn) {
            // If we have a 180 flip, alter the spin so it feels like it
            // continues on (used by dslerp)
            if (spins == 0)
                spins = -1;
            else
                spins = 0;
        }
    }

    if (1.0 - cosTheta > 0.00001f)
    {
        const float theta = acos(clamp(cosTheta, -1.0f, 1.0f));
        const float phi = theta + spins * 3.14159265358979323846264338327950f;
        const float sinTheta = sin(theta);
        const float s1 = sin(theta - alpha*phi) / sinTheta;
        const float s2 = sin(alpha*phi) / sinTheta;
        return s1 * p + s2 * tmp;
    }
    else
    {
        //	Quaternions nearly opposite, can't spin
        return (1.0f - alpha) * p + alpha * tmp;
    }

}

// This struct must EXACTLY match the TransformationMatrix defined in the CPU code for this deformer.
// OpenCL has strict alignment requirements for structs (see OpenCL documentation section 6.1.5).
// These alignment requirements mean that TransformationMatrix.matrix must be 64 byte aligned.
// Right now TransfomrationMatrix has 224 bytes of data (1*64 + 2*16 + 8*16).  Given that matrix
// must be 64 byte aligned we know that the compiler will pad the structure to 256 bytes.
// However, the CPU version of TransformationMatrix doesn't have the same strict alignment requirements
// and therefore it will not automatically be padded by the compiler.  For this reason I choose to
// pad both the CPU and GPU versions of TransformationMatrix, so they are both explicitly 256 bytes.
// If the size of the useful data in TransformationMatrix grows larger than 256 bytes then the next
// possible valid size for TransformationMatrix is 320 bytes (256 + 64).  OpenCL does not require
// that the size or alignment of a struct be a power of two (see OpenCL documentation section 6.1.5).
struct TransformationMatrix
{
    float16 matrix;                     // float16 has a 64 byte alignment and size
    float3 scalePivotPoint;             // float3 has a 16 byte alignment and size
    float3 scale;
    float3 shear;
    float3 scalePivotTranslation;
    float3 rotatePivotPoint;
    float4 rotationOrientation;         // float4 has a 16 byte alignment and size
    float4 rotation;
    float3 rotatePivotTranslation;
    float3 translation;
    float3 eulerRotation;
    float4 padding[2];
};

__kernel void clusterPerVertexWeights(
    __global float* finalPos ,
    __global const float* initialPos ,
    const struct TransformationMatrix matrixA,
    const struct TransformationMatrix matrixB,
    const uint interpDir,
    const float envelope,
    __global const float* weights,
    __global const unsigned int* affectMap,
    const uint affectCount
    )
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float3 initialPosition = vload3( positionId , initialPos );

    // Perform interpolation at the same time as transformation of the point.
    // Because the resulting blended transformation is used only once, it's
    // better to apply transformation as we go instead of building a
    // transformation matrix.
    float3 finalPosition = initialPosition;

    // Before matrix is in matrixA.
    finalPosition = mul( matrixA.matrix , finalPosition );

    // [Sp]^-1
    float3 scalePivotPoint = matrixB.scalePivotPoint;
    finalPosition -= scalePivotPoint;
    // [S]
    float3 scale = lerp( matrixA.scale , matrixB.scale , weight );
    finalPosition *= scale;
    // [Sh]
    float3 shear = lerp( matrixA.shear , matrixB.shear , weight );
    finalPosition = (float3)(
        finalPosition.x + shear.s0 * finalPosition.y + shear.s1 * finalPosition.z ,
        finalPosition.y + shear.s2 * finalPosition.z ,
        finalPosition.z
        );
    // [Sp]
    finalPosition += scalePivotPoint;
    // [St]
    float3 scalePivotTranslation = lerp( matrixA.scalePivotTranslation , matrixB.scalePivotTranslation , weight );
    finalPosition += scalePivotTranslation;
    // [Rp]^-1
    float3 rotatePivotPoint = matrixB.rotatePivotPoint;
    finalPosition -= rotatePivotPoint;
    // [Ro]
    float4 rotationOrientation = quaternion_slerp( matrixA.rotationOrientation , matrixB.rotationOrientation , weight );
    // [R]
    float4 rotation;
    if (interpDir == 0 || interpDir == 3)
        rotation = core_slerp( matrixA.rotation, matrixB.rotation, weight, 0, 0);
    else if (interpDir == 1)
        rotation = core_slerp( matrixA.rotation, matrixB.rotation, weight, 0, 1);
    else if (interpDir == 2)
        rotation = core_slerp( matrixA.rotation, matrixB.rotation, weight, -1, 1);
	else
        rotation = matrixA.rotation;

    finalPosition = quaternion_transform(
        quaternion_multiply( rotation , rotationOrientation ) ,
        finalPosition
        );
    // [Rp]
    finalPosition += rotatePivotPoint;
    // [Rt]
    float3 rotatePivotTranslation = lerp( matrixA.rotatePivotTranslation , matrixB.rotatePivotTranslation , weight );
    finalPosition += rotatePivotTranslation;
    // [T]
    float3 translation = lerp( matrixA.translation , matrixB.translation , weight );
    finalPosition += translation;

    // After matrix is in matrixB.
    finalPosition = mul( matrixB.matrix , finalPosition );

    vstore3( finalPosition , positionId , finalPos );

}
