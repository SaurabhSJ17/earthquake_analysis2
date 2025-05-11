# Databricks notebook source
# MAGIC %run ../utils

# COMMAND ----------

dbutils.widgets.text("date_val","")
date_val = dbutils.widgets.get("date_val")


# COMMAND ----------

date_val= calculate_date(date_val)
print(date_val)

# COMMAND ----------

input_location = f"/mnt/sj-container2/silver_layer/{date_val}/earthquake_monthly_data"
df = spark.read.parquet(input_location)
df.display()

# COMMAND ----------

region_summary = df.groupBy("place").agg(
    count("*").alias("total_earthquakes"),
    avg("mag").alias("avg_magnitude"),
    max_("mag").alias("max_magnitude")
).orderBy(col("total_earthquakes").desc())
# print(region_summary.show())

region_summary.write.mode("overwrite").format("parquet").save(f"/mnt/sj-container2/gold_layer/{date_val}/se1_region_summary")

# COMMAND ----------

daily_counts = df.withColumn("event_date", to_date(col("time_timestamp"))).groupBy("event_date").agg(
    count("*").alias("daily_earthquake_count")
).orderBy(col("event_date").desc())
print(daily_counts.show())

daily_counts.write.mode("overwrite").format("parquet").save(f"/mnt/sj-container2/gold_layer/{date_val}/se2_daily_counts")

# COMMAND ----------

last_7th_date = (datetime.utcnow() - timedelta(days=7)).date()

high_mag_df = df.withColumn("event_date", to_date(col("time_timestamp"))).filter(
    (col("mag") > 5.0) & (col("event_date") >= lit(last_7th_date))
)

print(high_mag_df.show())

daily_counts.write.mode("overwrite").format("parquet").save(f"/mnt/sj-container2/gold_layer/{date_val}/se3_daily_counts")

# COMMAND ----------

df = df.withColumn("event_date", to_date(col("time_timestamp"))) \
       .withColumn("month", month(col("event_date"))) \
       .withColumn("year", year(col("event_date"))) \
       .withColumn("region", (col("place")))

features_df = df.groupBy("region", "year", "month").agg(
    count("*").alias("monthly_quake_count"),
    avg("mag").alias("avg_monthly_magnitude")
)

print(features_df.show())

features_df.write.mode("overwrite").format("parquet").save(f"/mnt/sj-container2/gold_layer/{date_val}/se4_features_df")
