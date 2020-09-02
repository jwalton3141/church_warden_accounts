#! /usr/bin/env python3

"""Plot and tabulate changes in tax payers."""

import matplotlib.pyplot as plt
import numpy as np
import os.path as path
import pandas as pd

from pretty import make_fig_ax
from migration.utils.read_data import load_tax


def compute_tax_payer_changes():
    """Compute the percentage change in tax-payers each year."""
    # Construct table to record results in
    df = pd.DataFrame(columns=data.columns,
                      index=data.columns)

    np.fill_diagonal(df.values, 100)

    # Loop over cohorts
    for i, cohort in enumerate(data.columns):
        cohort_names = set(data[cohort].dropna())
        cohort_size = len(cohort_names)

        # Loop over future years
        for j in range(i+1, len(data.columns)):
            # Get future year
            future_year = data.columns[j]
            # Get names of rate payers in future year
            future_year_names = set(data[future_year].dropna())

            # Remove members of cohort who didn't pay tax in future_year
            cohort_names = cohort_names.intersection(future_year_names)

            # Percentage of cohort still paying in future_year
            df.iloc[i, j] = len(cohort_names) / cohort_size * 100

    return df


def construct_output_path():
    """Construct the path to the output directory."""
    output_path = path.join(
                      path.dirname(
                          path.dirname(
                              path.realpath(__file__))),
                      'output')
    return output_path


def write_table(output_path, df):
    """Write computed values to dataframe."""
    with open(path.join(output_path, 'tax_payers.txt'), 'w') as f:
        f.write(df.rename_axis(columns="%").to_string(na_rep='-'))


if __name__ == "__main__":
    # Load rate payers data
    data = load_tax()

    # Crunch numbers
    df = compute_tax_payer_changes()

    output_path = construct_output_path()

    # Write output to table
    write_table(output_path, df)
