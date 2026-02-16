def square_generator():
    i = 0
    while True:
        yield i ** 2
        i += 1


N = int(input())

gen = square_generator()

for _ in range(N+1):
    print(next(gen))
