# synthetic_clinical_study_generator.py

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()


# CONFIGURATION

n_sites = 10
n_subjects = 300
visit_names = ['Screening', 'Baseline', 'Week 4', 'Week 8', 'Week 12', 'End of Study']
lab_tests = ['ALT','AST','Hemoglobin','WBC','Creatinine']
ae_terms = ['Headache','Nausea','Fatigue','Fever','Chest Pain','Dizziness']
conmeds_list = ['Lisinopril','Metformin','Atorvastatin','Omeprazole','Levothyroxine']
deviation_types = ['Visit Window Missed','Missing Lab Sample','Protocol Violation','Unscheduled Visit']
issue_types = ['Missing Form','Missing Severity','Out-of-Range Lab','Duplicate Record']

start_date = datetime(2025,1,1)


# 1) Sites

sites_data = []
for i in range(1, n_sites+1):
    site_id = f"S{i:03d}"
    sites_data.append([
        site_id,
        fake.company(),
        fake.country(),
        fake.name(),
        start_date + timedelta(days=random.randint(0,30))
    ])

sites_df = pd.DataFrame(sites_data, columns=['site_id','site_name','country','principal_investigator','site_activation_date'])
sites_df.to_csv('data/raw/sites.csv', index=False)


# 2) Subjects

subjects_data = []
for i in range(1, n_subjects+1):
    subject_id = f"SUBJ{i:03d}"
    site_id = f"S{random.randint(1,n_sites):03d}"
    sex = random.choice(['M','F'])
    age = np.random.randint(18,80)
    screening_date = start_date + timedelta(days=random.randint(0,90))
    randomization_date = screening_date + timedelta(days=random.randint(1,7)) if random.random()>0.1 else None
    status = random.choices(['Completed','Active','Discontinued','Screen Failed'], weights=[0.5,0.3,0.1,0.1])[0]
    subjects_data.append([subject_id, site_id, sex, age, screening_date, randomization_date, status])

subjects_df = pd.DataFrame(subjects_data, columns=['subject_id','site_id','sex','age','screening_date','randomization_date','status'])
subjects_df.to_csv('data/raw/subjects.csv', index=False)


# 3) Visits

visits_data = []
visit_id_counter = 1
for subject in subjects_df.itertuples():
    for vname in visit_names:
        visit_date = subject.screening_date + timedelta(days=7*visit_names.index(vname)) + timedelta(days=random.randint(-2,2))
        visit_status = random.choices(['Completed','Missed','Scheduled'], weights=[0.85,0.1,0.05])[0]
        form_flag = random.choices(['Y','N'], weights=[0.9,0.1])[0]
        visits_data.append([f"V{visit_id_counter:04d}", subject.subject_id, vname, visit_date, visit_status, form_flag])
        visit_id_counter += 1

visits_df = pd.DataFrame(visits_data, columns=['visit_id','subject_id','visit_name','visit_date','visit_status','form_completed_flag'])
visits_df.to_csv('data/raw/visits.csv', index=False)


# 4) Labs

labs_data = []
lab_id_counter = 1
for visit in visits_df.itertuples():
    for lab in lab_tests:
        # normal value ranges
        ranges = {
            'ALT': (7,56),
            'AST': (10,40),
            'Hemoglobin': (12,16),
            'WBC': (4,11),
            'Creatinine': (0.6,1.3)
        }
        low, high = ranges[lab]
        # introduce some out-of-range values
        if random.random() < 0.05:
            value = high + random.uniform(1,10)
        elif random.random() < 0.05:
            value = low - random.uniform(1,3)
        else:
            value = np.random.uniform(low, high)
        # 5% missing
        if random.random() < 0.05:
            value = None
        labs_data.append([f"L{lab_id_counter:05d}", visit.subject_id, visit.visit_id, lab, round(value,2) if value is not None else None, low, high, visit.visit_date])
        lab_id_counter += 1

labs_df = pd.DataFrame(labs_data, columns=['lab_id','subject_id','visit_id','lab_test','lab_value','normal_range_low','normal_range_high','collection_date'])
labs_df.to_csv('data/raw/labs.csv', index=False)


# 5) Adverse Events

