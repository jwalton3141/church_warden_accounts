#! /usr/bin/env python3

import matplotlib.pyplot as plt

from utils.read_data import read

pairs, counts, locations = read()


# PLOT ALL #
fig, ax = plt.subplots(1, 1)

# Scatter towns
ax.scatter(locations['Longitude'],
           locations['Latitude'])

# Annotate townships
for i, row in locations.iterrows():
    ax.annotate(row['Title'], row[['Longitude', 'Latitude']])

# Draw edges between marriages
for pair in pairs:
    pair_locs = locations[locations['Title'].isin(pair)]
    ax.plot(pair_locs.Longitude.values,
            pair_locs.Latitude.values,
            color='k',
            alpha=0.65)

ax.set_xticks([])
ax.set_yticks([])

fig.tight_layout(pad=0)

fig.savefig('test_all.png')


# ZOOM PLOT # 
fig, ax = plt.subplots(1, 1)

# Scatter towns
ax.scatter(locations['Longitude'],
           locations['Latitude'])

mean = locations[['Longitude', 'Latitude']].mean()
var = locations[['Longitude', 'Latitude']].var()

ax.set_xlim((mean.Longitude - var.Longitude,
             mean.Longitude + var.Longitude))
ax.set_ylim((mean.Latitude - var.Latitude,
             mean.Latitude + var.Latitude))

# Annotate townships
for i, row in locations.iterrows():
    ax.annotate(row['Title'], row[['Longitude', 'Latitude']])

ax.set_xticks([])
ax.set_yticks([])

fig.tight_layout(pad=0)
