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

MergeDF = MergeDF.dropna()

MergeDF["Total Renewable Energy - TWh"] = (
    MergeDF["Electricity from wind - TWh"] +
    MergeDF["Electricity from hydro - TWh"] +
    MergeDF["Electricity from solar - TWh"] + 
    MergeDF["Other renewables including bioenergy - TWh"]
)

NonCountries = [
   "World", "High-income countries", "Upper-middle-income countries",
    "Lower-middle-income countries", "Low-income countries", "Asia", 
    "Europe", "North America", "South America", "Africa", "Oceania", "European Union (27)" 
]

MergeDF = MergeDF[~MergeDF["Entity"].isin(NonCountries)]

# Finding Top Renewable countries
TopCountries = MergeDF.groupby("Entity")["Total Renewable Energy - TWh"].sum()
TopCountries = TopCountries.sort_values(ascending=False).head(4).index

TopCountriesDS = MergeDF[MergeDF["Entity"].isin(TopCountries)]

fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharey=False)
axes = axes.flatten()

for i, Country in enumerate(TopCountries):
    CountryData = TopCountriesDS[TopCountriesDS["Entity"] == Country]

    axes[i].plot(CountryData["Year"], CountryData["Total Renewable Energy - TWh"], label="Total Renewable Energy in Terrawatt Hours (TWh)", color="blue")

    ax2 = axes[i].twinx()
    ax2.plot(CountryData["Year"], CountryData["Annual CO₂ emissions"], label="CO₂ Emissions", color="red")
    ax2.autoscale(enable=True, axis="y")

    axes[i].set_title(f"{Country}")
    axes[i].set_xlabel("Year")
    axes[i].set_ylabel("Total Renewable Energy (TWh)", color="blue")
    ax2.set_ylabel("CO₂ Emissions (tons)", color="red")

    axes[i].legend(loc="upper left", fontsize="small")
    ax2.legend(loc="upper right", fontsize="small")

for j in range(len(TopCountries), len(axes)):
    fig.delaxes(axes[j])

plt.tight_layout()
plt.show()

