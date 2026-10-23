# Databricks DevOps & MLOps Medallion Project

This project demonstrates a production-ready DevOps and MLOps lifecycle for Databricks using the Medallion Architecture.

## 📂 Project Structure
- `notebooks/`: Contains the data and ML pipeline logic.
    - `01_bronze_ingest.py`: Raw ingestion.
    - `02_silver_clean.py`: Data cleansing.
    - `03_gold_aggregate.py`: Business reports.
    - `04_ml_model_training.py`: ML Model training and MLflow tracking.
- `scripts/`: Contains the Python SDK script used to deploy the workflow as code.
- `.github/workflows/`: contains the CI/CD automation for GitHub Actions.

## 🛠️ How to use this project

### 1. Setup Databricks Secrets
In your GitHub Repository, go to **Settings > Secrets and variables > Actions** and add:
- `DB_HOST`: Your Databricks Workspace URL.
- `DB_TOKEN`: Your Personal Access Token (PAT).

### 2. Deploy
1. Push your code to the `main` branch.
2. GitHub Actions will automatically trigger the `deploy.yml` workflow.
3. The `deploy_pipeline.py` script will create the Medallion Workflow in your Databricks workspace.

## 📐 Architecture

### Medallion Data Pipeline
- **Bronze**: Raw ingestion.
- **Silver**: Data cleaning and filtering.
- **Gold**: Business aggregations.

### MLOps Pipeline
We use **MLflow** to implement the ML lifecycle:
1. **Experiment Tracking**: Every time `04_ml_model_training.py` runs, it logs the `RMSE` metric and hyperparameters to MLflow.
2. **Model Registry**: The best model is saved to the **MLflow Model Registry** as `housing_price_model`.
3. **Reproducibility**: Because the training is part of the GitHub-deployed workflow, we can reproduce the exact model version for any date.
