-- Visits with missing forms
SELECT subject_id, visit_name, visit_date, form_completed_flag
FROM visits
WHERE form_completed_flag = 'N'
ORDER BY visit_date;