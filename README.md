View the **demo** (WIP): https://job-market-pipeline.omrahnfaqiri.com/
---
# Job Market Pipeline

A serverless data pipeline for processing job market data using AWS Lambda functions. The pipeline ingests raw job data, cleans and transforms it, and prepares it for analysis.

## Features

- **Ingestion Lambda**: Scrapes and ingests raw job data from SerpAPI.
- **Cleaning Lambda**: Processes and cleans the data, extracting skills, salaries, and other attributes.
- **Automated Deployment**: Deploys to AWS Lambda via GitHub Actions on pushes to `main` branch.

## Prerequisites

- Python 3.12
- AWS account with Lambda permissions
- IAM role for OIDC authentication (configured for GitHub Actions)

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/imrahnf/job-market-pipeline.git
   cd job-market-pipeline
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure AWS:
   - Create Lambda functions: `job-cleaning` and `job-ingestion` in region `ca-central-1`.
   - Set up IAM role with OIDC trust for GitHub Actions.
   - Add `AWS_ROLE_TO_ASSUME` secret in GitHub repo settings.

## Deployment

The pipeline deploys automatically via GitHub Actions when changes are pushed to `src/` or the workflow file. Manual deployment can be triggered by pushing to `main`.

# **Data Flow**:
Raw data > Ingestion > Cleaning > ...

## Project Structure

```
src/
├── ingestion/
│   └── scrape_jobs_lambda.py
├── cleaning/
│   ├── clean_jobs_lambda.py
│   ├── salary_parser.py
│   ├── skill_extractor.py
│   └── text_cleaning.py
└── utils/
    └── s3_io.py
```

## Contributing
Contributions are welcome!
