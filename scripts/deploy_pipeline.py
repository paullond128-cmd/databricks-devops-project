import os
import sys
import base64
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.jobs import Task, NotebookTask, TaskDependency, Source, JobSettings
from databricks.sdk.service.workspace import ImportFormat, Language

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
    print(f"📤 Uploading notebooks to Databricks Workspace ({base_path})...")
    w.workspace.mkdirs(base_path)

    local_notebooks_dir = "notebooks"
    for filename in sorted(os.listdir(local_notebooks_dir)):
        if filename.endswith(".py"):
            local_path = os.path.join(local_notebooks_dir, filename)
            workspace_path = f"{base_path}/{filename.replace('.py', '')}"

            with open(local_path, "rb") as f:
                content_b64 = base64.b64encode(f.read()).decode("utf-8")
                w.workspace.import_(
                    path=workspace_path,
                    content=content_b64,
                    format=ImportFormat.SOURCE,
                    language=Language.PYTHON,
                    overwrite=True
                )
            print(f"  - Uploaded {filename} to {workspace_path}")

    # 2. Define Paths for the Job
    notebooks = {
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

    # 4. Deploy or Update Job
    job_name = "Housing_Medallion_Production_Pipeline"
    existing_jobs = list(w.jobs.list(name=job_name))
    if existing_jobs:
        job_id = existing_jobs[0].job_id
        w.jobs.reset(
            job_id=job_id,
            new_settings=JobSettings(
                name=job_name,
                tasks=tasks,
                max_concurrent_runs=1,
            )
        )
        print(f"🔄 Existing Job updated! Job ID: {job_id}")
    else:
        job = w.jobs.create(
            name=job_name,
            tasks=tasks,
            max_concurrent_runs=1,
        )
        job_id = job.job_id
        print(f"🚀 Job Deployed! Job ID: {job_id}")

    # 5. Trigger the Run
    print("🏃 Triggering a smoke test run...")
    run = w.jobs.run_now(job_id=job_id)
    print(f"✅ Run started! Run ID: {run.run_id}")
    print(f"📈 View your run here: {host}/#job/{job_id}/run/{run.run_id}")

if __name__ == "__main__":
    run_deployment()