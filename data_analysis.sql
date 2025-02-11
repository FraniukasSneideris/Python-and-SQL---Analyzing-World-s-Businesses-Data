-- oldest_business_continent
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


-- count_missing
SELECT co.continent, 
       COUNT(co.country) AS countries_without_businesses
FROM countries AS co
LEFT JOIN (SELECT * FROM businesses
           UNION
           SELECT * FROM new_businesses) AS b
USING (country_code)
WHERE b.business IS NULL
GROUP BY co.continent;


-- oldest_by_continent_category
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
