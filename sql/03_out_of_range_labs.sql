-- Out-of-range labs
SELECT subject_id, visit_id, lab_test, lab_value, normal_range_low, normal_range_high
FROM labs
WHERE lab_value < normal_range_low OR lab_value > normal_range_high
ORDER BY subject_id;