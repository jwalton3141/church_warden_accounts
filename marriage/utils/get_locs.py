#! /usr/bin/env python3

"Modules to automate the lookup of pasish locations."""

import pandas as pd
import numpy as np
import os.path as path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def selenium_lookup(parishes):
    """Look up the latitude and longitude of the parishes."""
    # Get chrome up and running
    driver = webdriver.Chrome()
    # Wait up to 10 seconds for things to appear
    driver.implicitly_wait(10)
    # Navigate to map tool
    driver.get("https://gridreferencefinder.com/os.php")

    # Loop over parishes
    for i, parish in enumerate(parishes):
        # Grab the location entry
        elem = driver.find_element_by_id("txtLocation")
        # Clear any residual text in search box
        elem.clear()

        # Input parish name
        elem.send_keys(parish)
        # Search
        elem.send_keys(Keys.RETURN)

    txt = ''
    # Sometimes it takes a couple of goes for the data to appear
    while '\n' not in txt:
        # Export csv
        driver.execute_script('ukgrExports.exportCsv();')
        # Grab element which pops up
        elem = driver.find_element_by_id("dialog1-txtarea1")
        # Extract text from element
        txt = elem.text 

        # Click and close pop up
        elem = driver.find_element_by_id('dialog1-button1')
        elem.click()

    driver.close()

    # Tidy up the extracted data
    df = tidy_txt(txt)
    # Include parishes which couldn't be found by map tool
    df = fill_empties(df, parishes)

    return df


def tidy_txt(txt):
    """Clean up the data as extracted from the web."""
    # Split at newlines
    txt = txt.split('\n')
    # Strip newlines
    txt = [line.replace('\n', '') for line in txt]
    # Split entries for each parish
    txt =  [line.split('",') for line in txt]

    # Read into pandas dataframe
    df = pd.DataFrame(txt[1:], columns=txt[0])

    # Strip extra quotes from entries
    for col in range(df.shape[1]):
        df.iloc[:, col] = df.iloc[:, col].str.replace('"', '')

    # Strip extra quotes from column titles
    cols = list(df.columns)
    cols = [col.replace('"', '') for col in cols]
    df.columns = cols

    return df


def fill_empties(df, parishes):
    """Add in locations which couldn't be found as NANs."""
    # Boolean array which indicates whether an array was found or not
    located = np.array([np.any(df.Title.str.contains(parish)) for parish in parishes])

    # Extract the locations which couldn't be found
    df_lost = pd.DataFrame({'Title': parishes[~located]})

    # Pad columns to append with df
    for col in df.columns[1:]:
        df_lost[col] = np.nan

    # Append missing parishes
    df = df.append(df_lost, ignore_index=True)
    # Sort alphabetically
    df = df.sort_values('Title', ignore_index=True)

    return df

