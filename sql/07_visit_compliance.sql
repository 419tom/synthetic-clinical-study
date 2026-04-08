-- Missed visits by visit type
SELECT visit_name, COUNT(*) AS missed_visits
FROM visits
WHERE visit_status = 'Missed'
GROUP BY visit_name
ORDER BY missed_visits DESC;