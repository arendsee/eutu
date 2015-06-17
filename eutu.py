#!/usr/bin/env python3

import argparse
import httplib2
import sys
import xml.etree.ElementTree as etree
import io

__version__ = '0.0.0'
__prog__ = 'eutu'

ENTREZ = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# ===============
# Command Parsing
# ===============

class Parser:
    def __init__(self):
        self.parser = self._build_base_parser()
        self.subparsers = self._build_subparsers()
        self.usage = __prog__ + ' <global options> {} < subcommand options>'

    def _build_base_parser(self):
        parser = argparse.ArgumentParser(
            prog=__prog__,
            usage='%s <global options> <subcommand> <subcommand options>' % __prog__,
            description='An entrez query tool')
        parser.add_argument(
            '-v', '--version',
            action='version',
            version='%s %s' % (__prog__, __version__)
        )
        return(parser)

    def _build_subparsers(self):
        subparsers = self.parser.add_subparsers(
            metavar='[ for help on each: %(prog)s <subcommand> -h ]',
            title='subcommands')
        return(subparsers)

def build_common_options(parser, args):
    if('retmax' in args):
        parser.add_argument(
            '-r', '--retmax',
            help="Maximum number of records to retrieve",
            type=int,
            default=10
        )
    parser.add_argument(
        '--cache',
        help='Set a caching directory'
    )
    parser.add_argument(
        '--debug',
        help='Print HTTP request data',
        action='store_true',
        default=False
    )

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


# ===========
# Subcommands
# ===========

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
        build_common_options(parser=parser, args=('retmax'))
        parser.set_defaults(func=self.func)

    def generator(self, args, gen):
        pass

    def write(self, args, out=sys.stdout):
        pass


# ====
# Guts
# ====

def parse_xml(xmlstring):
    tree = etree.parse(io.StringIO(xmlstring))
    term = dict()
    for key in ('QueryKey', 'WebEnv', 'Count', 'RetMax'):
        try:
            value = tree.getroot().findall('.//' + key)[0].text
        except IndexError:
           continue
        term[key] = value
    term['ids'] = tuple(x.text for x in tree.getroot().findall('.//IdList/Id'))
    return(term)

def fetch(webenv, querykey, db, args):
    base = "%s/efetch.fcgi?&retmax=%d&query_key=%s&WebEnv=%s&db=%s&rettype=text"
    url = base % (ENTREZ, args.retmax, querykey, webenv, db)
    response, content = h.request(url)
    return(content.decode())

if __name__ == '__main__':
    args = parse()
    if args.debug:
        httplib2.debuglevel = 1

    h = httplib2.Http(args.cache)

    base = "%s/esearch.fcgi?db=pubmed&term=%s&retmax=%d&usehistory=y"
    url = base % (ENTREZ, args.term, args.retmax)
    response, content = h.request(url)

    xmlstring = content.decode()

    terms = parse_xml(xmlstring)

    output = fetch(webenv=terms['WebEnv'],
                   querykey=terms['QueryKey'],
                   db='pubmed',
                   args=args)
    print(output)
