# 01_Bronze_Ingestion
# This notebook ingests raw data from an API and saves it as a Delta Table

print("🚀 Starting Bronze Ingestion...")

# In a real scenario, you'd use requests.get() here
# df = spark.read.json("https://api.housing.com/raw_data")
# For this sample, we create dummy data
data = [("1", "NY", 500000), ("2", "LA", 700000), ("3", "CHI", 300000)]
columns = ["id", "city", "price"]
df = spark.createDataFrame(data, columns)

df.write.format("delta").mode("append").saveAsTable("housing_bronze")
print("✅ Bronze table 'housing_bronze' updated.")
