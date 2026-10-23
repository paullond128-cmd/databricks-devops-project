import os
import sys
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, TaskDependency, Source

def run_deployment():
    host = os.getenv("DATABRICKS_HOST")
    token = os.getenv("DATABRICKS_TOKEN")

    if not host or not token:
        print("❌ Error: Missing environment variables.")
        sys.exit(1)

    w = WorkspaceClient(host=host, token=token)
    user = w.current_user.me()
    
    base_path = f"/Users/{user.user_name}/Housing_Project"
    
    # 1. UPLOAD NOTEBOOKS TO WORKSPACE
    # This is the missing piece! We upload local files to the Databricks Workspace.
    print("📤 Uploading notebooks to Databricks Workspace...")
    local_notebooks_dir = "notebooks"
    
    # We loop through the local notebooks folder and upload each file
    for filename in os.listdir(local_notebooks_dir):
        if filename.endswith(".py"):
            local_path = os.path.join(local_notebooks_dir, filename)
            # The workspace path removes the '.py' extension as Databricks treats them as notebooks
            workspace_path = f"{base_path}/{filename.replace('.py', '')}"
            
            with open(local_path, "r") as f:
                content = f.read()
                w.workspace.import_content(path=workspace_path, content=content, format="SOURCE")
            print(f"  - Uploaded {filename} to {workspace_path}")

    # 2. Define Paths for the Job
    notebook_paths = {
        "bronze": f"{base_path}/01_bronze_ingest",
        "silver": f"{base_path}/02_silver_clean",
        "gold": f"{base_path}/03_gold_aggregate",
        "ml": f"{base_path}/04_ml_model_training",
        "rag": f"{base_path}/05_rag_agent",
    }

    # 3. Define the DAG
    tasks = [
        Task(task_key="bronze", notebook_task=NotebookTask(notebook_path=notebooks["bronze"], source=Source.WORKSPACE)),
        Task(task_key="silver", depends_on=[TaskDependency(task_key="bronze")], notebook_task=NotebookTask(notebook_path=notebooks["silver"], source=Source.WORKSPACE)),
        Task(task_key="gold", depends_on=[TaskDependency(task_key="silver")], notebook_task=NotebookTask(notebook_path=notebooks["gold"], source=Source.WORKSPACE)),
        Task(task_key="ml_training", depends_on=[TaskDependency(task_key="silver")], notebook_task=NotebookTask(notebook_path=notebooks["ml"], source=Source.WORKSPACE)),
        Task(task_key="rag_agent", depends_on=[TaskDependency(task_key="gold")], notebook_task=NotebookTask(notebook_path=notebooks["rag"], source=Source.WORKSPACE)),
    ]

    # 4. Deploy and Trigger
    job = w.jobs.create(
        name="Housing_Medallion_Production_Pipeline",
        tasks=tasks,
        max_concurrent_runs=1,
    )
    print(f"🚀 Job Deployed! Job ID: {job.job_id}")

    print("🏃 Triggering a smoke test run...")
    run = w.jobs.run_now(job_id=job.job_id)
    print(f"✅ Run started! Run ID: {run.run_id}")
    print(f"📈 View your run here: {host}/#job/{job.job_id}/run/{run.run_id}")

if __name__ == "__main__":
    run_deployment()