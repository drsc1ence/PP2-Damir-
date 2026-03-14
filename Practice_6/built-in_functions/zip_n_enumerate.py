n = int(input())

a = list(map(int, input().split()))
b = list(map(int, input().split()))

result = 0

for index, (x, y) in enumerate(zip(a, b)):
    result += x * y
    print("Index:", index, "Values:", x, y)

print("Dot product:", result)