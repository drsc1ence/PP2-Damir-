class Animal:
    def __init__(self, name):
        self.name = name

    def info(self):
        return f"Animal name: {self.name}"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)  # call parent constructor
        self.breed = breed


dog = Dog("Rex", "Labrador")
print(dog.info())
