from typing import Any, List, Tuple


def max_w_ind(lst: List) -> Tuple[int, Any]:
    """
    Returns the max value and its index
    :param lst: The list to get the max value in
    :return: Max value and its index
    """
    val = max(lst)
    ind = lst.index(val)
    return ind, val


def min_w_ind(lst: List) -> Tuple[int, Any]:
    """
    Returns the min value and its index
    :param lst: The list to get the max value in
    :return: Min value and its index
    """
    val = min(lst)
    ind = lst.index(val)
    return ind, val
