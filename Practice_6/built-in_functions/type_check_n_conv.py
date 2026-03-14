a = input("Enter a number: ")
b = input("Enter another number: ")

print("Type of a before conversion:", type(a))
print("Type of b before conversion:", type(b))

a = int(a)
b = int(b)

print("Type of a after conversion:", type(a))
print("Type of b after conversion:", type(b))

result = a + b

print("Sum:", result)