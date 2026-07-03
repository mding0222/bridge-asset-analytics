-- China Bridge Asset Demo Database (synthetic data)
-- Use this with SQLite / DB Browser for SQLite. All records are simulated for portfolio practice.

.mode csv
.import dim_province.csv dim_province
.import dim_road.csv dim_road
.import dim_bridge.csv dim_bridge
.import fact_inspection.csv fact_inspection
.import fact_defect.csv fact_defect
.import fact_maintenance.csv fact_maintenance

-- 1. Bridge count and average BCI by province
SELECT p.province_name, COUNT(*) AS bridge_count, ROUND(AVG(CAST(b.latest_BCI AS REAL)),1) AS avg_bci,
       SUM(CASE WHEN CAST(b.latest_condition_class AS INTEGER) >= 4 THEN 1 ELSE 0 END) AS class_4_5_count
FROM dim_bridge b
JOIN dim_province p ON b.province_id = p.province_id
GROUP BY p.province_name
ORDER BY class_4_5_count DESC;

-- 2. Top 10 high-risk bridges by estimated defect cost
SELECT b.bridge_id, b.bridge_name, p.province_name, b.road_class, b.bridge_type,
       b.latest_condition_class, b.latest_BCI,
       ROUND(SUM(CAST(d.estimated_repair_cost_cny AS REAL)),0) AS total_defect_cost_cny
FROM dim_bridge b
JOIN dim_province p ON b.province_id = p.province_id
LEFT JOIN fact_defect d ON b.bridge_id = d.bridge_id
GROUP BY b.bridge_id, b.bridge_name, p.province_name, b.road_class, b.bridge_type, b.latest_condition_class, b.latest_BCI
ORDER BY total_defect_cost_cny DESC
LIMIT 10;

-- 3. Defect distribution by component and severity
SELECT component, severity, COUNT(*) AS defect_count,
       ROUND(SUM(CAST(estimated_repair_cost_cny AS REAL)),0) AS estimated_cost_cny
FROM fact_defect
GROUP BY component, severity
ORDER BY estimated_cost_cny DESC;

-- 4. Maintenance budget by planned year and priority
SELECT planned_year, priority, COUNT(*) AS work_items,
       ROUND(SUM(CAST(estimated_budget_cny AS REAL)),0) AS budget_cny
FROM fact_maintenance
GROUP BY planned_year, priority
ORDER BY planned_year, budget_cny DESC;

-- 5. Bridges needing special inspection
SELECT b.bridge_id, b.bridge_name, p.province_name, b.latest_condition_class, b.latest_BCI,
       COUNT(d.defect_id) AS severe_or_critical_defects
FROM dim_bridge b
JOIN dim_province p ON b.province_id=p.province_id
JOIN fact_defect d ON b.bridge_id=d.bridge_id
WHERE d.requires_special_inspection='True'
GROUP BY b.bridge_id, b.bridge_name, p.province_name, b.latest_condition_class, b.latest_BCI
ORDER BY severe_or_critical_defects DESC, CAST(b.latest_BCI AS REAL) ASC;
