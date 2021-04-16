import inline as inline
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px



# Import my dataset
covid_vac_prog = pd.read_csv("/Users/deborahbarrett/Downloads/country_vaccinations-4.csv")

# To check the length of the dataset
print(len(covid_vac_prog))

# To check the first 5 rows
# Once run I can see Afghanistan is the first country mentioned in the dataset
print(covid_vac_prog.head())

# To check the last 5 rows
# I can see that Zimbabwe
print(covid_vac_prog.tail())

# Find how many rows and columns
print(covid_vac_prog.shape)

# loc refers to the label index
# .iloc refers to the positional index
# Check cols date, country and daily_vaccinations and check positional index 1 and the last index -1
index_check = covid_vac_prog[["date", "country", "daily_vaccinations"]]
print(index_check.iloc[[1, -1]])

# To check the first row, i.e. index 0.
print(index_check.iloc[[0]])

# Get first two elements, as seen below index 0 and 1.
print(covid_vac_prog[0:2])

# Check positional index 0 and last row
print(index_check.iloc[[0, -1]])

# Get an overview of some basic descriptive stats for all numeric columns
print(covid_vac_prog.describe())

# Get to know the names of the columns to see if all are needed
print(covid_vac_prog.columns)

# Certain cols are not needed and can be dropped - I decided that I would not need source name and source website
print(covid_vac_prog.drop(['source_name','source_website'], inplace=True, axis=1))

# Check how many rows and columns are in the dataset now that I removed the two cols earlier
# To make sure all is as it should be with certain rows removed as requested above
print(covid_vac_prog.shape)

# To check that these have now been successfully removed I am going to check my cols again
print(covid_vac_prog.columns)

# check the level of the dataset that is the primary key
print(len(covid_vac_prog.country.unique()))
# Hence each row represents unique country

# To check the data type of each column
print(covid_vac_prog.dtypes)

# To list of all the columns in the dataset and the type of data each column contains
print(covid_vac_prog.info())

# All cols appear to have the correct dataset except for the date col - I saw this earlier
# The dates are not represented by the correct data type
# I am going to use the .to_datetime() to parse the the column as Datetime
covid_vac_prog['date']=pd.to_datetime(covid_vac_prog['date'])
## Now I am going to check the new type of the date column I have changed
print(covid_vac_prog['date'].dtype)

# Double checking that all datatypes are now correct
print(covid_vac_prog.dtypes)

# To check how many missing values I have
missing_values_count = covid_vac_prog.isnull().sum()
print(missing_values_count)

# Plot missing values
covid_vac_prog.isna().sum().plot(kind="bar")
sns.set_style("darkgrid") ##There are five preset seaborn themes: darkgrid, whitegrid, dark, white, and ticks
sns.set_context("paper")
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()

# high number of missing values, if these were dropped a lot of data would be lost
# fill the missing values with 0 except for ISO_CODE as replacing this with 0 would not be correct.
# use apply for columns with checking dtype whether it is numeric or not by checking the dtype.kind
# 'biufc' represents - boolean, integer, unicode, float& complex data type
# The below fills 0 for the biufc type values and fills unknown other wise.
cleaned_covid_data = covid_vac_prog.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc'else x.fillna('unknown'))
##Now to check if there is any missing values and that the "cleaned data" was done correctly
print(cleaned_covid_data.isnull().sum())
# This now shows there is no missing values

# As a checking point (sanity check) I am going to check my rows and columns again to ensure these are all intact as they should be
print(cleaned_covid_data.shape)
# All looks as it should be 8191 rows and 13 columns as I dropped the two cols website and source earlier

# to see how many times a Country appears in the dataset
# appear the exact same number of times as that of the United Kingdom. As these are part of the UK I could delete these rows.
print(covid_vac_prog['country'].value_counts())
# interestingly I can see England, Northern Ireland, Scotland, Wales
# Add .head(10) after to display only top 10 if I want.

# Remove Scotland, England, Northern Ireland, Wales as these are all included under the United Kingdom.
# Check shape then again to ensure everything is as it should be.
cleaned_covid_data = cleaned_covid_data[cleaned_covid_data.country.apply(lambda x: x not in ['England', 'Scotland', 'Wales', 'Northern Ireland'])]
print(cleaned_covid_data.shape)

