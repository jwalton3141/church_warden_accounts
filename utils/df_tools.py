"""
These functions are intended to make it easier to perform common manipulations with the 
Disbursements dataset.
"""

import pandas as pd


def make_year_col(data):
    """Create a 'Year' column."""
    data['Year'] = data['Date'].map(lambda x: x.year)
    return data


def total_from_pds(data):
    """Compute the total expenditure in pence."""
    data['Total'] = (data.Pounds * 20 * 12
                   + data.Shillings * 12
                   + data.Pence)
    return data


def tidy_pds(data):
    """Tidy up 'Pounds', 'Shillings' and 'Pence column."""
    data = data.astype({"Pounds": int,
                        "Shillings": int,
                        "Pence": int})
    # Convert pence to shillings
    data.Shillings += data.Pence // 12
    # Left over / uncoverted pence
    data.Pence %= 12
    # Convert shillings to pounds
    data.Pounds += data.Shillings // 20
    # Left over / unconverted shillings
    data.Shillings %= 20
    return data
