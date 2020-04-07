#! /usr/bin/env python3

"""
This script is intended to make it easier to sum up monies, detailed in pounds,
shillings and pence.
"""

import numpy as np

# Create empty lists to store input in
pounds = []
shillings = []
pence = []

# Prompt for input
while True:
    # Get user input
    entry = input("Enter pounds, shillling, pence (comma separated). Or hit [n] to sum total: ")
    if entry.lower() == 'n':
        break        
    else:
        # Remove any miscellaneous spaces that have worked their way in
        entry = entry.replace(" ", "")
        # Split values into pounds, shillings and pence
        monies = entry.split(',')
        # Append to list of values
        pounds.append(int(monies[0]))
        shillings.append(int(monies[1]))
        pence.append(int(monies[2]))

# Make lists in arrays
pounds = np.array(pounds)
shillings = np.array(shillings)
pence = np.array(pence)

# Add up total in pence
pence_total = (20 * 12 * pounds + 12 * shillings + pence).sum()

# Convert pence sum back into pounds, shillings and pence
pounds_total = pence_total // (20*12)
shillings_total = (pence_total - pounds_total * 20 * 12) // 12
pence_total = (pence_total - pounds_total * 20 * 12 - shillings_total * 12)

print('\nTotal is: {} pounds, {} shillings and {} pence.'.format(pounds_total,
                                                                 shillings_total,
                                                                 pence_total))