#Check how many countries now remain as England, Scotland, Wales and NI have been removed.
print(len(cleaned_covid_data.country.unique()))
#This resulted in 149 countries - which is correct (153 were listed earlier now I have removed 4 therefore 149 is correct)

# Check the unique values on the complete dataset
print(cleaned_covid_data.nunique())
# again from this I can confirm 149 countries/iso codes and  also 26 vaccine brand combinations

# To see how many unique vaccine brand combinations, although I can see this from the above
# To find out how many unique brand combinations offered I can see 26 from the below
print(len(cleaned_covid_data.vaccines.unique()))

# Different countries are using different brands and some are using a combination in the fight against Covid-19.
print(cleaned_covid_data['vaccines'].value_counts())
# At a quick glance it looks like Moderna, Oxford/ AstraZeneca, Pfizer/ BioNTech combinaton is used the most.
# i.e. it appears 2005 times in the Dataset - there are 2005 rows that have this combination.

# See where 'Moderna, Oxford/ AstraZeneca, Pfizer/ BioNTech brand combination features in the dataset
df_blended_top_3_brands=cleaned_covid_data[cleaned_covid_data['vaccines']=='Moderna, Oxford/AstraZeneca, Pfizer/BioNTech']
print(df_blended_top_3_brands.shape)
# This indicates that there is 2005 rows and 14 cols that contain Vaccines - Moderna, Oxford/AstraZeneca, Pfizer/BioNTech'

print(df_blended_top_3_brands['vaccines'].unique())

df_blended_top_3_brands=df_blended_top_3_brands.sort_values(by='total_vaccinations', ascending=False)
print(df_blended_top_3_brands.head(10))

print(df_blended_top_3_brands.groupby('country').agg(['max','min','mean']))

# Moderna, Oxford/AstraZeneca, Pfizer/BioNTech country daily vaccinations using this brand
plt.figure(figsize=(20,14))
sns.barplot(df_blended_top_3_brands['daily_vaccinations'],df_blended_top_3_brands['country'])
plt.title('Country VS daily_vaccinations - for those using Moderna, Oxford/AstraZeneca, Pfizer/BioNTech', fontsize=20)
plt.xlabel('daily_vaccinations', fontsize=20)
plt.ylabel('Country', fontsize=20)
plt.show()

# Now I am going to create a dictionary to see what countries are using what vaccine brand
# Create a dictionary of each vaccine combination and its country of usage.

dict = {}
for v in cleaned_covid_data["vaccines"].unique():
    dict[v] = [cleaned_covid_data["country"][c] for c in cleaned_covid_data[cleaned_covid_data["vaccines"] == v].index]

# If I display this directly, I will get repeated values within the key, as the country names appear multiple times.
# Therefore need to remove repeated values in each key.

output = {}
for key, value in dict.items():
    output[key] = set(value)
print(output)

# Find the number of values for each key in the dictionary.
# This allows me to count the number of countries using each vaccine combination.
for key, value in output.items():
    result = print(key, len([item for item in value if item]))

# From the below we can see 38 countries are using Oxford / AstraZeneca,
# 24 countries Moderna, Oxford/AstraZeneca, Pfizer/BioNTech
# 21 countries are using Pfizer/BioNTech,
# 9 countries are using Sputnik v

# Which country is using what vaccine, create new column that will print the string  'is using the following Covid19 vaccine:'
country_usage= cleaned_covid_data['country_vacc_brand']=cleaned_covid_data['country'] + ', is using the following Covid19 vaccine: ' +  cleaned_covid_data['vaccines']
for C in cleaned_covid_data['country_vacc_brand'].unique():
    print(C)

# To check that I did create a new column
print(cleaned_covid_data.shape)
# 14 cols - which is what I expected

# When I wanted to get an overview of some statistical information within the dataset,
# I got some '+e' within the dataset earlier
# Used the options.display.float format to make data easier to read when using the pandas describe ()
pd.options.display.float_format = "{:.2f}".format
print(cleaned_covid_data.describe())

