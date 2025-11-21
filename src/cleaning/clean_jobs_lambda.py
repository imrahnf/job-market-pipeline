# cleaning.clean_jobs_lambda.py
import os
from urllib.parse import unquote_plus

from utils.s3_io import download_json, upload_json
from cleaning.text_cleaning import clean_title, clean_desc
from cleaning.salary_parser import parse_salary
from cleaning.skill_extractor import extract_skills

CLEAN_BUCKET = os.getenv("CLEAN_BUCKET", "job-market-clean")

def clean_job(job):
    cleaned = {}
    cleaned["title"] = clean_title(job.get("title", ""))
    cleaned["company"] = clean_desc(job.get("company_name", ""))
    cleaned["location"] = clean_desc(job.get("location", ""))
    cleaned["description"] = clean_desc(job.get("description", ""))
    cleaned["salary"] = parse_salary(
        job.get("description", "") + " " + job.get("title", "")
    )
    cleaned["skills"] = extract_skills(
        job.get("title", "") + " " + job.get("description", "")
    )
    return cleaned


def handler(event, context):
    """
    handler expected to be invoked by S3 event.
    it reads the object key from the event, downloads JSON, cleans, and ruploads.
    """
    # extract bucket key from S3 event
    try:
        record = event["Records"][0]
        bucket = record["s3"]["bucket"]["name"]
        key = unquote_plus(record["s3"]["object"]["key"])
    except Exception as e:
        return {"statusCode": 400, "message": f"invalid S3 event: {e}"}

    # download
    raw_data = download_json(bucket, key)

    # clean
    cleaned = [clean_job(j) for j in raw_data]

    if key.startswith("raw/"):
        clean_key = key.replace("raw/", "clean/")
    else:
        clean_key = f"clean/{key.rsplit('/',1)[-1]}"

    upload_json(CLEAN_BUCKET, clean_key, cleaned)
    return {"statusCode": 200, "message": f"Cleaned {len(cleaned)} items", "s3_key": clean_key}
