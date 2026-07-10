-- ============================================================
-- 1. Bridge defect and maintenance summary
-- Purpose:
-- Summarise defect and maintenance records separately before
-- joining them, avoiding row multiplication between fact tables.
-- ============================================================

WITH defect_summary AS
(
    SELECT
        bridge_id,
        COUNT(*) AS defect_count
    FROM fact_defect
    GROUP BY bridge_id
),

maintenance_summary AS
(
    SELECT
        bridge_id,
        COUNT(*) AS maintenance_count
    FROM fact_maintenance
    GROUP BY bridge_id
)

SELECT
    b.bridge_id,
    b.bridge_name,
    b.latest_BCI,
    COALESCE(d.defect_count, 0) AS defect_count,
    COALESCE(m.maintenance_count, 0) AS maintenance_count
FROM dim_bridge b
LEFT JOIN defect_summary d
    ON b.bridge_id = d.bridge_id
LEFT JOIN maintenance_summary m
    ON b.bridge_id = m.bridge_id
ORDER BY b.latest_BCI ASC;

-- ============================================================
-- 2. Bridges with above-average defect counts
-- ============================================================

WITH defect_summary AS
(
    SELECT
        bridge_id,
        COUNT(*) AS defect_count
    FROM fact_defect
    GROUP BY bridge_id
)

SELECT
    bridge_id,
    defect_count
FROM defect_summary
WHERE defect_count >
(
    SELECT AVG(defect_count)
    FROM defect_summary
)
ORDER BY defect_count DESC;

-- ============================================================
-- 3. Bridges with above-average defect and maintenance counts
-- ============================================================

WITH defect_summary AS
(
    SELECT
        bridge_id,
        COUNT(*) AS defect_count
    FROM fact_defect
    GROUP BY bridge_id
),

maintenance_summary AS
(
    SELECT
        bridge_id,
        COUNT(*) AS maintenance_count
    FROM fact_maintenance
    GROUP BY bridge_id
)

SELECT
    b.bridge_id,
    b.bridge_name,
    b.latest_BCI,
    d.defect_count,
    m.maintenance_count
FROM dim_bridge b
INNER JOIN defect_summary d
    ON b.bridge_id = d.bridge_id
INNER JOIN maintenance_summary m
    ON b.bridge_id = m.bridge_id
WHERE d.defect_count >
(
    SELECT AVG(defect_count)
    FROM defect_summary
)
AND m.maintenance_count >
(
    SELECT AVG(maintenance_count)
    FROM maintenance_summary
)
ORDER BY
    d.defect_count DESC,
    m.maintenance_count DESC;
    
    -- ============================================================
-- 5. Latest inspection record for each bridge
-- CTE + JOIN approach
-- ============================================================

WITH latest_inspection_dates AS
(
    SELECT
        bridge_id,
        MAX(inspection_date) AS latest_inspection_date
    FROM fact_inspection
    GROUP BY bridge_id
)

SELECT
    i.inspection_id,
    i.bridge_id,
    b.bridge_name,
    i.inspection_date,
    i.BCI
FROM latest_inspection_dates l
INNER JOIN fact_inspection i
    ON l.bridge_id = i.bridge_id
   AND l.latest_inspection_date = i.inspection_date
INNER JOIN dim_bridge b
    ON i.bridge_id = b.bridge_id
ORDER BY i.bridge_id;
    
    
    