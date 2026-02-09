class Counter:
    def __init__(self):
        self.value = 0  # each object has its own value

    def increase(self):
        self.value += 1  # self refers to THIS object

    def show(self):
        return self.value


# creating objects
c1 = Counter()
c2 = Counter()

c1.increase()
c1.increase()
c2.increase()

print(c1.show())  # 2
print(c2.show())  # 1
