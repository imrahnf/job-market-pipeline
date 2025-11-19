# src/cleaning/clean_jobs.py
import json
import os

from src.cleaning.text_cleaning import clean_title, clean_desc
from src.cleaning.salary_parser import parse_salary
from src.cleaning.skill_extractor import extract_skills

RAW_DIR = "src/local_tests/sample_raw_data"
OUTPUT_DIR = "src/local_tests/sample_clean_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_raw_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_job(job):
    cleaned = {}

    # clean strings & text
    cleaned["title"] = clean_title(job.get("title", ""))
    cleaned["company"] = clean_desc(job.get("company_name", ""))
    cleaned["location"] = clean_desc(job.get("location", ""))
    cleaned["description"] = clean_desc(job.get("description", ""))

    # salary parsing {min, max, currency, period}
    cleaned["salary"] = parse_salary(job.get("description", "") + " " + job.get("title", ""))

    # skills []
    cleaned["skills"] = extract_skills(
        job.get("title", "") + " " + job.get("description", "")
    )

    return cleaned


raw_files = [f for f in os.listdir(RAW_DIR) if f.endswith('.json')]
latest_file = sorted(raw_files)[-1] # by name

raw_path = os.path.join(RAW_DIR, latest_file)
data = load_raw_json(raw_path)

cleaned_output = [clean_job(job) for job in data]
for j in cleaned_output:
    print("-"*90)
    print(j["title"])
    print(j["company"])
    print(j["location"])
    print(j["skills"])
    print(j["salary"])
    print("-"*90)
