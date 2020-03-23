# Comscore Coding Exercise

### Table of Contents

- [Assignment](Assignment.md)
- [Requirements](#requirements)
- [Setup](#setup)
- [Execution](#execution)
- [Overview](#overview)

### Requirements

* Python 3.6.x and above

### Setup

* Install Python 3.6.x and above. You can use your favourite tool to install the software (HomeBrew, pyenv) etc.

* Set up virtualenv with the following command ``virtualenv -p `which python3` env``. Activate the virtual environment using the command `source env/bin/activate`

* Install the python packages required by the project by executing `pipenv install` command.

## Execution

* Run the command `python datastore_importer.py < file.txt` or `python datastore_importer.py input.txt` to execute the program.

* Run the command `pytest` to run the unit tests. The code coverage reports will generated and displayed on the console.

## Overview

I chose Python to implement the assignment because Python 3's [fileinput API](https://docs.python.org/3/library/fileinput.html) can read from both input file if as a command line argument, but can also default to standard input without any change in code. In addition, Python ecosystem supports all the tools and libraries required to write good quality code in that language.
