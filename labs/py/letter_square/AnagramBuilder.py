import sys
import random

sAlpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

minDict = 3

def Canonical(s):
    s = s.strip().upper()
    a = [ch for ch in s]
    a.sort()
    return ''.join(a)

class WordHist():
    def __init__(self, s):
        self.mch = {}
        for ch in s:
            self.mch[ch] = self.mch.get(ch, 0) + 1

    def FInWord(self, s):
        # Optimize to not even call full histogram of test word
        for ch in s:
            if ch not in self.mch:
                return False

        wh = WordHist(s)
        for ch in wh.mch:
            if wh.mch[ch] > self.mch.get(ch, 0):
                return False
        return True

class AnagramBuilder():
    """ Create angramming puzzles by chosing N letters at random.
    Can set a minimum number of total words desired from puzzle.

    Class variables:
      aWordList - list of words from our dictionary
      maWordList - dictionary of lists of words of different lengths
    """

    _fileDict = open("ospd.txt")
    maWordList = {}
    aWordList = []
    for _word in _fileDict:
        _word = _word.strip().upper()
        _cch = len(_word)
        if _cch < minDict:
            continue
        if _cch not in maWordList:
            maWordList[_cch] = []
        maWordList[_cch].append(_word)
        aWordList.append(_word)
    _fileDict.close()
                      
    def __init__(self, maxLen=6, minWords=20, minLen=3):
        self.maxLen = maxLen
        self.minWords = minWords
        self.minLen = minLen

    def GenerateValid(self):
        while True:
            self.Generate()
            if len(self.aWords) >= self.minWords:
                return
            
    def Generate(self, sChoice=None):
        """ Generate a puzzle by picking a maxLen sized word - letters returned in sorted order. """
        if sChoice is None:
            sChoice = random.choice(self.maWordList[self.maxLen])
        self.aLetters = [ch for ch in sChoice]
        self.aLetters.sort()
        self.sLetters = ''.join(self.aLetters)
        wh = WordHist(sChoice)
        self.aWords = []
        for word in self.aWordList:
            if len(word) < self.minLen:
                continue
            if wh.FInWord(word):
                self.aWords.append(word)

        self.aWords.sort(lambda x,y: len(x) - len(y))

    def Print(self, f=None):
        if not f:
            f = sys.stdout
        f.write("{letters:'%s',\n" % self.sLetters)
        f.write(" words:[\n")
        chSep = ''
        for word in self.aWords:
            f.write("%s'%s'" % (chSep, word) )
            chSep = ', '
        f.write("]\n}\n")

def BestAnagrams(size=6):
    """ Try all words of a given length, and count how many anagrammed words are contained within
    each of them.
    """

    ab = AnagramBuilder(maxLen=size)
    mHist = {}
    cwMax = 0
    for word in ab.maWordList[size]:
        ab.Generate(word)
        cw = len(ab.aWords)
        print cw
        if cw not in mHist:
            mHist[cw] = 0
        mHist[cw] += 1
        if cw > cwMax:
            cwMax = cw
            aBest = []
        if cw == cwMax:
            aBest.append(word)
            ab.Print()

    print "Best words"
    for word in aBest:
        print word
        
def RunProfile():
    import cProfile, pstats, StringIO, logging
    prof = cProfile.Profile()
    prof = prof.runctx("ProfileTest()", globals(), locals())
    stream = StringIO.StringIO()
    stats = pstats.Stats(prof, stream=stream)
    stats.sort_stats("time")  # time or cumulative
    stats.print_stats(80)  # lines to print
    # The rest is optional.
    # stats.print_callees()
    # stats.print_callers()
    print "Profile data:\n%s" % stream.getvalue()

def ProfileTest():
    ab = AnagramBuilder()
    ab.Generate('SAMPLES')
    ab.Print()


# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

class TestWordHist(unittest.TestCase):
    def test_Basic(self):
        wh = WordHist('CAT')
        self.assertEqual(wh.FInWord('AT'), True)
        self.assertEqual(wh.FInWord('DOG'), False)
        self.assertEqual(wh.FInWord('ACT'), True)
        self.assertEqual(wh.FInWord('CATX'), False)
        

class TestAnagram(unittest.TestCase):
    def test_Basic(self):
        ab = AnagramBuilder()
        ab.GenerateValid()
        self.assert_(len(ab.aWords) >= ab.minWords)

if __name__ == '__main__':
    unittest.main()
