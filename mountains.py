import json
import itertools as it

with open('mountains.json', encoding="utf-8") as data_file:
    mountains = json.load(data_file)

print(f"Read {len(mountains)} mountains from the JSON file.")
print("JSON data file generated from Wolfram Mathematica.")

with open('countries.json', encoding="utf-8") as data_file:
    countries = json.load(data_file)

print(f"Read {len(countries)} countries from the JSON file.")

mic, tallest = {}, {}
smallest = (0, 'Molehill') # Made-up placeholder

for mountain in mountains:
    for country in mountain['Countries']:
        mic[country] = mic.get(country, []) + [mountain['Name']]
        (te, tb) = tallest.get(country, smallest)
        try:
            e = int(mountain['Elevation'].split(' ')[0])
            if e > te:
                tallest[country] = (e, mountain['Name'])
        except ValueError:
            pass

print("\nHere are top thirty countries sorted by their tallest mountains:")

countries = sorted(countries,
                   key = (lambda c: tallest.get(c['Name'], smallest)),
                   reverse = True)
for (i, c) in it.islice(enumerate(countries), 30):
    (te, tn) = tallest[c['Name']]
    print(f'{i+1:2}. {c["Name"]} with {tn}, elevation {te} m.')

print("\nHere are the top hundred countries sorted by named mountains:")

countries = sorted(countries,
                   key = (lambda c: (len(mic.get(c['Name'], [])), c['Name'])),
                   reverse = True)

for (i, c) in it.islice(enumerate(countries), 100):
    print(f'{i+1:2}. {c["Name"]} has {len(mic[c["Name"]])} named mountains.')

# https://en.wikipedia.org/wiki/Benford%27s_law
print("\nLet's see how well Benford's law applies to mountain heights.")

# meters, feet, yards
muls = (1, 0.3048, 0.9144)
leading = [ {} for m in muls ]

count = 0
for mountain in mountains:
    try:
        # Elevation of the current mountain
        m = int(mountain['Elevation'].split(' ')[0])
        # Convert to various units and update the leading digit counter.
        for (dic, mul) in zip(leading, muls):
            h = int(str(mul * m)[0]) # Leading digit in the current units
            dic[h] = dic.get(h, 0) + 1
        count += 1
    except ValueError:
        pass
    
from math import log
benford = [100 * (log(d+1, 10) - log(d, 10)) for d in range(1, 10)]

print("Digit   Meters  Feet    Yards   Benford")
for d in range(1, 10):
    print(f"{d:4}{100 * leading[0].get(d,0) / count:8.1f}{100 * leading[1].get(d,0) / count:8.1f}"
          +f"{100 * leading[2].get(d,0) / count:8.1f}{benford[d-1]:8.1f}")