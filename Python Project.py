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

## Check the unique values on the complete dataset
print(cleaned_covid_data.nunique())
##again from this I can confirm 149 countries/iso codes and  also 26 vaccine brand combinations

## To see how many unique  vaccine brand combinatons, although I can see this from the above
## To find out how many unique brand combinations offered I can see 26 from the below
print(len(cleaned_covid_data.vaccines.unique()))

## Different countries are using different brands and some are using a combination in the fight against Covid-19.
print(cleaned_covid_data['vaccines'].value_counts())
## At a quick glance it looks like Moderna, Oxford/ AstraZeneca, Pfizer/ BioNTech combinaton is used the most.
##i.e. it appears 2005 times in the Dataset - there are 2005 rows that have this combination.

##See where 'Moderna, Oxford/ AstraZeneca, Pfizer/ BioNTech brand combination features in the dataset
df_blended_top_3_brands=cleaned_covid_data[cleaned_covid_data['vaccines']=='Moderna, Oxford/AstraZeneca, Pfizer/BioNTech']
print(df_blended_top_3_brands.shape)
##This indicates that there is 2005 rows and 14 cols that contain Vaccines - Moderna, Oxford/AstraZeneca, Pfizer/BioNTech'

print(df_blended_top_3_brands['vaccines'].unique())

df_blended_top_3_brands=df_blended_top_3_brands.sort_values(by='total_vaccinations', ascending=False)
print(df_blended_top_3_brands.head(10))

print(df_blended_top_3_brands.groupby('country').agg(['max','min','mean']))

## Moderna, Oxford/AstraZeneca, Pfizer/BioNTech country daily vaccinations using this brand
plt.figure(figsize=(20,14))
sns.barplot(df_blended_top_3_brands['daily_vaccinations'],df_blended_top_3_brands['country'])
plt.title('Country VS daily_vaccinations - for those using Moderna, Oxford/AstraZeneca, Pfizer/BioNTech', fontsize=20)
plt.xlabel('daily_vaccinations', fontsize=20)
plt.ylabel('Country', fontsize=20)
plt.show()

## Now I am going to create a dictionary to see what countries are using what vaccine brand
# Create a dictionary of each vaccine combination and its country of usage.

dict = {}
for v in cleaned_covid_data["vaccines"].unique():
    dict[v] = [cleaned_covid_data["country"][c] for c in cleaned_covid_data[cleaned_covid_data["vaccines"] == v].index]

# If I display this directly, I will get repeated values within the key, as the country names appear multiple times.
# Therefore need to remove repeated values in each key.

output = {}
for key, value in dict.items():
    output[key] = set(value)
output

# Find the number of values for each key in the dictionary.
# This allows me to count the number of countries using each vaccine combination.
for key, value in output.items():
    result = print(key, len([item for item in value if item]))
print(result)
## From the below we can see 38 countries are using Oxford / AstraZeneca,
## 24 countries Moderna, Oxford/AstraZeneca, Pfizer/BioNTech
## 21 countries are using Pfizer/BioNTech,
## 9 countries are using Sputnik v

## Which country is using what vaccine, create new column that will print the string  'is using the following Covid19 vaccine:'
country_usage= cleaned_covid_data['country_vacc_brand']=cleaned_covid_data['country'] + ', is using the following Covid19 vaccine: ' +  cleaned_covid_data['vaccines']
for C in cleaned_covid_data['country_vacc_brand'].unique():
    print(C)

## To check that I did create a new column
print(cleaned_covid_data.shape)
## 14 cols - which is what I expected 