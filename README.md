# Python-and-SQL---Analyzing-World-s-Businesses-Data
Analyzing Data with 2 Different Programming Languages: SQL vs Python

## Project Overview
In this project, I aimed to explore and analyze a dataset containing information about the oldest businesses across the world. The dataset has been compiled by BusinessFinancing.co.uk and contains information from various countries, providing insights into businesses that have lasted for centuries. By analyzing the data in two different programming languages—SQL and Python—I compare how each approach handles data manipulation, aggregation, and analysis tasks.

### Business Context
One of the oldest businesses in the world is the Staffelter Hof Winery, established in 862 under the Carolingian dynasty. This winery has survived through dramatic historical changes, including the rise and fall of empires, and continues to serve customers today. What makes a business endure such turbulent times? This question is central to my analysis, and through this project, I aim to uncover patterns and insights about longevity across business categories and continents.

### Data Sources
The project uses several CSV files that contain data on the world's oldest businesses, which have been cleaned and structured for analysis.

#### Files:
- `data/businesses.csv` — Contains information on businesses, including their name, founding year, and category code.
- `data/new_businesses.csv` — Contains data on new businesses.
- `data/countries.csv` — Provides country details, including the ISO country code and continent.
- `data/categories.csv` — Provides a description for each business category based on the category code.

#### Columns:

**businesses.csv**:
| Column        | Description                                      |
|---------------|--------------------------------------------------|
| business      | Name of the business                             |
| year_founded  | Year the business was founded                    |
| category_code | Code for the business category                   |
| country_code  | ISO 3166-1 three-letter country code             |

**countries.csv**:
| Column       | Description                                      |
|--------------|--------------------------------------------------|
| country_code | ISO 3166-1 three-letter country code             |
| country      | Name of the country                              |
| continent    | Continent where the country is located           |

**categories.csv**:
| Column       | Description                                      |
|--------------|--------------------------------------------------|
| category_code| Code for the business category                   |
| category     | Description of the business category             |

## Analysis Questions
The dataset provides the foundation for answering the following questions:

1. **What is the oldest business on each continent?**
   I identify the oldest business for each continent, displaying its country, name, and founding year. The resulting DataFrame, `oldest_business_continent`, will contain columns: `continent`, `country`, `business`, and `year_founded`.

2. **How many countries per continent lack data on the oldest businesses?**
   I will count the number of countries per continent that lack business data, both with and without the inclusion of `new_businesses`. This will help determine whether including new businesses changes the landscape of missing data. The results will be stored in a DataFrame named `count_missing` with columns `continent` and `countries_without_businesses`.

3. **Which business categories are best suited to last many years, and on what continent are they?**
   I will create a DataFrame named `oldest_by_continent_category` that stores the oldest founding year for each continent and business category combination. This will contain columns: `continent`, `category`, and `year_founded`.

## Data Analysis
### 1) Finding the oldest business on each continent
#### SQL analysis
I used a combination of `JOIN` and `GROUP BY` statements to find the oldest business on each continent. The query is efficient, concise, and leverages SQL's ability to aggregate data in a straightforward manner with the `MIN()` function. The subquery within the `WHERE` clause ensures that only the oldest business for each continent is selected. This approach is quick to write and execute, especially when working with relational databases.
```sql
SELECT b.business, 
       b.year_founded,
	   co.country,
	   co.continent
FROM businesses AS b
LEFT JOIN countries AS co
ON b.country_code = co.country_code
WHERE year_founded IN (SELECT MIN(b.year_founded)
                       FROM businesses AS b
                       LEFT JOIN countries AS co
                       ON b.country_code = co.country_code
                       GROUP BY co.continent)
ORDER BY year_founded;
```
#### Python analysis
I used merge() to combine the businesses and countries dataframes, followed by groupby() to find the minimum founding year for each continent. After merging the results with the original dataframe, I extracted the necessary columns and sorted them by the founding year. Although Python allows more flexibility in data manipulation, the code is longer and requires multiple steps, which can make it harder to debug for complex operations.
```python
businesses_countries = businesses.merge(countries, on='country_code')
oldest_year_continent = businesses_countries.groupby('continent').min('year_founded')
oldest_business_continent = businesses_countries.merge(oldest_year_continent, on=['continent', 'year_founded'])[['business', 'year_founded', 'country', 'continent']].sort_values('year_founded')
oldest_business_continent = oldest_business_continent.set_index('business')
oldest_business_continent.to_csv('oldest_business_continent.csv')
```
### 2) Finding how many countries per continent lack data on the oldest businesses
#### SQL analysis
SQL handles the task of counting countries missing business data efficiently with a LEFT JOIN and a WHERE clause to filter out countries that have no corresponding business data. The query is simple and returns the count of countries without businesses per continent in a single operation.
```sql
SELECT co.continent, 
       COUNT(co.country) AS countries_without_businesses
FROM countries AS co
LEFT JOIN (SELECT * FROM businesses
           UNION
           SELECT * FROM new_businesses) AS b
USING (country_code)
WHERE b.business IS NULL
GROUP BY co.continent;
```
#### Python analysis
I used pd.concat() to combine both the businesses and new_businesses dataframes, followed by a merge() with the countries dataframe. After filtering out rows where the business column is null, I used groupby() and count() to get the results. While this approach gives more control over how data is merged and filtered, it is more verbose and less intuitive for simple tasks like counting missing data.
```python
businesses_all = pd.concat([businesses, new_businesses])
businesses_all_countries = businesses_all.merge(countries, on='country_code', how='outer')
filtered = businesses_all_countries[businesses_all_countries['business'].isnull()]
count_missing = filtered.groupby('continent')['country'].count().reset_index(name='countries_without_businesses')
count_missing = count_missing.set_index('continent')
count_missing.to_csv('count_missing.csv')
```
### 3) Finding which business categories are best suited to last many years, and on what continent are they
#### SQL analysis
The SQL query used INNER JOIN to merge the businesses, categories, and countries tables, then grouped by continent and category to find the oldest founding year for each combination. The query is compact and powerful, providing the desired results in a single step.
```sql
SELECT co.continent, 
       ca.category, 
	   MIN(b.year_founded) AS year_founded
FROM businesses b
INNER JOIN categories AS ca 
ON b.category_code = ca.category_code
INNER JOIN countries AS co 
ON b.country_code = co.country_code
GROUP BY co.continent, ca.category
ORDER BY co.continent, ca.category;
```
#### Python analysis
I used merge() to combine the businesses, categories, and countries dataframes. Then, I used groupby() to calculate the oldest business year for each category and continent combination. Although Python provides more flexibility for additional analysis, this approach is less compact than the SQL version.
```python
businesses_categories = businesses.merge(categories, on='category_code', how='inner')
business_categories_countries = businesses_categories.merge(countries, on='country_code', how='inner')
oldest_by_continent_category = business_categories_countries.groupby(['continent', 'category']).min('year_founded')
oldest_by_continent_category.to_csv('oldest_by_continent_category.csv')
```
### Comparing methods
Overall, SQL is the clear winner in terms of conciseness and simplicity for tasks involving data aggregation and joining. It allows me to quickly extract meaningful insights with minimal code. Python, on the other hand, excels in data manipulation flexibility and visualization capabilities, which are extremely valuable when further analyzing and presenting data. While SQL is easier and more concise for the core analysis, Python's ability to handle complex data manipulations and produce advanced visualizations (which I'll show in the "Results" section).

