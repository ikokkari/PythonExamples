#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import json

with open('mountains.json', encoding="utf-8") as data_file:
    mountains = json.load(data_file)
    
def clean(obj, field, default=0):
    try:
        e = int(obj[field].split(' ')[0])
    except ValueError:
        e = default
    return e
    
# Histogram plot.
hts = np.array(list(map(lambda x: clean(x, 'Elevation'), mountains)))
plt.hist(hts, 20, normed=1, facecolor='blue', alpha=0.75)
plt.figure(1)
print("Histogram of heights of named mountains.")
plt.show(1)

# Ordinary data plot.
plt.figure(2)
plt.plot(np.sort(hts),'--',path_effects=[path_effects.SimpleLineShadow(),
                       path_effects.Normal()])
print("Heights of world's mountains.")
plt.show(2)

with open('countries.json', encoding="utf-8") as data_file:
    countries = json.load(data_file)
    
pops = np.array(list(map(lambda x: clean(x, 'Population'), countries)))
gdp = np.array(list(map(lambda x: clean(x, 'GDP'), countries)))
gdppc = 0.1 * gdp / pops
pops = np.log(pops) / np.log(10)

# Scatter plot
plt.figure(3)
plt.autoscale(enable=True, axis='x', tight=False)
plt.scatter(gdppc, pops, c='g')
plt.xlabel("GDP Per Person")
plt.ylabel("Population $10^k$")
print("Scatterplot of countries GDP/Person and population.")
plt.show(3)

continental_pops = {}
total_pop = 0
for country in countries:
    name = country["Name"]
    continent = country["Continent"]
    pop = int(country["Population"].split(" ")[0])
    continental_pops[continent] = continental_pops.get(continent, 0) + pop
    total_pop += pop
    
keys = continental_pops.keys()
cp = np.array([continental_pops[continent] for continent in keys])

# Pie plot
plt.figure(4)
plt.axes([1,1,1,1])
plt.pie(cp, labels = keys, explode = [0,0,.1,0,0,.3])
print("Portion of world's population in each continent.")
plt.show(4)