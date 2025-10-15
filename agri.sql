-- 1️⃣ Create database
CREATE DATABASE IF NOT EXISTS securecheck
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE securecheck;

-- 2️⃣ Create agri_data table
CREATE TABLE agri_data (
  dist_code VARCHAR(50),
  year INT,
  state_code VARCHAR(50),
  state_name VARCHAR(100),
  dist_name VARCHAR(100),
  rice_area_1000_ha FLOAT,
  rice_production_1000_tons FLOAT,
  rice_yield_kg_per_ha FLOAT,
  wheat_area_1000_ha FLOAT,
  wheat_production_1000_tons FLOAT,
  wheat_yield_kg_per_ha FLOAT,
  kharif_sorghum_area_1000_ha FLOAT,
  kharif_sorghum_production_1000_tons FLOAT,
  kharif_sorghum_yield_kg_per_ha FLOAT,
  rabi_sorghum_area_1000_ha FLOAT,
  rabi_sorghum_production_1000_tons FLOAT,
  rabi_sorghum_yield_kg_per_ha FLOAT,
  sorghum_area_1000_ha FLOAT,
  sorghum_production_1000_tons FLOAT,
  sorghum_yield_kg_per_ha FLOAT,
  pearl_millet_area_1000_ha FLOAT,
  pearl_millet_production_1000_tons FLOAT,
  pearl_millet_yield_kg_per_ha FLOAT,
  maize_area_1000_ha FLOAT,
  maize_production_1000_tons FLOAT,
  maize_yield_kg_per_ha FLOAT,
  finger_millet_area_1000_ha FLOAT,
  finger_millet_production_1000_tons FLOAT,
  finger_millet_yield_kg_per_ha FLOAT,
  barley_area_1000_ha FLOAT,
  barley_production_1000_tons FLOAT,
  barley_yield_kg_per_ha FLOAT,
  chickpea_area_1000_ha FLOAT,
  chickpea_production_1000_tons FLOAT,
  chickpea_yield_kg_per_ha FLOAT,
  pigeonpea_area_1000_ha FLOAT,
  pigeonpea_production_1000_tons FLOAT,
  pigeonpea_yield_kg_per_ha FLOAT,
  groundnut_area_1000_ha FLOAT,
  groundnut_production_1000_tons FLOAT,
  groundnut_yield_kg_per_ha FLOAT,
  sunflower_area_1000_ha FLOAT,
  sunflower_production_1000_tons FLOAT,
  sunflower_yield_kg_per_ha FLOAT,
  soybean_area_1000_ha FLOAT,
  soybean_production_1000_tons FLOAT,
  soybean_yield_kg_per_ha FLOAT,
  oilseeds_area_1000_ha FLOAT,
  oilseeds_production_1000_tons FLOAT,
  oilseeds_yield_kg_per_ha FLOAT,
  sugarcane_area_1000_ha FLOAT,
  sugarcane_production_1000_tons FLOAT,
  sugarcane_yield_kg_per_ha FLOAT,
  cotton_area_1000_ha FLOAT,
  cotton_production_1000_tons FLOAT,
  cotton_yield_kg_per_ha FLOAT,
  fruits_area_1000_ha FLOAT,
  vegetables_area_1000_ha FLOAT,
  fruits_and_vegetables_area_1000_ha FLOAT,
  potatoes_area_1000_ha FLOAT,
  onion_area_1000_ha FLOAT,
  fodder_area_1000_ha FLOAT
);
INSERT INTO agri_data (
  dist_code, year, state_code, state_name, dist_name,
  rice_area_1000_ha, rice_production_1000_tons, rice_yield_kg_per_ha,
  wheat_area_1000_ha, wheat_production_1000_tons, wheat_yield_kg_per_ha,
  sunflower_area_1000_ha, sunflower_production_1000_tons, sunflower_yield_kg_per_ha,
  oilseeds_area_1000_ha, oilseeds_production_1000_tons, oilseeds_yield_kg_per_ha,
  sugarcane_area_1000_ha, sugarcane_production_1000_tons, sugarcane_yield_kg_per_ha,
  groundnut_area_1000_ha, groundnut_production_1000_tons, groundnut_yield_kg_per_ha,
  soybean_area_1000_ha, soybean_production_1000_tons, soybean_yield_kg_per_ha
)
VALUES
('WB01', 2020, 'WB', 'West Bengal', 'Kolkata',
  350.5, 1100.8, 3100,
  45.2, 150.6, 3333,
  10.4, 25.5, 2450,
  60.3, 170.1, 2820,
  100.5, 7200.5, 71000,
  20.1, 55.2, 2745,
  25.2, 70.3, 2780
),

('UP02', 2020, 'UP', 'Uttar Pradesh', 'Lucknow',
  420.8, 1400.2, 3328,
  300.3, 890.1, 2964,
  8.5, 19.7, 2320,
  55.0, 155.6, 2820,
  125.8, 8100.8, 64300,
  22.8, 58.9, 2585,
  18.2, 50.1, 2750
),

('MH03', 2020, 'MH', 'Maharashtra', 'Pune',
  210.4, 700.5, 3329,
  10.2, 30.3, 2971,
  15.8, 45.1, 2850,
  48.9, 130.4, 2666,
  90.7, 6100.6, 67300,
  28.5, 78.3, 2748,
  40.1, 120.6, 3008
);

-- First, find top 3 states by total rice production
WITH top_states AS (
  SELECT state_name,
         SUM(rice_production_1000_tons) AS total_rice
  FROM agri_data
  GROUP BY state_name
  ORDER BY total_rice DESC
  LIMIT 3
)

-- Then, get year-wise for those states
SELECT
  year,
  state_name,
  SUM(rice_production_1000_tons) AS rice_prod_1000_tons
