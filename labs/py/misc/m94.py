#!/usr/bin/env python

import re
import random
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


class M94(object):
    """ Simulate am M94 cipher machine.

    >>> M94.group_letters('thisisrunontext')
    'thisi sruno ntext'
    >>> m = M94('general electric company')
    >>> m.translate_line('hello there', 0)
    'HELLO THERE'
    >>> m.translate_line('hello there', 1)
    'UTNCT QZRLF'
    """
    re_non_alpha = re.compile(r"[^A-Z]")

    def __init__(self, phrase):
        self.order = self.order_from_phrase(phrase)

    def encode(self, message):
        results = []
        for i in range(0, len(message), 25):
            part = message[i:i + 25]
            # Should not send the current line, or the one directly above or below.
            offset = random.randint(2, 24)
            results.append(self.translate_line(part, offset))

        return '\n'.join(results)

    def translate_line(self, line, offset):
        line = self.strip(line)
        result = ''
        for i in range(len(line)):
            wheel = wheels[self.order[i] - 1]
            j = (wheel.find(line[i]) + offset) % 26
            result += wheel[j]
        return self.group_letters(result)

    @staticmethod
    def order_from_phrase(phrase):
        """ Follow instructions in section 2 for calculating the number disk
        order from a pass-phrase.

        >>> M94.order_from_phrase("general electric company")
        [11, 6, 17, 7, 22, 1, 14, 8, 15, 9, 3, 24, 23, 13, 4, 5, 20, 16, 21, 2, 18, 25, 12, 10, 19]
        """
        phrase = M94.strip(phrase)
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

    @staticmethod
    def strip(s):
        s = s.upper()
        s = M94.re_non_alpha.sub('', s)
        return s

    @staticmethod
    def group_letters(letters):
        return ' '.join([letters[i:i + 5] for i in range(0, len(letters), 5)])
