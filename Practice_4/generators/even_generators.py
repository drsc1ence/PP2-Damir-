def even_generator():
    i = 0
    while True:
        yield i
        i += 2


N = int(input())

gen = even_generator()

for _ in range(N+1):
    print(next(gen))
