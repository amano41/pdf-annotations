#!/usr/bin/env python3

import sys

def convert(infile, outfile=sys.stdout):

    for line in infile:

        line = line.strip()

        if not line:
            continue

        if line.startswith('##'):

            section = line[3:]

            if section == 'Nits':
                section = 'Underlines'

            print('\n[[' + section + ']]\n', file=outfile)
            continue

        if line.startswith('* Page'):
            continue

        if line.startswith('> '):
            print('\t' + line[2:], file=outfile)
            continue

        print('parse error: ' + line)

if __name__ == '__main__':
    convert(sys.stdin)
