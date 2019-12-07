from datetime import date, timedelta

now = date.today()
print(f"Today's date in standard form is {now}.")

# Time objects have a handy method to insert their components to strings.
print(now.strftime("Today is a %A. It is the month of %B in the year %Y."))   

# Objects of type timedelta represent time differences that can be added
# and subtracted to times. We can easily solve the "Gigasecond challenge"
# from the Code Wars katas.

billion_seconds = timedelta(seconds = 10 ** 9)
gsfuture = now + billion_seconds
print(f"A billion seconds from now, the date will be {gsfuture}.")
gspast = now - billion_seconds
print(f"A billion seconds ago, the date was {gspast}.")

# A date object can be created in many different ways.
ludwig = date(1770, 12, 17)
td = now - ludwig    

print(f"Ludwig van Beethoven was born {td.days} days ago.")

if now.month < ludwig.month or\
   (now.month == ludwig.month and now.day <= ludwig.day):
    td = date(now.year, ludwig.month, ludwig.day) - now
else:
    td = date(now.year + 1, ludwig.month, ludwig.day) - now

if td.days == 0:
    print("Rejoice with celebration of Ludwig van Beethoven!")
elif td.days == 1:
    print("Sleep tight thinking of Ludwig van Beethoven tomorrow!") 
else:
    print(f"Only {td.days} days until Ludwig van Beethoven's birthday!")