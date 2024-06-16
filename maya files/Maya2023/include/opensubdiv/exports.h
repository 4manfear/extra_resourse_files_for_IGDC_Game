#ifndef OPENSUBDIV3_EXPORTS
#define OPENSUBDIV3_EXPORTS

#ifdef WIN32
#  ifdef OPENSUBDIV_AS_DLL
#    define OPENSUBDIV_EXPORT __declspec(dllexport)
#  else
#    define OPENSUBDIV_EXPORT __declspec(dllimport)
#  endif
#else
#  define OPENSUBDIV_EXPORT
#endif

#endif