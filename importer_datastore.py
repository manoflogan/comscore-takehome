"""Entry point for importer and datastore. It accepts arguments in two ways.

1. through the file argument. The invocation would be something like

python importer_datastore.py datastore.csv

2. through standard input such as

python importer_datastore.py < datastore.csv
"""

import fileinput
import logging
from logging import config


config.fileConfig('logging.conf')
logger = logging.getLogger('root')


if __name__ == '__main__':
    print('Testing')
