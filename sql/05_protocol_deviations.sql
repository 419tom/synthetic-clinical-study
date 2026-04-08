-- Deviations by site
SELECT pd.site_id, s.site_name, pd.severity, COUNT(*) AS n_deviations
FROM protocol_deviations pd
JOIN sites s ON pd.site_id = s.site_id
GROUP BY pd.site_id, s.site_name, pd.severity
ORDER BY pd.site_id;