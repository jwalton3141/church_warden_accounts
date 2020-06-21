#! /usr/bin/env python3

"""Run this script to generate all outputs for latest data."""

from utils.read_data import accdb2pkl
import plot.make
import plot.standards


def main():
    accdb = accdb2pkl()

    data = accdb["Disbursements"]

    plot.standards.primary_categories(data)
    plot.standards.annual_total(data)

    plot.make.custom(data, 'Standardized_Category', 'Funeral')
    plot.make.custom(data, 'Standardized_Category', 'Perambulation')
    plot.make.custom(data, 'Standardized_Category', 'Book of Common Prayer')
    plot.make.custom(data, 'Standardized_Category', 'Sermons')


if __name__ == "__main__":
    main()
