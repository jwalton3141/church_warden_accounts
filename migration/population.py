#! /usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os

from utils.read_data import read_population
from plot.pretty import make_fig_ax, savefig

data = read_population()


groupby = data.groupby('Year').sum()
groupby = groupby.reset_index(level=0)

fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        groupby['Baptism Total'] - groupby['Burial Total'],
        c='C2', marker='o')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlabel('Year')
ax.set_ylabel('Annual population change (baptisms - burials)')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/annual_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        groupby['Baptism Total'] / groupby['Burial Total'],
        c='C2', marker='o')
ax.hlines(1, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlabel('Year')
ax.set_ylabel('Ratio of annual baptisms to burials')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/annual_ratio.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Baptism Total'] - groupby['Burial Total']),
        c='C2', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative population change')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        groupby['Boy Baptism'] - groupby['Boy Burials'],
        c='C0', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Male population change (baptisms - burials)')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/annual_male_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        groupby['Girl Baptism'] - groupby['Girl Burials'],
        c='C6', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Female population change (baptisms - burials)')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/annual_female_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        groupby['Boy Baptism'] - groupby['Boy Burials'],
        c='C0', label='Male', marker='o')
ax.plot(groupby.Year,
        groupby['Girl Baptism'] - groupby['Girl Burials'],
        c='C6', label='Female', marker='o')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlabel('Year')
ax.set_ylabel('Annual population change (baptisms - burials)')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())
ax.legend(loc=0)

fig.tight_layout(pad=0)
fig.savefig('output/annual_gender_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Boy Baptism'] - groupby['Boy Burials']),
        c='C0', label='Male', marker='o')
ax.plot(groupby.Year,
        np.cumsum(groupby['Girl Baptism'] - groupby['Girl Burials']),
        c='C6', label='Female', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative population change')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())
ax.legend(loc=0)

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_gender_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Boy Baptism'] - groupby['Boy Burials']),
        c='C0', label='Male', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Male population change')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_male_change.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Girl Baptism'] - groupby['Girl Burials']),
        c='C6', label='Female', marker='o')
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Female population change')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_female_change.png')

fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Boy Baptism']),
        c='C0', label='Male', marker='o')
ax.plot(groupby.Year,
        np.cumsum(groupby['Girl Baptism']),
        c='C6', label='Female', marker='o')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Baptisms')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())
ax.legend(loc=0)

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_baptisms.png')


fig, ax = make_fig_ax()
ax.plot(groupby.Year,
        np.cumsum(groupby['Boy Burials']),
        c='C0', label='Male', marker='o')
ax.plot(groupby.Year,
        np.cumsum(groupby['Girl Burials']),
        c='C6', label='Female', marker='o')
ax.hlines(0, groupby.Year.min(), groupby.Year.max(),
          color='k', alpha=0.65, linestyle='--', linewidth=1.5)
ax.set_xlabel('Year')
ax.set_ylabel('Cumulative Burials')
ax.set_xlim(groupby.Year.min(), groupby.Year.max())
ax.legend(loc=0)

fig.tight_layout(pad=0)
fig.savefig('output/cumulative_burials.png')
