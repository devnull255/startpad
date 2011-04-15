import math
import sys

DEBUG = False

class LetterSquare():
    """ Place a word into the cells of a square grid such that
    you can trace the letters of the word by visiting adjacent
    squares.  Inspired by puzzazz.com puzzles.
    """

    def __init__(self, word):
        self.word = word.upper()
        self.letters = {}
        self.sLetters = ''
        self.fIllegal = False
        
        chLast = None
        for ch in self.word:
            if ch not in self.letters:
                ltr = Letter(ch, len(self.sLetters))
                self.letters[ch] = ltr
                self.sLetters += ch
            else:
                ltr = self.letters[ch]

            if chLast is not None:
                ltr.Contact(chLast)
                self.letters[chLast].Contact(ch)

            chLast = ch

        self.dim = int(math.sqrt(len(self.sLetters)))
        self.board = [['' for i in range(self.dim)] for i in range(self.dim)]
        self.aCorners = (((0,0), (self.dim-1, 0)),
                         ((self.dim-1, 0), (0, self.dim-1)),
                         ((0,0), (self.dim-1, self.dim-1)))

        # We don't have a perfect square of unique letters
        if len(self.sLetters) != self.dim*self.dim:
            self.fIllegal = True

        # Double letters are not allowed
        for ltr in self.letters.values():
            if ltr.ch in ltr.contacts:
                self.fIllegal = True;


        if DEBUG:
            print "\"%s\" has %d letters" % (word, len(self.sLetters))
            if not self.fIllegal:
                print "Contacts:"
                for ltr in self.letters.values():
                    print "%s:%d (%s)" % (ltr.ch, len(ltr.contacts), ''.join([ch for ch in ltr.contacts]))

    def Solve(self, solutions=1):
        try:
            self.solutions = 0
            self.solutionsMax = solutions
            self.SolveRec(0)
        except:
            pass
        
    def SolveRec(self, iPlace=0):
        if self.fIllegal:
            print "Illegal input (%s). Not a perfect square." % self.word
            return

        # Found a solution - print it
        if iPlace == self.dim*self.dim:
            if self.solutions == 0:
                print "Solution(s) for '%s'" % self.word
            self.Dump()
            self.solutions += 1
            if self.solutions == self.solutionsMax:
                raise Exception("Found max solutions")
            return True

        for ch in self.sLetters:
            if self.Place(iPlace, ch):
                self.SolveRec(iPlace+1)
                self.Unplace(ch)

        return False

    def Place(self, iPlace, ch):
        ltr = self.letters[ch]
        
        # Letter already used
        if ltr.pos:
            return False

        i = iPlace % self.dim
        j = iPlace / self.dim

        # Any contact letters already on the board must be adjacent
        for chT in ltr.contacts:
            pos = self.letters[chT].pos
            if pos and (abs(pos[0]-i) > 1 or abs(pos[1]-j) > 1):
                return False

        self.board[j][i] = ch

        # Canoncialize solutions by requiring:
        # UL < UL[N,0] < UL[0,N]
        # UL < UL[N,N]
        for aPos in self.aCorners:
            ch2 = self.board[aPos[1][1]][aPos[1][0]]
            if ch2 == '':
                continue
            ch1 = self.board[aPos[0][1]][aPos[0][0]]
            if self.letters[ch2].ich < self.letters[ch1].ich:
                self.board[j][i] = ''
                return False
                  
        ltr.pos = (i, j)
        return True

    def Unplace(self, ch):
        ltr = self.letters[ch]
        self.board[ltr.pos[1]][ltr.pos[0]] = ''
        self.letters[ch].pos = None

    def Dump(self, f=None):
        if not f:
            f = sys.stdout
        f.write("Board:\n")

        for i in range(self.dim):
            f.write("%s\n" % self.board[i])

        f.write("Remaining:%s\n" % ''.join([ch for ch in self.sLetters if self.letters[ch].pos is None]))

class Letter:
    def __init__(self, ch, ich):
        self.ch = ch
        self.ich = ich
        self.pos = None
        self.contacts = {}

    def Contact(self, ch):
        self.contacts[ch] = self.contacts.get(ch, 0) + 1

def Test():
    tests = ["abcdefghij", "abcdefghia", "contraindicate", "contraindications",
             "Humanitarianism", "Vindictively"]

    for test in tests:
        ls = LetterSquare(test)
        ls.Solve(3)

def Search():
    """ Look at all N letter (and greater) words to find possible
    letter squares
    """
    N = 13
    
    dict = open("dict.txt")
    words = []
    for line in dict:
        word = line.strip()
        if len(word) >= N:
            words.append(word)
    
    print "There are %d %d-letter (and longer) words in this dictionary." % (len(words), N)
        
    solutions = []
    boards = {}

    for word in words:
        ls = LetterSquare(word)
        if not ls.fIllegal:
            ls.Solve(1)
            if ls.solutions != 0:
                solutions.append(word)
                boards[word] = ls

    solutions.sort(lambda x,y: len(y)-len(x))

    # Dump 100 longest solutions into a file
    c = 100
    f = open("output.txt", 'w')
    for word in solutions:
        f.write("%s\n" % word)
        boards[word].Dump(f)
        c -= 1
        if c == 0:
            break
    f.close()

