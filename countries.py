import json

with open('countries.json', encoding="utf-8") as data_file:
    countries = json.load(data_file)

print(f"Read {len(countries)} countries from the JSON file.")

continental_pops = {}
total_pop = 0
for country in countries:
    continent = country["Continent"]
    pop = int(country["Population"].split(" ")[0])
    continental_pops[continent] = continental_pops.get(continent, 0) + pop
    total_pop += pop

print("\nThe total population in each continent:")
for continent in sorted(continental_pops.keys(),
                        key = lambda c: continental_pops[c],
                        reverse = True):
    print(f"{continent} has a total of {continental_pops[continent]} people.")
print(f"That gives a total of {total_pop} people on Earth.")

hazard_table = {}
for country in countries:
    hazards = country["NaturalHazards"]
    for hazard in hazards:
        hazard_table[hazard] = hazard_table.get(hazard, 0) + 1

print("\nHere are the hazards found around the world:")
for hazard in sorted(hazard_table,
                     key = lambda haz: hazard_table[haz],
                     reverse = True):
    print(f"{hazard[0].upper() + hazard[1:]} is a hazard in {hazard_table[hazard]} countries.")