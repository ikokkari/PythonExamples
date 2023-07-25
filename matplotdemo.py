import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import json

with open('mountains.json', encoding="utf-8") as data_file:
    mountains = json.load(data_file)


# Utility function to extract data from country objects.

def extract(obj, field, default=0):
    try:
        e = int(obj[field].split(' ')[0])
    except ValueError:
        e = default
    return e


# Heights of the world's mountains.

hts = np.array([extract(m, "Elevation") for m in mountains])

# Histogram plot of mountain heights.

with plt.xkcd():  # Cueball: "Why?"  Black hat: "Why not?"
    plt.hist(hts, 20, facecolor='cyan', alpha=0.75)
    plt.figure(1)
    print("Histogram of the heights of named mountains.")
    plt.xlabel("Mountain height")
    plt.ylabel("Mountain count")
    plt.show()

# Ordinary data plot of mountain heights.

plt.figure(2)
pef = [path_effects.SimpleLineShadow(), path_effects.Normal()]
plt.plot(np.sort(hts), '-', path_effects=pef)
print("Heights of the mountains of the world.")
plt.show()

with open('countries.json', encoding="utf-8") as data_file:
    countries = json.load(data_file)

pops = np.array([extract(c, "Population") for c in countries])
gdp = np.array([extract(c, "GDP") for c in countries])
gdppc = gdp / pops
pops_log = np.log(pops) / np.log(10)

# Scatter plot of population against GDP per person.

plt.figure(3)
plt.autoscale(enable=True, axis='x', tight=False)
plt.scatter(pops_log, gdppc, c='g', marker='.')
plt.xlabel('Population ($10^k$)')  # LaTeX-style math markup
plt.ylabel('GDP / person')
plt.show()
print("Scatterplot of countries GDP/Person and population.")

# Compute the total population of each continent.

continental_pops = {}
for country in countries:
    name, continent = country['Name'], country['Continent']
    pop = extract(country, 'Population', 0)
    continental_pops[continent] = continental_pops.get(continent, 0) + pop

keys = continental_pops.keys()
cp = np.array([continental_pops[continent] for continent in keys])

# Pie plot of continental populations.

plt.figure(4)
plt.pie(cp, labels=keys, explode=[0, 0, .1, -.1, 0, .3])
print("Portion of world's population in each continent.")
plt.show()
# plt.savefig("continental_pie.svg")
