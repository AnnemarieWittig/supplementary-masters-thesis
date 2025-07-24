import os
import pandas as pd
import json
import logging
from collections import defaultdict

# Track discovered users with source info: {user: [(repo, filename, column, row_index)]}
user_sources = defaultdict(list)

# ------------------ Logging ------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("restructuring.log"),
        logging.StreamHandler()
    ]
)
log = logging.getLogger()

# ------------------ Paths ------------------
path_to_files = "./HRE"
path_to_by_person = os.path.join(path_to_files, 'by_person')
os.makedirs(path_to_by_person, exist_ok=True)

subdirectories = [
    os.path.join(path_to_files, d)
    for d in os.listdir(path_to_files)
    if os.path.isdir(os.path.join(path_to_files, d)) and d != 'by_person'
]

# ------------------ Field Mappings ------------------
user_discovery_fields = {
    'branches.csv': ['created_by','last_author'],
    'commits.csv': ['author'],
    'pull_requests.csv': ['author','merged_by'],
    'releases.csv': ['author'],
    'workflow_runs.csv': ['author'],
}

per_person_match_fields = {
    'branches.csv': ['created_by','last_author'],
    'commits.csv': ['author', 'message'],
    'pull_requests.csv':  ['author','merged_by','title','description','requested_reviewers','assignees'],
    'releases.csv': ['author', 'message'],
    'workflow_runs.csv': ['author', 'name'],
}

file_types_to_filter_by_shas = {
    'files.json': ['commit_sha'],
}

# ------------------ Phase 1: Extract All Persons ------------------
all_people = set()

for repo_path in subdirectories:
    repo_name = os.path.basename(repo_path)
    log.info(f"Scanning repo: {repo_path}")
    
    for filename, cols in user_discovery_fields.items():
        file_path = os.path.join(repo_path, filename)
        if not os.path.exists(file_path):
            log.debug(f"Missing file: {file_path}")
            continue
        try:
            df = pd.read_csv(file_path, dtype=str)
        except Exception as e:
            log.warning(f"Could not read {file_path}: {e}")
            continue

        for col in cols:
            if col in df.columns:
                series = df[col].dropna().astype(str)
                for idx, val in series.items():
                    parts = [v.strip() for v in val.split(',') if v.strip()]
                    for part in parts:
                        if part not in all_people:
                            log.info(f"Found user '{part}' in {repo_name}/{filename}")
                            all_people.add(part)

                        user_sources[part].append((repo_name, filename, col, idx))

log.info(f"Total unique persons identified: {len(all_people)}")
log.info("User discovery details:")

# for user, occurrences in user_sources.items():
#     for repo, file, col, idx in occurrences:
#         log.info(f"User '{user}' found in {repo}/{file} column '{col}' at row {idx}")

# ------------------ Phase 2: Per Person Processing ------------------
for person in all_people:
    person_dir = os.path.join(path_to_by_person, person)
    os.makedirs(person_dir, exist_ok=True)
    person_shas = set()

    log.info(f"Processing person: {person}")

    for repo_path in subdirectories:
        for filename, cols in per_person_match_fields.items():
            file_path = os.path.join(repo_path, filename)
            if not os.path.exists(file_path):
                continue
            try:
                df = pd.read_csv(file_path, dtype=str)
            except Exception as e:
                log.warning(f"Could not read {file_path}: {e}")
                continue

            mask = pd.Series(False, index=df.index)
            for col in cols:
                if col in df.columns:
                    col_data = df[col].astype(str)
                    # First: direct user matches (split by comma)
                    direct_match = col_data.str.split(',').apply(
                        lambda items: any(person == item.strip() for item in items)
                    )
                    # Second: general substring (for text fields)
                    substr_match = col_data.str.contains(person, case=False, na=False)
                    mask |= direct_match | substr_match


            filtered_df = df[mask]
            if not filtered_df.empty:
                out_path = os.path.join(person_dir, filename)
                filtered_df.to_csv(out_path, mode='a', header=not os.path.exists(out_path), index=False)
                log.info(f"Wrote {len(filtered_df)} rows to {out_path}")

                if filename == 'commits.csv' and 'sha' in filtered_df.columns:
                    new_shas = set(filtered_df['sha'].dropna().astype(str))
                    person_shas.update(new_shas)
                    log.debug(f"Tracking {len(new_shas)} SHAs for {person} from commits.csv")


# ------------------ Phase 3: Collect Files by Person ------------------
all_files = []
all_shas = []
for repo_path in subdirectories:
    file_path = os.path.join(repo_path, 'files.json')
    if not os.path.exists(file_path):
        log.debug(f"Missing file: {file_path}")
        continue
    with open(file_path, 'r') as f:
        files = json.load(f)
        all_files.extend(files)
        for file in files:
            sha = file.get('commit_sha')
            all_shas.append(sha)
unique_shas = set(all_shas)

for person in all_people:
    commit_file = os.path.join(path_to_by_person, person, 'commits.csv')
    personal_file_information = []
    if os.path.exists(commit_file):
        df = pd.read_csv(commit_file, dtype=str)
        commits_in_df = df['sha'].dropna().astype(str).unique()
        for file_info in all_files:
            sha = file_info.get('commit_sha')
            if sha in commits_in_df:
                personal_file_information.append(file_info)
                
    if personal_file_information:
        out_path = os.path.join(path_to_by_person, person, 'files.json')
        with open(out_path, 'w') as f:
            json.dump(personal_file_information, f, indent=2)
        log.info(f"Wrote {len(personal_file_information)} items to {out_path} (files.json for {person})")
    else:
        log.info(f"No matching files found for {person} in commits.csv")
        