# Find the maximum number of total vaccinations for each country and display them in descending order.
# Total Vaccinations refers to the absolute number of total immunizations in the country.
total_country_vacc = cleaned_covid_data.groupby(['country'])['total_vaccinations'].max().reset_index()
total_sorted = total_country_vacc.sort_values('total_vaccinations', ascending = False, ignore_index = True)
print(total_sorted.style.background_gradient(cmap = 'Oranges'))
# US has administered 133.3 million doses of COVID-19
# China has administered 91.3 million
# Compared to the Bahamas which  has administered 110 doses of COVID vaccines so far.

# Visualise the top ten countries with the most number of vaccines administered.
fig, ax = plt.subplots(figsize=(18, 10))
total_vacc = sns.barplot(ax=ax, data=total_sorted.iloc[:10],x="country",y="total_vaccinations")
ax.set_xlabel('Country', fontsize=20)
ax.set_ylabel('Total Vaccinations - absolute number of immunizations', fontsize=20)
ax.set_title('Top 10 countries by total vaccinations', fontsize=20)
for amount in total_vacc.patches:
    total_vacc.annotate('{:.2f}'.format(amount.get_height()), (amount.get_x(), amount.get_height()+1))
plt.show()

# Visualise top 30 countires in terms of total vaccinations
top = 30
vaccinations_data = cleaned_covid_data.groupby('country')['total_vaccinations'].max()
vaccinations_data = pd.DataFrame(vaccinations_data)
vaccinations_data = vaccinations_data.sort_values(ascending=False, by='total_vaccinations').iloc[:top]
fig = px.bar(x=vaccinations_data.index, y=vaccinations_data['total_vaccinations'],
             color=vaccinations_data.index,
             title=f'Top {top} Countries - Total Vaccinations',
             labels={"x": "Country", "y": "Number of Vaccinations"},
            color_discrete_sequence =px.colors.sequential.Electric)
fig.show()

# World COVID Vaccine Progress by Time
# Vaccines were first administered in early Dec 2020.
# Check to see how the world has made the progress in total vaccination numbers, people fully vaccinated over the past few months.
# Group by date and take the sum of each feature for all countries.
# Plot to see how 'total vaccinations' and 'people fully vaccinated' have progressed over a period of time.
# groupby date and get the sum
covid_vacc_by_date = cleaned_covid_data.groupby('date').sum()
fig = px.bar(covid_vacc_by_date, x = covid_vacc_by_date.index, y ='total_vaccinations', hover_data=['total_vaccinations'],color='total_vaccinations',height=600, title='Total Vaccinations from 13th December to 25th March ')
fig.show()

# Total number of people vaccinated - a person, depending on the immunization scheme, will receive one or more (typically 2) vaccines;
# At a certain moment, the number of vaccination might be larger than the number of people;
people_vaccinated = cleaned_covid_data.groupby(['country'])['people_vaccinated'].max().reset_index()
people_vaccinated_sorted = people_vaccinated.sort_values(by='people_vaccinated', ascending = False, ignore_index = True).style.background_gradient(cmap = 'Blues')
print(people_vaccinated_sorted)

# Look at the  total number of vaccination doses administered per 100 people in the total population
# In order to assess how successful the vaccine has been rolled out either partially or completely.
# Which country is leading in fully vaccinating the maximum percentage of its total population?
# This differs from our earlier results of the country where highest number of people are fully vaccinated.
# This calculation takes the population into consideration while calculating it.

people_per_100 = cleaned_covid_data.groupby(['country'])['people_vaccinated_per_hundred'].max().reset_index()
sorted_people_per_100 = people_per_100.sort_values(by='people_vaccinated_per_hundred', ascending = False, ignore_index = True)
sorted_people_per_100.style.background_gradient(cmap = 'RdYlGn_r')
# From this we can see that Gibraltar, Seychelles and Israel have the highest number of vaccinations does administered per 100
# Biggest number in red, smaller number decreasing in colour to the smallest numbers in green.
# US overall has the highest number of vaccinations administered,
# However Gibraltar has the overall highest percentage of vaccinations administered per 100 people.
# I will need to get the populations sizes of these countries
# From the visualization it is evident that Gibraltar, Seychelles and Israel are leading the way globally in terms of the number of doses per head of population,
# Gibraltar has more than 91 doses given for every 100 people
# The population of these countries isn't really high, that may be reason for this indicators.

