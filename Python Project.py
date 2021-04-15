import inline as inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

## Import my dataset
covid_vac_prog = pd.read_csv("/Users/deborahbarrett/Downloads/country_vaccinations-4.csv")

## To check the length of the dataset
print(len(covid_vac_prog))

## To check the first 5 rows
## Once run I can see Afghanistan is the first country mentioned in the dataset
print(covid_vac_prog.head())

## To check the last 5 rows
## I can see that Zimbabwe
print(covid_vac_prog.tail())

## Find how many rows and columns
print(covid_vac_prog.shape)

## loc refers to the label index
## .iloc refers to the positional index
## Check cols date, country and daily_vaccinatons and check positional index 1 and the last index -1
index_check = covid_vac_prog[["date", "country", "daily_vaccinations"]]
print(index_check.iloc[[1, -1]])

#To check the first row, i.e. index 0.
print(index_check.iloc[[0]])

## get first two elements, as seen below index 0 and 1.
print(covid_vac_prog[0:2])

## Check positional index 0 and last row
print(index_check.iloc[[0, -1]])

## Get an overview of some summary stats
print(covid_vac_prog.describe())

## Get to know the names of the columns to see if all are needed
print(covid_vac_prog.columns)

## Certain cols are not needed and can be dropped - I decided that I would not need source name and source website
print(covid_vac_prog.drop(['source_name','source_website'], inplace=True, axis=1))

## Check how many rows and columns are in the dataset now that I removed the two cols earlier
## to make sure all is as it should be with certain rows removed as requested above
print(covid_vac_prog.shape)

## To check that these have now been successfully removed I am going to check my cols again
print(covid_vac_prog.columns)

## check the level of the dataset that is the primary key
print(len(covid_vac_prog.country.unique()))
## Hence each row represents unique country

## To check the data type of each column
print(covid_vac_prog.dtypes)

## To list of all the columns in the dataset and the type of data each column contains
print(covid_vac_prog.info())

## All cols appear to have the correct dataset except for the date col - I saw this earlier
## The dates are not represented by the correct data type
## I am going to use the .to_datetime() to parse the the column as Datetime
covid_vac_prog['date']=pd.to_datetime(covid_vac_prog['date'])
## Now I am going to check the new type of the date column I have changed
print(covid_vac_prog['date'].dtype)

## Double checking that all datatypes are now correct
print(covid_vac_prog.dtypes)

## To check how many missing values I have
missing_values_count = covid_vac_prog.isnull().sum()
print(missing_values_count)

## Plot missing values
covid_vac_prog.isna().sum().plot(kind="bar")
sns.set_style("darkgrid")
sns.set_context("paper")
plt.xticks(rotation = 90)
plt.show()

## high number of missing values, if these were dropped alot of data would be lost
## fill the missing values with 0 except for ISO_CODE as replacing this with 0 would not be correct.
## use apply for columns with checking dtype whether it is numeric or not by checking the dtype.kind
## 'biufc' represents - boolean, integar, unicode, float& complex data type
##The below fills 0 for the biufc type values and fills unknown other wise.
cleaned_covid_data = covid_vac_prog.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc'else x.fillna('unknown'))
##Now to check if there is any missing values and that the "cleaned data" was done correctly
print(cleaned_covid_data.isnull().sum())
## This now shows there is no missing values

## As a checking point (santity check) I am going to check my rows and columns again to ensure these are all intact as they should be
print(cleaned_covid_data.shape)
## All looks as it should be 8191 rows and 13 columns as I dropped the two cols website and source earlier

## to see how many times a Country appears in the dataset
##appear the exact same number of times as that of the United Kingdom. As these are part of the UK I could delete these rows.
print(covid_vac_prog['country'].value_counts())
##interestingly I can see England, Northern Ireland, Scotland, Wales
## add .head(10) after to display only top 10 if I want.

### Remove Scotland, England, Northern Ireland, Wales as these are all included under the United Kingdom.
## Check shape then again to ensure everything is as it should be.
cleaned_covid_data = cleaned_covid_data[cleaned_covid_data.country.apply(lambda x: x not in ['England', 'Scotland', 'Wales', 'Northern Ireland'])]
print(cleaned_covid_data.shape)

##Check how many countries now remain as England, Scotland, Wales and NI have been removed.
print(len(cleaned_covid_data.country.unique()))
##This resulted in 149 countries - which is correct (153 were listed earlier now I have removed 4 therefore 149 is correct)