#!/usr/bin/env python

import os
import re
import sys
import time
import subprocess
from optparse import OptionParser


def main():
    parser = OptionParser(
        usage="%prog [options]")
    parser.add_option('-v', '--verbose', action='store_true',
        help="run all checks with more output")
    (options, args) = parser.parse_args()
    print('hello, world')


if __name__ == '__main__':
    main()
