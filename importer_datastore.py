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
OUTPUT_DIRECTORY_ROOT: str = 'output'  # Root directory in this project.
FILE_HEADER: str = None  # File Header


def create_file_path_from_stb_title_string(stb: str, title: str,
                                           date_str: str) -> str:
    """
    Constructs a file path from `std`, 'title', and 'date' as string

    Args:
        stb: stb as string
        title: title as string
        date_str: date as string

    Returns:
        constructed file path as string
    """
    return '{0}_{1}_{2}.csv'.format(stb.lower(),
                                    title.lower().replace(' ', '_'),
                                    date_str.replace('-', '_'))


def write_to_a_directory():
    """The implementation does the following

    1. Creates a directory output directory if does not exist.
    2. Reads the header if it not already parsed; if the header has not been
        parsed, then a directory is created
    3. If the header is already
    """
    output_dir: str = os.path.normpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     OUTPUT_DIRECTORY_ROOT))
    # Step 1: Create a directory if it does not exist.
    os.makedirs(output_dir, exist_ok=True)

    is_header_parsed: bool = False
    for content in fileinput.input():
        if not is_header_parsed:
            FILE_HEADER = content.split('|')
            is_header_parsed = True  # Ignore the first line
        else:

            # Step # 2: Parse the header
            data_set = content.split('|')
            stb, title, _, date, _, _ = data_set
            file_dir = os.path.join(
                output_dir,
                create_file_path_from_stb_title_string(stb, title, date))
            import pdb
            pdb.set_trace()
            # Creating the directory per stb, title, and date
            logging.info('Directory created : {}'.format(file_dir))
            # Check if file exists
            file_exists: bool = os.path.exists(file_dir)
            with open(file_dir, 'a', encoding='utf-8') as file_object:
                file_writer = csv.writer(file_object, delimiter='|',
                                         escapechar='\\',
                                         quoting=csv.QUOTE_NONE)
                if not file_exists:
                    file_writer.writerow(FILE_HEADER)
                file_writer.writerow(data_set)


if __name__ == '__main__':
    write_to_a_directory()
