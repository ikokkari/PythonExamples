def sign(a):
    if a < 0:
        return -1
    elif a > 0:
        return +1
    else:
        return 0


# Three different ways to find the median. Note that in the first one,
# operator <= is necessary, whereas in the second one, < is correct.
# Why is this so?

def median(a, b, c):
    if a <= b <= c or c <= b <= a:
        return b
    elif b <= a <= c or c <= a <= b:
        return a
    else:
        return c


def median_other_way(a, b, c):
    if a > b and a > c:  # a is maximum of three
        return max(b, c)
    elif a < b and a < c:  # a minimum of three
        return min(b, c)
    else:
        return a  # the only possibility that remains


# Integer arithmetic can sometimes do the job of logical
# decisions. Unlike Trix, integers are not just for kids.

def median_using_arithmetic(a, b, c):
    return a + b + c - min(a, b, c) - max(a, b, c)


# Determine how many days there are in the given month.

def days_in_month(month, leap_year=False):
    if month < 1 or month > 12:
        return 0
    elif month == 2:
        # One-liner choice between two values
        return 29 if leap_year else 28
    else:
        # Canonical way to check if m is member of a known handful
        return 30 if month in (4, 6, 9, 11) else 31


# Three functions to solve the same problems of determining
# whether the given year is a leap year.

def is_leap_year(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    else:
        return year % 400 == 0


def is_leap_year_another_way(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    else:
        return year % 4 == 0


def is_leap_year_with_logic(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


# Sneak preview of for-loops to iterate through the elements of the given
# sequence. Verify that all three functions for leap year testing give the
# same answer to all years ranging between those mentioned in the famous
# song "In the year 2525" by Zager & Evans.

def test_leap_year():
    for year in range(2525, 9596):
        a1 = is_leap_year(year)
        a2 = is_leap_year_another_way(year)
        a3 = is_leap_year_with_logic(year)
        # Chaining comparison operators works for equality just as well.
        if not (a1 == a2 == a3):  # a1 != a2 or a2 != a3:
            return False  # "Tear it down and start again."
    return True           # "I am pleased where man has been."
