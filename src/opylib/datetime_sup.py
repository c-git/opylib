from datetime import datetime, time, timezone
from typing import Union


def get_now_str(fmt: str = "%Y-%m-%d %H%M") -> str:
    return datetime.now().strftime(fmt)


def is_aware(value: Union[datetime, time]) -> bool:
    """
    Returns true if an object is timezone aware else false

    Throws an exception if an object of unexpected type is received

    Implemented based on information found in official documentation at
    https://docs.python.org/3/library/datetime.html in the section
    "Determining if an Object is Aware or Naive"
    :param value: The object to determine if it is timezone aware
    :return: true if an object is timezone aware else false
    """
    if isinstance(value, datetime):
        return value.tzinfo is not None \
               and value.tzinfo.utcoffset(value) is not None
    if isinstance(value, time):
        return value.tzinfo is not None \
               and value.tzinfo.utcoffset(None) is not None
    raise TypeError(
        f'Expected object of type datetime or time but got {value.__class__}')


def make_aware(
        value: Union[datetime, time],
        def_timezone: timezone = timezone.utc) -> \
        Union[datetime, time]:
    """
    Makes the parameter passed timezone aware if it wasn't already
    :param value: The object to be made timezone aware
    :param def_timezone: The timezone to set if the object is not yet
    timezone aware
    :return: An object that is timezone aware
    """
    if not is_aware(value):
        value = value.replace(tzinfo=def_timezone)
        assert is_aware(value)
    return value
