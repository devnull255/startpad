/*----------------------------------------------------------------------------
	lists.h
		Templates for embedded lists.

	Copyright (C) 1993 Microsoft Corporation
	All rights reserved.

	ToDo: I'd like a single template implementation for all pointer
		instances of this template (i.e., a (void *) instance with all
		other pointer instances trivial derivations of that so the non
		inline code does not get replicated).  Actually, many functions
		only depend on the size of the link pointers and can be shared
		by ALL instances of the template.

		In looking at the cod file, we seem to be instatiating the code
		for inline members as separate callable functions (that are never
		used).  Is this an optimization bug in the compiler?

		Add InsertBefore and InsertAfter members to ListEnum<T>.

	Authors:
		MikeKo	Michael C. Koss, Microsoft

	History:
		11/22/94	MikeKo	Created.
 ----------------------------------------------------------------------------*/


/*!C---------------------------------------------------------------------------
	List class
		Templates for embedded lists.

	There are two public templates and one internal implementation template
	in the lists class template.

	To create a list of elements of type T:

		List<T> lt;

	The members available on a List<T> are:

			.Insert(t)	Insert at the head of the list.
			.Remove()	Remove from the head of the list.
			.FEmpty()	fTrue iff the list is empty.
			.Head()		Returns (non-const) reference to the head data member.
						Assumes list non-empty.

	The definition of a list is a simple pointer (may be efficiently embedded as a
	class memeber).

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
class List
{
	friend class ListEnum<T>;
public:
	List() : m_ppltHead(0) {};
	void Insert(T t);
	void Remove();
	BOOL FEmpty() {return m_ppltHead == 0;}
	T &Head()
		{
		Assert(m_ppltHead);
		return ((ListElt<T> *) m_ppltHead)->m_t;
		}
private:
	ListElt<T> **m_ppltHead;
};

/*!C--------------------------------------------------------------------------
	CntList class
		Just like List, but maintains a count of elements in the list as well.

	Additional members over and above List<T>:

		.Count()	Returns number of elements in the list.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
 template <class T>
 class CntList : public List<T>
 {
 public:
 	CntList() : m_ct(0) {};
 	void Insert(T t);
	void Remove();
	int Count() const {return m_ct;};
private:
	int m_ct;
 };


/*!C--------------------------------------------------------------------------
	ListElt class
		Internal class for the implementation of embedded lists.

	A list element is just a next pointer and a data member.  The only
	thing implemented directly by this class is construction.  All the
	interesting functions on a ListElt are contained in the ListEnum class.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
class ListElt
{
	friend class List<T>;
	friend class ListEnum<T>;
private:
	ListElt(T t, ListElt<T> **ppltNext) : m_t(t), m_ppltNext(ppltNext) {};

	ListElt<T> **m_ppltNext;
	T m_t;
};

/*!C--------------------------------------------------------------------------
	ListEnum<T> class
		Enumerator (iterator) over an embedded list.


	To create an enumerator over a list of type T:

		ListEnum<T> enumlt(lt);

	A loop over the list (using the enumeration macro) looks like:

		ENUM(enumlt)
			{
			......enumlt.Member().....
			}

	The members of ListEnum<T> are:

		.Init()			Standard functions for the ENUM() macro.
		.FCont()
		.Next()
		.SetList(lt)	Reset the head of the list.
		.Member()		Returns a (non const) reference to the data member
						of the current list element.


	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
class ListEnum
{
public:
	ListEnum(List<T> &list) {SetList(list);}
	void SetList(List<T> &list) {m_ppltHead = (ListElt<T> **) &list.m_ppltHead;}
	void Init();
	BOOL FCont() {return m_ppltCur != 0;}
	void Next();
	T &Member() {return ((ListElt<T> *) m_ppltCur)->m_t;}
private:
	ListElt<T> **m_ppltHead;
	ListElt<T> **m_ppltCur;
	ListElt<T> **m_ppltPrev;
};

/*!--------------------------------------------------------------------------
	List<T>::Insert
		Insert an element at the head of the list.

	A new ListElt is constructed and then added to the lsit.  Any current
	enumerator over the list may become invalid.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void List<T>::Insert(T t)
{
	m_ppltHead = (ListElt<T> **) new ListElt<T>(t, m_ppltHead);
}

/*!--------------------------------------------------------------------------
	List<T>::Remove
		Remove the initial element from the list.

	Assumes a non-empy list.  Any current enumerator over the list may become
	invalid.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void List<T>::Remove()
{
	ListElt<T> **ppltNext;

	Assert(m_ppltHead);

	ppltNext = (ListElt<T> **) *m_ppltHead;
	delete (ListElt<T> *) m_ppltHead;
	m_ppltHead = ppltNext;
}

/*!--------------------------------------------------------------------------
	CntList<T>::Insert
		Insert an element at the head of the list and increment the count.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void CntList<T>::Insert(T t)
{
	List<T>::Insert(t);
	m_ct++;
}

/*!--------------------------------------------------------------------------
	CntList<T>::Remove
		Remove the initial element from the list and decrement the count.

	Detailed description.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void CntList<T>::Remove()
{
	List<T>::Remove();
	m_ct--;
}


/*!--------------------------------------------------------------------------
	ListEnum<T>::Init
		Initialize an enumeration.

	Start an enumeration over the elements of a list.  Member() begins pointing
	to the first element of the list.

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void ListEnum<T>::Init()
{
	Assert(m_ppltHead);
	m_ppltPrev = m_ppltHead;
	m_ppltCur = (ListElt<T> **) *m_ppltHead;
}

/*!--------------------------------------------------------------------------
	ListEnum<T>::Next
		Continue an enumeration over a list.

	Advance the current pointer in the list.  Assumes that we have not already
	reached the end of the list (i.e., FCont() is true).

	Author: MikeKo
 ---------------------------------------------------------------------------*/
template <class T>
void ListEnum<T>::Next()
{
	Assert(m_ppltCur);
	m_ppltPrev = m_ppltCur;
	m_ppltCur = (ListElt<T> **) *m_ppltCur;
}


