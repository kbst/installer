"""Kubestack Installer

Usage:
  cmd.py [--debug] serve [--port=<port>] <scenario>
  cmd.py [--debug] print_manifest <scenario>
  cmd.py (-h | --help)
  cmd.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --debug       Log debug output.

"""
import logging

from docopt import docopt

from .runner import Runner
from .scenario import Scenario


if __name__ == '__main__':
    arguments = docopt(__doc__, version='v0.0.1')

    # Configure logging
    logging.basicConfig(level=getattr(logging, 'INFO'))
    if arguments['--debug']:
        logging.basicConfig(level=getattr(logging, 'DEBUG'))

    logging.debug(f'Parsed arguments: \n{arguments}')

    if arguments['serve']:
        s = Scenario.load(file_name=arguments['<scenario>'])
        r = Runner(s)
        r.run()
