import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# ----------------------------
# Base project path
# ----------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")

os.makedirs(PROCESSED_DIR, exist_ok=True)

# ----------------------------
# File paths
# ----------------------------
ae_path = os.path.join(RAW_DIR, "adverse_events.csv")
pd_path = os.path.join(RAW_DIR, "protocol_deviations.csv")
inc_path = os.path.join(RAW_DIR, "incident_change_log.csv")

print("Loading files from:")
print(RAW_DIR)

# ----------------------------
# Load datasets
# ----------------------------
ae_df = pd.read_csv(ae_path)
pd_df = pd.read_csv(pd_path)
inc_df = pd.read_csv(inc_path)

# ----------------------------
# Ensure description column exists
# ----------------------------
def ensure_text_column(df, text_col, fallback_cols=None):
    if text_col not in df.columns:
        print(f"Column '{text_col}' not found. Attempting fallback...")

        if fallback_cols:
            for col in fallback_cols:
                if col in df.columns:
                    print(f"Using fallback column: {col}")
                    df[text_col] = df[col].astype(str)
                    return df

        print(f"No fallback found. Creating empty '{text_col}' column.")
        df[text_col] = ""

    return df

# Apply fallback logic
ae_df = ensure_text_column(ae_df, "description", fallback_cols=["ae_term"])
pd_df = ensure_text_column(pd_df, "description", fallback_cols=["deviation_type"])
inc_df = ensure_text_column(inc_df, "description", fallback_cols=["issue_category"])

# ----------------------------
# Generic clustering function
# ----------------------------
def cluster_text(df, text_col, cluster_col, n_clusters=3):
    df[text_col] = df[text_col].fillna("").astype(str).str.lower()

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df[text_col])

    # Prevent crash if very few unique rows
    n_clusters = min(n_clusters, max(1, len(df[text_col].unique())))
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    df[cluster_col] = kmeans.fit_predict(X)

    return df

# ----------------------------
# AE clustering
# ----------------------------
ae_df = cluster_text(ae_df, "description", "ae_cluster", 3)
ae_df.to_csv(os.path.join(PROCESSED_DIR, "ae_text_clusters.csv"), index=False)

# ----------------------------
# Protocol deviation clustering
# ----------------------------
pd_df = cluster_text(pd_df, "description", "deviation_cluster", 3)
pd_df.to_csv(os.path.join(PROCESSED_DIR, "protocol_deviation_clusters.csv"), index=False)

# ----------------------------
# Incident clustering
# ----------------------------
inc_df = cluster_text(inc_df, "description", "incident_cluster", 3)
inc_df.to_csv(os.path.join(PROCESSED_DIR, "incident_topics.csv"), index=False)

print("NLP analysis complete.")
print("Processed files saved to:")
print(PROCESSED_DIR)