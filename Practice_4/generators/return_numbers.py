def returning(n):
    for i in range(n, -1, -1):
        yield i


n = int(input())

for value in returning(n):
    print(value)
