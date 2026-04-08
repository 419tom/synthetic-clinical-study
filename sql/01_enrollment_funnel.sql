-- Enrollment funnel by site
SELECT s.site_id, s.site_name, sub.status, COUNT(*) AS n_subjects
FROM subjects sub
JOIN sites s ON sub.site_id = s.site_id
GROUP BY s.site_id, s.site_name, sub.status
ORDER BY s.site_id, sub.status;