/*----------------------------------------------------------------------------
	mstrmind.cpp
		Mastermind playing program

	Copyright (C) 1995 Michael C. Koss
	All rights reserved.

	Authors:
		MikeKo	Michael C. Koss, Microsoft

	History:
		05/14/95	MikeKo	Created.
 ----------------------------------------------------------------------------*/
#include <stdio.h>
#include <stdlib.h>
#define NOAFX
#include "std.h"

// Total number of pegs
#define iclrMax 5

typedef int CLR;
#define clrRed 0
#define clrWhite 1
#define clrBlue 2
#define clrGreen 3
#define clrYellow 4
#define clrBlack 5
#define clrMax 5
//char *mpclrsz[clrMax] = {"Red", "White", "Blue", "Green", "Yellow", "Black"};
char *mpclrsz[] = {"Square", "Circle", "Triangle", "Diamond", "+", "X", "V", "@"};

class State
{
	friend class Response;
public:
	void Init();
	BOOL FCont();
	void Next();

	void Print() const;
	void PrintProgress() const;
	void Set(int iclr, CLR clr);
	void SetIstate(int istate);
	int Istate() const;
	BOOL operator==(const State &s);

private:
	int m_istate;
	CLR m_rgclr[iclrMax];
};

class StateSet
{
	friend class EnumStateSet;

public:
	StateSet();
	~StateSet();
	void All();
	void None();
	void BestGuess(State *psGuess);
	void Reduce(const State &sGuess, const Response &r);
	int Size();
	void Add(const State &s);
	BOOL FMember(const State &s) const;
	static int istateMax;
	
private:
	void SetF(BOOL f);

	int *m_mpistatef;
};

int StateSet::istateMax;

void State::Init()
{
	int iclr;

	m_istate = 0;
	for (iclr = 0; iclr < iclrMax; iclr++)
		m_rgclr[iclr] = 0;
}

BOOL State::FCont()
{
	return m_istate != StateSet::istateMax;
}

void State::Next()
{
	int iclr;

	m_istate++;

	for (iclr = 0; iclr < iclrMax; iclr++)
		{
		if (m_rgclr[iclr] < clrMax-1)
			{
			m_rgclr[iclr]++;
			return;
			}
		m_rgclr[iclr] = 0;
		}
}

void State::Print() const
{
	int iclr;
	
	for (iclr = 0; iclr < iclrMax; iclr++)
		{
		printf("%s ", mpclrsz[m_rgclr[iclr]]);
		}
	printf("\n");
}

void State::PrintProgress() const
{
	if (m_istate % 100 == 0)
		printf("Progress %d of %d.\n", m_istate, StateSet::istateMax);
}

void State::Set(int iclr, CLR clr)
{
	m_rgclr[iclr] = clr;
}


void State::SetIstate(int istate)
{
	int iclr;

	for (iclr = 0; iclr < iclrMax; iclr++)
		{
		m_rgclr[iclr] = istate % clrMax;
		istate = istate / clrMax;
		}
	Assert(istate == 0);
}

int State::Istate() const
{
	int istate = 0;
	int iclr;

	for (iclr = iclrMax-1; iclr >= 0; iclr--)
		{
		istate = istate * clrMax + m_rgclr[iclr];
		}
	return istate;
}

BOOL State::operator==(const State &s)
{
	int iclr;

	for (iclr = 0; iclr < iclrMax; iclr++)
		if (m_rgclr[iclr] != s.m_rgclr[iclr])
			return fFalse;
	return fTrue;
}

class EnumStateSet
{
	friend class StateSet;

public:
	EnumStateSet(const StateSet &ss);
	void Init();
	BOOL FCont();
	void Next();
	const State &S();

private:
	const StateSet &m_ss;
	int m_istateCur;
	State m_s;
};

EnumStateSet::EnumStateSet(const StateSet &ss) :
	m_ss(ss),
	m_istateCur(0)
{
}

void EnumStateSet::Init()
{
	m_istateCur = -1;
	Next();
}

BOOL EnumStateSet::FCont()
{
	return m_istateCur < StateSet::istateMax;
}

void EnumStateSet::Next()
{
	for (m_istateCur++;
	m_istateCur < StateSet::istateMax && m_ss.m_mpistatef[m_istateCur] == fFalse;
		 m_istateCur++) ;
}

const State &EnumStateSet::S()
{
	m_s.SetIstate(m_istateCur);
	return m_s;
}

class Response
{
	friend class ResponseSet;

public:
	void SetResponse(const State &sGuess, const State &sHidden);
	BOOL operator!=(const Response &r) const;
	void Input();
	int CpegBlack() const;

private:
	int m_cpegColorOK;		// Only color
	int m_cpegColorPosOK;		// Color and position
};

