# first parent class
class Flyer:
    def fly(self):
        return "I can fly"

# second parent class
class Swimmer:
    def swim(self):
        return "I can swim"

# child class inherits from BOTH parents
class Duck(Flyer, Swimmer):
    pass


d = Duck()

print(d.fly())    # from Flyer
print(d.swim())   # from Swimmer
