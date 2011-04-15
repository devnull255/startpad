#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NOAFX

#include <std.h>
#include <lists.h>

HungarianClass(CharHist, CHST)
HungarianClass(Word, WRD)

/*!C--------------------------------------------------------------------------
	CharHist class
		Character histogram.

	Counts the number of alphabetic characters in the passed in string (separate
	count for each of A..Z).  Some simple addition and subtraction of historgrams
	is also provided.

	Member functions:
		.SetString(sz)	Initialize the histogram from a zero terminated string.
		.FSubHist(chst)	Subtract the given histogram from this (return fFalse if
						there are negative histogram elements).
		.AddHist(chst)	Add the given histogram to this.
		.FAnagram(chst)	fTrue iff the given histogram is identical to this.
		.FEmpty()		fTrue if all character counts are zero.		

	Author: MikeKo
 ---------------------------------------------------------------------------*/
class CharHist
{
public:
	CharHist();
	void SetString(const char *sz);
	BOOL FSubHist(const CharHist &chst);
	void AddHist(const CharHist &chst);
	BOOL FAnagram(const CharHist &chst) const;
	BOOL FEmpty() const;
	int Count() const;

private:
	int m_rgcch[26];
};

/*!C--------------------------------------------------------------------------
	Word class
		Combines CharHist with buffer for storing the original word.

	Really just a structure that bundles up the CharHist and a character
	buffer.  Used as a member of a List<Word> class.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
class Word
{
public:
	Word(const char *sz);
	const CharHist &Chst() const { return m_chst; }
	const char *Sz() const {return m_rgch;}

private:
	CharHist m_chst;
	char m_rgch[32];
};

/*!--------------------------------------------------------------------------
	CharHist::CharHist
		Character historgram constructor.

	Initializes all counts to zero.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
CharHist::CharHist()
{
	for (int icch = 0; icch < 26; icch++)
		m_rgcch[icch] = 0;
}

/*!--------------------------------------------------------------------------
	CharHist::SetString
		Initialized the histogram from the alphabetic characters in the given
		string.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void CharHist::SetString(const char *sz)
{
	unsigned ch;

	for (; ch = *sz; sz++)
		{
		if (ch >= 'A' && ch <= 'Z')
			ch += 'a' - 'A';
		else if (ch < 'a' || ch > 'z')
			continue;
		Assert(ch >= 'a' && ch <= 'z');
		m_rgcch[ch - 'a']++;
		}
}


/*!--------------------------------------------------------------------------
	CharHist::FAnagram
		Compares histograms for element by element equality.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
BOOL CharHist::FAnagram(const CharHist &chst) const
{
	for (int icch = 0; icch < 26; icch++)
		if (m_rgcch[icch] < chst.m_rgcch[icch])
			return fFalse;

	return fTrue;
}

/*!--------------------------------------------------------------------------
	CharHist::FEmpty
		Return fTrue iff all character counts are zero.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
BOOL CharHist::FEmpty() const
{
	for (int icch = 0; icch < 26; icch++)
		if (m_rgcch[icch])
			return fFalse;
	return fTrue;
}

int CharHist::Count() const
{
	int cch = 0;

	for (int icch = 0; icch < 26; icch++)
		cch += m_rgcch[icch];

	return cch;
}

/*!--------------------------------------------------------------------------
	CharHist::FSubHist
		Subtracts given histogram from this one.

	Returns fFalse iff there are negative counts in the result.  The following
	is guaranteed to be a no-op:

		chst.FSubHist(chst1);
		chst.AddHist(chst1);

	Author: MikeKo
 ---------------------------------------------------------------------------*/
BOOL CharHist::FSubHist(const CharHist &chst)
{
	BOOL fRet = fTrue;

	for (int icch = 0; icch < 26; icch++)
		{
		m_rgcch[icch] -= chst.m_rgcch[icch];
		if (m_rgcch[icch] < 0)
			fRet = fFalse;
		}
	return fRet;		
}

