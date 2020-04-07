# About

`run_me.py` is the master script for this project. It will produce plots and
other outputs for the latest version of our Microsoft Access Database.

## How it works

All of the output generated by `run_me.py` will be saved in the `output/`
directory. For `run_me.py` to find the Access Database correctly, `run_me.py`
must be located one directory deeper than the database. An example directory
set up for this project could look like the following:

`
.
├── CWAs_F.accdb
└── python
    ├── output
    ├── README.md
    ├── run_me.py
    ├── scripts
    │   ├── plot_cost_breakdown.py
    │   └── read_data.py
    └── tools
        └── pds_calc.py
`

## Microsoft drivers

To be able to read the latest version of our Access database we need to use
a machine with the appropriate windows drivers. Linux solutions to this
problem are unstable and difficult to get right. 
