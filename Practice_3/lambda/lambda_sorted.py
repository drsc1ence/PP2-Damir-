pairs = [(1, 3), (4, 1), (2, 2)]

# sort by the second element of each tuple
sorted_pairs = sorted(pairs, key=lambda x: x[1])

print(sorted_pairs)
