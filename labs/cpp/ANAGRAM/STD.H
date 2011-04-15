/*----------------------------------------------------------------------------
	std.h
		Standard header file.

	Copyright (C) 1993 Microsoft Corporation
	All rights reserved.

	Authors:
		MikeKo	Michael C. Koss, Microsoft

	History:
		11/18/93	MikeKo	Created.
 ----------------------------------------------------------------------------*/
#ifdef _STD_H
#error std.h included twice!
#else
#define _STD_H

#ifndef NOAFX
#ifndef __AFX_H__
#include <afx.h>
#endif
#endif

#ifndef BOOL
typedef int BOOL;
#endif

#ifndef FALSE
#define FALSE 0
#define TRUE 1
#endif

#define PURE = 0;
#define IMPL ;

#define fTrue (TRUE)
#define fFalse (FALSE)

#define FAssign(f)			((f) != 0)
#define FImplies(f1, f2)	(!(f1) || (f2))
#define FOREVER				for (;;)

#ifdef NOAFX

#ifdef _DEBUG
#define DEBUG
#endif

#ifdef DEBUG

#ifndef _INC_STDLIB
#include <stdlib.h>
#endif

void AssertFailedLine(char *szFileName, int nLine, char *sz);
#define Assert(f) if (!(f)) AssertFailedLine(__FILE__, __LINE__, #f);
#define SideAssert(f) Assert(f)
#else
#define Assert(f)
#define SideAssert(f) f
#endif

#else // AFX

#define Assert ASSERT
#define SideAssert VERIFY

#endif

#define Panic() Assert(fFalse)
#define NYI() Panic()

#define CodeSz(szName, sz) static const char BASED_CODE szName[] = sz

#ifndef MAKELONG
#define MAKELONG(low, high) ((LONG)(((WORD)(low)) | (((DWORD)((WORD)(high))) << 16)))
#endif

#define ENUM(enum) for((enum).Init(); (enum).FCont(); (enum).Next())

// BitBlt codes (not defined in windows.h)
#define DSna (0x00220326L)

#define New DEBUG_NEW

#ifdef DEBUG
#define IfDebug(x)	x
#define IfNotDebug(x)
#else
#define IfDebug(x)
#define IfNotDebug(x) x
#endif

/*---------------------------------------------------------------------------
	Standard Hungarian definitions
 ---------------------------------------------------------------------------*/
#define Hungarian(type, hung) typedef type hung;
#define HungarianNoDef(type, hung)
#define HungarianClass(klass, hung) \
	class klass; \
	typedef klass hung;

HungarianClass(CBrush, BR)
HungarianClass(CPen, PEN)
HungarianClass(CRect, RC)
HungarianClass(CPoint, PT)
HungarianClass(CDC, DC)
HungarianClass(CSize, DPT)
HungarianClass(CWnd, WND)
//HungarianClass(CPrintInfo, INFO)
Hungarian(char *, SZ)
HungarianClass(CString, ST)
HungarianClass(CTime, TM)
#ifdef _WIN
HungarianNoDef(MSG, MSG)
HungarianClass(CMetaFileDC, MDC)
Hungarian(HMETAFILE, HMF)
Hungarian(GLOBALHANDLE, HG)
HungarianClass(CBitmap, BMP)
Hungarian(BITMAP, BI)
HungarianNoDef(COLORREF, RGB)
#endif

/*---------------------------------------------------------------------------
	Standard Windows RGB values
 ---------------------------------------------------------------------------*/
#define rgbDkGray RGB(128, 128, 128)
#define rgbLtGray RGB(192, 192, 192)
#define rgbWhite RGB(255, 255, 255)
#define rgbBlack RGB(0, 0, 0)

/*!--------------------------------------------------------------------------
	Override
		Use in place of virtual for overridden member functions.

	Where you would previously had:

		virtual Type Func(...arg list...);

	now use:

		Override(Base, Type, Func, (...arg list...));

	If the base function changes signature, you will now get a compiler
	warning in the derived class.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
#define Override(Base, Type, Func, Args) \
	void Override##Func() {Type (Base:: *pfn)##Args = Base::Func;} \
	virtual Type Func##Args

#define OverrideConst(Base, Type, Func, Args) \
	void Override##Func() {Type (Base::*pfn)##Args; \
			*(Type (Base::**)##Args const) &pfn = Base::Func;} \
	virtual Type Func##Args const

/*---------------------------------------------------------------------------
	Serialization helpers (from std.cpp)
 ---------------------------------------------------------------------------*/
#ifndef NOAFX

void SerializeInt(CArchive &ar, int *pw);
void SerializePt(CArchive &ar, CPoint *ppt);
void SerializeSize(CArchive &ar, CSize *psize);
#ifdef _WIN
void SerializeRgb(CArchive &ar, COLORREF *prgb);
void MetaFileToClipboard(HMETAFILE hmf, CWnd *pwnd, CSize size);
#endif // _WIN

#endif

/*---------------------------------------------------------------------------
	Misc inline functions
 ---------------------------------------------------------------------------*/
#ifndef _SIZE_T_DEFINED
typedef unsigned int size_t;
#define _SIZE_T_DEFINED
#endif

inline void *operator new(size_t size, void *pv)
{
 	return pv;
}

inline int WMax(int w1, int w2)
{
	return w1 > w2 ? w1 : w2;
}

inline int WMin(int w1, int w2)
{
	return w1 < w2 ? w1 : w2;
}

#endif // _STD_H
