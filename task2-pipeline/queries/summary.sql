-- Average temperature range and total rainfall by day
-- Shows which days had the highest thermal variation

SELECT
  date,
  location,
  ROUND(temperature_2m_max, 1) AS max_temp_c,
  ROUND(temperature_2m_min, 1) AS min_temp_c,
  ROUND(temp_range_c, 1)       AS temp_range_c,
  ROUND(precipitation_sum, 2)  AS rainfall_mm,
  is_rainy_day,
  ROUND(windspeed_10m_max, 1)  AS max_wind_kmh
FROM `rapid-pottery-497706-n0.weather_pipeline.forecasts`
ORDER BY date ASC;
