# 03_Gold_Aggregate
# This notebook aggregates Silver data into a final report

print("🚀 Starting Gold Aggregation...")

# Read from Silver
df = spark.table("housing_silver")

# Aggregation: Average price per city
from pyspark.sql.functions import avg
df_gold = df.groupBy("city").agg(avg("price").alias("avg_price"))

df_gold.write.format("delta").mode("overwrite").saveAsTable("housing_gold_report")
print("✅ Gold report 'housing_gold_report' updated.")
