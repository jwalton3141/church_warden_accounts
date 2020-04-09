#! /usr/bin/env python3

"""
Run this script to generate all outputs for latest data.

Running this script will overwrite all the output in the output/ directory.
This script and all subsequent scripts will never alter the accdb file.
"""

from utils.read_data import accdb2pkl
import plotting as plot


def main():
    accdb = accdb2pkl()

    data = accdb["Disbursements"]
    plot_data(data)


def plot_data(data):
    plot.funeral_costs(data)
    plot.primary_categories(data)
    plot.annual_total(data)
    plot.perambulation_costs(data)


if __name__ == "__main__":
    main()
