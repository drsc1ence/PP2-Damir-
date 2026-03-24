import configparser

def generate_perfect_ini():
    config = configparser.ConfigParser()
    
    # Setting up the exact data you provided
    config['postgresql'] = {
        'host': 'localhost',
        'database': 'newphonebook',
        'user': 'postgres',
        'password': 'damir2007'
    }

    # Python will write this in pure, clean UTF-8
    with open('database.ini', 'w', encoding='utf-8') as f:
        config.write(f)
        
    print("Success! A brand new, totally clean database.ini has been created.")

if __name__ == '__main__':
    generate_perfect_ini()