class Student:
    university = "KBTU"  # class variable (shared by all students)

    def __init__(self, name):
        self.name = name  # instance variable (unique for each student)


s1 = Student("Damir")
s2 = Student("Nurali")

print(s1.university)  # same for everyone
print(s2.university)

print(s1.name)        # unique
print(s2.name)

# changing class variable
Student.university = "NU"

print(s1.university)
print(s2.university)

# changing instance variable (only affects one object)
s1.name = "Sagyn"

print(s1.name)
print(s2.name)
