#this function will convert pounds to kg
def pounds_to_kg(pounds): #pounds is a parameter 
    kg = pounds * 0.454
    return kg

pound = int(input())
print(pounds_to_kg(pound)) #pound is an argument
    
