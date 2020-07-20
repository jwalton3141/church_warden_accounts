#! /usr/bin/env python3

"""Modules to load excel data and match parishes to geographical locations."""

import pandas as pd
import numpy as np
import os
import os.path as path
import re
import sys

from utils.get_locs import selenium_lookup


def read_population(file_name=None):
    """Load the population changes data."""

    # Get the path to the data directory
    data_dir_path = path.join(path.dirname(
                              path.dirname(
                              path.realpath(__file__))),
                              'data')

    if not file_name:
        # Get all the files in the data directory
        files = os.listdir(data_dir_path)

        if 'Population_Change.xlsx' in files:
            file_name = path.join(data_dir_path, 'Population_Change.xlsx')
        else:
            print("Could not find spreadsheet with name "
                  "'Population_Change.xlsx' in folder "
                  "{}.".format(data_dir_path))

    data = pd.read_excel(file_name, sheet_name=None, index_col=0)['Sheet1']

    return data


def read_marriages(file_name=None):
    """Load marriages data."""
    # Get the path to the data directory
    data_dir_path = path.join(path.dirname(
                              path.dirname(
                              path.realpath(__file__))),
                              'data')

    if not file_name:
        # Get all the files in the data directory
        files = os.listdir(data_dir_path)

        if 'Marriage_Migration.xlsx' in files:
            file_name = path.join(data_dir_path, 'Marriage_Migration.xlsx')
        else:
            print("Could not find spreadsheet with name "
                  "'Marriage_Migration.xlsx' in folder "
                  "{}.".format(data_dir_path))

    # Load data
    data = pd.read_excel(file_name, sheet_name=None)

    # Tidy data
    data = tidy_marriages(data)

    # Count occurances of pairs
    pairs, counts = np.unique(data, axis=0, return_counts=True)

    # Get locations 
    locations = lookup_locs(data)

    return pairs, counts, locations


def tidy_marriages(data):
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


def lookup_locs(data):
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
            df = df.sort_values('Title')

            # Write lookup table
            df.to_excel(path_to_table)

    # Drop locations outside UK
    df.drop(df.index[df['Grid Reference'] == 'Not in UK'], inplace=True)

    # Drop locations with missing longitude or latitude
    df.drop(df.index[df.Longitude.isna() | df.Latitude.isna()], inplace=True)

    return df


if __name__ == "__main__":
    read_marriages()