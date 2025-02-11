import matplotlib.pyplot as plt
import seaborn as sns

## Line Plot - Evolution of Founding Years by Category
sns.relplot(x='year_founded', y='category', data=oldest_by_continent_category, hue='continent', style='continent', kind='line', markers=True, aspect=3)
plt.xlabel('Year of Foundation')
plt.ylabel('Business Category')
plt.show()

## Pie Chart - Proportional Business Representation by Continent
plt.figure(figsize=(4, 4))
business_counts = oldest_by_continent_category.groupby('continent').size()
business_counts.plot(kind='pie', autopct='%1.1f%%', startangle=140, colors=sns.color_palette('Set2'))
plt.ylabel('') 
plt.show()

## Heatmap - Category vs. Continent with Business Age
heatmap_data = oldest_by_continent_category.pivot_table(index='category', columns='continent', values='year_founded', aggfunc='min')
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='Greens', fmt='.0f')
plt.title('Business Foundation Date by Category and Continent')
plt.xlabel('Category')
plt.ylabel('Continent')
plt.show()

## Heatmap - Business Longevity by Category and Continent
# Calculate the difference between the founding year and 2024
oldest_by_continent_category['business_age'] = 2024 - oldest_by_continent_category['year_founded']
# Pivot the table to get a matrix for heatmap
heatmap_data = oldest_by_continent_category.pivot_table(index='category', columns='continent', values='business_age', aggfunc='mean')
# Create the heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, cmap='magma_r', fmt='.1f', linewidths=0.5)
plt.title('Business Longevity by Category and Continent')
plt.xlabel('Continent')
plt.ylabel('Business Category')
plt.show()
