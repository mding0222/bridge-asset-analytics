USE bridge_asset_db;

-- Total defects
SELECT
    COUNT(*) AS total_defects
FROM fact_defect;

-- Most common defect types
SELECT
    defect_type,
    COUNT(*) AS defect_count
FROM fact_defect
GROUP BY defect_type
ORDER BY defect_count DESC;

-- Defects by bridge component
SELECT
    component,
    COUNT(*) AS defect_count
FROM fact_defect
GROUP BY component
ORDER BY defect_count DESC;

-- Defects by component and defect type
SELECT
    component,
    defect_type,
    COUNT(*) AS defect_count
FROM fact_defect
GROUP BY component, defect_type
ORDER BY component, defect_count DESC;