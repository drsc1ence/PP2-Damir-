n = int(input())
nlist = list(map(int, input().split()))

filtered = filter(lambda x: x > 0, nlist)
squared = map(lambda x: x**2, filtered)

print(sum(squared))