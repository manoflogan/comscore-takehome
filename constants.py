"""Utility function to encapsulate constants."""

import os


OUTPUT_DIRECTORY_ROOT: str = 'output'
OUTPUT_DIRECTORY: str = os.path.normpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)),
                 OUTPUT_DIRECTORY_ROOT))
# Root directory in this project.
OUTPUT_FILE_NAME: str = '{}_{}_{}.csv'
