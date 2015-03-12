#!/usr/bin/env python3

import argparse
import httplib2
import sys

__version__ = '0.0.0'
__prog__ = 'eutu'

ENTREZ = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"

class Parser:
    def __init__(self):
        self.parser = self._build_base_parser()
        self.subparsers = self._build_subparsers()
        self.usage = __prog__ + ' {} <options>'

    def _build_base_parser(self):
        parser = argparse.ArgumentParser(
            prog=__prog__,
            usage='%(prog)s <subcommand> <options>',
            description='Tools for studying and manipulating fasta files')
        parser.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s {}'.format(__version__)
        )
        return(parser)

    def _build_subparsers(self):
        subparsers = self.parser.add_subparsers(
            metavar='[ for help on each: %(prog)s <subcommand> -h ]',
            title='subcommands')
        return(subparsers)

def parse(argv=None):

    parser = Parser()

    subcommands = [Litsrc]
    for cmd in subcommands:
        cmd(parser)

    argv = argv if argv else sys.argv[1:]

    if not argv:
        parser.parser.print_help()
        sys.exit(0)

    args = parser.parser.parse_args(argv)

    return(args)

class Subcommand:
    def __init__(self, parser_obj):
        self.func = self.write
        self.usage = parser_obj.usage
        self.subparsers = parser_obj.subparsers
        self._parse()

    def _parse(self):
        raise NotImplemented

    def write(self, args, gen, out=sys.stdout):
        raise NotImplemented


class Litsrc(Subcommand):
    def _parse(self):
        cmd_name = 'litsrc'
        parser = self.subparsers.add_parser(
            cmd_name,
            usage=self.usage.format(cmd_name),
            help="Query pubmed"
        )
        parser.add_argument(
            '-t', '--term',
            help="Pubmed query term"
        )
        parser.set_defaults(func=self.func)


    def generator(self, args, gen):
        pass

    def write(self, args, out=sys.stdout):
        print("Query: %s" % args.term, file=out)


if __name__ == '__main__':

    args = parse()
