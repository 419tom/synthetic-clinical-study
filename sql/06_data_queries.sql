-- Open queries by site
SELECT dq.site_id, s.site_name, dq.issue_type, COUNT(*) AS n_open_queries
FROM data_queries dq
JOIN sites s ON dq.site_id = s.site_id
WHERE dq.status = 'Open'
GROUP BY dq.site_id, s.site_name, dq.issue_type
ORDER BY n_open_queries DESC;