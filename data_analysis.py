import pandas as pd

# Load the data
businesses = pd.read_csv("data/businesses.csv")
new_businesses = pd.read_csv("data/new_businesses.csv")
countries = pd.read_csv("data/countries.csv")
categories = pd.read_csv("data/categories.csv")

# oldest_business_continent
businesses_countries = businesses.merge(countries, on='country_code')
oldest_year_continent = businesses_countries.groupby('continent').min('year_founded')
oldest_business_continent = businesses_countries.merge(oldest_year_continent, on=['continent', 'year_founded'])[['business', 'year_founded', 'country', 'continent']].sort_values('year_founded')
oldest_business_continent = oldest_business_continent.set_index('business')
oldest_business_continent.to_csv('oldest_business_continent.csv')

# count_missing
businesses_all = pd.concat([businesses, new_businesses])
businesses_all_countries = businesses_all.merge(countries, on='country_code', how='outer')
filtered = businesses_all_countries[businesses_all_countries['business'].isnull()]
count_missing = filtered.groupby('continent')['country'].count().reset_index(name='countries_without_businesses')
count_missing = count_missing.set_index('continent')
count_missing.to_csv('count_missing.csv')

# oldest_by_continent_category
businesses_categories = businesses.merge(categories, on='category_code', how='inner')
business_categories_countries = businesses_categories.merge(countries, on='country_code', how='inner')
oldest_by_continent_category = business_categories_countries.groupby(['continent', 'category']).min('year_founded')
oldest_by_continent_category.to_csv('oldest_by_continent_category.csv')
