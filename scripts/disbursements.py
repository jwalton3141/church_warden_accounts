"""Functions to plot and summarise disbursements data in various ways."""

import matplotlib.pyplot as plt
import os

from utils.df_tools import total_from_pds, tidy_pds, make_year_col


plt.rcParams['text.usetex'] = False

# If running under windows use times new roman font
if os.name == 'nt':
    plt.rcParams["font.family"] = "Times New Roman"


def make_fig_ax():
    """Create figure and axes instances to plot on."""
    return plt.subplots(1, 1, figsize=[10, 6.18])


def tabulate_summary(df, tab_name):
    """"Tabulate expenditure detailed in df."""
    df = tidy_pds(df)
    table_path = os.path.join('output', tab_name)

    with open(table_path, 'w') as f:
        f.write(df[["Pounds", "Shillings", "Pence"]].to_string())


def plot_parishes(data, plot_fn):
    """Loop over parishes detailed in data and apply plot_fn()."""
    # List of parishes detailed in data
    parishes = data.index.get_level_values(0).unique()

    # Loop over parishes and plot
    for parish in parishes:
        fig, ax = make_fig_ax()
        plot_fn(fig, ax, data, parish)


def funeral_costs(data):
    """
    Plot and tabulate annual funeral expenditure for each parish as a percentage of total
    annual expenditure.
    """
    data = make_year_col(data)

    # Extract data relating to funerals
    funerals = data[data['Standardized_Category'] == 'Funeral']

    # Sum over parish and year
    funerals_groupby = funerals.groupby(['Parish_Name', 'Year']).sum()
    data_groupby = data.groupby(['Parish_Name', 'Year']).sum()

    # Rewrite pounds, shilling and pence nice
    funerals_groupby = total_from_pds(funerals_groupby)
    data_groupby = total_from_pds(data_groupby) 
# Compute funeral expenditure as a percentage of total expenditure
    funeral_expenditure = (funerals_groupby.Total
                           / data_groupby.Total).dropna() * 100

    # Plot data
    plot_parishes(funeral_expenditure, funeral_costs_plot)

    # Tabulate data
    tabulate_summary(funerals_groupby, 'funeral_costs.txt')


def funeral_costs_plot(fig, ax, data, parish):
    """
    Plot annual funeral expenditure as a percentage of total expenditure for all parishes.
    """
    # Line plot year against expenditure
    ax.plot(data.loc[parish].reset_index().Year,
            data.loc[parish])

    # Scatter  plot year against expenditure
    ax.scatter(data.loc[parish].reset_index().Year,
               data.loc[parish])

    # Title and labels
    ax.set_title('{}: funeral expenditure as a '
                 'percentage of total expenditure.'.format(parish))
    ax.set_xlabel('Year')
    ax.set_ylabel('% Spending on funerals')

    # Save plot
    savefig(fig, 'funeral_expenditure', parish, bbox_inches='tight')


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
    plot_parishes(category_spends, primary_categories_plot)

    # Tabulate data
    tabulate_summary(category_spends, 'primary_categories.txt')


def primary_categories_plot(fig, ax, data, parish):
    """Produce pie chart of parish spending by primary category."""
    # Plot pie on ax
    patches, texts, autotexts = ax.pie(data.loc[parish, 'Total'],
                                       labels=None,
                                       autopct='%1.f%%',
                                       pctdistance=1.15)

    # Title, labels and legend
    ax.set_title(parish)
    ax.set_ylabel('')
    ax.legend(labels=data.loc[parish].index,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              title="Expenditure by primary category")

    # Save plot
    savefig(fig, 'primary_category', parish, bbox_inches='tight')


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
    plot_parishes(groupby, annual_total_plot)

    # Tabulate data
    tabulate_summary(groupby, 'total_expenditure.txt')


def annual_total_plot(fig, ax, data, parish):
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


def perambulation_costs(data):
    """Plot and tabulate the annual spend on perambulation."""
    data = make_year_col(data)

    # Extract data regarding perambulation
    perambulation = data[data['Standardized_Category'] == 'Perambulation']

    # Sum expenditure by year and parish
    perambulation_groupby = perambulation.groupby(['Parish_Name',
                                                   'Year']).sum()
    # Tidy pounds, shillings and pence
    perambulation_groupby = total_from_pds(perambulation_groupby)

    # Plot expenditure
    plot_parishes(perambulation_groupby.Total, perambulation_plot)

    # Tabulate expenditure
    tabulate_summary(perambulation_groupby, 'perambulation.txt')


def perambulation_plot(fig, ax, data, parish): 
    """Plot annual expenditure on perambulation for parish."""
    # Line plot of year vs. perambulation expenditure
    ax.plot(data.loc[parish].reset_index().Year,
            data.loc[parish])
    # Scatter plot of year vs. perambulation expenditure
    ax.scatter(data.loc[parish].reset_index().Year,
               data.loc[parish])

    # Titles and labels
    ax.set_title('{}: Annual perambulation expenditure'.format(parish))
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    # Save plot
    savefig(fig, 'perambulation_expenditure', parish, bbox_inches='tight')


def savefig(fig, plot_base, parish, **kwargs):
    """Convenience function for saving plots."""
    fig.tight_layout()

    # Construct file name of plot
    file_name = os.path.join('output', '{}_{}.png'.format(plot_base, parish))
    fig.savefig(file_name, format='png', **kwargs)

