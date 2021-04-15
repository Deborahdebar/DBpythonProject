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