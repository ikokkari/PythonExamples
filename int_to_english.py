__googol = 10 ** 100

# http://lcn2.github.io/mersenne-english-name/tenpower/tenpower.html
__power_names = (("thousand", 3), ("million", 6), ("billion", 9),
                 ("trillion", 12), ("quadrillion", 15), ("quintillion", 18),
                 ("sextillion", 21), ("septillion", 24), ("octillion", 27),
                 ("nonillion", 30), ("decillion", 33), ("undecillion", 36),
                 ("duodecillion", 39), ("tredecillion", 42),
                 ("quattuordecillion", 45), ("quindecillion", 48),
                 ("sexdecillion", 51), ("eptendecillion", 54),
                 ("octadecillion", 57), ("novemdecillion", 60),
                 ("vigintillion", 63), ("unvigintillion", 66),
                 ("duovigintillion", 69), ("trevigintillion", 72),
                 ("quattuorvigintillion", 75), ("quinvigintillion", 78),
                 ("sexvigintillion", 81), ("septenvigintillion", 84),
                 ("octavigintillion", 87), ("novemvigintillion", 90),
                 ("trigintillion", 93), ("untrigintillion", 96),
                 ("duotrigintillion", 99)
                 )

# Dictionary comprehension, analogous to list comprehension.
__power_names = {p: n for n, p in __power_names}


def __int_to_eng(n):
    """Return the English name of a three-digit positive number."""
    assert 0 < n < 1000
    if n < 20:  # Numbers 0 to 19 with a simple lookup table.
        return ["ERROR", "one", "two", "three", "four", "five",
                "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve", "thirteen", "fourteen", "fifteen",
                "sixteen", "seventeen", "eighteen", "nineteen"][n]
    elif n < 100:  # Numbers 20 to 99, again with a lookup table.
        tens = ["ERROR", "ERROR", "twenty", "thirty", "forty", "fifty",
                "sixty", "seventy", "eighty", "ninety"][n // 10]
        return tens if n % 10 == 0 else f"{tens}-{__int_to_eng(n % 10)}"
    else:  # Numbers 100 to 999
        name = f"{__int_to_eng(n//100)} hundred"
        if n % 100 != 0:
            name += f" and {__int_to_eng(n%100)}"
        return name


def int_to_english(n):
    """Construct the English name of the given integer n."""
    if n < 0:  # Negative numbers
        return "minus " + int_to_english(-n)
    if n == 0:  # Zero as a special case
        return "zero"
    if n >= __googol:  # Huge numbers
        first = int_to_english(n // __googol)
        rest = int_to_english(n % __googol)
        return f"{first} googol" + ("" if rest == "zero" else f" and {rest}")
    # Otherwise, break the number into blocks of three and convert.
    result, p = [], 0
    while n > 0:
        last_three_digits = n % 1000
        if last_three_digits > 0:
            result.append(__int_to_eng(last_three_digits) + ("" if p == 0 else " " + __power_names[p]))
        n = n // 1000
        p += 3
    return " ".join(reversed(result))


def __int_to_english_demo():
    for x in [42, 3**7, 6**20, -(2**100), 9**200, 10**500 + 1]:
        print(f"{x} written in English is {int_to_english(x)}.")
    alpha = ', '.join([int_to_english(n) for n in sorted(range(0, 101), key=int_to_english)])
    by_length = [int_to_english(n) for n in sorted(range(0, 101),
                                                   key=lambda n: (len(int_to_english(n)), n))]
    by_length = ', '.join(by_length)
    no_os = ', '.join([str(x) for x in range(1001) if 'o' not in int_to_english(x)])
    print("\nIntegers 0-100 sorted in alphabetical order:")
    print(alpha)
    print("\nIntegers 0-100 sorted by their name lengths:")
    print(by_length)
    print("\nIntegers 0-1000 whose name does not contain the letter 'o':")
    print(no_os)


if __name__ == '__main__':
    __int_to_english_demo()
