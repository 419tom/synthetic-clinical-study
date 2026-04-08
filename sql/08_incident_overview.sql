-- Incidents summary
SELECT status, COUNT(*) AS n_incidents
FROM incident_change_log
GROUP BY status;