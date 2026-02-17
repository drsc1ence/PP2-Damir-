import datetime

now = datetime.datetime.now() #shows date time of today
yesterday = datetime.datetime(now.year, now.month, now.day - 1) #shows date time of yesterday
tomorrow = datetime.datetime(now.year, now.month, now.day + 1) #shows date time of tomorrow
today = datetime.datetime(now.year, now.month, now.day)
print(yesterday.strftime("%Y-%m-%d"))
print(today.strftime("%Y-%m-%d"))
print(tomorrow.strftime("%Y-%m-%d"))