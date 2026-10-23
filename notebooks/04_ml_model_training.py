# 04_ML_Model_Training
# This notebook trains a basic ML model and tracks it using MLflow

import mlflow
import mlflow.spark
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.evaluation import RegressionEvaluator

# 1. Initialize MLflow Experiment
try:
    current_user = spark.sql("SELECT current_user()").first()[0]
    mlflow.set_experiment(f"/Users/{current_user}/Housing_Project/Price_Prediction_Model")
except Exception:
    mlflow.set_experiment("Price_Prediction_Model")

print("🚀 Starting ML Training with MLflow...")

# 2. Load Silver Data
df = spark.table("housing_silver")

# 3. Feature Engineering
# Convert city (string) to index (numeric)
indexer = StringIndexer(inputCol="city", outputCol="city_index")
df_indexed = indexer.fit(df).transform(df)

# Assemble features into a vector
assembler = VectorAssembler(inputCols=["city_index"], outputCol="features")
final_data = assembler.transform(df_indexed).select("features", "price")

# Split data
train_df, test_df = final_data.randomSplit([0.8, 0.2], seed=42)

# 4. Model Training with MLflow Tracking
with mlflow.start_run(run_name="Housing_Linear_Regression") as run:
    # Hyperparameters
    lr_param = 0.1
    mlflow.log_param("learning_rate", lr_param)

    # Train Model
    lr = LinearRegression(featuresCol="features", labelCol="price")
    model = lr.fit(train_df)

    # Predict and Evaluate
    predictions = model.transform(test_df)
    evaluator = RegressionEvaluator(labelCol="price", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)

    # Log Metric to MLflow
    mlflow.log_metric("rmse", rmse)
    print(f"✅ Model trained. RMSE: {rmse}")

    # Log Model to MLflow Registry
    try:
        # On Databricks serverless compute, SparkML requires a UC volume tmpdir
        dfs_tmp = "/Volumes/workspace/default/housing_landing"
        mlflow.spark.log_model(model, "model", dfs_tmpdir=dfs_tmp, registered_model_name="housing_price_model")
        print("🚀 Model logged to MLflow Model Registry as 'housing_price_model'")
    except Exception as e:
        print(f"⚠️ MLflow model registry logging failed: {e}")
        try:
            mlflow.spark.log_model(model, "model", dfs_tmpdir="/Volumes/workspace/default/housing_landing")
            print("🚀 Model logged as MLflow artifact.")
        except Exception as e2:
            print(f"⚠️ Fallback model logging note: {e2}")
