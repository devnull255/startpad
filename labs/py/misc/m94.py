#!/usr/bin/env python

import re
import logging

"""
M-94 Cipher device simulator.

See:
    http://maritime.org/tech/csp488.htm
    http://maritime.org/tech/csp488man.htm
"""

wheels = ['ABCEIGDJFVUYMHTQKZOLRXSPWN',
          'ACDEHFIJKTLMOUVYGZNPQXRWSB',
          'ADKOMJUBGEPHSCZINXFYQRTVWL',
          'AEDCBIFGJHLKMRUOQVPTNWYXZS',
          'AFNQUKDOPITJBRHCYSLWEMZVXG',
          'AGPOCIXLURNDYZHWBJSQFKVMET',
          'AHXJEZBNIKPVROGSYDULCFMQTW',
          'AIHPJOBWKCVFZLQERYNSUMGTDX',
          'AJDSKQOIVTZEFHGYUNLPMBXWCR',
          'AKELBDFJGHONMTPRQSVZUXYWIC',
          'ALTMSXVQPNOHUWDIZYCGKRFBEJ',
          'AMNFLHQGCUJTBYPZKXISRDVEWO',
          'ANCJILDHBMKGXUZTSWQYVORPFE',
          'AODWPKJVIUQHZCTXBLEGNYRSMF',
          'APBVHIYKSGUENTCXOWFQDRLJZM',
          'AQJNUBTGIMWZRVLXCSHDEOKFPY',
          'ARMYOFTHEUSZJXDPCWGQIBKLNV',
          'ASDMCNEQBOZPLGVJRKYTFUIWXH',
          'ATOJYLFXNGWHVCMIRBSEKUPDZQ',
          'AUTRZXQLYIOVBPESNHJWMDGFCK',
          'AVNKHRGOXEYBFSJMUDQCLZWTIP',
          'AWVSFDLIEBHKNRJQZGMXPUCOTY',
          'AXKWREVDTUFOYHMLSIQNJCPGBZ',
          'AYJPXMVKBQWUGLOSTECHNZFRID',
          'AZDNBUHYFWJLVGRCQMPSOEXTKI',
          ]


re_non_alpha = re.compile(r"[^A-Z]")

def order_from_phrase(phrase):
    """ Follow instructions in section 2 for calculating the number disk
    order from a pass-phrase.

    >>> order_from_phrase("general electric company")
    [11, 6, 17, 7, 22, 1, 14, 8, 15, 9, 3, 24, 23, 13, 4, 5, 20, 16, 21, 2, 18, 25, 12, 10, 19]
    """
    phrase = phrase.upper()
    phrase = re_non_alpha.sub('', phrase)
    if len(phrase) < 15:
        raise ValueError("Key too short - should be at least 15 characters (not %d)." %
                         len(phrase))

    if len(phrase) < 25:
        phrase = phrase + phrase

    phrase = phrase[:25]

    order = [0] * 25

    n = 1
    for i in range(26):
        ch = chr(ord('A') + i)
        s = 0
        while s != -1:
            s = phrase.find(ch, s)
            if s != -1:
                order[s] = n
                n += 1
                s += 1

    return order
