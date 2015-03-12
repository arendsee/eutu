#!/usr/bin/env python3

import argparse
import httplib2
import sys

__version__ = '0.0.0'
__prog__ = 'eutu'

def parser(argv=None):
    parser = argparse.ArgumentParser(
        prog=__prog__,
        usage="%s <subcommand> [options]" % __prog__,
        description="Interface with entrez"
    )
    parser.add_argument(
        '--version',
        help='Display version',
        action='version',
        version='%(prog)s {}'.format(__version__)
    )
    args = parser.parse_args(argv)
    return(args)


if __name__ == '__main__':

    args = parser()
