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


# Finding Top Renewable countries
NonCountries = [
   "World", "High-income countries", "Upper-middle-income countries",
    "Lower-middle-income countries", "Low-income countries", "Asia", 
    "Europe", "North America", "South America", "Africa", "Oceania", "European Union (27)" 
]

CountriesDS = MergeDF[~MergeDF["Entity"].isin(NonCountries)]


TopCountries = CountriesDS.groupby("Entity")["Total Renewable Energy - TWh"].sum()
TopCountries = TopCountries.sort_values(ascending=False).head(4).index

TopCountriesDS = CountriesDS[CountriesDS["Entity"].isin(TopCountries)]

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

fig.suptitle("Renewable Energy vs CO2 Emissions- Top 4 Renewable Energy Producing Countries", fontsize=16)
plt.tight_layout()
plt.show()




# Income Grouping based off of World Bank metrics
low_income_countries = [
    'Afghanistan', 'Burkina Faso', 'Burundi', 'Central African Republic',
    'Chad', 'Congo, Dem. Rep', 'Eritrea', 'Ethiopia', 'Gambia',
    'Guinea-Bissau', 'Liberia', 'Madagascar', 'Malawi', 'Mali', 'Mozambique',
    'Niger', 'Rwanda', 'Sierra Leone', 'Somalia', 'South Sudan', 'Sudan',
    'Togo', 'Uganda', 'Yemen'
]

lower_middle_income_countries = [
    'Angola', 'Bangladesh', 'Benin', 'Bhutan', 'Bolivia', 'Cabo Verde',
    'Cambodia', 'Cameroon', 'Comoros', 'Congo', "Cote d'Ivoire", 'Djibouti',
    'Egypt', 'Eswatini', 'Ghana', 'Guinea', 'Haiti', 'Honduras', 'India',
    'Jordan', 'Kenya', 'Kiribati', 'Kyrgyzstan', 'Laos', 'Lebanon', 'Lesotho',
    'Mauritania', 'Morocco', 'Myanmar', 'Nepal',
    'Nicaragua', 'Nigeria', 'Pakistan', 'Philippines', 'Senegal', 'Sri Lanka',
    'Sudan', 'Tajikistan', 'Tanzania', 'Tunisia', 'Ukraine', 'Uzbekistan',
    'Vietnam', 'Zambia', 'Zimbabwe'
]

upper_middle_income_countries = [
    'Albania', 'Algeria', 'Argentina', 'Armenia', 'Azerbaijan', 'Belarus',
    'Belize', 'Bosnia and Herzegovina', 'Botswana', 'Brazil', 'China',
    'Colombia', 'Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic',
    'Ecuador', 'Equatorial Guinea', 'Fiji', 'Georgia', 'Grenada', 'Indonesia',
    'Iran', 'Iraq', 'Jamaica', 'Kazakhstan', 'Kosovo', 'Libya', 'Malaysia',
    'Maldives', 'Mauritius', 'Mexico', 'Mongolia', 'Montenegro', 'Namibia',
    'North Macedonia', 'Paraguay', 'Peru', 'South Africa', 'St. Lucia',
    'Suriname', 'Thailand', 'Turkey', 'Turkmenistan', 'Venezuela'
]

high_income_countries = [
    'Australia', 'Austria', 'Bahamas', 'Bahrain', 'Barbados', 'Belgium',
    'Bermuda', 'Brunei', 'Canada', 'Croatia', 'Cyprus', 'Czechia', 'Denmark',
    'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hong Kong',
    'Hungary', 'Iceland', 'Ireland', 'Israel', 'Italy', 'Japan', 'Kuwait',
    'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'New Zealand',
    'Norway', 'Poland', 'Portugal', 'Qatar', 'Saudi Arabia', 'Singapore',
    'Slovakia', 'Slovenia', 'South Korea', 'Spain', 'Sweden', 'Switzerland',
    'Taiwan', 'United Arab Emirates', 'United Kingdom', 'United States'
]

# Add income group column to the dataset
income_group_mapping = {}

