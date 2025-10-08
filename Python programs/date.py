import datetime

curr_date=datetime.date.today()
curr_time=datetime.datetime.now()
curr_tym=curr_time.strftime("%H :%M: %S")
print(curr_time)
print(curr_tym)
print(curr_date)