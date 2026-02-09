#function that takes a list and a value
def add_number(numbers, value):
    numbers.append(value)  #list changes inside the function
    return numbers

data = list(map(int, input().split()))  #input list (example: 1 2 3)
value = int(input())                    #input value to add

result = add_number(data, value)        #pass list to function

print(data)    #original list after change
print(result)  #returned list