# People_fully_vaccinated_per_hundred
people_fully = cleaned_covid_data.groupby(['country'])['people_fully_vaccinated_per_hundred'].max().reset_index()
people_fully_vac = people_fully.sort_values(by='people_fully_vaccinated_per_hundred',ascending = False, ignore_index = True)
people_fully_vac.style.background_gradient(cmap = 'CMRmap_r')
# Gibraltar followed by Israel and Seychelles has the overall highest number of people fully vaccinated per hundred.
# While the US has the highest number of vaccinations(US has administerd 133.3 million doses of COVID-19)

# Plot the above i.e. top ten total number of vaccination doses administered per 100 people in the total population
sns.set_style('dark') # or darkgrid if I wanted lines
sns.set_context('talk')
fig, ax = plt.subplots(figsize=(16, 8))
sns.barplot(ax=ax, data=people_fully_vac.head(10), y="country", x = "people_fully_vaccinated_per_hundred")
plt.xlabel('Number of fully vaccinated people per hundred')
plt.ylabel('Countries')
plt.title(' Top 10 Countries - Number of People Fully Vaccinated per 100')
plt.show()

# Daily outlook - average number of vaccines administered
average = cleaned_covid_data.groupby(['country'])['daily_vaccinations'].mean().reset_index()
average_sorted = average.sort_values(by='daily_vaccinations', ascending = False, ignore_index = True)
average_sorted.style.background_gradient(cmap = 'Oranges')
# The US, China, India, the UK, and Brazil have the highest average daily vaccinations.

# Trend of the sum of daily vaccinations
trend = cleaned_covid_data.groupby("date", as_index=False)["daily_vaccinations"].sum()
print(trend)

# Plot trend of daily vaccinations over time
# Set the ticks to show every 7 days to avoid overlapping of dates.
# Autoformat the layout of the x-axis ticks.
# used for setting a tick for every integer multiple of a base within the view interval
import matplotlib.ticker as mticker
fig, ax = plt.subplots(figsize=(20, 7))
sns.lineplot(ax=ax, data=trend, x='date', y='daily_vaccinations', marker="8", linestyle= ":", color="blue")
myLocator = mticker.MultipleLocator(7)
ax.xaxis.set_major_locator(myLocator)
fig.autofmt_xdate()
plt.show()

# This could be because of the approval of several different vaccines
# and the increase in availability of these
# vaccines to countries over the first few months of 2021.
# the general trend of average daily vaccinations is in an upward direction.

# A way to work out what was the maximum daily vaccination for a particular country.
cleaned_covid_data.loc[cleaned_covid_data["country"] == 'China', "daily_vaccinations"].max()

# Plotting the daily average of vaccinations per country.
group_by_country =cleaned_covid_data.groupby("country")
group_by_country["daily_vaccinations"].mean().sort_values(ascending = False).head(25).plot.bar(figsize = (16 , 8), title = " Avg. daily vaccinations per country", color = 'purple')
plt.ylabel('Number of daily vaccinations (in millions)')
plt.show()

# The smallest daily vaccination rates
group_by_country["daily_vaccinations"].mean().sort_values(ascending = True).head(25).plot.bar(figsize = (16 , 8), title = " Avg. daily vaccinations per country")
plt.show()

# To see how daily vaccines are administered in certain countries
country_check = cleaned_covid_data[["date", "country", "daily_vaccinations"]]
print(country_check.head(10))

# China was looked at first country wise as this is where the virus
# As China had the first reported case of COVID-19,
# I wanted to see when they first started vaccinating.
country_china = country_check.loc[country_check['country'] == 'China']
print(country_china)

# We can now see that the first daily vaccination was reported on 16th December
# and last recorded date in the dataset is 25th March
print(country_china.iloc[[1, -1]])

