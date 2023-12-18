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
print(countries_of_interest.describe())

# Skewness
skewness = stats.skew(countries_of_interest.loc['1965':'2022']['China']
                      ['Population growth (annual %)'])
print(f'Skewness: \n {skewness}')

# Kurtosis
kurtosis = stats.kurtosis(countries_of_interest.loc['1965':'2022']['China']
                          ['Population growth (annual %)'])
print(f'Kurtosis: \n {kurtosis}')

# Population, total bar plot
canada_pop = (countries_of_interest.loc['1992':'2023':6]['Canada']
              ['Population, total'])
india_pop = (countries_of_interest.loc['1992':'2023':6]['India']
             ['Population, total'])
china_pop = (countries_of_interest.loc['1992':'2023':6]['China']
             ['Population, total'])
us_pop = (countries_of_interest.loc['1992':'2023':6]['United States']
          ['Population, total'])
eu_pop = (countries_of_interest.loc['1992':'2023':6]['European Union']
          ['Population, total'])
bar_df = {'Canada': canada_pop, 'India': india_pop, 'China': china_pop,
          'USA': us_pop, 'European Union': eu_pop}

fig, ax = plt.subplots(layout='constrained')

x = np.arange(len(np.arange(1992, 2023, 6)))  # the label locations
width = 0.15  # the width of the bars
multiplier = 0
print(bar_df.items())
for attribute, measurement in bar_df.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1
ax.set_ylabel('Population')
ax.set_xlabel('Years')
# ax.set_yscale('log')
ax.set_title('Population total')
ax.set_xticks(x + width, np.arange(1992, 2023, 6))
ax.legend(loc='upper left', ncols=3)
plt.savefig('Pop_bar.png')
plt.show()

# CO2 emissions bar plot
canada_pop = (countries_of_interest.loc['1992':'2023':6]['Canada']
              ['CO2 emissions (kt)'])
india_pop = (countries_of_interest.loc['1992':'2023':6]['India']
             ['CO2 emissions (kt)'])
china_pop = (countries_of_interest.loc['1992':'2023':6]['China']
             ['CO2 emissions (kt)'])
us_pop = (countries_of_interest.loc['1992':'2023':6]['United States']
          ['CO2 emissions (kt)'])
eu_pop = (countries_of_interest.loc['1992':'2023':6]['European Union']
          ['CO2 emissions (kt)'])
bar_df = {'Canada': canada_pop, 'India': india_pop, 'China': china_pop,
          'USA': us_pop, 'EU': eu_pop}

fig, ax = plt.subplots(layout='constrained')

x = np.arange(len(np.arange(1992, 2023, 6)))  # the label locations
width = 0.15  # the width of the bars
multiplier = 0

for attribute, measurement in bar_df.items():
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1
ax.set_ylabel('CO2')
ax.set_xlabel('Years')
# ax.set_yscale('log')
ax.set_title('CO2 emissions (kt)')
ax.set_xticks(x + width, np.arange(1992, 2023, 6))
ax.legend(loc='upper left', ncols=3)
plt.savefig('CO2_bar.png')
plt.show()

# Correlation heatmap for China
china_df = (countries_of_interest.loc['1992':'2022']['China']
            [['Urban population (% of total population)', 'Population, total',
              'Arable land (% of land area)', 'Forest area (% of land area)',
              'CO2 emissions (kt)',
              'Electric power consumption (kWh per capita)']])
print(china_df.corr())

# Call the heatmap function
map_corr(china_df, 7, 'cividis', 'China')

# Correlation heatmap for EU
eu_df = (countries_of_interest.loc['1992':'2022']['European Union']
         [indicators_of_interest])

# Create a correlation
print(eu_df.corr())

# Call the mapping function
map_corr(eu_df, 7, 'bone_r', 'European Union')

# Correlation heat map for United States
us_df = (countries_of_interest.loc['1992':'2023']['United States']
         [indicators_of_interest])
print(us_df.corr())
# Call the mapper
map_corr(us_df, 7, 'coolwarm', 'USA')

# Table for Electric power consumption
ec_df = (countries_of_interest.xs(
    'Electric power consumption (kWh per capita)', level='Indicator Name',
    axis=1, drop_level=False).loc['1992':'2022':6])
ec_df.rename(columns={'Electric power consumption (kWh per capita)': 'EPC'},
             inplace=True)
ec_df = ec_df.round(2)
# Create a figure and axis
fig, ax = plt.subplots(figsize=(20, 6), dpi=200)
fig

# Hide the axes
ax.axis('off')

# Plot the table
table = (ax.table(cellText=ec_df.values, rowLabels=ec_df.index,
                  colLabels=ec_df.columns, cellLoc='center', loc='center',
                  colWidths=[0.07 for x in ec_df.columns], bbox=[0, 0, 1, 1]))
table.auto_set_font_size(False)
table.set_fontsize(12)
# Save the table as an image
plt.savefig('urban_population_table.png', bbox_inches='tight')

# Show the plot (optional)
plt.show()

# Arable land % plot
arable_df = (countries_of_interest.xs('Arable land (% of land area)',
                                      level='Indicator Name', axis=1,
                                      drop_level=False).loc['1992':'2022'])
print(f'Arable land: \n {arable_df}')
arable_df.plot()
plt.legend(labels=['Canada', 'India', 'China', 'USA', 'EU'])
plt.ylim(0, 80)
plt.xlabel('Years')
plt.ylabel('Land (%)')
plt.tight_layout()
plt.savefig('arable.png')

# Forest area % plot
forest_df = (countries_of_interest.xs('Forest area (% of land area)',
                                      level='Indicator Name', axis=1,
                                      drop_level=False).loc['1992':'2022'])
print(f'Forest land: \n {forest_df}')
forest_df.plot(style='--')
plt.legend(labels=['Canada', 'India', 'China', 'USA', 'EU'])
plt.ylim(0, 80)
plt.xlabel('Years')
plt.ylabel('Land (%)')
plt.tight_layout()
plt.savefig('forest_area.png')
