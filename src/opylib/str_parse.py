from typing import List


def get_attr_multi_level(obj, name: str):
    """
    Returns the attribute 'name' from obj. Support attributes of attributes
    separated by '.' So if you have a top level class MyClass which has a
    subclass Sub1 and that one has a subclass Sub2 and that has an attribute
    address you could access it with
    get_attr_multi_level(MyClass, 'Sub1.Sub2.address')
    :param obj: The base object to get name from
    :param name: The name of desired attribute (can be multiple levels deep)
    :return: The desired attribute
    """
    names = name.split('.')
    for x in names:
        obj = getattr(obj, x)
    return obj


def str_to_class(cls_name: str) -> type:
    """
    Converts a string into the class that it represents

    NB: Code based on https://stackoverflow.com/questions/452969/does-python
    -have-an-equivalent-to-java-class-forname
    :param cls_name: The string representation of the desired class
    :return: A pointer to the class (Able to be used as a constructor)
    """
    parts = cls_name.split('.')
    modules = '.'.join(parts[:-1])
    result = __import__(modules)
    for comp in parts[1:]:
        result = getattr(result, comp)
    return result


def strs_to_classes(cls_names: List[str]) -> List[type]:
    result = []
    for s in cls_names:
        result.append(str_to_class(s))
    return result


def dsv_line_to_list(line: str, *, delimiter=',', quote='"') -> List[str]:
    """
    Splits line into fields on delimiter ignoring delimiters in fields that
    start and end with quote

    NB: Empty fields produce an empty string

    :param line: The line to be split
    :param delimiter: The delimiter to use to split the fields
    :param quote: The quote char to surround fields that contain the delimiter
    :return: a list of the fields found
    """
    result = []
    within_quoted_field = False
    at_start_of_field = True
    last_was_quote = False  # Used to see if quote is not at end of field
    field = ''

    def new_field():
        nonlocal field, within_quoted_field, at_start_of_field, last_was_quote
        result.append(field)
        within_quoted_field = False
        at_start_of_field = True
        last_was_quote = False
        field = ''

    for char in line:
        if at_start_of_field:
            at_start_of_field = False
            # Check for quote
            if char == quote:
                within_quoted_field = True
                continue  # Skip quote do not include in field

        if within_quoted_field:
            if char == quote:
                last_was_quote = True
                continue  # May not want to add this char if end of field
            if last_was_quote:
                if char == delimiter:
                    new_field()
                    continue
                else:
                    field += quote
                    last_was_quote = False
            field += char
        else:
            if char == delimiter:
                new_field()
            else:
                field += char

    # Add last field that was being filled (or empty if empty in comma)
    result.append(field)

    return result
