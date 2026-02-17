import datetime

def get_date():
    user_string = input("Enter year, month, day, hour, minutes and seconds  of the date separated by commas (e.g., '1, 5, 10'): ")
    date_list = user_string.split(",")
    for i in date_list:
        i = i.strip()

    return datetime.datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(date_list[3]), int(date_list[4]), int(date_list[5]))

    

date1 = get_date()
date2 = get_date()
diff = date2 - date1
print(diff.total_seconds())