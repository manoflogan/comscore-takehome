"""The file serves as an entry point to query tool.

The query tool accepts command line arguments representing the query parameters
"""

import argparse
import csv
import operator
import sys
import typing

import constants


class DelimiterSeparatedInput(object):
    """An callable that accepts the separator, and converts to a list"""

    def __init__(self, item_type: typing.Callable[[str], typing.List[str]],
                 separator: str = ','):
        """Initialises the separated type.

        Args:
            item_type: typee to which the argument is to be converted
            separator: separator string
        """
        self.item_type = item_type
        self.separator = separator

    def __call__(self, values) -> typing.List[str]:
        """Creates a separator delimited list of arguments."""
        if not values:
            return list()
        try:
            return [self.item_type(val)
                    for val in values.split(self.separator)]
        except Exception:
            raise argparse.ArgumentError(
                'The value {} can not be parsed'.format(values))


class Criteria(object):
    """An instance of this class encapsulates all the selection criteria to
    query the underlying data.
    """

    def __init__(self, select: typing.List[str],
                 order: typing.List[str] = None,
                 filter_list: typing.List[str] = None):
        """Initialises the criteria.

        Args:
            select: selection criteria
            order: order criteria
            filter: filter criteria
        """
        self.select = set(select or [])
        self.order = order or []
        self.filter_list = set(filter_list or [])

    def __call__(self,
                 csv_generator: typing.Generator[
                     typing.List[str], typing.List[str],
                     typing.List[str]]) -> typing.List[str]:
        """Applies the criteria to filter a row by criteria."""
        # First order by keys.
        if self.filter_list:
            filtered_dict_combo = dict([
                (row_filter[0], row_filter[1])
                for row_filter in (f.split('=') for f in self.filter_list)])
            filtered_rows = []
            for row in csv_generator:
                filter_count = 0
                for filter_key in filtered_dict_combo:
                    if row[filter_key] == filtered_dict_combo[filter_key]:
                        filter_count += 1
                # If all filters match, then all filter
                if filter_count == len(filtered_dict_combo):
                    filtered_rows.append(row)
        else:
            # No filter so use the entire row
            filtered_rows = [row for row in csv_generator]

        # If ordering exists, then it needs to be ordered
        if self.order:
            filtered_rows = sorted(filtered_rows,
                                   key=operator.itemgetter(*self.order))

        output_rows = []
        if self.select:
            for filtered_row in filtered_rows:
                output_rows.append(
                    [filtered_row[select_column]
                     for select_column in self.select])
        return output_rows

    def __repr__(self):
        return '{}[{}]'.format(self.__class__.__name__,
                               self.__dict__)


def query_datastore(select: typing.List[str], order: typing.List[str] = None,
                    filter_list: typing.List[str] = None):
    """Query the data stores by selection criteria."""
    with open(constants.OUTPUT_FILE_PATH, 'r', encoding='utf-8') as data_file:
        csv_reader = csv.DictReader(data_file, delimiter='|')
        criteria = Criteria(select, order, filter_list)
        filtered_output = criteria(csv_reader)
        import pdb; pdb.set_trace()
        print(filtered_output)
        return filtered_output


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', type=DelimiterSeparatedInput(str),
                        help='Fields to be selected', required=True)
    parser.add_argument('-o', type=DelimiterSeparatedInput(str),
                        help='Fields to be ordered', required=False)
    parser.add_argument('-f', type=DelimiterSeparatedInput(str),
                        help='Fields to be filtered by', required=False)
    (arguments, _) = parser.parse_known_args(sys.argv[1:])

    query_datastore(arguments.s, arguments.o, arguments.f)
