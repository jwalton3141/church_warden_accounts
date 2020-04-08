"""Functions to plot and summarise disbursements data in various ways."""

import matplotlib.pyplot as plt
import os

from utils.df_tools import total_from_pds, tidy_pds, make_year_col


plt.style.use('seaborn')
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
    # Loop over parishes and plot
    parishes = data.index.get_level_values(0).unique()

    for parish in parishes:
        fig, ax = make_fig_ax()
        plot_fn(fig, ax, data, parish)


def funeral_costs(data):
    """
    Plot the annual funeral expenditure for each parish as a percentage of
    total annual expenditure.
    """
    data = make_year_col(data)

    funerals = data[data['Standardized_Category'] == 'Funeral']

    funerals_groupby = funerals.groupby(['Parish_Name', 'Year']).sum()
    data_groupby = data.groupby(['Parish_Name', 'Year']).sum()

    funerals_groupby = total_from_pds(funerals_groupby)
    data_groupby = total_from_pds(data_groupby) 

    funeral_expenditure = (funerals_groupby.Total
                           / data_groupby.Total).dropna() * 100

    plot_parishes(funeral_expenditure, funeral_costs_plot)

    tabulate_summary(funerals_groupby, 'funeral_costs.txt')


def primary_categories(data):
    """
    Plot the total expenditure for each parish, grouping by primary category.
    """
    category_spends = data.groupby(['Parish_Name', 'Primary_category']).sum()

    category_spends = total_from_pds(category_spends)

    # Sort within groups on total expenditure
    g = category_spends.groupby(level=0, group_keys=False)
    category_spends = g.apply(lambda x: x.sort_values(by="Total",
                                                      ascending=False))

    plot_parishes(category_spends, primary_categories_plot)

    tabulate_summary(category_spends, 'primary_categories.txt')


def annual_total(data):
    """
    Plot the total annual expenditure for each parish.
    """
    data = make_year_col(data)

    groupby = data.groupby(['Parish_Name', 'Year']).sum()
    groupby = total_from_pds(groupby)

    plot_parishes(groupby, annual_total_plot)

    tabulate_summary(groupby, 'total_expenditure.txt')


def perambulation_costs(data):
    data = make_year_col(data)

    perambulation = data[data['Standardized_Category'] == 'Perambulation']

    perambulation_groupby = perambulation.groupby(['Parish_Name',
                                                   'Year']).sum()
    perambulation_groupby = total_from_pds(perambulation_groupby)

    plot_parishes(perambulation_groupby.Total, perambulation_plot)

    tabulate_summary(perambulation_groupby, 'perambulation.txt')


def savefig(fig, plot_base, parish, **kwargs):
    fig.tight_layout()
    file_name = os.path.join('output', '{}_{}.png'.format(plot_base, parish))
    fig.savefig(file_name, format='png', **kwargs)


def funeral_costs_plot(fig, ax, data, parish):
    ax.plot(data.loc[parish].reset_index().Year,
            data.loc[parish])
    ax.scatter(data.loc[parish].reset_index().Year,
               data.loc[parish])

    ax.set_title('{}: funeral expenditure as a '
                 'percentage of total expenditure.'.format(parish))
    ax.set_xlabel('Year')
    ax.set_ylabel('% Spending on funerals')

    savefig(fig, 'funeral_expenditure', parish, bbox_inches='tight')


def primary_categories_plot(fig, ax, data, parish):
    patches, texts, autotexts = ax.pie(data.loc[parish, 'Total'],
                                       labels=None,
                                       autopct='%1.f%%',
                                       pctdistance=1.15)

    ax.set_title(parish)
    ax.set_ylabel('')
    ax.legend(labels=data.loc[parish].index,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1),
              title="Expenditure by primary category")

    savefig(fig, 'primary_category', parish, bbox_inches='tight')


def annual_total_plot(fig, ax, data, parish):
    ax.plot(data.loc[parish].reset_index().Year, data.loc[parish, 'Total'])
    ax.scatter(data.loc[parish].reset_index().Year, data.loc[parish, 'Total'])

    ax.set_title(parish + ': total annual expenditure')
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    savefig(fig, 'total_expenditure', parish, bbox_inches='tight')


def perambulation_plot(fig, ax, data, parish): 
    ax.plot(data.loc[parish].reset_index().Year,
            data.loc[parish])
    ax.scatter(data.loc[parish].reset_index().Year,
               data.loc[parish])

    ax.set_title('{}: Annual perambulation expenditure'.format(parish))
    ax.set_xlabel('Year')
    ax.set_ylabel('Expenditure in pence')

    savefig(fig, 'perambulation_expenditure', parish, bbox_inches='tight')

