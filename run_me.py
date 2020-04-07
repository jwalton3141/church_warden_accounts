#! /usr/bin/env python3

"""
Run this script to generate all the plots for the latest version of CWAs_F.accdb.

Running this script will overwrite all the plots saved in the output/ directory, so do be
careful! This script and all the associated python scripts will never alter CWAs_F.accdb.
"""

from utils.read_data import accdb2pkl
import scripts.plotting as plot

if __name__ == "__main__":
    accdb = accdb2pkl()

    data = accdb["Disbursements"]

    plot.annual_funeral_spends(data)
    plot.primary_category_spends(data)
    plot.total_annual_spends(data)

