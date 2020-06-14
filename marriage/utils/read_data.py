#! /usr/bin/env python3

"""Modules to load excel data and match parishes to geographical locations."""

import pandas as pd
import numpy as np
import os
import os.path as path
import re

from get_locs import selenium_lookup


def load_data(file_name=None):
    """Load data."""
    # Get the path to the data directory
    data_dir_path = path.join(path.dirname(
                              path.dirname(
                              path.realpath(__file__))),
                              'data')

    if not file_name:
        # Get all the files in the data directory
        files = os.listdir(data_dir_path)
        # Get files with spreadsheet file extenstion
        spreadsheets = [file for file in files if file.endswith('.xlsx')]

        # Prompt user to ensure data is located where it should be
        if len(spreadsheets) > 1:
            print("{} spreadsheets found in {}. Ensure directory only contains 1 "
                  "spreadsheet.".format(len(spreadsheets), data_dir_path))
            sys.exit(1)
        elif len(spreadsheets) == 0:
            print("No spreadsheets found in {0}. Ensure {0} contains spreadsheet "
                  "file.".format(data_dir_path))
            sys.exit(1)

        # Construct path to spreadsheet
        file_name = path.join(data_dir_path, spreadsheets[0])

    # Load data
    data = pd.read_excel(file_name, sheet_name=None)

    # Tidy data
    data = tidy_data(data)

    # Add locations to data
    data = add_locs(data)

    return data


def tidy_data(data):
    """Extract the groom and bride parish from spreadsheet and clean."""
    # Extract parsishes of Groom (dropping nans and empty entries)
    x = [list(values['Parish']) for values in data.values() if np.any(values['Parish'])]
    # Extract parished of Bride (dropping nans and empty entries)
    y = [list(values['Parish.1']) for values in data.values() if np.any(values['Parish.1'])]

    # Flatten list of lists structure
    x = [item for sublist in x for item in sublist]
    y = [item for sublist in y for item in sublist]

    # Remove whitespace that may mistakenly occur at the beginning or end of entries
    x = [re.sub(r'^\s+|\s+$', '', string) for string in x]
    y = [re.sub(r'^\s+|\s+$', '', string) for string in y]

    return np.vstack([np.array(x), np.array(y)]).T


def add_locs(data):
    """Append location data to Parish names."""
    # Make sure our lookup table is up to date
    update_lookup(data)
    return data


def update_lookup(data):
    """Get location data for each parish."""
    # Get list of parishes referenced
    parishes = np.unique(data)

    # Get path to output directory
    out_dir = path.join(
                path.dirname(
                path.dirname(
                    path.realpath(__file__))),
                'output')
    # Get path to spreadsheet
    path_to_table = path.join(out_dir, 'parish_locations.xlsx')

    if not path.isfile(path_to_table):
        # Lookup all listed parishes
        df = selenium_lookup(parishes)
        # Write lookup table
        df.to_excel(path_to_table)
    else:
        # Read in what we've already got
        df = pd.read_excel(path_to_table, index_col=0)

        # Construct boolean which indicates whether a parish is in the lookup table
        # regex drops problems with titles including brackets
        located = np.array([np.any(df.Title.str.contains(parish, regex=False))
                            for parish in parishes])

        # If there are any parishes in data which aren't in df, look them up
        if len(parishes[~located]) >0:
            # Lookup locations of parishes not listed in current table
            new_locs = selenium_lookup(parishes[~located])

            # Append missing parishes
            df = df.append(new_locs, ignore_index=True)

            # Sort alphabetically
            df = df.sort_values('Title', ignore_index=True)

            # Write lookup table
            df.to_excel(path_to_table)


if __name__ == "__main__":
    load_data()
