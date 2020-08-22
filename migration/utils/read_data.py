#! /usr/bin/env python3

"""Modules to load excel data and match parishes to geographical locations."""

import pandas as pd
import numpy as np
import os
import os.path as path
import re

from utils.get_locs import selenium_lookup


def read_excel(file_name, **kwargs):
    """Load excel spreadsheet from data directory."""
    # Ensure filename ends with xlsx extension
    file_name += (not file_name.endswith('.xlsx')) * '.xlsx'

    # Construct path to data directory
    data_dir_path = path.join(
                        path.dirname(
                            path.dirname(
                                path.realpath(__file__))),
                        'data')

    # List the files in the data directory
    files = os.listdir(data_dir_path)

    # Check that the requested file exists
    assert file_name in files, \
            "file '{}' not found in directory '{}'".format(file_name,
                                                           data_dir_path)

    # Read and return
    return pd.read_excel(path.join(data_dir_path, file_name), **kwargs)


def load_population():
    """Load the population changes data."""
    return read_excel('Population_Change', {'index_col': 0})


def load_marriages():
    """Load and prep marriage data."""
    # Load data
    data = read_excel('Marriage_Migration', {'sheet_name': None})

    # Tidy data
    data = tidy_marriages(data)

    # Count occurances of pairs
    pairs, counts = np.unique(data, axis=0, return_counts=True)

    # Get locations
    locations = lookup_locs(data)

    return pairs, counts, locations


def load_tax():
    """Load tax data."""
    df = read_excel('Rate_Payers_Excel.xlsx')
    # Drop Empty columns
    df = df.loc[:, [isinstance(col, int) for col in df.columns]]
    return df

def tidy_marriages(data):
    """Extract the groom and bride parish from spreadsheet and clean."""
    # Extract parsishes of Groom (dropping nans and empty entries)
    x = [list(values['Parish']) for values in data.values()
            if np.any(values['Parish'])]
    # Extract parished of Bride (dropping nans and empty entries)
    y = [list(values['Parish.1']) for values in data.values()
            if np.any(values['Parish.1'])]

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

    # Construct the path to the output directory
    out_dir = path.join(
                  path.dirname(
                      path.dirname(
                          path.realpath(__file__))),
                  'output')

    # Construct path to lookup table
    path_to_table = path.join(out_dir, 'parish_locations.xlsx')

    # If lookup table does not exist
    if not path.isfile(path_to_table):
        # Perform lookup 
        df = selenium_lookup(parishes)
        # Write lookup table
        df.to_excel(path_to_table)
    else:
        # Read in current lookup table
        df = pd.read_excel(path_to_table, index_col=0)

        # Construct boolean indicating which parishes already exist in lookup
        # regex drops problems with titles which include parentheses
        located = np.array([np.any(df.Title.str.contains(parish, regex=False))
                            for parish in parishes])

        # Lookup parishes not already listed
        if len(parishes[~located]) >0:
            # New entries
            new_locs = selenium_lookup(parishes[~located])

            # Append new entries
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

