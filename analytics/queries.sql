-- Query 1: Which airline has the highest average delay?
SELECT 
    a.airline_code,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.dep_delay)::numeric, 2) AS avg_dep_delay,
    ROUND(AVG(f.arr_delay)::numeric, 2) AS avg_arr_delay
FROM fact_flights f
JOIN dim_airline a ON f.airline_id = a.airline_id
GROUP BY a.airline_code
ORDER BY avg_dep_delay DESC;

-- Query 2: Which routes from JFK have worst delays?
SELECT 
    f.dest,
    a.city_name,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.dep_delay)::numeric, 2) AS avg_delay
FROM fact_flights f
JOIN dim_airport a ON f.dest_id = a.airport_id
GROUP BY f.dest, a.city_name
ORDER BY avg_delay DESC
LIMIT 10;

-- Query 3: Which day of week has worst delays?
SELECT 
    t.day_of_week,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.dep_delay)::numeric, 2) AS avg_delay
FROM fact_flights f
JOIN dim_time t ON f.date_id = t.date_id
GROUP BY t.day_of_week
ORDER BY avg_delay DESC;

-- Query 4: What caused most cancellations?
SELECT 
    cancellation_code,
    COUNT(*) AS total_cancellations,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM fact_flights
WHERE cancellation_code != 'N'
GROUP BY cancellation_code
ORDER BY total_cancellations DESC;

-- Query 5: How did delays trend across January 2025?
SELECT 
    t.full_date,
    t.day_of_week,
    COUNT(*) AS total_flights,
    ROUND(AVG(f.dep_delay)::numeric, 2) AS avg_delay
FROM fact_flights f
JOIN dim_time t ON f.date_id = t.date_id
GROUP BY t.full_date, t.day_of_week
ORDER BY t.full_date;
