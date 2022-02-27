import random


def shuffle(*iterables):
    """
    Takes one or more iterable objects and shuffles them keeping their items
    that were at the same index as another item still at the same index as
    the other item.

    WARNING: Uses zip and will reduce the length of the items to the length
    of the shortest among them

    :iterables: The items to be shuffled
    :return: the pair wise same but shuffled iterables
    """
    join = list(zip(*iterables))
    random.shuffle(join)
    return zip(*join)


if __name__ == '__main__':
    a = [1, 2, 3, 4, 5, 6]  # Note that 6 goes missing as it is extra
    b = ['a', 'b', 'c', 'd', 'e']
    c = ['A', 'B', 'C', 'D', 'E']
    a, b, c = shuffle(a, b, c)
    print(a)
    print(b)
    print(c)
