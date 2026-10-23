# Databricks DevOps, MLOps & LLMOps Medallion Project

This project demonstrates a production-ready lifecycle for Databricks, spanning Data Engineering, Machine Learning, and Generative AI.

## 📂 Project Structure
- `notebooks/`: The logic layer.
    - `01_bronze_ingest.py`: Raw ingestion.
    - `02_silver_clean.py`: Data cleansing.
    - `03_gold_aggregate.py`: Business reports.
    - `04_ml_model_training.py`: ML Training + MLflow tracking.
    - `05_rag_agent.py`: RAG Agent (Text-to-SQL).
- `scripts/`: Infrastructure as Code (IaC).
    - `deploy_pipeline.py`: SDK script to deploy the full DAG.
- `.github/workflows/`: CI/CD automation.
- `mcp_config.json`: MCP Server definition for AI connectivity.

## 📐 Architecture

### 1. DataOps (Medallion)
Bronze $\rightarrow$ Silver $\rightarrow$ Gold. Ensures high-quality, curated data.

### 2. MLOps (Lifecycle)
Using **MLflow**, we implement:
- **Experiment Tracking**: Log metrics (RMSE) and hyperparameters.
- **Model Registry**: Versioning and promoting models to production.

### 3. LLMOps (RAG & MCP)
We implement a **RAG (Retrieval-Augmented Generation)** agent to allow users to "chat with their data."

- **The RAG Pattern**: 
  `User Question` $\rightarrow$ `LLM converts to SQL` $\rightarrow$ `Query Gold Table` $\rightarrow$ `LLM formats Answer`.
- **MCP (Model Context Protocol)**:
  We use an **MCP Server** definition (`mcp_config.json`) to standardize how an AI Model (like Claude or GPT) connects to the Databricks "Housing Agent" tool. This decouples the LLM from the data source.

## 🛠️ How to Deploy
1. **Secrets**: Add `DB_HOST` and `DB_TOKEN` to GitHub Secrets.
2. **Push**: Push code to `main` branch.
3. **Result**: GitHub Actions deploys the full pipeline (Data $\rightarrow$ ML $\rightarrow$ RAG) to your workspace.
