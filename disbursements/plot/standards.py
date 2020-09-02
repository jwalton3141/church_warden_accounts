"""Functions to plot and summarise disbursements data in various ways."""

import matplotlib.pyplot as plt
import os

from utils.df_tools import total_from_pds, tidy_pds, make_year_col
from plot.pretty import make_fig_ax, savefig

plt.style.use('seaborn')


# Ensure categories are represented by the same colour in each plot
categories = ['Bells',
              'Charity',
              'Churchyard',
              'Church Interior',
              'Church Structure',
              'Communion Bread and Wine',
              'Miscellaneous',
              'Parish Administration']
category_colours = dict(zip(categories, plt.cm.tab10.colors[:len(categories)]))


def annual_total(data):
    """
    Plot and tabulate the total annual expenditure for each parish.
    """
    data = make_year_col(data)

    # Sum expenditure over parish and year
    groupby = data.groupby(['Parish_Name', 'Year']).sum()
    # Tiday pounds, shillings and pence
    groupby = total_from_pds(groupby)

    # Plot data
    __plot_parishes(groupby, __annual_total_plot)

    # Tabulate data
    __tabulate_summary(groupby, 'total_expenditure.txt')


def primary_categories(data):
    """
    Plot and tabulate total expenditure for each parish, grouping by primary category.
    """
    # Sum expenditure over parish and category
    category_spends = data.groupby(['Parish_Name', 'Primary_category']).sum()

    # Tidy up pounds, shillings and pence totals
    category_spends = total_from_pds(category_spends)

    # Sort within groups on total expenditure
    g = category_spends.groupby(level=0, group_keys=False)
    category_spends = g.apply(lambda x: x.sort_values(by="Total",
                                                      ascending=False))

    # Plot data
    __plot_parishes(category_spends, __primary_categories_plot)

    # Tabulate data
    __tabulate_summary(category_spends, 'primary_categories.txt')


def __primary_categories_plot(fig, ax, data, parish):
    """Produce pie chart of parish spending by primary category."""
    # Display categories alphatbetically
    data.sort_index(inplace=True)
    colors = [category_colours[v] for v in data.loc[parish].index]
    # Plot pie on ax
    patches, texts, autotexts = ax.pie(data.loc[parish, 'Total'],
                                       labels=None,
                                       autopct='%1.f%%',
                                       pctdistance=1.15,
                                       colors=colors)

    # Title, labels and legend
    ax.set_title(parish)
    ax.set_ylabel('')
    ax.legend(labels=data.loc[parish].index,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              title="Expenditure by primary category")

    # Save plot
    savefig(fig, 'primary_category', parish, bbox_inches='tight')


def __annual_total_plot(fig, ax, data, parish):
    """Plot total annual expenditure for parish."""
    # Line plot of year vs. total expenditure
    ax.plot(data.loc[parish].reset_index().Year,
            data.loc[parish, 'Total'])
    # Scatter plot of year vs. total expenditure
    ax.scatter(data.loc[parish].reset_index().Year,
            data.loc[parish, 'Total'])

    # Set title and labels
    ax.set_title(parish + ': total annual expenditure')
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    # Save plot
    savefig(fig, 'total_expenditure', parish, bbox_inches='tight')


def __tabulate_summary(df, tab_name):
    """"Tabulate expenditure detailed in df."""
    df = tidy_pds(df)
    table_path = os.path.join('output', 'standards', tab_name)

    with open(table_path, 'w') as f:
        f.write(df[["Pounds", "Shillings", "Pence"]].to_string())


def __plot_parishes(data, plot_fn):
    """Loop over parishes detailed in data and apply plot_fn()."""
    # List of parishes detailed in data
    parishes = data.index.get_level_values(0).unique()

    # Loop over parishes and plot
    for parish in parishes:
        fig, ax = make_fig_ax()
        plot_fn(fig, ax, data, parish)

