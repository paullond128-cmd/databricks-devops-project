# 03_Gold_Aggregate
# This notebook aggregates Silver data into a final report

print("🚀 Starting Gold Aggregation...")

# Read from Silver
df = spark.table("housing_silver")

# Aggregation: Average price per city
df_gold = df.groupBy("city").avg("price")

df_gold.write.format("delta").mode("overwrite").saveAsTable("housing_gold_report")
print("✅ Gold report 'housing_gold_report' updated.")
