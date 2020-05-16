def sign(a):
    if a < 0:
        return -1
    elif a > 0:
        return +1
    else:
        return 0
    
def median(a, b, c):
    if a <= b <= c or c <= b <= a:
        return b
    elif b <= a <= c or c <= a <= b:
        return a
    else:
        return c
    
def median_other_way(a, b, c):
    if a > b and a > c: # a is maximum of three
        return max(b, c)
    elif a < b and a < c: # a minimum of three
        return min(b, c)
    else:
        return a  # the only possibility that remains
    
def days_in_month(m, leap_year = False):
    if m < 1 or m > 12:
        return 0
    elif m == 2:
        if leap_year:
            return 29
        else:
            return 28
    elif m in (4, 6, 9, 11):
        return 30
    else:
        return 31
    
def is_leap_year(y):
    if y % 4 != 0:
        return False
    if y % 100 != 0:
        return True
    return y % 400 == 0

# The same conditions written in a different way.

def is_leap_year_another_way(y):
    if y % 400 == 0:
        return True
    if y % 100 == 0:
        return False
    return y % 4 == 0

# The whole function as a Pythonesque one-liner.

def is_leap_year_with_logic(y):
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

def test_leap_year():
    for y in range(2525, 9596):
        a1 = is_leap_year(y)
        a2 = is_leap_year_another_way(y)
        a3 = is_leap_year_with_logic(y)
        if(a1 != a2 or a2 != a3):
            return False # Tear it down and start again.
    return True     # I am pleased where man has been.