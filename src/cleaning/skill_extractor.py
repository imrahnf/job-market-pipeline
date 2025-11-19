import re
from typing import List

# ai generated list of keywords
SKILL_KEYWORDS = {

    # --- Programming Languages ---
    "Python": ["python", "py"],
    "SQL": ["sql", "structured query language"],
    "R": ["r", "r programming", "tidyverse"],
    "Java": ["java", "jvm"],
    "C++": ["c++", "cpp"],
    "C": ["c language"],
    "C#": ["c#", "csharp", "dotnet c#"],
    "JavaScript": ["javascript", "js", "nodejs", "node.js"],
    "TypeScript": ["typescript", "ts"],
    "Go": ["go", "golang"],
    "Scala": ["scala"],
    "Ruby": ["ruby", "ruby on rails", "rails"],
    "PHP": ["php"],
    "Swift": ["swift"],
    "Kotlin": ["kotlin"],
    "MATLAB": ["matlab"],
    "SAS": ["sas", "statistical analysis system"],
    "Julia": ["julia programming"],
    "Shell Scripting": ["bash", "shell", "shell script", "sh", "zsh"],
    "Perl": ["perl"],

    # --- Cloud & Infrastructure ---
    "AWS": ["aws", "amazon web services", "amazon cloud"],
    "Azure": ["azure", "microsoft azure"],
    "GCP": ["gcp", "google cloud", "google cloud platform"],
    "Terraform": ["terraform", "iac", "infrastructure as code"],
    "CloudFormation": ["cloudformation", "aws cloudformation"],
    "Ansible": ["ansible"],
    "Puppet": ["puppet"],
    "Chef": ["chef"],
    "OpenStack": ["openstack"],

    # --- DevOps, Containers & CI/CD ---
    "Docker": ["docker", "containerization", "containers"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Jenkins": ["jenkins"],
    "GitLab CI": ["gitlab ci", "gitlab pipelines"],
    "GitHub Actions": ["github actions"],
    "CircleCI": ["circleci"],
    "ArgoCD": ["argocd", "argo"],
    "Istio": ["istio", "service mesh"],

    # --- Data Engineering & Big Data ---
    "Spark": ["spark", "apache spark", "pyspark", "spark sql"],
    "Hadoop": ["hadoop", "hdfs", "yarn"],
    "Hive": ["hive", "apache hive"],
    "Pig": ["pig", "apache pig"],
    "Kafka": ["kafka", "apache kafka"],
    "Flink": ["flink", "apache flink"],
    "Airflow": ["airflow", "apache airflow", "dag"],
    "Luigi": ["luigi"],
    "Prefect": ["prefect"],
    "Databricks": ["databricks", "dbx", "pyspark databricks"],
    "Snowflake": ["snowflake", "snowflake sql"],
    "Redshift": ["redshift", "amazon redshift"],
    "BigQuery": ["bigquery", "google bigquery"],
    "Synapse": ["synapse", "azure synapse"],
    "ETL": ["etl", "data pipelines", "extract transform load"],
    "ELT": ["elt", "extract load transform"],

    # --- Databases ---
    "PostgreSQL": ["postgres", "postgresql"],
    "MySQL": ["mysql"],
    "MSSQL": ["mssql", "sql server", "microsoft sql server"],
    "OracleDB": ["oracle", "oracle database"],
    
    # NoSQL
    "NoSQL": ["nosql"],
    "MongoDB": ["mongodb"],
    "DynamoDB": ["dynamodb"],
    "Cassandra": ["cassandra"],
    "Redis": ["redis", "redis db"],
    "Firebase": ["firebase"],
    "Elasticsearch": ["elasticsearch", "elastic search", "elastic"],

    # --- Python Libraries for Data & ML ---
    "Pandas": ["pandas"],
    "NumPy": ["numpy"],
    "SciPy": ["scipy"],
    "Matplotlib": ["matplotlib"],
    "Seaborn": ["seaborn"],
    "Scikit-learn": ["scikit-learn", "sklearn"],
    "TensorFlow": ["tensorflow", "tf"],
    "Keras": ["keras"],
    "PyTorch": ["pytorch", "torch"],
    "XGBoost": ["xgboost"],
    "LightGBM": ["lightgbm", "lgbm"],
    "CatBoost": ["catboost"],

    # --- Machine Learning & Data Science ---
    "Machine Learning": ["machine learning", "ml"],
    "Deep Learning": ["deep learning", "neural networks", "dl"],
    "AI": ["ai", "artificial intelligence"],
    "Data Science": ["data science", "data scientist"],
    "Computer Vision": ["computer vision", "cv"],
    "NLP": ["nlp", "natural language processing", "llm", "large language models"],
    "MLOps": ["mlops", "machine learning ops"],
    "Model Deployment": ["model deployment", "model serving"],
    "Model Monitoring": ["model monitoring"],

    # --- BI / Analytics Tools ---
    "Tableau": ["tableau"],
    "Power BI": ["powerbi", "power bi"],
    "Looker": ["looker"],
    "Qlik": ["qlik", "qlikview", "qliksense"],
    "Excel": ["excel", "microsoft excel", "vlookup", "pivot tables"],
    "Google Analytics": ["google analytics", "ga4"],

    # --- Version Control & Collaboration ---
    "Git": ["git", "github", "gitlab", "bitbucket"],
    "JIRA": ["jira"],
    "Confluence": ["confluence"],
    "Agile": ["agile", "scrum"],

    # --- Operating Systems ---
    "Linux": ["linux", "ubuntu", "debian", "red hat", "centos"],
    "Windows": ["windows", "windows server"],
    "MacOS": ["macos"],

    # --- APIs & Backend ---
    "REST": ["rest", "rest api"],
    "GraphQL": ["graphql"],
    "FastAPI": ["fastapi"],
    "Flask": ["flask"],
    "Django": ["django"],
    "Spring Boot": ["springboot", "spring boot"],
    "Express.js": ["express", "expressjs"],

    # --- Data Modeling & Architecture ---
    "Data Modeling": ["data modeling", "dimensional modeling", "star schema"],
    "Data Warehousing": ["data warehouse", "dwh", "data warehousing"],
    "Microservices": ["microservices", "microservice architecture"],
    "Streaming": ["streaming", "stream processing", "real-time data"],

}

def extract_skills(text: str) -> List[str]:
    if not text:
        return []
    
    text = text.lower()
    found = []

    for skill, patterns in SKILL_KEYWORDS.items():
        for pattern in patterns:
            if re.search(r"\b" + re.escape(pattern) + r"\b", text):
                found.append(skill)

    return list(sorted(set(found)))
