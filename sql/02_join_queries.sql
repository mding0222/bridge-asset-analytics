USE bridge_asset_db;

-- Bridge count by province name
SELECT
    p.province_name,
    COUNT(DISTINCT b.bridge_id) AS bridge_count
FROM dim_bridge b
JOIN dim_province p
    ON b.province_id = p.province_id
GROUP BY p.province_name
ORDER BY bridge_count DESC;

-- Maintenance cost by province
SELECT
    p.province_name,
    ROUND(SUM(m.estimated_budget_cny) / 1000000, 2) AS estimated_maintenance_cost_m
FROM fact_maintenance m
JOIN dim_bridge b
    ON m.bridge_id = b.bridge_id
JOIN dim_province p
    ON b.province_id = p.province_id
GROUP BY p.province_name
ORDER BY estimated_maintenance_cost_m DESC;

-- Defect count by province
SELECT
    p.province_name,
    COUNT(d.defect_id) AS total_defects
FROM fact_defect d
JOIN dim_bridge b
    ON d.bridge_id = b.bridge_id
JOIN dim_province p
    ON b.province_id = p.province_id
GROUP BY p.province_name
ORDER BY total_defects DESC;

-- Bridge count by road class
SELECT
    r.road_class,
    COUNT(DISTINCT b.bridge_id) AS bridge_count
FROM dim_bridge b
JOIN dim_road r
    ON b.road_id = r.road_id
GROUP BY r.road_class
ORDER BY bridge_count DESC;