#! /usr/bin/env python3

"""
Run this script to generate all outputs for latest data.

Running this script will overwrite all the output in the output/ directory.
This script and all subsequent scripts will never alter the accdb file.
"""

from utils.read_data import accdb2pkl
import scripts.plotting as plot

if __name__ == "__main__":
    accdb = accdb2pkl()

    data = accdb["Disbursements"]

    plot.annual_funeral_spends(data)
    plot.primary_category_spends(data)
    plot.total_annual_spends(data)
