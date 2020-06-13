#! /usr/bin/env python3

"""
Run this script to generate all outputs for latest data.

Running this script will overwrite all the output in the output/ directory.
This script and all subsequent scripts will never alter the accdb file.
"""

from utils.read_data import accdb2pkl
import disbursements as disb


def main():
    accdb = accdb2pkl()

    disbursements = accdb["Disbursements"]
    plot_disburements(disbursements)


def plot_disbursements(data):
    disb.funeral_costs(data)
    disb.primary_categories(data)
    disb.annual_total(data)
    disb.perambulation_costs(data)


if __name__ == "__main__":
    main()