for country in low_income_countries:
    if country in MergeDF["Entity"].unique():
        income_group_mapping[country] = "Low-income countries"

for country in lower_middle_income_countries:
    if country in MergeDF["Entity"].unique():
        income_group_mapping[country] = "Lower-middle-income countries"

for country in upper_middle_income_countries:
    if country in MergeDF["Entity"].unique():
        income_group_mapping[country] = "Upper-middle-income countries"

for country in high_income_countries:
    if country in MergeDF["Entity"].unique():
        income_group_mapping[country] = "High-income countries"

MergeDF["Income Group"] = MergeDF["Entity"].map(income_group_mapping)

# Filter dataset for income groups
IncomeGroups = [
    "High-income countries",
    "Upper-middle-income countries",
    "Lower-middle-income countries",
    "Low-income countries"
]

# Find renewable energy vs co2 for income grouped countries
IncomeGroupsDS = MergeDF[MergeDF["Income Group"].isin(IncomeGroups)]
AggregatedData = IncomeGroupsDS.groupby(["Income Group", "Year"])[
    ["Total Renewable Energy - TWh", "Annual CO₂ emissions"]
].sum().reset_index()

fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharey=False)
axes = axes.flatten()

for i, IncomeGroup in enumerate(IncomeGroups):
    GroupData = AggregatedData[AggregatedData["Income Group"] == IncomeGroup]

    axes[i].plot(GroupData["Year"], GroupData["Total Renewable Energy - TWh"], label="Total Renewable Energy in Terrawatt Hours (TWh)", color="blue")

    ax2 = axes[i].twinx()
    ax2.plot(GroupData["Year"], GroupData["Annual CO₂ emissions"], label="CO₂ Emissions", color="red")
    ax2.autoscale(enable=True, axis="y")

    axes[i].set_title(f"{IncomeGroup}")
    axes[i].set_xlabel("Year")
    axes[i].set_ylabel("Total Renewable Energy (TWh)", color="blue")
    ax2.set_ylabel("CO₂ Emissions (tons)", color="red")

    axes[i].legend(loc="upper left", fontsize="small")
    ax2.legend(loc="upper right", fontsize="small")

for j in range(len(IncomeGroups), len(axes)):
    fig.delaxes(axes[j])

fig.suptitle("Renewable Energy vs CO2 Emissions by Income Group", fontsize=16)
plt.tight_layout()
plt.show()




# Pie Chart to show renewable energy sources in 2000, 2010, 2020

# Filter data for the years 2000, 2010, and 2020
selected_years = [2000, 2010, 2020]
filtered_data = MergeDF[MergeDF["Year"].isin(selected_years)]

# Group by year and aggregate the total renewable energy by source
aggregated_data = filtered_data.groupby("Year")[[
    "Electricity from wind - TWh", 
    "Electricity from hydro - TWh", 
    "Electricity from solar - TWh", 
    "Other renewables including bioenergy - TWh"
]].sum()

categories = [
    "Electricity from hydro - TWh", 
    "Electricity from wind - TWh", 
    "Electricity from solar - TWh", 
    "Other renewables including bioenergy - TWh"
]
colors = ['orange', 'blue', 'green', 'red']


# Plot pie charts
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

for i, year in enumerate(selected_years):
    year_data = aggregated_data.loc[year]
    axes[i].pie(
        year_data, 
        labels=None, 
        autopct='%1.1f%%', 
        startangle=140,
        colors=colors
    )
    axes[i].set_title(f"Proportion of Renewable Energy Types in {year}")

fig.legend(
    labels=categories, 
    loc='upper center', 
    bbox_to_anchor=(0.5, 0.05),  # Adjust position of the legend
    ncol=4,  # Arrange the categories in a single row
    fontsize='medium'
)

fig.suptitle("Global Renewable Energy Composition (2000, 2010, 2020) in Terrawatt hours (TWh)", fontsize=16)
plt.tight_layout(rect=[0, 0.15, 1, 0.9])
plt.show()