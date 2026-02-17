import datetime

now = datetime.datetime.now() #shows date time of today
sub5 = datetime.datetime(now.year, now.month, now.day - 5) #shows date time from 5 days ago
print(sub5)