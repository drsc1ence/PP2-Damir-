# defining a class with data and behavior
class Person:
    def __init__(self, name, age):
        self.name = name    # store person's name
        self.age = age     # store person's age

    def greet(self):
        return f"Hi, my name is {self.name} and I am {self.age} years old."


# creating objects (instances)
p1 = Person("Damir", 18)
p2 = Person("Nurali", 19)

print(p1.greet())
print(p2.greet())
