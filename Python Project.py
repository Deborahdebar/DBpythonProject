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
print(covid_vac_prog.head())