-- Count AEs by severity
SELECT severity, COUNT(*) AS n_events
FROM adverse_events
GROUP BY severity
ORDER BY n_events DESC;