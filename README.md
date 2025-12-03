# Job Market Pipeline

A serverless data pipeline for processing job market data using AWS Lambda functions. The pipeline ingests raw job data, cleans and transforms it, and prepares it for analysis.

## Features

- **Ingestion Lambda**: Scrapes and ingests raw job data from SerpAPI.
- **Cleaning Lambda**: Processes and cleans the data, extracting skills, salaries, and other attributes.
- **Automated Deployment**: Deploys to AWS Lambda via GitHub Actions on pushes to `main` branch.
- **Frontend Showcase**: A static web showcase of the pipeline architecture and insights, automatically deployed to GitHub Pages.

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

### Lambda Functions
The pipeline deploys automatically via GitHub Actions when changes are pushed to `src/` or the workflow file. Manual deployment can be triggered by pushing to `main`.

### Frontend Showcase
The frontend is automatically deployed to GitHub Pages on every push to `main` that includes changes to the `frontend/` directory.

**Live Site**: [https://imrahnf.github.io/job-market-pipeline/](https://imrahnf.github.io/job-market-pipeline/)

**How it works**:
- The `.github/workflows/deploy-pages.yml` workflow is triggered on pushes to `main` branch
- Only the contents of the `frontend/` directory are deployed to GitHub Pages
- The site is a static HTML/CSS/JavaScript application with no build step required
- Deployment is fully automated via GitHub Actions with proper permissions

**Manual Deployment**:
You can also trigger a manual deployment from the Actions tab in GitHub using the "workflow_dispatch" trigger.

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
frontend/
├── index.html          # Main showcase page
├── styles.css          # Styling
├── scripts/
│   └── main.js         # Data loading and visualization
└── data/
    ├── clean.json      # Sample cleaned data
    └── raw.json        # Sample raw data
```

## Contributing
Contributions are welcome!
