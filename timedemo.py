from datetime import datetime, timedelta

# datetime objects represent individual fixed points in time. If only
# the date component is needed, but not the hour, minute and seconds,
# you can use the datetime.date type instead.

now = datetime.today()
print(f"Current time in standard form is {now}.")

# datetime offers a handy method to insert its components into strings.
print(now.strftime("Today is a %A. It is %d of %B in the year %Y."))   

# Objects of type timedelta represent time differences that can be added
# and subtracted to times. We can easily solve the "Gigasecond challenge"
# from the Code Wars katas.

billion_seconds = timedelta(seconds = 10 ** 9)
gsfuture = now + billion_seconds
print(f"A billion seconds from now, the time is {gsfuture}.")
gspast = now - billion_seconds
print(f"A billion seconds ago, the time was {gspast}.")

# A datetime object can be created in many different ways.
ludwig = datetime(year = 1770, month = 12, day = 17)
elapsed = now - ludwig    

print(f"Ludwig van Beethoven was born {elapsed.days} days ago.")

if now.month < ludwig.month or\
   (now.month == ludwig.month and now.day <= ludwig.day):
    towait = datetime(now.year, ludwig.month, ludwig.day) - now
else:
    towait = datetime(now.year + 1, ludwig.month, ludwig.day) - now

if towait.days == 0:
    print("Rejoice with celebration of Ludwig van Beethoven!")
elif towait.days == 1:
    print("Sleep tight thinking of Ludwig van Beethoven tomorrow!") 
else:
    print(f"Still {towait.days} days until Ludwig van Beethoven's birthday!")