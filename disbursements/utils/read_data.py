"""Read data from .accdb file, store as a dict object and pickle."""

import os
import os.path as path
import pandas as pd
import pickle
import pyodbc


def __read_accdb(file_path):
    """Read accdb file from file_path and store as a dictionary."""
    # Establish a connection to desired file
    conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' +
                          r'Dbq={}'.format(file_path))

    # List of table in file
    tables = ['Disbursements',
              'Disbursement_Totals',
              'Receipts',
              'Receipts_Totals',
              'Remains']

    # Read tables in
    accdb = {table: pd.read_sql('select * from {}'.format(table), conn)
             for table in tables}

    return accdb


def accdb2pkl(file_path=None):
    """Load accdb file and save as a pickled dictionary."""
    # Construct the path to the data/ directory
    data_dir_path = path.join(
                        path.dirname(
                            path.dirname(
                                path.realpath(__file__))),
                        'data')

    # If database not specified explicitly
    if not file_path:
        # List files with accdb extension in data/ directory
        databases = [file for file in os.listdir(data_dir_path)
                     if file.endswith('.accdb')]

        # Prompt user to ensure data is located where it should be
        assert len(databases) == 1, \
            ("{} databases found in {}. "
             "Ensure directory contains 1 database.".format(len(databases),
                                                            data_dir_path))

        # Construct path to database
        file_path = path.join(data_dir_path, databases[0])

    # Read accdb file in and store as a dictionary
    accdb = __read_accdb(file_path)

    # Output name
    pkl_path = path.join(data_dir_path, 'accdb.pkl')

    # Pickle accdb and save in the output directory
    with open(pkl_path, 'wb') as f:
        pickle.dump(accdb, f, protocol=-1)

    return accdb


def load_pkl_accdb(pkl_path=None):
    """Load and return the pickled accdb dictionary."""
    if not pkl_path:
        # Construct path to data directory
        data_dir_path = path.join(
                            path.dirname(
                                path.dirname(
                                    path.realpath(__file__))),
                            'data')
        # Get path to file
        pkl_path = path.join(data_dir_path, 'accdb.pkl')

    # Load file pkl_path
    with open(pkl_path, 'rb') as f:
        accdb = pickle.load(f)

    return accdb
