#if __OPENCL_VERSION__ <= CL_VERSION_1_1

#if defined(cl_khr_fp64)
    #pragma OPENCL EXTENSION cl_khr_fp64 : enable
#elif defined(cl_amd_fp64)
	#pragma OPENCL EXTENSION cl_amd_fp64 : enable
#endif

#endif

struct MatrixPair
{
    float16 deformToGeom;
    float16 geomToDeform;
};

// transform x by the homogeneous matrix m, such that x' = M * x.
// M is assumed to be densely packed in row major form.
//
inline float3 transformPoint(const float16 M, const float3 x)
{
    return (float3)(
        dot(M.s012, x)+M.s3,
        dot(M.s456, x)+M.s7,
        dot(M.s89a, x)+M.sb
    );
}

// return true if a with eps tolerance of b and false otherwise
//
inline bool equivalent(double a, double b)
{
    return (fabs(a-b) < 1e-12);
}

// Linearly interpolation between minVal and maxVal
// Assumes x is in the range [0,1]
inline double lerp(double x, double minVal, double maxVal)
{
    return minVal + (x*(maxVal-minVal));
}

inline double computeMagnitude(double factor)
{
    if (factor>=0.0)
        return (1.0+factor);
    else
        return (1.0/(1.0-factor));
}

//------------------------------------------------------------------------------
__kernel void deformSine(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope,
    __global const float*        weights ,
    __global const unsigned int* affectMap,
    const uint                   affectCount)
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt     = transformPoint(geomToDeform, origPt);

    // beginning of sine algorithm
    {
        double dropoff   = params[0];
        double lowBound  = params[1];
        double highBound = params[2];
        double amplitude = params[3];
        double period    = params[4];
        double offset    = params[5];

        double y = clamp((double)pt.y, lowBound, highBound);
        double maxBound = max(-lowBound, highBound);
        if (maxBound == 0.0)
            maxBound = 0.0001;

        double absY = fabs(y);
        double factor = 1.0;
        if (dropoff > 0.0)
            factor -= ( dropoff * absY/maxBound);
        if (dropoff < 0.0)
            factor -= (-dropoff * (maxBound-absY)/maxBound);

        double frequency = (period != 0.) ?
            ( M_PI * 2 ) / period :
            0. ;

        double result = sin((y+offset)*frequency)*amplitude*factor;
        pt.x += result;
    }
    // end of sine algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * weight;
    vstore3(pt, positionId , finalPos);
}

//------------------------------------------------------------------------------
__kernel void deformBend(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope,
    __global const float*        weights ,
    __global const unsigned int* affectMap,
    const uint                   affectCount)
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt     = transformPoint(geomToDeform, origPt);

    // beginning of bend algorithm
    {
        double lowBound  = params[0];
        double highBound = params[1];
        double curvature = params[2];

        if (!equivalent(curvature, 0.))
        {
            double ff2 = 1.0/curvature;
            double y   = pt.y;
            double over_size = 0.;
            if (y < lowBound)
            {
                over_size = y - lowBound;
                y = lowBound;
            }
            if (y > highBound)
            {
                over_size = y - highBound  ;
                y = highBound;
            }

            double tt = y*curvature;
            double c  = cos(tt);
            double s  = sin(tt);
            pt.y = s*(ff2-pt.x)     + c*over_size;
            pt.x = c*(pt.x-ff2)+ff2 + s*over_size;
        }
    }
    // end of bend algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * weight;
    vstore3(pt, positionId, finalPos);
}

//------------------------------------------------------------------------------
__kernel void deformTwist(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope,
    __global const float*        weights ,
    __global const unsigned int* affectMap,
    const uint                   affectCount)
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt     = transformPoint(geomToDeform, origPt);

    // Twist algorithm
    {
        double lowBound   = params[0];
        double highBound  = max(params[1], lowBound);
        double startAngle = params[2];
        double endAngle   = params[3];

        double y = clamp((double)pt.y, lowBound, highBound);

        double relativeY;
        double boundDiff = (highBound - lowBound);
        if (boundDiff == 0.)
            relativeY = (pt.y > highBound)? 1. : 0.;
        else
            relativeY = (y-lowBound)/boundDiff;

        double ff = lerp(relativeY, startAngle, endAngle);
        if (ff != 0.)
        {
            double c = cos(ff);
            double s = sin(ff);
            double a = pt.x*c - pt.z*s;
            double b = pt.x*s + pt.z*c;

            pt.x = a;
            pt.z = b;
        }
    }
    // end of twist algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * weight;
    vstore3(pt, positionId , finalPos);
}

