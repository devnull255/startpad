"""
A generic date parser.  Tries to be flexible in interpreting a date string
by trying these formats in order:

    m/d/y
    m/d/y hh:mm
    m/d/y hh:mm am/pm
    mmm d, y
    mmmm d, y
    m.d.y
    YYYY-MM-DD
    YYYY-MM-DDTHH:MM
    YYYY-MM-DDTHH:MM:SS

Strptime codes are document here:
    http://docs.python.org/library/time.html
"""

from datetime import datetime
import re

formats = ['%m/%d/%y',
           '%m/%d/%Y',
           '%d/%m/%y %H:%M',
           '%d/%m/%y %I:%M %p',
           '%d.%m.%y',
           '%b %d, %y',
           '%b %d, %Y',
           '%B %d, %Y',
           '%Y-%m-%d',
           '%Y-%m-%dT%H:%M',
           '%Y-%m-%dT%H:%M:%S',
           ]
           
regWhite = re.compile('\s+')

def parse_date(s):
    s = s.strip()
    s = regWhite.sub(' ', s)
    for format in formats:
        try:
            dt = datetime.strptime(s, format)
            return dt
        except Exception, e:
            pass
    return None