void Response::SetResponse(const State &sGuess, const State &sHidden)
{
	int iclrGuess;
	int iclrHid;
	State sH = sHidden;
	State sG = sGuess;

	m_cpegColorOK = 0;
	m_cpegColorPosOK = 0;
	
	for (iclrGuess = 0; iclrGuess < iclrMax; iclrGuess++)
		{
		if (sG.m_rgclr[iclrGuess] == sH.m_rgclr[iclrGuess])
			{
			m_cpegColorPosOK++;
			// Remove matched color from further matches
			sH.m_rgclr[iclrGuess] = clrMax;
			sG.m_rgclr[iclrGuess] = clrMax;
			}
		}

	for (iclrGuess = 0; iclrGuess < iclrMax; iclrGuess++)
		for (iclrHid = 0; iclrHid < iclrMax; iclrHid++)
			if (sG.m_rgclr[iclrGuess] != clrMax &&
					sG.m_rgclr[iclrGuess] == sH.m_rgclr[iclrHid])
				{
				Assert(iclrHid != iclrGuess);
				m_cpegColorOK++;
				sH.m_rgclr[iclrHid] = clrMax;
				// No need to patch sG - we never visit again.
				break;
				}
}

BOOL Response::operator!=(const Response &r) const
{
	return m_cpegColorOK != r.m_cpegColorOK ||
			m_cpegColorPosOK != r.m_cpegColorPosOK;
}

void Response::Input()
{
	char sz[256];

Pos:
	printf("Number of correct colors in the correct position: ");
	if (gets(sz) == NULL || sscanf(sz, "%d", &m_cpegColorPosOK) != 1)
		goto Pos;

Color:
	printf("Number of correct colors NOT in the correct position: ");
	if (gets(sz) == NULL || sscanf(sz, "%d", &m_cpegColorOK) != 1)
		goto Color;
}

int Response::CpegBlack() const
{
	return m_cpegColorPosOK;
}

class ResponseSet
{
public:
	ResponseSet();
	int CountResponse(Response &r);
	void Print();
	int ExpSize() const;
	static int ExpSizeMax();

private:
	int m_rgcResp[iclrMax+1][iclrMax+1];	// index: color, colorpos
};

ResponseSet::ResponseSet()
{
	int iclrColor;
	int iclrColorPos;
	
	for (iclrColor = 0; iclrColor < iclrMax+1; iclrColor++)
		for (iclrColorPos = 0; iclrColorPos < iclrMax+1; iclrColorPos++)
			m_rgcResp[iclrColor][iclrColorPos] = 0;
}

int ResponseSet::CountResponse(Response &r)
{
	Assert(r.m_cpegColorOK >= 0 && r.m_cpegColorOK <= iclrMax);
	Assert(r.m_cpegColorPosOK >= 0 && r.m_cpegColorPosOK <= iclrMax);
	return ++m_rgcResp[r.m_cpegColorOK][r.m_cpegColorPosOK];
}

void ResponseSet::Print()
{
	int iclrColor;
	int iclrColorPos;
	
	for (iclrColorPos = 0; iclrColorPos < iclrMax+1; iclrColorPos++)
		for (iclrColor = 0; iclrColor < iclrMax+1; iclrColor++)
			if (m_rgcResp[iclrColor][iclrColorPos])
				{
				printf("%d Black, %d White: %d possible\n",
						iclrColorPos, iclrColor,
						m_rgcResp[iclrColor][iclrColorPos]);
				}
}

int ResponseSet::ExpSize() const
{
	int iclrColor;
	int iclrColorPos;
	int cExp = 0;

	for (iclrColor = 0; iclrColor < iclrMax+1; iclrColor++)
		for (iclrColorPos = 0; iclrColorPos < iclrMax+1; iclrColorPos++)
			cExp += m_rgcResp[iclrColor][iclrColorPos] *
					m_rgcResp[iclrColor][iclrColorPos];
	return cExp;
}

int ResponseSet::ExpSizeMax()
{
	return StateSet::istateMax * StateSet::istateMax;
}

StateSet::StateSet()
{
	if (istateMax == 0)
		{
		istateMax = 1;
		for (int iclr = 0; iclr < iclrMax; iclr++)
			istateMax *= clrMax;
		}
	m_mpistatef = new int [istateMax];
}

StateSet::~StateSet()
{
	delete [] m_mpistatef;
}

void StateSet::All()
{
	SetF(fTrue);
}

void StateSet::None()
{
	SetF(fFalse);
	Assert(Size() == 0);
}

void StateSet::SetF(BOOL f)
{
	int istate;

	for (istate = 0; istate < istateMax; istate++)
		m_mpistatef[istate] = f;
}

