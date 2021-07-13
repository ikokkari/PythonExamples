import json
from itertools import islice
from math import log

with open('mountains.json', encoding="utf-8") as data_file:
    mountains = json.load(data_file)

# Uncomment this line to repeat this analysis for a subset of mountains.
# mountains = [m for m in mountains if m['ClimbingDifficulty'] == "Walk Up"]

print(f"Read {len(mountains)} mountains from the JSON file.")
print("JSON data file generated from Wolfram Mathematica.")

with open('countries.json', encoding='utf-8') as data_file:
    countries = json.load(data_file)

print(f"Read {len(countries)} countries from the JSON file.")

mountains_in_country, tallest_in_country = {}, {}
smallest = (0, 'Molehill')  # Made-up placeholder

for mountain in mountains:
    name = mountain['Name']
    for country in mountain['Countries']:
        if country in mountains_in_country:
            mountains_in_country[country].append(name)
        else:
            mountains_in_country[country] = [name]
        (te, tb) = tallest_in_country.get(country, smallest)
        try:
            e = int(mountain['Elevation'].split(' ')[0])
            if e > te:
                tallest_in_country[country] = (e, mountain['Name'])
        except ValueError:
            pass

print("\nHere are top thirty countries sorted by their tallest mountains:")

countries = sorted(countries,
                   key=lambda cc: tallest_in_country.get(cc['Name'], smallest),
                   reverse=True)

# itertools.islice is a handy way to impose cutoff on the sequence length.

for (i, c) in islice(enumerate(countries), 30):
    (te, tn) = tallest_in_country.get(c['Name'], smallest)
    print(f'{i+1:2}. {c["Name"]} with {tn}, elevation {te} m.')

print("\nHere are the top hundred countries sorted by named mountains:")

countries = sorted(countries,
                   key=lambda cc: (len(mountains_in_country.get(cc['Name'], [])), cc['Name']),
                   reverse=True)

for (i, c) in islice(enumerate(countries), 100):
    print(f'{i+1:2}. {c["Name"]} has {len(mountains_in_country.get(c["Name"], []))} named mountains.')

# https://en.wikipedia.org/wiki/Benford%27s_law
print("\nLet's see how well mountain heights follow Benford's law.\n")

# meters, feet, yards, inches, points, fathoms
muls = (1, 0.3048, 0.9144, 1 / 0.0254, 1 / 0.003528, 0.5468)
# Build a separate counter dictionary for each unit.
leading = [{} for m in muls]

count = 0
for mountain in mountains:
    try:
        # Elevation of the current mountain
        m = int(mountain['Elevation'].split(' ')[0])
        # Convert to various units and update the leading digit counter.
        for (dic, mul) in zip(leading, muls):
            h = int(str(mul * m)[0])  # Leading digit of integer
            dic[h] = dic.get(h, 0) + 1
        count += 1
    except ValueError:
        pass

benford = [100 * (log(d+1, 10) - log(d, 10)) for d in range(1, 10)]

print("Digit   Meters  Feet    Yards   Inches  Points  Fathoms Benford")
for d in range(1, 10):
    line = f"{d:4}"
    for lead in leading:
        line += f"{100 * lead.get(d, 0) / count:8.1f}"
    line += f"{benford[d-1]:8.1f}"
    print(line)
