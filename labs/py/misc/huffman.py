"""
   Huffman coding utilities.
   
   - Tree building
   - Encoding/decoding strings
   
   (c) 2010 Mike Koss
"""

import heapq

def same_weight_chars(sSyms):
    return zip(list(sSyms), (1,) * len(sSyms))

""" Output symbols are lists of tuples: (string, cost) """
binary_output = same_weight_chars('01')
morse_output = [('.', 1), ('-', 3)]
alpha_output = same_weight_chars(''.join([chr(65+i) for i in range(26)]))

""" Input symbols are list of tuples: (string/char, freq)
    Approx letter frequency from http://en.wikipedia.org/wiki/Letter_frequency
"""
alpha_input = [
    ('A', 8.167), ('B', 1.492), ('C', 2.782), ('D', 4.253), ('E', 12.702),
    ('F', 2.228), ('G', 2.015), ('H', 6.094), ('I', 6.966), ('J', 0.153),
    ('K', 0.772), ('L', 4.025), ('M', 2.406), ('N', 6.749), ('O', 7.507),
    ('P', 1.929), ('Q', 0.095), ('R', 5.987), ('S', 6.327), ('T', 9.056),
    ('U', 2.758), ('V', 0.978), ('W', 2.360), ('X', 0.150), ('Y', 1.974),
    ('Z', 0.074)
    ]

def build_huffman(input_symbols, output_symbols=binary_output):
    """ Build a huffman encoding for a given set of input symbols, using
    the (optionally) specified set of output symbols.
    
    Input symbols in list of tuples: (string, freq)
    """
    heap = [(sym[1], {'sym':sym[0]}) for sym in input_symbols]
    heapq.heapify(heap)
    while len(heap) >= 2:
        left, right = heapq.heappop(heap), heapq.heappop(heap)
        parent = (left[0]+right[0], {'left':left, 'right':right})
        heapq.heappush(heap, parent)
        
    def build_dict(node, prefix):
        if 'sym' in node[1]:
            d[node[1]['sym']] = prefix
            return
        
        build_dict(node[1]['left'], prefix + '0')
        build_dict(node[1]['right'], prefix+ '1')
    
    d = {}
    build_dict(heap[0], '')
    return d

if __name__ == '__main__':
    import code
    import pprint
    
    pp = pprint.PrettyPrinter()
    
    heap = build_huffman(alpha_input)
    pp.pprint(heap)
    
    code.interact(local=globals())