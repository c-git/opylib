"""
Collection of functions that work on streaming data (data we only see once
one element at a time and cannot store for processing or regular processing
may overflow type limits)

NB: Some functions may only be able to give an approximation.
"""


def mean(curr_avg: float, n: int, new_value: float) -> float:
    """
    Updates an average value using the real time streaming algorithm which
    uses constant space for calculations and doesn't overflow a sum counter.
    Gives the exact value not an approximation.

    NB: If first value is being added set current average to 0 (any value works)

    :param curr_avg: The current average value
    :param n: The number of values that have been summed so far (before the
        new one, should be 0 for first value)
    :param new_value: The value to be added to the average
    :return: The newly updated average value
    """
    return (curr_avg * n + new_value) / (n + 1)
