from functools import reduce

n = int(input())

numbers = list(map(int, input().split()))

product = reduce(lambda acc, x: acc * x, numbers)

print(product)