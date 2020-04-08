#! /usr/bin/env python3

"""
This script is intended to make it easier to sum up monies detailed in pounds,
shillings and pence.
"""

import numpy as np
import pandas as pd
import sys

from df_tools import tidy_pds


def get_inputs():
    """Get the pounds, shillings and pence to sum from the user.
    
    The data can be specified either "row"wise or "column"wise.
    
    In row-wise entry each individual input must contain three comma separated
    values: pounds,shillings,pence.

    In column-wise entry one first lists all the pounds to sum, followed by all
    the shillings to sum and then all the pence to sum.
    """
    # Query how data will be entered
    entry = input("Row or column input? ").lower()[:3]
    if entry not in ['row','col']:
        print("Input must either be 'row' or 'col', not '{}'".format(entry))
        sys.exit(1)

    if entry == 'row':
        df = get_row_inputs()
    else:
        df = get_col_inputs()

    return df


def get_row_inputs():
    """Parse user input where each entry is given as pounds,shillings,pence."""
    # Create empty lists to store data
    data = {'Pounds': [],
            'Shillings': [],
            'Pence': []
            }

    # For row-wise input we don't know the number of entries to expect
    while True:
        # Get input
        entry = input("Enter pounds, shilings and pence separated by commas, "
                      "or enter [n] to sum total: ")

        # Stop prompting for entries if [n] input received
        if entry.lower() == 'n':
            break
        else:
            # Make sure entry looks like we expect
            if entry.count(',') != 2:
                print("Expected three comma separated values as "
                      "'pounds,shillings,pence'. Last entry not included. "
                      "Please re-input the last entry.")
                continue

            # Remove miscellaneous spaces
            entry = entry.replace(" ", "")
            # Split values into pounds, shillings and pence
            monies = entry.split(',')

            # Append entries to lists
            data['Pounds'].append(int(monies[0]))
            data['Shillings'].append(int(monies[1]))
            data['Pence'].append(int(monies[2]))

    return pd.DataFrame(data)


def get_col_inputs():
    """
    Parse user input where all the pounds are first detailed, followed by
    all the shillings and finally all the pence.
    """
    data = {}

    for denomination in ['Pounds', 'Shillings', 'Pence']:
        prompt_text = ("Enter {}, separated by commas, "
                       "including 0 entries: ".format(denomination))
        data[denomination] = input(prompt_text).split(',')
        # From strings to ints
        data[denomination] = [int(val) for val in data[denomination]]

    # Get the numbers of entry for each denomination
    lengths = [len(denom) for denom in list(data.values())]
    if not lengths[1:] == lengths[:-1]:
        print("You must enter an equal number of pounds, pence and shillings. "
              "You made {} pound entries, {} shilling entries and {} pence "
              "entries.".format(lengths[0], lengths[1], lengths[2]))
        sys.exit(1)

    return pd.DataFrame(data)


def perform_sum(data):
    """Add all the numbers up innit"""
    summed = tidy_pds(data.sum())

    print('\nTotal is: {} pounds, {} shillings'
          ' and {} pence.'.format(summed.Pounds,
                                  summed.Shillings,
                                  summed.Pence))


def main():
    df = get_inputs()
    perform_sum(df)


if __name__ == "__main__":
    main()
