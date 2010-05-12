import sys
import random

sAlpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
sAlphaLower = sAlpha.lower()

class CryptoSolver():
    """ Solve crytpogram puzzles.

    Class variables:
      aWordList - list of words from our dictionary
      maWordList - dictionary of lists of words of different lengths
      msCandidates - candidate letters for each cipertext letter
    """

    _fileDict = open("ospd.txt")
    maWordList = {}
    aWordList = []
    for _word in _fileDict:
        _word = _word.strip().upper()
        _cch = len(_word)
        if _cch not in maWordList:
            maWordList[_cch] = []
        maWordList[_cch].append(_word)
        aWordList.append(_word)
    _fileDict.close()
                      
    def __init__(self):
        self.InitCandidates()

    def InitCandidates(self):
        self.msCandidates = {}
        for ch in sAlpha:
            self.msCandidates[ch] = sAlpha.replace(ch, '')

    def FindIt(self):
        import re
        reg = re.compile("^.(?P<h>.)..(?P=h){2}$")
        for word in self.aWordList:
            if reg.match(word):
                print word

        reg = re.compile("^.ESH.$")
        for word in self.aWordList:
            if reg.match(word):
                print word

    def WordPattern(self, sPattern):
        """ Return array of all words (in our dictionary) that match the given word patter (given the
        current restrictions on the candidate letters for each cipher text letter.  Lower case letters
        are used for ciphertext, uppercase, for known plaintext letters
        """

        aMatches = []
        cch = len(sPattern)

        mKnowns = set()
        for ch in sPattern:
            if ch in sAlpha:
                mKnowns.add(ch)
        
        for word in self.maWordList[cch]:
            fMatch = True
            for i in range(cch):
                ch = sPattern[i]
                if ch in sAlpha:
                    if word[i] != ch:
                        fMatch = False
                        break
                else:
                    if word[i] in mKnowns:
                        fMatch = False
                        break
            if fMatch:
                aMatches.append(word)
        return aMatches
                
                

# --------------------------------------------------------------------
# Unit Tests
# --------------------------------------------------------------------
import unittest

class TestCrypto(unittest.TestCase):
    def test_Basic(self):
        cs = CryptoSolver()
        self.assert_('A' in cs.msCandidates['B'])
        self.assert_(not 'A' in cs.msCandidates['A'])

    def test_WordPattern(self):
        cs = CryptoSolver()
        print "testing"
        matches = cs.WordPattern("aOOb")
        print matches
        self.assert_(len(matches) >= 30)
        self.assert_("FOOD" in matches)
        matches = cs.WordPattern("aEbcEE")
        print matches
        self.assert_(len(matches) >= 2)

if __name__ == '__main__':
    unittest.main()
