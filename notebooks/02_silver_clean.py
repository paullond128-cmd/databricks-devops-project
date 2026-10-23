# 02_Silver_Clean
# This notebook cleans and transforms data from Bronze to Silver

print("🚀 Starting Silver Transformation...")

# Read from Bronze
df = spark.table("housing_bronze")

# Cleaning: Filter out rows with missing prices
from pyspark.sql.functions import col
df_cleaned = df.filter(col("price").isNotNull())

df_cleaned.write.format("delta").mode("overwrite").saveAsTable("housing_silver")
print("✅ Silver table 'housing_silver' updated.")
