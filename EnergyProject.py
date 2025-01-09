# Import Libraries
import pandas as pd
import matplotlib.pyplot as plt

# Import csv
RenewableEnergy = pd.read_csv('modern-renewable-prod.csv')
co2Emission = pd.read_csv('annual-co2-emissions-per-country.csv')


# Merge Dataframes
MergeDF = pd.merge(
    RenewableEnergy,
    co2Emission,
    on=["Entity", "Year"],
    how="inner"
)

EnergyDF = MergeDF.dropna()

print(EnergyDF.head())