#China min date within the dataset
cleaned_covid_data.loc[cleaned_covid_data["country"] == "China", "date"].min()
# This will report the first date that activity was reported for China
# However there is no daily vaccinations on that min day as shown below.
# But there is a value somewhere in the dataset that is related to this min date
# just not daily vaccinations

# Lets plot how the daly vaccination progress looks in China
# Set the ticks to show every 7 days to avoid overlapping of dates.
# Autoformat the layout of the x-axis ticks.
fig, ax = plt.subplots(figsize=(20, 7))
sns.lineplot(ax=ax, data=country_china, x='date', y='daily_vaccinations', marker="8", linestyle= ":", color="red")
myLocator = mticker.MultipleLocator(7)
ax.xaxis.set_major_locator(myLocator)
fig.autofmt_xdate()
fig.show()

# Check the minimum date within the dataset - this would be the first reported activity in the dataset.
print(cleaned_covid_data["date"].min())

# I wanted to see which country reported activity for this date
print(cleaned_covid_data[cleaned_covid_data["date"] == "2020-12-13"])
# From this it should United Kingdom was the first country to report daily vaccinations within this dataset

# Now I checked for the Uk
country_uk = country_check.loc[country_check['country'] == 'United Kingdom']
print(country_uk)

# From this we can see the UK reported its first daily vaccination figures on the 14th
# Yet they had  reported activity on the 13th within the dataset (total vaccinations & people vaccinated cols were populated with data
# This was shown above on the min date check
print(country_uk.iloc[[1, -1]])

# Set the ticks to show every 7 days to avoid overlapping of dates.
# Autoformat the layout of the x-axis ticks.
fig, ax = plt.subplots(figsize=(20, 7))
sns.lineplot(ax=ax, data=country_uk, x='date', y='daily_vaccinations', marker="8", linestyle= ":", color="darkgoldenrod")
myLocator = mticker.MultipleLocator(7)
ax.xaxis.set_major_locator(myLocator)
fig.autofmt_xdate()
plt.show()

# Plotting the daily vaccination rates in the UK show that the daily rates continued to grow levelled off in Feb
# Daily vac rates grew again mid March
# specifically around 11th March, so I wanted to check rates from this date onwards
country_uk_date_check = country_uk.loc[country_uk['date'] > '2021-03-11']
print(country_uk_date_check)

# Check the average daily vaccination for the UK / or change max to get the highest daily vaccination rate
print(cleaned_covid_data.loc[cleaned_covid_data["country"] == 'United Kingdom', "daily_vaccinations"].mean())

# Ireland - see how daily vacc rates are going
country_ireland = country_check.loc[country_check['country'] == "Ireland"]
print(country_ireland)

# First and last date verification of daily vaccinations
print(country_ireland.iloc[[1, -1]])

# Check average daily vaccination rate for Ireland
# or change max to get the highest daily vaccination rate
print(cleaned_covid_data.loc[cleaned_covid_data["country"] == 'Ireland', "daily_vaccinations"].mean())

# Plot how daily vaccs look to see any peaks and troughs
fig, ax = plt.subplots(figsize=(20, 7))
sns.lineplot(ax=ax, data=country_ireland, x='date', y='daily_vaccinations', marker="8", linestyle= ":", color="green")
myLocator = mticker.MultipleLocator(7)
ax.xaxis.set_major_locator(myLocator)
fig.autofmt_xdate()
plt.show()

# (Ireland) Date range greater than the 10th of March shows the drop in daily vaccinations recorded.
country_ireland_date_check = country_ireland.loc[country_ireland['date'] > '2021-03-10']
print(country_ireland_date_check)

# Daily vaccinations - did they go down over the AstraZeneca Scandal?
# Denmark, Norway, Latvia, The Netherlands have stopped completely - how does this look
fig, ax = plt.subplots(figsize=(10,8))
import matplotlib.dates as mdates
graph = sns.lineplot(data=cleaned_covid_data[cleaned_covid_data['iso_code'].isin(['DNK','NOR','NLD','LVA'])]
                     .sort_values(by="date"), x="date", y="daily_vaccinations",hue='country')