## Results

### Oldest Businesses by Continent

| Business                         | Year Founded | Country     | Continent     |
|----------------------------------|--------------|-------------|---------------|
| Kongō Gumi                       | 578          | Japan       | Asia          |
| St. Peter Stifts Kulinarium      | 803          | Austria     | Europe        |
| La Casa de Moneda de México      | 1534         | Mexico      | North America |
| Casa Nacional de Moneda          | 1565         | Peru        | South America |
| Mauritius Post                   | 1772         | Mauritius   | Africa        |
| Australia Post                   | 1809         | Australia   | Oceania       |

### Countries Without Data on the Oldest Businesses

| Continent         | Countries Without Businesses |
|-------------------|------------------------------|
| Africa           | 3                            |
| Asia             | 7                            |
| Europe           | 2                            |
| North America    | 5                            |
| Oceania          | 10                           |
| South America    | 3                            |

### Best Business Categories for Longevity by Continent

| Continent     | Category                               | Year Founded |
|---------------|----------------------------------------|--------------|
| Africa        | Agriculture                            | 1947         |
|               | Aviation & Transport                   | 1854         |
|               | Banking & Finance                      | 1892         |
|               | Distillers, Vintners, & Breweries      | 1933         |
|               | Energy                                 | 1968         |
|               | Food & Beverages                       | 1878         |
|               | Manufacturing & Production             | 1820         |
|               | Media                                  | 1943         |
|               | Mining                                 | 1962         |
|               | Postal Service                         | 1772         |
| Asia          | Agriculture                            | 1930         |
|               | Aviation & Transport                   | 1858         |
|               | Banking & Finance                      | 1830         |
|               | Cafés, Restaurants & Bars              | 1153         |
|               | Conglomerate                           | 1841         |
|               | Construction                           | 578          |
|               | Defense                                | 1808         |
|               | Distillers, Vintners, & Breweries      | 1853         |
|               | Energy                                 | 1928         |
|               | Food & Beverages                       | 1820         |
|               | Manufacturing & Production             | 1736         |
|               | Media                                  | 1931         |
|               | Mining                                 | 1913         |
|               | Postal Service                         | 1800         |
|               | Retail                                 | 1883         |
|               | Telecommunications                     | 1885         |
|               | Tourism & Hotels                       | 1584         |
| Europe        | Agriculture                            | 1218         |
|               | Banking & Finance                      | 1606         |
|               | Cafés, Restaurants & Bars              | 803          |
|               | Consumer Goods                         | 1649         |
|               | Defense                                | 1878         |
|               | Distillers, Vintners, & Breweries      | 862          |
|               | Manufacturing & Production             | 864          |
|               | Media                                  | 1999         |
|               | Medical                                | 1422         |
|               | Mining                                 | 1248         |
|               | Postal Service                         | 1520         |
|               | Telecommunications                     | 1912         |
|               | Tourism & Hotels                       | 1230         |
| North America | Agriculture                            | 1638         |
|               | Aviation & Transport                   | 1870         |
|               | Banking & Finance                      | 1891         |
|               | Distillers, Vintners, & Breweries      | 1703         |
|               | Food & Beverages                       | 1920         |
|               | Manufacturing & Production             | 1534         |
|               | Media                                  | 1909         |
|               | Retail                                 | 1670         |
|               | Tourism & Hotels                       | 1770         |
| Oceania        | Banking & Finance                      | 1861         |
|               | Postal Service                         | 1809         |
| South America | Banking & Finance                      | 1565         |
|               | Cafés, Restaurants & Bars              | 1877         |
|               | Defense                                | 1811         |
|               | Food & Beverages                       | 1660         |
|               | Manufacturing & Production             | 1621         |