/*!--------------------------------------------------------------------------
	StateSet::BestGuess
		Gives the remaining states in the current state set, make the
		best guess for the next move in mastermind.

		Criteria for the best guess:
			1. Minimize the maximum number of state alternatives
			   for any answer given to the guess.
			2. Pick a guess with smallest EXPECTED state remaining size.
			3. If any of the possible guesses are one of the possible
			   states, choose it (we may get lucky and answer the puzzle
			   early).

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void StateSet::BestGuess(State *psGuess)
{
	State sGuess;
	State sGuessBest;
	EnumStateSet essHidden(*this);
	int cResponseMinMax = istateMax;
	StateSet ssBests;

	ENUM(sGuess)
		{
		ResponseSet rs;
		Response r;
		int cResponseMax = 0;
		int cResponse;

		sGuess.PrintProgress();
		ENUM(essHidden)
			{
			r.SetResponse(sGuess, essHidden.S());
			cResponse = rs.CountResponse(r);
			if (cResponse > cResponseMax)
				{
				cResponseMax = cResponse;
				}
			}

		if (cResponseMax < cResponseMinMax)
			{
			cResponseMinMax = cResponseMax;

			printf("Better max: %d with guess: ", cResponseMax);
			sGuess.Print();
			ssBests.None();
			}
		if (cResponseMax == cResponseMinMax)
			{
			ssBests.Add(sGuess);
			}
		}

	Assert(cResponseMinMax < istateMax);

	int cs;
	int csBest = 0;
	BOOL fMember;

	cs = ssBests.Size();
	Assert(cs >= 1);
	printf("%d guesses yield the mini-max (%d) of remaining states.\n",
			cs, cResponseMinMax);
	
	EnumStateSet essBests(ssBests);
	int cRespExp;
	int cRespExpMin = ResponseSet::ExpSizeMax();

	ENUM(essBests)
		{
		ResponseSet rs;
		Response r;
		
		ENUM(essHidden)
			{
			r.SetResponse(essBests.S(), essHidden.S());
			rs.CountResponse(r);
			}
		//printf("Responses for guess ");
		//essBests.S().Print();
		//rs.Print();
		cRespExp = rs.ExpSize();
		if (cRespExp < cRespExpMin)
			{
			cRespExpMin = cRespExp;
			sGuessBest = essBests.S();
			fMember = FMember(sGuessBest);
			printf("Better distribution: ");
			if (fMember)
				printf("(could be solution) ");
			sGuessBest.Print();
			rs.Print();
			csBest = 0;
			}
		if (cRespExp == cRespExpMin)
			{
			csBest++;
			if (!fMember && FMember(essBests.S()))
				{
				sGuessBest = essBests.S();
				printf("Found an equivalent guess that COULD be the answer: ");
				sGuessBest.Print();
				rs.Print();
				fMember = fTrue;
				}
			}
		}

	printf("%d/%d had the best distribution of states.\n", csBest, cs);
	
	*psGuess = sGuessBest;
}

void StateSet::Reduce(const State &sGuess, const Response &r)
{
	EnumStateSet ess(*this);
	Response rT;

	ENUM(ess)
		{
		rT.SetResponse(sGuess, ess.S());
		if (r != rT)
			m_mpistatef[ess.m_istateCur] = 0;
		}
	printf("Number of possible states: %d\n", Size());
	if (Size() < 20)
		{
		ENUM(ess)
			{
			ess.S().Print();
			}
		}
}

void StateSet::Add(const State &s)
{
	Assert(!FMember(s));

	m_mpistatef[s.Istate()] = fTrue;
}

BOOL StateSet::FMember(const State &s) const
{
	return m_mpistatef[s.Istate()];
}

int StateSet::Size()
{
	int istate;
	int cstate = 0;
	
	for (istate = 0; istate < istateMax; istate++)
		{
		if (m_mpistatef[istate])
			cstate++;
		}
	return cstate;
}

void _cdecl main()
{
	StateSet ss;
	StateSet ssT;
	State sGuess;
	Response r;
	int cGuesses = 0;

	ss.All();

	FOREVER
		{
		cGuesses++;
		if (cGuesses == -1)
			{
			sGuess.Set(0, clrBlack);
			sGuess.Set(1, clrWhite);
			sGuess.Set(2, clrBlack);
			sGuess.Set(3, clrWhite);
			}
		else
			ss.BestGuess(&sGuess);
Retry:
		sGuess.Print();
		r.Input();
		ssT = ss;
		ss.Reduce(sGuess, r);
		if (ss.Size() == 0)
			{
			printf("Impossible - no colors can match answers given.\n");
			ss = ssT;
			goto Retry;
			}
		if (r.CpegBlack() == iclrMax)
			{
			printf("%d guesses (including the known one).\n", cGuesses);
			exit(0);
			}
		}
}