graph.xaxis.set_major_locator(mdates.DayLocator(interval = 7))
plt.xticks(rotation = 90)
plt.tight_layout()
plt.show()

# Check Norway to see if there was any decline in daily vaccinations
# This could be because of the AstraZeneca blood clotting issue
country_norway = country_check.loc[country_check['country'] == "Norway"]
country_norway_date_check = country_norway.loc[country_norway['date'] > '2021-03-10']
print(country_norway_date_check)

# Check type of data type
print(country_norway.dtypes)

# I want to check the percentage difference from the 11th March until the last date in the dataset
# Norway, Netherlands, Denmark and Lativa
# I will create a custom function so that I use this for a few countries
def pct_change(first,second):
    diff = second - first
    change =0
    try:
        if diff > 0:
            diff = first - second
            change = (diff/first)*100
        elif diff <0:
            diff = first - second
            change = -((diff / first)*100)
    except ZeroDivisonError:
        return float('int')
    return change

#Now check percentage change from 11th March to 24th - while calling the custom function.
pct_change(15327,12122)
#This shows there was a decrease of 20.9% from 11th March to 24th in Daily Vaccinations for Norway

#Denmark check
country_denmark = country_check.loc[country_check['country'] == "Denmark"]
print(country_denmark)

# Checking to see rates greater than the 10th March
# because this is when AstraZeneca issue began to arose
country_denmark_date_check = country_denmark.loc[country_denmark['date'] > '2021-03-10']
print(country_denmark_date_check)

# Check the %age change for Denmark in Daily Vaccinations rates from 11th March to 24th.
pct_change(17659,15360)

# Netherlands check
country_netherlands = country_check.loc[country_check['country'] == "Netherlands"]
print(country_netherlands)

# Netherlands date check in relation to AstraZeneca to see if any effect on daily rates
country_netherlands_date_check = country_netherlands.loc[country_netherlands['date'] > '2021-03-10']
print(country_netherlands_date_check)

# Latvia country check now
country_latvia = country_check.loc[country_check['country'] == "Latvia"]
print(country_latvia)

country_latvia_date_check = country_latvia.loc[country_latvia['date'] > '2021-03-10']
print(country_latvia_date_check)

# Latvia's daily rates begin to show a drop on 17th March.
pct_change(2107,1791)

# Latvia change from 11th until 19th -60% drop....
pct_change(2107,853)

# I needed to check population of certain countries - needed to get another dataset that has this info
# rather than a general Google search
data_pop = pd.read_csv("/Users/deborahbarrett/Downloads/worldometer_coronavirus_summary_data.csv")
print(data_pop.shape)

# Examine the names of the columns & to see if all are needed
print(data_pop.columns)

#Check data types of this additional dataset that has population
print(data_pop.info())

## Then merge with first dataset on the country cols as this is common to both datasets
data_with_pop_merged = pd.merge(cleaned_covid_data, data_pop, how='left', on='country')

# Check the first 5 rows of the merged dataset
print(data_with_pop_merged.head())

print(data_with_pop_merged.info())

# Check the missing values in the merged dataset
missing_values_merged = data_with_pop_merged.isnull().sum()
print(missing_values_merged)

# Replace the missing values with 0
cleaned_merged_data = data_with_pop_merged.apply(lambda x: x.fillna(0) if x.dtype.kind in 'biufc'else x.fillna('unknown'))
print(cleaned_merged_data.isnull().sum())

# To list of all the columns in the dataset and the type of data each column contains
print(cleaned_merged_data.info())

# Use country & population columns within the merged dataset
cleaned_merged_data = data_with_pop_merged[["country", "population"]]
print(cleaned_merged_data.head(10))
print(cleaned_merged_data.tail(10))

# Unique number of population
print(len(cleaned_merged_data.population.unique()))

# Check the population of Gibraltar
print(cleaned_merged_data[cleaned_merged_data["country"] == "Gibraltar"])

# Check the population of Seychelles
print(cleaned_merged_data[cleaned_merged_data["country"] == "Seychelles"])

# Check the population of Israel
print(cleaned_merged_data[cleaned_merged_data["country"] == "Israel"])


