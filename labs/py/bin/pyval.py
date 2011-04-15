import sys

from pprint import pprint

if __name__ == '__main__':
    value = sys.stdin.read()
    pprint(eval(value.strip()))
