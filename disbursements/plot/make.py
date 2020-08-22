"""Functions to plot and tabulate expenditure on entry."""

import matplotlib.pyplot as plt
import os

from utils.df_tools import total_from_pds, tidy_pds, make_year_col
from plot.pretty import make_fig_ax, savefig


def custom(data, category, entry):
    """Plot expenditure of entry in category."""
    # Plot per parish
    __custom_parish(data, category, entry)

    # Global plot over summed parishes
    __custom_total(data, category, entry)


def __custom_parish(data, category, entry):
    """Plot expenditure of entry in category per parish."""
    # Compute expenditure
    entry_total, entry_percent = __compute_expenditure(data, category, entry)

    # Plot expenditure
    __plot_parishes(entry_total.Total, entry, __plot_total)
    __plot_parishes(entry_percent, entry, __plot_percent)

    # Tabulate expenditure
    __tabulate_summary(entry_total, entry)


def __custom_total(data, category, entry):
    """Plot expenditure of entry in category over all parishes."""
    # Compute expenditure
    entry_total, entry_percent = __compute_expenditure(data, category, entry, by_parish=False)

    __plot_overall(entry_total.Total, entry)
    __plot_overall_percent(entry_percent, entry)


def __compute_expenditure(data, category, entry, by_parish=True):
    """Compute total and proportional expenditure."""
    data = data.copy()
    data = make_year_col(data)

    # Extract entry from category
    entry_data = data[data[category] == entry]

    # Sum expenditure by year and parish
    if by_parish:
        entry_groupby = entry_data.groupby(['Parish_Name', 'Year']).sum()
        data_groupby = data.groupby(['Parish_Name', 'Year']).sum()
    else:
        entry_groupby = entry_data.groupby(['Year']).sum()
        data_groupby = data.groupby(['Year']).sum()

    # Express expenditure in pence
    entry_groupby = total_from_pds(entry_groupby)
    data_groupby = total_from_pds(data_groupby)

    entry_total = entry_groupby.Total
    # Compute expenditure as percentage of total annual expenditure
    entry_percent = (entry_total / data_groupby.Total).dropna() * 100

    return entry_groupby, entry_percent


def __plot_overall(data, entry):
    fig, ax = make_fig_ax()
    __plot(ax, data)

    # Titles and labels
    ax.set_title('Annual {} expenditure'.format(entry))
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    # Save plot
    savefig(fig,
            '{}_expenditure'.format(entry),
            'overall',
            entry,
            bbox_inches='tight')


def __plot_overall_percent(data, entry):
    fig, ax = make_fig_ax()
    __plot(ax, data)

    # Titles and labels
    # Title and labels
    ax.set_title('Annual {} expenditure as a '
                 'percentage of total expenditure.'.format(entry))
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of total expenditure')

    # Save plot
    savefig(fig,
            '{}_percent_expenditure'.format(entry),
            'overall',
            entry,
            bbox_inches='tight')




def __plot_parishes(data, entry, plot_fn):
    """Loop over parishes detailed in data and apply plot_fn()."""
    # List of parishes detailed in data
    parishes = data.index.get_level_values(0).unique()

    # Loop over parishes and plot
    for parish in parishes:
        fig, ax = make_fig_ax()
        plot_fn(fig, ax, data, entry, parish)


def __plot_total(fig, ax, data, entry, parish):
    """Plot expenditure of parish on entry over time."""
    __plot(ax, data.loc[parish])

    # Titles and labels
    ax.set_title('{}: Annual {} expenditure'.format(parish, entry))
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    # Save plot
    savefig(fig,
            '{}_expenditure'.format(entry),
            parish,
            entry,
            bbox_inches='tight')


def __plot_percent(fig, ax, data, entry, parish):
    """Plot proportional expenditure of parish on entry over time."""
    __plot(ax, data.loc[parish])

    # Title and labels
    ax.set_title('{}: Annual {} expenditure as a '
                 'percentage of total expenditure.'.format(parish, entry))
    ax.set_xlabel('Year')
    ax.set_ylabel('Percentage of total expenditure')

    # Save plot
    savefig(fig,
            '{}_percent_expenditure'.format(entry),
            parish,
            entry,
            bbox_inches='tight')


def __plot(ax, data):
    """Plot parish data over time."""
    # Line plot of year vs. expenditure
    ax.plot(data.reset_index().Year, data)

    # Scatter plot of year vs. expenditure
    ax.scatter(data.reset_index().Year, data)

    # Set xlimits
    ax.set_xlim(data.reset_index().Year.min(),
                data.reset_index().Year.max())


def __tabulate_summary(df, entry):
    """"Tabulate expenditure detailed in df."""
    df = tidy_pds(df)
    table_path = os.path.join('output',
                              entry,
                              '{}_expenditure.txt'.format(entry))

    with open(table_path, 'w') as f:
        f.write(df[["Pounds", "Shillings", "Pence"]].to_string())

