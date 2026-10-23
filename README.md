# Databricks DevOps Medallion Project

This project demonstrates a production-ready DevOps lifecycle for Databricks using the Medallion Architecture.

## 📂 Project Structure
- `notebooks/`: Contains the data pipeline logic (Bronze, Silver, Gold).
- `scripts/`: Contains the Python SDK script used to deploy the workflow as code.
- `.github/workflows/`: contains the CI/CD automation for GitHub Actions.

## 🛠️ How to use this project

### 1. Setup Databricks Secrets
In your GitHub Repository, go to **Settings > Secrets and variables > Actions** and add:
- `DB_HOST`: Your Databricks Workspace URL (e.g., `https://adb-xxxx.azuredatabricks.net`)
- `DB_TOKEN`: Your Personal Access Token (PAT).

### 2. Deploy
1. Push your code to the `main` branch.
2. GitHub Actions will automatically trigger the `deploy.yml` workflow.
3. The `deploy_pipeline.py` script will create the Medallion Workflow in your Databricks workspace.

## 📐 Architecture
- **Bronze**: Raw ingestion.
- **Silver**: Data cleaning and filtering.
- **Gold**: Business aggregations and reports.
