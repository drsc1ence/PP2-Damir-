numbers = [1, 2, 3, 4, 5, 6]

# filter keeps elements where the condition is True
evens = list(filter(lambda x: x % 2 == 0, numbers))

print(evens)
