USE bridge_asset_db;

-- Preview bridge asset table
SELECT *
FROM dim_bridge
LIMIT 10;

-- Total number of bridges
SELECT
    COUNT(DISTINCT bridge_id) AS total_bridges
FROM dim_bridge;

-- Total bridge length in kilometres
SELECT
    ROUND(SUM(length_m) / 1000, 2) AS total_bridge_length_km
FROM dim_bridge;

-- Bridge count by province ID
SELECT
    province_id,
    COUNT(*) AS bridge_count
FROM dim_bridge
GROUP BY province_id
ORDER BY bridge_count DESC;

-- Bridge condition distribution
SELECT
    latest_condition_class,
    COUNT(*) AS bridge_count
FROM dim_bridge
GROUP BY latest_condition_class
ORDER BY latest_condition_class;