ae_data = []
ae_id_counter = 1
for subject in subjects_df.itertuples():
    n_ae = np.random.poisson(0.3)  # most subjects have 0–1 AE
    for _ in range(n_ae):
        term = random.choice(ae_terms)
        serious_flag = random.choices(['Y','N'], weights=[0.05,0.95])[0]
        severity = random.choices(['Mild','Moderate','Severe'], weights=[0.5,0.4,0.1])[0] if random.random()>0.05 else None
        start_date = subject.screening_date + timedelta(days=random.randint(0,90))
        end_date = start_date + timedelta(days=random.randint(1,7))
        related = random.choices(['Y','N'], weights=[0.7,0.3])[0]
        ae_data.append([f"AE{ae_id_counter:05d}", subject.subject_id, term, serious_flag, severity, start_date, end_date, related])
        ae_id_counter +=1

ae_df = pd.DataFrame(ae_data, columns=['ae_id','subject_id','ae_term','serious_flag','severity','start_date','end_date','related_to_study_drug'])
ae_df.to_csv('data/raw/adverse_events.csv', index=False)


# 6) Concomitant Medications

conmed_data = []
conmed_id_counter = 1
for subject in subjects_df.itertuples():
    n_med = np.random.poisson(1)  # some subjects have meds
    for _ in range(n_med):
        med = random.choice(conmeds_list)
        start_date = subject.screening_date - timedelta(days=random.randint(30,60))
        end_date = start_date + timedelta(days=random.randint(30,90)) if random.random()>0.3 else None
        indication = fake.word()
        conmed_data.append([f"CM{conmed_id_counter:05d}", subject.subject_id, med, start_date, end_date, indication])
        conmed_id_counter +=1

conmed_df = pd.DataFrame(conmed_data, columns=['conmed_id','subject_id','medication_name','start_date','end_date','indication'])
conmed_df.to_csv('data/raw/conmeds.csv', index=False)


# 7) Protocol Deviations

deviation_data = []
deviation_id_counter = 1
for subject in subjects_df.itertuples():
    if random.random() < 0.15:  # 15% subjects have deviations
        dev_type = random.choice(deviation_types)
        site_id = subject.site_id
        dev_date = subject.screening_date + timedelta(days=random.randint(0,90))
        severity = random.choices(['Minor','Major'], weights=[0.7,0.3])[0]
        description = f"{dev_type} for subject {subject.subject_id}"
        deviation_data.append([f"PD{deviation_id_counter:05d}", subject.subject_id, site_id, dev_type, dev_date, severity, description])
        deviation_id_counter +=1

pd_df = pd.DataFrame(deviation_data, columns=['deviation_id','subject_id','site_id','deviation_type','deviation_date','severity','description'])
pd_df.to_csv('data/raw/protocol_deviations.csv', index=False)


# 8) Data Queries

query_data = []
query_id_counter = 1
for subject in subjects_df.itertuples():
    n_query = np.random.poisson(0.5)
    for _ in range(n_query):
        source = random.choice(['visits','labs','adverse_events'])
        issue = random.choice(issue_types)
        description = f"{issue} found in {source} for {subject.subject_id}"
        status = random.choices(['Open','Closed','Pending'], weights=[0.2,0.7,0.1])[0]
        opened_date = subject.screening_date + timedelta(days=random.randint(0,90))
        closed_date = opened_date + timedelta(days=random.randint(1,10)) if status=='Closed' else None
        assigned = f"DataMgr{random.randint(1,5)}"
        query_data.append([f"Q{query_id_counter:05d}", subject.subject_id, subject.site_id, source, issue, description, status, opened_date, closed_date, assigned])
        query_id_counter +=1

queries_df = pd.DataFrame(query_data, columns=['query_id','subject_id','site_id','source_table','issue_type','issue_description','status','opened_date','closed_date','assigned_to'])
queries_df.to_csv('data/raw/data_queries.csv', index=False)


# 9) Incident / Change Log

incident_data = []
incident_id_counter = 1
for _ in range(30):
    category = random.choice(['Report Logic','Missing Data Export','System Error'])
    description = f"{category} observed in study reports"
    reported_date = start_date + timedelta(days=random.randint(0,90))
    status = random.choice(['Open','Closed'])
    resolution_date = reported_date + timedelta(days=random.randint(1,10)) if status=='Closed' else None
    change_flag = random.choice(['Y','N'])
    incident_data.append([f"INC{incident_id_counter:04d}", category, description, reported_date, status, resolution_date, change_flag])
    incident_id_counter +=1

incident_df = pd.DataFrame(incident_data, columns=['incident_id','issue_category','description','reported_date','status','resolution_date','change_request_flag'])
incident_df.to_csv('data/raw/incident_change_log.csv', index=False)

print("All synthetic clinical study CSVs generated successfully!")