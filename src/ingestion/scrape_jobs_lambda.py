# /ingestion/srape_jobs_lambda.py
import os
from datetime import datetime, UTC
from serpapi import GoogleSearch

from utils.s3_io import upload_json

# config
SEARCHES = ["Data Analyst", "Data Engineer", "Backend Developer", "Cloud Engineer", "Software Developer"]
LOCATION = "Toronto, Ontario, Canada"
RAW_BUCKET = os.getenv("RAW_BUCKET", "job-market-raw")
SERPAPI_KEY = os.getenv("SERPAPI_KEY")

def scrape_once(query):
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google_jobs",
        "google_domain": "google.ca",
        "q": query,              # loop later
        "hl": "en",
        "gl": "ca",
        "location": LOCATION
    }
    search = GoogleSearch(params)
    results = search.get_dict() or {}
    return results.get("jobs_results", [])

def handler(event, context):
    # Lambda entry point. Scrapes SerpAPI and uploads to S3.
    all_jobs = []

    for q in SEARCHES:
        try:
            jobs = scrape_once(q)
            all_jobs.extend(jobs)
        except Exception as e:
            # keep going if one query fails
            print(f"error scraping {q}: {e}")

    # normalized into dicts
    parsed_jobs = []
    for job in all_jobs:
        # extract apply links
        application_links = []
        apply_options = job.get("apply_options")

        if apply_options:
            for option in apply_options:
                app_title = option.get("title")
                app_link = option.get("link")
                application_links.append({
                    "title": app_title, 
                    "link": app_link
                })

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
    
    # upload to S3
    today = datetime.today().strftime("%Y-%m-%d")
    key = f"serpapi_jobs_{today}.json"
    upload_json("job-market-raw", key, parsed_jobs)

    return {
        "statusCode": 200,
        "message": f"Uploaded {len(parsed_jobs)} jobs to s3://job-market-raw/{key}"
    }