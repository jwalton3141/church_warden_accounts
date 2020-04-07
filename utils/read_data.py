"""Read data from .accdb file, store as a dict object and pickle."""


import pandas as pd
import pickle
import pyodbc

def load_accdb(file_path):
    """
    Load accdb file located at file_path and store the data as a dictionary.
    """
    # Establish a connection to desired file
    conn = pyodbc.connect(
        r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};' +
        r'Dbq={}'.format(file_path))

    # Create empty dictionary to store tables in
    accdb = {}
    # List of table in file
    tables = ['Disbursements', 'Disbursement_Totals', 'Receipts',
              'Receipts_Totals', 'Remains']

    # Loop over all tables in file
    for table in tables:
        # Read data in table and add to dictionary
        accdb[table] = pd.read_sql('select * from {}'.format(table), conn)

    return accdb

def accdb2pkl(file_path="..\CWAs_F.accdb"):
    """
    Load the accdb file and save as a pickled dictionary.
    """
    # Read accdb file in and store as a dictionary
    accdb = load_accdb(file_path)

    # Pickle the dictionary object and save in the output directory
    with open(r"output\accdb.pkl", "wb") as f:
         pickle.dump(accdb, f, protocol=-1)

    return accdb

def load_pkl_accdb(pkl_path=r"output\accdb.pkl"):
    """ Load and return the pickled accdb dictionary """
    with open(pkl_path, 'rb') as f:
        accdb = pickle.load(f)
    return accdb