FROM agri_data
WHERE state_name IN (SELECT state_name FROM top_states)
GROUP BY year, state_name
ORDER BY year, state_name;

-- 2 Top 5 districts by wheat yield increase
-- Determine max year
SET @max_year = (SELECT MAX(year) FROM agri_data);

WITH recent AS (
  SELECT dist_name,
         AVG(wheat_production_1000_tons / NULLIF(wheat_area_1000_ha,0)) AS yield_recent
  FROM agri_data
  WHERE year BETWEEN @max_year - 4 AND @max_year
  GROUP BY dist_name
),
previous AS (
  SELECT dist_name,
         AVG(wheat_production_1000_tons / NULLIF(wheat_area_1000_ha,0)) AS yield_prev
  FROM agri_data
  WHERE year BETWEEN @max_year - 9 AND @max_year - 5
  GROUP BY dist_name
)

SELECT
  r.dist_name,
  ROUND(r.yield_recent - p.yield_prev, 2) AS yield_increase,
  ROUND(r.yield_recent,2) AS yield_recent,
  ROUND(p.yield_prev,2) AS yield_previous
FROM recent r
JOIN previous p ON r.dist_name = p.dist_name
ORDER BY yield_increase DESC
LIMIT 5;

-- Oilseed production growth --
SET @max_year = (SELECT MAX(year) FROM agri_data);

WITH curr5 AS (
  SELECT state_name,
         SUM(
           groundnut_production_1000_tons
           + sesamum_production_1000_tons
           + sunflower_production_1000_tons
           + soyabean_production_1000_tons
           + rapeseed_and_mustard_production_1000_tons
         ) AS prod_last5
  FROM agri_data
  WHERE year BETWEEN @max_year - 4 AND @max_year
  GROUP BY state_name
),
prev5 AS (
  SELECT state_name,
         SUM(
           groundnut_production_1000_tons
           + sesamum_production_1000_tons
           + sunflower_production_1000_tons
           + soyabean_production_1000_tons
           + rapeseed_and_mustard_production_1000_tons
         ) AS prod_prev5
  FROM agri_data
  WHERE year BETWEEN @max_year - 9 AND @max_year - 5
  GROUP BY state_name
)

SELECT
  c.state_name,
  ROUND( ((c.prod_last5 - p.prod_prev5) / NULLIF(p.prod_prev5,0)) * 100, 2) AS pct_growth,
  c.prod_last5,
  p.prod_prev5
FROM curr5 c
JOIN prev5 p ON c.state_name = p.state_name
ORDER BY pct_growth DESC
LIMIT 10;

SELECT
  dist_name,
  year,
  rice_area_1000_ha   AS rice_area,
  rice_production_1000_tons AS rice_prod,
  wheat_area_1000_ha  AS wheat_area,
  wheat_production_1000_tons AS wheat_prod,
  maize_area_1000_ha  AS maize_area,
  maize_production_1000_tons AS maize_prod
FROM agri_data
WHERE 
  rice_area_1000_ha IS NOT NULL
  AND wheat_area_1000_ha IS NOT NULL
  AND maize_area_1000_ha IS NOT NULL;
  
-- Find top 5 states by cotton production total
WITH top5 AS (
  SELECT state_name,
         SUM(cotton_production_1000_tons) AS total_cotton
  FROM agri_data
  GROUP BY state_name
  ORDER BY total_cotton DESC
  LIMIT 5
)
SELECT
  year,
  state_name,
  SUM(cotton_production_1000_tons) AS cotton_prod
FROM agri_data
WHERE state_name IN (SELECT state_name FROM top5)
GROUP BY year, state_name
ORDER BY state_name, year;

SELECT dist_name,
       groundnut_production_1000_tons AS groundnut_prod_latest
FROM agri_data
WHERE year = (SELECT MAX(year) FROM agri_data)
ORDER BY groundnut_prod_latest DESC
LIMIT 10;

SELECT
  year,
  ROUND( SUM(maize_production_1000_tons) / NULLIF(SUM(maize_area_1000_ha),0), 2) AS avg_maize_yield_kg_per_ha
FROM agri_data
GROUP BY year
ORDER BY year;

SET @max_year = (SELECT MAX(year) FROM agri_data);

SELECT
  dist_name,
  ROUND(rice_production_1000_tons / NULLIF(rice_area_1000_ha,0), 2) AS rice_yield_latest
FROM agri_data
WHERE year = @max_year
ORDER BY rice_yield_latest DESC
LIMIT 20;

SELECT
  dist_name,
  ROUND(
    SUM(rice_production_1000_tons) / NULLIF(SUM(rice_area_1000_ha),0),
    2
  ) AS avg_rice_yield
FROM agri_data
GROUP BY dist_name
ORDER BY avg_rice_yield DESC
LIMIT 20;

SET @max_year = (SELECT MAX(year) FROM agri_data);

-- Find top 5 states by combined rice + wheat production over the last 10 years
WITH top5 AS (
  SELECT state_name,
         SUM(rice_production_1000_tons + wheat_production_1000_tons) AS total_rw
  FROM agri_data
  WHERE year BETWEEN @max_year - 9 AND @max_year
  GROUP BY state_name
  ORDER BY total_rw DESC
  LIMIT 5
)

SELECT
  year,
  state_name,
  SUM(rice_production_1000_tons) AS rice_prod,
  SUM(wheat_production_1000_tons) AS wheat_prod
FROM agri_data
WHERE
  year BETWEEN @max_year - 9 AND @max_year
  AND state_name IN (SELECT state_name FROM top5)
GROUP BY year, state_name
ORDER BY state_name, year;

ALTER USER 'vikram'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Vikram123';
FLUSH PRIVILEGES;

















