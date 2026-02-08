#this function will create and update database of computer users
def computer_database(db, name, computer = "no computer"):
    db[name] = computer 
    return db

database = {}
user_input = input().split()
if len(user_input) == 2:
    # if name and computer are given
    name = user_input[0]
    computer = user_input[1]
    updated_database = computer_database(database, name, computer)
elif len(user_input) == 1:
    # if only name is given, computer is set to default
    name = user_input[0]
    updated_database = computer_database(name = name, db = database)
else: 
    # wrong input format
    print("ERROR")
    updated_database = database
    
print(updated_database)