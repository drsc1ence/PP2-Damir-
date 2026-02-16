def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 3 == 0 and i % 4 == 0:
            yield i


N = int(input())

for number in divisible_by_3_and_4(N):
    print(number)
