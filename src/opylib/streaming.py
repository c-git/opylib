def mean(curr_avg: float, n: int, new_value: float) -> float:
    """
    Updates an average value using the real time streaming algorithm which
    uses constant space for calculations and doesn't overflow a sum counter

    NB: If first value is being added set current average to 0

    :param curr_avg: The current average value
    :param n: The number of values that have been summed so far (before the
    new one)
    :param new_value: The value to be added to the average
    :return: The newly updated average value
    """
    return (curr_avg * n + new_value) / (n + 1)