//------------------------------------------------------------------------------
__kernel void deformWave(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope,
    __global const float*        weights ,
    __global const unsigned int* affectMap,
    const uint                   affectCount)
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt = transformPoint(geomToDeform, origPt);

    // wave algorithm
    {
        double dropoff         = params[0];
        double maxRadius       = params[1];
        double minRadius       = min(params[2], maxRadius);
        double amplitude       = params[3];
        double wavelength      = params[4];
        double offset          = params[5];
        double dropoffPosition = params[6];

        double diff = maxRadius - minRadius;
        if (diff > 0.0)
        {
            double dist = sqrt(pt.x*pt.x + pt.z*pt.z);
            dist = clamp(dist, minRadius, maxRadius);
            double maxDropoff = lerp(dropoffPosition, minRadius, maxRadius);
            double dropoffFactor = 1.0;

            if (dist > maxDropoff)
                if (maxRadius == maxDropoff)
                    dropoffFactor = (dropoff * (dist-minRadius)/diff);
                else
                    dropoffFactor = 1.0-(fabs(dropoff)*(dist-maxDropoff)/(maxRadius-maxDropoff));
            else
                if (minRadius == maxDropoff)
                    dropoffFactor = 1.0-(dropoff * (dist-minRadius)/diff);
                else
                    dropoffFactor = 1.0-(fabs(dropoff)*(maxDropoff-dist)/(maxDropoff-minRadius));

            if (dropoff < 0.0)
                dropoffFactor = 1.0-dropoffFactor;

            double lengthToAngle = (wavelength == 0.0 ? 0.0 : (M_PI*2.) / wavelength);
            double angOffset = lengthToAngle * offset;

            pt.y += sin((dist-minRadius)*lengthToAngle+angOffset+M_PI_2)*amplitude*dropoffFactor;
        }
    }
    // end of wave algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * weight;
    vstore3(pt, positionId , finalPos);
}

//------------------------------------------------------------------------------
__kernel void deformSquash(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope,
    __global const float*        weights ,
    __global const unsigned int* affectMap,
    const uint                   affectCount)
{
    unsigned int id = get_global_id(0);
    if ( id >= affectCount ) return;

    const unsigned int positionId = (affectMap ? affectMap[id] : id);
    const float weight = envelope * (weights ? weights[ id ] : 1.0f);

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt = transformPoint(geomToDeform, origPt);

    // squash algorithm
    {
        double lowBound        = params[0];
        double highBound       = max(params[1], lowBound);
        double startSmoothness = params[2];
        double endSmoothness   = params[3];
        double maxPos          = params[4];
        double expand          = params[5];
        double magnitude       = computeMagnitude(params[6]);

        if (pt.y <= lowBound)
            pt.y += lowBound * (magnitude-1);
        else if (pt.y >= highBound)
            pt.y += highBound * (magnitude-1);
        else
        {
            double factor = (pt.y - lowBound) / (highBound - lowBound); // In [0, 1]

            // Remap 0 maxPos 1 to 0 .5 1, using X^Y function
            // .69314718055994530941 = Log(2)
            double expos = - .69314718055994530941 / log(maxPos);
            factor = pow(factor, expos);

            double interval = (factor < 0.5)? startSmoothness : endSmoothness;
            interval = clamp(interval, 0., 1.);

            double radius = 1 + interval;
            double max = radius - sqrt(radius*radius - 1.0);
            double scale = (1.0 - interval)/max;

            factor = 2*factor-1; // move to [-1, 1]
            double val = scale * ( sqrt(radius*radius - factor*factor) - radius + max );

            double x = cos(M_PI_2 * factor);
            x *= x * interval;

            factor = val + x;
            factor *= expand;

            double ff = 2*(sqrt(magnitude)-1)*factor+1;
            if (ff!=0)
            {
                pt.x/=ff;
                pt.y*=magnitude;
                pt.z/=ff;
            }
        }
    }
    // end of squash algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * weight;
    vstore3(pt, positionId , finalPos);
}

//------------------------------------------------------------------------------
#if 0
__kernel void deformFlare(
    __global float             * finalPos ,
    __global const float       * initialPos,
    __global struct MatrixPair * matrices,
    __global const double      * params,
    const float                  envelope ,
    const uint                   positionCount
    )
{
    unsigned int positionId = get_global_id(0);
    if ( positionId >= positionCount )
        return;

    float16 deformToGeom = matrices->deformToGeom;
    float16 geomToDeform = matrices->geomToDeform;

    float3 origPt = vload3(positionId, initialPos);
    float3 pt = transformPoint(geomToDeform, origPt);

    // Flare algorithm
    {
        double lowBound    = params[0];
        double highBound   = max(params[1], lowBound);
        double startFlareX = params[2];
        double startFlareZ = params[3];
        double endFlareX   = params[4];
        double endFlareZ   = params[5];
        double curve       = params[6];

        double y = clamp((double)pt.y, lowBound, highBound);

        double relativeY;
        double diff = (highBound - lowBound);
        if (diff == 0.)
        {
            if (pt.y > highBound)
                relativeY = 1.0;
            else
                relativeY = 0.0;
        }
        else
        {
            relativeY = (y-lowBound)/diff;
        }

        pt.x *= lerp(relativeY, startFlareX, endFlareX);
        pt.z *= lerp(relativeY, startFlareZ, endFlareZ);

        double s = sin(relativeY*M_PI);
        s *= curve;
        s += 1.;
        pt.x *= s;
        pt.z *= s;
    }
    // end of flare algorithm

    float3 delta = transformPoint(deformToGeom, pt) - origPt;
    pt = origPt + delta * envelope;
    vstore3(pt, positionId , finalPos);
}
#endif