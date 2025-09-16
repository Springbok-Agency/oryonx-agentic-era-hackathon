SELECT 
distinct * 
FROM `bigquery-public-data.google_trends.international_top_rising_terms` 
WHERE refresh_date = "2025-09-15" 
and country_name = "Netherlands"

