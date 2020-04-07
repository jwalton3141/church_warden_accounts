"""Functions to plot and summarise disbursements data in various ways."""

import matplotlib.pyplot as plt
import os

import utils.df_tools as df

plt.rcParams['text.usetex'] = False

def annual_funeral_spends(data):
    """
    Plot the annual funeral expenditure for each parish, as a percentage of total annual
    expenditure.
    """
    data = df.make_year_col(data)

    funeral_data = data[data['Standardized_Category'] == 'Funeral']

    funeral_groupby = funeral_data.groupby(['Parish_Name', 'Year']).sum()
    data_groupby = data.groupby(['Parish_Name', 'Year']).sum()

    funeral_groupby = df.total_from_pds(funeral_groupby)
    data_groupby = df.total_from_pds(data_groupby) 

    percent_on_funeral = (funeral_groupby.Total / data_groupby.Total).dropna() * 100

    # Loop over parishes and plot
    parishes = funeral_groupby.index.levels[0]
    for parish in parishes:
        fig, ax = plt.subplots(1, 1, figsize=[10, 5])

        ax.plot(percent_on_funeral.loc[parish].reset_index().Year,
                percent_on_funeral.loc[parish])

        ax.set_title(parish + ': funeral expenditure as a percentage of total expenditure.')
        ax.set_xlabel('Year')
        ax.set_ylabel('% Spending on funerals')

        fig.tight_layout()
        file_name = os.path.join(r'output', '{}_funeral_expenditure.png'.format(parish))
        fig.savefig(file_name, format='png', bbox_inches='tight')

    funeral_groupby = df.tidy_pds(funeral_groupby)
    table_name = os.path.join('output', 'funeral_expenditure.txt')
    with open(table_name, 'w') as f:
        f.write(funeral_groupby[["Pounds", "Shillings", "Pence"]].to_string())


def primary_category_spends(data):
    """
    Plot the total expenditure for each parish, grouping by primary category.
    """
    groupby = data.groupby(['Parish_Name', 'Primary_category']).sum()

    groupby = df.total_from_pds(groupby)

    # Sort within groups on total expenditure
    g = groupby.groupby(level=0, group_keys=False)
    groupby = g.apply(lambda x: x.sort_values(by="Total", ascending=False))

    # Loop over parishes and plot
    parishes = groupby.index.levels[0]
    for parish in parishes:
        fig, ax = plt.subplots(1, 1, subplot_kw=dict(aspect="equal"), figsize=[10, 5])

        patches, texts, autotexts = ax.pie(groupby.loc[parish, 'Total'],
                                           labels=None,
                                           autopct='%1.f%%',
                                           pctdistance=1.15)

        ax.set_title(parish)
        ax.set_ylabel('')
        ax.legend(labels=groupby.loc[parish].index,
                  loc="center left",
                  bbox_to_anchor=(1, 0, 0.5, 1),
                  title="Expenditure by primary category")

        fig.tight_layout()
        file_name = os.path.join(r'output', '{}_primary_category.png'.format(parish))
        fig.savefig(file_name, format='png', bbox_inches='tight')

    groupby = df.tidy_pds(groupby)
    table_name = os.path.join('output', 'primary_category.txt')
    with open(table_name, 'w') as f:
        f.write(groupby[["Pounds", "Shillings", "Pence"]].to_string())


def total_annual_spends(data):
    """
    Plot the total annual expenditure for each parish.
    """
    data = df.make_year_col(data)

    groupby = data.groupby(['Parish_Name', 'Year']).sum()
    groupby = df.total_from_pds(groupby)

    # Loop over parishes and plot
    parishes = groupby.index.levels[0]
    for parish in parishes:
        fig, ax = plt.subplots(1, 1, figsize=[10, 5])

        ax.plot(groupby.loc[parish].reset_index().Year,
                groupby.loc[parish, 'Total'])

        ax.set_title(parish + ': total annual expenditure')
        ax.set_xlabel('Year')
        ax.set_ylabel('Expenditure in pence')
        fig.tight_layout()

        file_name = os.path.join(r'output', '{}_total_expenditure.png'.format(parish))
        fig.savefig(file_name, format='png')

    groupby = df.tidy_pds(groupby)
    table_name = os.path.join('output', 'total_expenditure.txt')
    with open(table_name, 'w') as f:
        f.write(groupby[["Pounds", "Shillings", "Pence"]].to_string())

