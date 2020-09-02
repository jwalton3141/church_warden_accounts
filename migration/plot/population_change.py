#! /usr/bin/env python3

"""This is an absolute state please sort it."""

import matplotlib.pyplot as plt
import numpy as np
import os

from migration.utils.read_data import read_population
from plot.pretty import make_fig_ax, savefig

data = read_population()


groupby = data.groupby('Year').sum()
groupby = groupby.reset_index(level=0)


def make_plot(cols, ylabel, save_name, ratio=False, cumsum=False):
    fig, ax = make_fig_ax()

    if ratio:
        y1 = groupby[col[0]] / groupby[col[1]]
        hline = 1

        if len(cols) > 2:
            y2 = groupby[col[2]] / groupby[col[3]]
        else:
            y2 = None
    else:
        y1 = groupby[col[0]] - groupby[col[1]]
        hline = 0

        if len(cols) > 2:
            y2 = groupby[col[2]] - groupby[col[3]]
        else:
            y2 = None

        if cumsum:
            y1 = np.cumsum(y1)
            if y2 is not None:
                y2 = np.cumsum(y2)
            hline = None

    ax.plot(groupby.Year, y1,
            groupy.Year, y2)

    ax.set_xlabel('Year')
    ax.set_ylabel(ylabel)

    ax.hlines(hline, groupby.Year.min(), groupby.Year.max(),
              color='k', alpha=0.65, linestyle='--', linewidth=1.5)

    ax.set_xlim(groupby.Year.min(), groupby.Year.max())

    fig.tight_layout(pad=0)

    fig.savefig(path.join('output', save_name))


make_plot(['Baptism Total', 'Burial Total'],
          'Annual population change (baptisms - burials)',
          'annual_change.png')

make_plot(['Baptism Total', 'Burial Total'],
          'Ratio of annual baptisms to burials',
          'annual_ratio.png',
          ratio=True)

make_plot(['Baptism Total', 'Burial Total'],
          'Cumulative population change',
          'cumulative_change.png',
          cumsum=True)

make_plot(['Boy Baptism', 'Boy Burials'],
          'Male population change (baptisms - burials)',
          'annual_male_change.png')

make_plot(['Girl Baptism', 'Girl Burials'],
          'Female population change (baptisms - burials)',
          'annual_female_change.png')

make_plot(['Boy Baptism', 'Boy Burials', 'Girl Baptism', 'Girl Burials'],
          'Annual population change (baptisms - burials)',
          'annual_gender_change.png')

make_plot(['Boy Baptism', 'Boy Burials', 'Girl Baptism', 'Girl Burials'],
          'Cumulative population change',
          'cumulative_gender_change.png',
          cumsum=True)

make_plot(['Boy Baptism', 'Boy Burials'],
          'Cumulative Male population change',
          'cumulative_male_change.png',
          cumsum=True)

make_plot(['Girl Baptism', 'Girl Burials'],
          'Cumulative Female population change',
          'cumulative_female_change.png',
          cumsum=True)

