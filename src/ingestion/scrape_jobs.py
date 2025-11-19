# src/ingestion/srape_jobs.py
from dotenv import load_dotenv
from serpapi import GoogleSearch
from datetime import datetime, UTC
import os
import json

load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

SEARCHES = ["Data Analyst", "Data Engineer", "Backend Developer", "Cloud Engineer", "Software Developer"]
LOCATION = "Toronto, Ontario, Canada"

OUTPUT_DIR = "src/local_tests/sample_raw_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# SEARCH FIELDS
params = {
    "api_key": SERPAPI_KEY,
    "engine": "google_jobs",
    "google_domain": "google.ca",
    "q": SEARCHES[0],
    "hl": "en",
    "gl": "ca",
    "location": LOCATION
}

search = GoogleSearch(params)
results = search.get_dict()
jobs_results = results.get("jobs_results", [])

parsed_jobs = []

for job in jobs_results:
    application_links = []
    apply_options = job.get("apply_options")

    if apply_options:
        for option in apply_options:
            app_title = option.get("title")
            app_link = option.get("link")
            application_links.append({"title": app_title, "link": app_link})

    detected = job.get("detected_extensions", {})

    parsed_jobs.append({
        "job_id": job.get("job_id", "N/A"),
        "title": job.get("title", "N/A"),
        "company_name": job.get("company_name", "N/A"),
        "location": job.get("location", "N/A"),
        "posted_at": detected.get("posted_at"),
        "schedule_type": detected.get("schedule_type"),
        "work_from_home": detected.get("work_from_home"),
        "description": job.get("description", "N/A"),
        "application_links": application_links,
        "fetched_at": datetime.now(UTC).isoformat()
    })

# save output
today = datetime.today().strftime("%Y-%m-%d")
output_file = os.path.join(OUTPUT_DIR, f"serpapi_jobs_{today}.json")

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(parsed_jobs, f, indent=2)

print(f"Saved {len(parsed_jobs)} jobs to {output_file}")