import math

n = int(input("Input number of sides:"))
l = int(input("Input the length of a side:"))

x = math.pi
z = x/n
y = math.tan(z)

area = (n * (l ** 2))/(4 * y)
print(round(f"The area of the polygon is: {area}"))
