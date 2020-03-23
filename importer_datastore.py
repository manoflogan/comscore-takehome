"""Entry point for importer and datastore. It accepts arguments in two ways.

1. through the file argument. The invocation would be something like

python importer_datastore.py datastore.csv

2. through standard input such as

python importer_datastore.py < datastore.csv
"""

import csv
import fileinput
import logging
from logging import config
import os


config.fileConfig('logging.conf')
logger = logging.getLogger('root')


# Global variables
OUTPUT_DIRECTORY_ROOT: str = 'output'
OUTPUT_DIRECTORY: str = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 OUTPUT_DIRECTORY_ROOT))
# Root directory in this project.
FILE_NAME = 'datastore.csv'
OUTPUT_FILE_PATH = os.path.join(OUTPUT_DIRECTORY, FILE_NAME)
FILE_HEADER: str = None  # File Header


def write_to_a_directory():
    """The implementation does the following

    1. Creates a directory output directory if does not exist.
    2. Reads the header if it not already parsed; if the header has not been
        parsed, then a file is created in append mode
    3. If the header has already been created, then we append to the existing
        file
    """

    # Step 1: Create a directory if it does not exist.
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    is_header_parsed: bool = False
    for content in fileinput.input():
        content = content.replace('\n', '')
        if not is_header_parsed:
            FILE_HEADER = content.split('|')
            is_header_parsed = True  # Ignore the first line
            with open(OUTPUT_FILE_PATH, 'a', encoding='utf-8') as file_object:
                file_writer = csv.writer(file_object, delimiter='|')
                file_writer.writerow(FILE_HEADER)
            logging.info('Directory created : {}'.format(OUTPUT_FILE_PATH))
        else:
            # Step # 2: Parse the header
            data_set = content.split('|')
            stb, title, _, date, _, _ = data_set
            # Creating the directory per stb, title, and date
            with open(OUTPUT_FILE_PATH, 'a', encoding='utf-8') as file_object:
                file_writer = csv.writer(file_object, delimiter='|')
                file_writer.writerow(data_set)


if __name__ == '__main__':
    write_to_a_directory()
