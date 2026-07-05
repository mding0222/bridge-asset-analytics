USE bridge_asset_db;

-- Top 10 risk bridges based on lowest latest BCI
SELECT
    b.bridge_name,
    p.province_name,
    r.road_class,
    b.bridge_type,
    b.latest_condition_class,
    b.latest_BCI,
    COUNT(d.defect_id) AS total_defects
FROM dim_bridge b
LEFT JOIN dim_province p
    ON b.province_id = p.province_id
LEFT JOIN dim_road r
    ON b.road_id = r.road_id
LEFT JOIN fact_defect d
    ON b.bridge_id = d.bridge_id
GROUP BY
    b.bridge_id,
    b.bridge_name,
    p.province_name,
    r.road_class,
    b.bridge_type,
    b.latest_condition_class,
    b.latest_BCI
ORDER BY b.latest_BCI ASC
LIMIT 10;

-- High-risk bridge count by condition class
SELECT
    latest_condition_class,
    COUNT(*) AS bridge_count
FROM dim_bridge
WHERE latest_condition_class >= 4
GROUP BY latest_condition_class
ORDER BY latest_condition_class DESC;