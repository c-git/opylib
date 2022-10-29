import csv
from typing import List, Optional, Tuple


def read_file(fn: str, has_header: bool = False, *,
              delimiter: str = ',',
              quotechar: str = ',') -> \
        Tuple[List[List[str]], Optional[List[str]]]:
    """
    Reads in a small csv file and returns the contents (Not intended for use
    on large files as the entire file is read into memory)
    :param fn: Filename to load the file from
    :param has_header: Determines if the file has a header and it should be
    extracted from the first line
    :param delimiter: The delimiter to used in the file
    :param quotechar: The quote character used in the file
    :return: The data from the file and the header if `has_header` was True.

    :raise: StopIteration: if `has_header` is True but the file is empty
    """
    result: List[List[str]] = []
    header: Optional[List[str]] = None

    with open(fn, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        if has_header:
            header = next(reader)
        for row in reader:
            result.append(row)
    return result, header
