"""
   new_morse.py - exploring the efficiency of mores code and alternative encodings.
"""

import operator

aMorse = ['.-', '-...', '-.-.', '-..', '.',             # A-E
          '..-.', '--.', '....', '..', '.---',          # F-J
          '-.-', '..-.', '--', '-.', '---',             # K-O
          '.--.', '--.-', '.-.', '...', '-',            # P-T
          '..-', '...-', '.--', '-..-', '-.--', '--..'  # U-Z
          ]

# Approx letter frequency from http://en.wikipedia.org/wiki/Letter_frequency
aFreq = [
    8.167, 1.492, 2.782, 4.253, 12.702,     # A-E
    2.228, 2.015, 6.094, 6.966, 0.153,      # F-J
    0.772, 4.025, 2.406, 6.749, 7.507,      # K-O
    1.929, 0.095, 5.987, 6.327, 9.056,      # P-T
    2.758, 0.978, 2.360, 0.150, 1.974, 0.074 # U-Z
    ]

sum_freq = reduce(operator.add, aFreq)
aFreq = [aFreq[i]/sum_freq for i in range(len(aFreq))]

def print_by_length(aMorse):
    n = len(aMorse)
    aStats = [(chr(65+i), aMorse[i], code_length(aMorse[i])) for i in range(n)]
    aStats.sort(lambda x,y: x[2]-y[2])
    for c in aStats:
        print "%s %s : %d" % c
        
    avg = reduce(operator.add, [aStats[i][2]*aFreq[i] for i in range(n)])
    
    print "Average length: %f" % avg
    
def code_length(sMorse):
    return sMorse.count('.') + 3 * sMorse.count('-') + len(sMorse) - 1

def enum_morse():
    """ Enumerate morse-like patterns in order of length """
    size = 1
    while True:
        for pattern in enum_morse_size(size):
            yield pattern
        size += 2
            
def enum_morse_size(size):
    assert(size >= 1 and size % 2 == 1)
    if size == 1:
        yield '.'
        return
    if size == 3:
        yield '-'
        yield '..'
        return
    for p in enum_morse_size(size-4):
        yield '-' + p
    for p in enum_morse_size(size-2):
        yield '.' + p

if __name__ == '__main__':
    import code
    
    print_by_length(aMorse)
    
    code.interact(local=globals())