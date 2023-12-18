# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 02:56:52 2023

@author: Rhino
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import stats

plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False


def read_and_process(file):
    """Reads a csv file and returns two dataframes"""
    df = pd.read_csv("climate.csv", skiprows=4)
    # Drop the unnamed column
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    # Drop unwanted columns
    df.drop(columns=['Indicator Code', 'Country Code'], inplace=True)
    # Transform to get countries as columns
    df.set_index(['Country Name', 'Indicator Name'], inplace=True)
    # Fill missing data
    countries_df = df.T.ffill()
    return countries_df, df


def map_corr(df, size=6, cmap='viridis', title=None):
    """Function creates heatmap of correlation matrix for each pair of
    columns in the dataframe.
    Input:
    df: pandas DataFrame
    size: vertical and horizontal size of the plot (in inch)
    """
    # Create a correlation matrix
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(size+2, size))
    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)
    im = ax.imshow(corr, cmap=cmap)
    labels = ['Urban pop (%)', 'Population, total', 'Arable land (%)',
              'Forest area (%)', 'CO2 emissions (kt)',
              'Electricity (kWh per capita)']
    # Setting ticks to column names
    plt.xticks(range(len(corr.columns)), labels, rotation=90)
    plt.yticks(range(len(corr.columns)), labels)
    plt.title(title)
    # Add the color bar
    cbar = ax.figure.colorbar(im, ax=ax)
    cbar.ax.set_ylabel("Color bar", rotation=-90, va='center')
    cbar.ax.set_yticks(np.arange(-1, 1.25, 0.25))
    plt.savefig(f'{title}_heatmap.png', bbox_inches='tight', dpi=200)


# Calling the main function to read the file
countries_df, years_df = read_and_process('climate.csv')

print(countries_df)

print(years_df)

# Statistical Summary
years_df.describe()
countries_of_interest = countries_df[['Canada', 'India', 'China',
                                      'United States', 'European Union']]
indicators_of_interest = ['Urban population (% of total population)',
                          'Population, total', 'Arable land (% of land area)',
                          'Forest area (% of land area)', 'CO2 emissions (kt)',
                          'Electric power consumption (kWh per capita)']
countries_of_interest.describe()

# Skewness
skewness = stats.skew(countries_of_interest.loc['1965':'2022']['China']
                      ['Population growth (annual %)'])
print(skewness)

# Kurtosis
kurtosis = stats.kurtosis(countries_of_interest.loc['1965':'2022']['China']
                          ['Population growth (annual %)'])
print(kurtosis)
