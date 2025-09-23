-- 1️⃣ Create database
CREATE DATABASE IF NOT EXISTS securecheck
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
USE securecheck;

-- 2️⃣ Create table
CREATE TABLE IF NOT EXISTS traffic_stops (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  stop_date DATE,
  stop_time TIME,
  country_name VARCHAR(100),
  driver_gender VARCHAR(20),
  driver_age SMALLINT,
  driver_race VARCHAR(50),
  violation_raw VARCHAR(120),
  violation VARCHAR(120),
  search_conducted TINYINT(1),
  search_type VARCHAR(120),
  stop_outcome VARCHAR(50),
  is_arrested TINYINT(1),
  stop_duration VARCHAR(30),
  drugs_related_stop TINYINT(1),
  vehicle_number VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3️⃣ Insert sample data
INSERT INTO traffic_stops
(stop_date, stop_time, country_name, driver_gender, driver_age, driver_race,
 violation_raw, violation, search_conducted, search_type, stop_outcome,
 is_arrested, stop_duration, drugs_related_stop, vehicle_number)
VALUES
('2025-08-26','14:25:00','India','Male',28,'Asian','Speeding - 25 km/h over','Speeding',0,NULL,'Warning',0,'0-15 Min',0,'TN10AB1234'),
('2025-08-26','10:15:00','India','Male',28,'Asian','Speeding over 60','Speeding',0,NULL,'Warning',0,'0-15 Min',0,'TN10AB1234'),
('2025-08-26','11:45:00','India','Female',34,'Asian','Red light violation','Signal Violation',1,'Vehicle search','Ticket',0,'16-30 Min',0,'TN22XY5678'),
('2025-08-25','20:05:00','India','Male',42,'Asian','Driving under influence','DUI',1,'Full search','Arrest',1,'30+ Min',1,'KA09GH4321');
USE securecheck;
INSERT INTO traffic_stops
(stop_date, stop_time, country_name, driver_gender, driver_age, driver_race,
 violation_raw, violation, search_conducted, search_type, stop_outcome,
 is_arrested, stop_duration, drugs_related_stop, vehicle_number)
VALUES
('2025-09-19','09:00:00','India','Male',22,'Asian','Speeding 10 km/h over','Speeding',0,NULL,'Warning',0,'0-15 Min',0,'TN11AB1111'),
('2025-09-19','15:30:00','India','Female',19,'Asian','Red light violation','Signal Violation',0,NULL,'Warning',0,'0-15 Min',0,'TN12CD2222');
SELECT COUNT(*) FROM traffic_stops WHERE driver_age < 25;
USE securecheck;
SHOW DATABASES;
USE agri;
SHOW TABLES;
DESC agri_data;
USE agri;

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
USE agri;

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
USE agri;

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
USE agri;

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
  
  USE agri;

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

USE agri;

SELECT dist_name,
       groundnut_production_1000_tons AS groundnut_prod_latest
FROM agri_data
WHERE year = (SELECT MAX(year) FROM agri_data)
ORDER BY groundnut_prod_latest DESC
LIMIT 10;

USE agri;

SELECT
  year,
  ROUND( SUM(maize_production_1000_tons) / NULLIF(SUM(maize_area_1000_ha),0), 2) AS avg_maize_yield_kg_per_ha
FROM agri_data
GROUP BY year
ORDER BY year;

USE agri;

SET @max_year = (SELECT MAX(year) FROM agri_data);

SELECT
  dist_name,
  ROUND(rice_production_1000_tons / NULLIF(rice_area_1000_ha,0), 2) AS rice_yield_latest
FROM agri_data
WHERE year = @max_year
ORDER BY rice_yield_latest DESC
LIMIT 20;

USE agri;

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

USE agri;

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

