/*!--------------------------------------------------------------------------
	CharHist::AddHist
		Adds given histogram to this one.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void CharHist::AddHist(const CharHist &chst)
{
	for (int icch = 0; icch < 26; icch++)
		m_rgcch[icch] += chst.m_rgcch[icch];
}

/*!--------------------------------------------------------------------------
	Word::Word
		Construct a word from the given zero terminated string.

	We do not copy any end-of-line characters into the local buffer.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
Word::Word(const char *sz)
{
	const char *pchIn = sz;
	char *pch = m_rgch;
	char *pchMax = m_rgch + sizeof(m_rgch);

	for (; *pchIn && pch < pchMax-1; pchIn++)
		{
		if (*pchIn != '\n' && *pchIn != '\r')
			*pch++ = *pchIn;
		
		}
	*pch = 0;
		
	 m_chst.SetString(sz);
}

void Anagrams(FILE *pfileDict, const CharHist &chstWord, List<Word> *plwrd);
void FullAnagrams(const CharHist &chstSrc, List<Word> lwrd, int cwrd);

/*!--------------------------------------------------------------------------
	main
		Program entry point.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void main(int csz, char *rgsz[])
{
	FILE *pfileDict;
	List<Word> lwrd;
	CharHist chst;
	int cwrd;

	if (csz != 2)
		{
		fprintf(stderr, "Need a single word argument\n");
		exit(1);
		}

	pfileDict = fopen("dict.txt", "r");
	if (pfileDict == NULL)
		{
		fprintf(stderr, "Can't open dictionary: %s\n", "dict.txt");
		exit(1);
		}

	chst.SetString(rgsz[1]);
	Anagrams(pfileDict, chst, &lwrd);
	for (cwrd = 1; cwrd <= (int) (strlen(rgsz[1])+2)/3; cwrd++)
		FullAnagrams(chst, lwrd, cwrd);

	fclose(pfileDict);
}

/*!--------------------------------------------------------------------------
	Anagrams
		Search through dictionary file for sub-anagrams of the given character
		histogram.

	Anagrams are printed to standard out and added to the passed in list.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void Anagrams(FILE *pfileDict, const CharHist &chstWord, List<Word> *plwrd)
{
	char szDWord[256];
	int cwrd = 0;

	rewind(pfileDict);

	while (fgets(szDWord, sizeof(szDWord), pfileDict))
		{
		CharHist chstD;

		chstD.SetString(szDWord);
		if (chstWord.FAnagram(chstD) && chstD.Count() > 2)
			{
			printf("Anagram: %s", szDWord);
			plwrd->Insert(Word(szDWord));
			cwrd++;
			}
		}
	printf("Total: %d\n", cwrd);
}

typedef ListEnum<Word> ELWRD;

/*!--------------------------------------------------------------------------
	FullAnagrams
		Finds all combinations of words from the given list that add up exactly
		to match the given histogram.

	We maintain a list of word-list enumerators.  The current list state
	represents the words we have successfully sub anagramed.  For each level,
	begin search at current word and continue through end of list (so we do not
	find each n word phase n times).

	We limit output to Anagrams that are precisely cwrd words in length.

	Preconditions of the loop:  The current word of the deepest enumerator
	has yet to be subtracted from the current histogram.

	Loop: Subtract current word.  If OK, create sub enumeration from the current
	one and continue.  If not OK, add the word back in and advance the enumerator.
	If the current enumerator is exhausted, pop the enumerator, and advance the
	outer enumerator.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
void FullAnagrams(const CharHist &chstSrc, List<Word> lwrd, int cwrd)
{
	CntList<ELWRD> lelwrd;
	ListEnum<Word> elwrd(lwrd);
	CharHist chst;
	BOOL fFoundSome = fFalse;

	elwrd.Init();
	lelwrd.Insert(elwrd);
	chst = chstSrc;

	FOREVER
		{
		Assert(lelwrd.Count() <= cwrd);

		// Current enumerator exhausted
		if (!lelwrd.Head().FCont())
			{
			lelwrd.Remove();
			if (lelwrd.FEmpty())
				break;
			chst.AddHist(lelwrd.Head().Member().Chst());
			lelwrd.Head().Next();
			}
		// Successfully subtracted current word - make a sub enumeration
		else if (chst.FSubHist(lelwrd.Head().Member().Chst()))
			{
			if (lelwrd.Count() == cwrd)
				{
				// Found an anagram of cwrd words.
				if (chst.FEmpty())
					{
					ListEnum<ELWRD> elelwrd(lelwrd);

					printf("Full anagram: ");

					ENUM(elelwrd)
						printf("%s ", elelwrd.Member().Member().Sz());

					printf("\n");
					fFoundSome = fTrue;
					}
				goto ContEnum;
				}

			lelwrd.Insert(lelwrd.Head());
			}
		// Word does not work - add it back in and advance enumerator
		else
			{
ContEnum:
			chst.AddHist(lelwrd.Head().Member().Chst());
			lelwrd.Head().Next();
			}
		}

	if (!fFoundSome)
		printf("No anagrams using %d word%s.\n", cwrd, cwrd > 1 ? "s" : "");
}
