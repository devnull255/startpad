class Flipper():
    '''
    Flip game.  Computer tries to set all bits to zero.  Opponent tries to
    keep him from doing that.  On each move, the cursor moves to the next bit
    (circular queue), and offers "1" bit moves to the computer and "0" bit
    moves to the player.  Each can either "Ignore" or "Flip" the state of the
    current bit.
    '''

    def __init__(self, size, user):
        self.size = size
        self.iLast = size - 1
        self.cOnesLast = 1
        self.bits = [0 for i in range(size)]
        self.bits[self.iLast] = 1
        
        self.i = 0
        self.user = user
        self.has_increased = False
        self.cOnes = 1

        self.moves = 0

    def __str__(self):
        st = ""
        if self.i >= 1:
            st +=  "".join(map(str, self.bits[0:self.i]))
        st += "[" + str(self.bits[self.i]) + "]"
        st += "".join(map(str, self.bits[self.i+1:]))
        return st

    def Play(self):     
        while not self.All_Zeros():
            self.moves += 1
            if (self.bits[self.i] == 0):
                self.user.Play(self)
            elif not self.has_increased:
                self.Set(0)
            self.Next()
                
        print self
        print "Computer wins after %d moves!" % self.moves

    def All_Zeros(self):
        return self.cOnes == 0

    def Set(self, bit):
        inc = bit - self.bits[self.i]
        if (inc != 0):
            print "Move %d: %s - Set to %d" % (self.moves, self, bit)

        self.cOnes += inc
        self.bits[self.i] = bit
        if (inc == 1):
            self.has_increased = True
            (cOnes, iRun) = self.MaxRun()
            if cOnes > self.cOnesLast:
                self.iLast = iRun
                self.cOnesLast = cOnes
                print "Longest run: %d ending at %d" % (self.cOnesLast, self.iLast)



    def Next(self):
        if self.i == self.iLast:
            self.has_increased = False
        self.i = (self.i + 1) % self.size

    def MaxRun(self):
        '''
        Return (cOnes, i) for ending position of max consecutive
        run of 1's in the array (including wrap around the end of the array)
        '''
        cOnesMax = 0
        cOnes = 0
        cOnesPre = 0
        fPrefix = True
        for i in range(self.size):
            if self.bits[i] == 1:
                cOnes += 1
                if cOnes > cOnesMax:
                    cOnesMax = cOnes
                    iMax = i
            else:
                if fPrefix:
                    fPrefix = False
                    cOnesPre = cOnes
                    iPre = i-1
                cOnes = 0

        if cOnesPre + cOnes > cOnesMax:
            return (cOnesPre + cOnes, iPre)

        return (cOnesMax, iMax)


# Interactive Console User Player
class UserConsole():
    def __init__(self):
        pass
        
    def Play(self, flip):
        print "Move %d: %s" % (flip.moves, flip)
        bit = int(raw_input("Set value (0 or 1):"))
        flip.Set(bit)

# Test player
class UserTest():
    def __init__(self):
        self.Reset()

    def Reset(self):
        pass

    def Play(self, flip):
        if not flip.has_increased and flip.i != (flip.iLast + 1) % flip.size:
            flip.Set(1)


# Some rudimentary test cases
# ToDo: Move to PyUnit format and move to package test directory?
if __name__ == "__main__":
    user = UserTest()

    for size in range(2, 10):
        user.Reset()
        flip = Flipper(size, user)
        flip.Play()
        #assert(flip.moves == size * 2**(size-3))

    Flipper(7, UserConsole()).Play()

