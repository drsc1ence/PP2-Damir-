# parent (base) class
class Animal:
    def speak(self):
        return "Animal makes a sound"


# child (derived) class
class Dog(Animal):
    def bark(self):
        return "Woof!"


dog = Dog()

print(dog.speak())  # inherited from parent class
print(dog.bark())   # defined in child class
