import sys, logging
from optparse import OptionParser

DEFAULT_FIXTURES_FILE = 'selexeFixtures.py'

options = [
    (('--selexe',), dict(action='store_true', help="execute selenium tests directly from *.sel files")),
    (('--baseuri', '-U'), dict(action='store', default=None,
                          help='base URI of server to run the selenium tests, e.g. "http://localhost:8080"')),
    (('--pmd',), dict(action='store_true', default=False, help='enable postmortem debugging')),
    (('--logging',), dict(action='store', default='info',
                         help='print verbose information about current test (debug, info, warning)')),
    (('--fixtures', '-F'), dict(action='store', default=DEFAULT_FIXTURES_FILE,
                                help='python module containing setUp() or tearDown() fixture functions'))
    ]


def parse_cmd_args():
    parser = OptionParser()
    for args, kw in options:
        parser.add_option(*args, **kw)
    opts, args = parser.parse_args()
    try:
        logLevel = getattr(logging, opts.logging.upper())
    except AttributeError:
        sys.stderr.write('invalid logging level "%s"! Valid values: debug, info, warning\n' % opts.logging)
        sys.exit(1)
    opts.logging = logLevel
    return opts, args
