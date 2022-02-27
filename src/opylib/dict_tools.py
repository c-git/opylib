# Most of the dict merging code was taken or based on
# https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries
# -in-a-single-expression-taking-union-of-dictiona


def merge_dicts(*dict_args):
    """
    This function is not meant to be used but rather to serve as a reminder to
    use the syntax {**x, **y, **z}.  This function works but is not as fast as
    that syntax by as much as twice.

    Given any number of dictionaries, shallow copy and merge into a new dict,
    precedence is given to key-value pairs in latter dictionaries.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def merge_two_dicts(d1, d2):
    """
    Slower implementation that works on older versions of python
    :param d1: Dict 1
    :param d2: Dict 2
    :return: Copy of d1 with new keys from d2 and overlap overwritten by d2
    """
    result = d1.copy()
    result.update(d2)
    return result


def merge_dict2(d1: dict, d2: dict) -> dict:
    """
    Merges exactly 2 dicts (For use when the syntax can't be remembered to
    do it inline as {**d1, **d2}
    NB: If the same key exists in both then d2 takes precedence
    :param d1: Dict 1
    :param d2: Dict 2
    :return: {**d1, **d2}
    """
    return {**d1, **d2}
