"""Read data from .accdb file, store as a dict object and pickle."""

import os.path as path
import pandas as pd
import pickle
import pyodbc

def read_accdb(file_path):
    """
    Read in accdb file located at file_path and store the data as a dictionary.
    """
    # Establish a connection to desired file
    conn = pyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' +
        r'Dbq={}'.format(file_path))

    # List of table in file
    tables = ['Disbursements', 'Disbursement_Totals', 'Receipts',
              'Receipts_Totals', 'Remains']

    # Read tables in
    accdb = {table: pd.read_sql('select * from {}'.format(table), conn)
             for table in tables}

    return accdb


def accdb2pkl(file_path=None):
    """Load the accdb file and save as a pickled dictionary."""
    proj_home = path.dirname(path.dirname(path.realpath(__file__)))
 
    if not file_path:
        file_path = path.join(path.dirname(proj_home), 'CWAs_Current_April.accdb')
      
    # Read accdb file in and store as a dictionary
    accdb = read_accdb(file_path)

    # Pickle the dictionary object and save in the output directory
    with open(path.join(proj_home, 'output', 'accdb.pkl'), "wb") as f:
         pickle.dump(accdb, f, protocol=-1)

    return accdb


def load_pkl_accdb(pkl_path=None):
    """Load and return the pickled accdb dictionary."""
    if not pkl_path:
        proj_home = path.dirname(path.realpath(__file__))
        pkl_path = path.join(proj_home, 'output', 'accdb.pkl')

    with open(pkl_path, 'rb') as f:
        accdb = pickle.load(f)

    return accdb
