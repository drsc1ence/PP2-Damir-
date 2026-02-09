def find_max(numbers):
    """
    Finds the maximum number in the list.

    numbers : list
        list of integers
    return : int
        the biggest value from the list
    """
    return max(numbers)

data = list(map(int, input().split()))

print(find_max(data))
