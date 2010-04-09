import unittest

class RateLimit(object):
    """
    Rate accumulator - using exponential decay over time.
    
    At any time, we can query the "current value" of a rate of values, and test if it has exceeded
    a specified threshold.  In the absence of updated values, the value of the level will
    drop by half each secs_half seconds.
    """
    def __init__(self, threshold, secs_half=60):
        self.value = 0.0
        self.threshold = threshold
        self.k = 0.5 ** (1.0/secs_half)
        self.secs_last = 0
        
    def is_exceeded(self, secs, value=1.0):
        """
        Update and return the current value of the accumulator IFF the accumulated
        value would not exceed the given threshold.
        """
        # Error - should not go back in time - just fail
        if secs < self.secs_last:
            return True

        _is_exceeded = self.current_value(secs) + value > self.threshold
        
        # Only update the score on success - allows minimum rate through
        # regardless of how frequently it is called.
        if not _is_exceeded:
            self.value += value
            
        return _is_exceeded
    
    def current_value(self, secs, value=0):
        """
        Return the value for the current time.  If value is given, add it
        to the current value (regardless of the threshold limit).
        """
        # Invalid time - return the value at the latest time, if a past time is given
        if secs < self.secs_last:
            return self.value
        
        # Decay current value
        self.value *= (self.k ** (secs - self.secs_last))
        self.secs_last = secs
        self.value += value
        
        return self.value

class TestRateLimit(unittest.TestCase):
    def test_base(self):
        rate = RateLimit(0)
        self.assertEqual(rate.current_value(10), 0)
        v = rate.current_value(20, 100)
        self.assertEqual(v, 100)
        self.assertEqual(rate.current_value(20), 100)
        self.assertAlmostEqual(rate.current_value(80), 50)
        self.assertAlmostEqual(rate.current_value(140), 25)
        
        rate = RateLimit(0)
        v = rate.current_value(1)
        for x in range(1, 100):
            v2 = rate.current_value(x,1)
            self.assert_(v2 > v)
            self.assert_(v2 < 100)
            v = v2

    def test_limits(self):
        rate = RateLimit(75)
        for x in range(1,200):
            v = rate.current_value(x)
            self.assert_(v <= 75)
            if rate.is_exceeded(x):
                break
        self.assert_(x > 100)
        
    def test_converge(self):
        for half in range(1,50,10):
            rate = RateLimit(100,half)
            limit = 1.0/(1.0 - rate.k)
            for x in xrange(half*10):
                rate.is_exceeded(x)
            #print "Half life: %d -> %.2f" % (half, rate.current_value(x))           
            self.assertAlmostEqual(rate.current_value(x), limit, 0)
        
if __name__ == '__main__':
    unittest.main()


