class Animal:
    def speak(self):
        return "Some sound"


# Dog is a child class of Animal
class Dog(Animal):
    pass


d = Dog()
print(d.speak())  # inherited from Animal
