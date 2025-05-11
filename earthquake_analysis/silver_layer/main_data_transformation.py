# Databricks notebook source
display(dbutils.fs.ls("dbfs:/mnt/sj-container2/bronze_layer/daily_data/2025-05-10/"))

# COMMAND ----------

# MAGIC %run ../utils

# COMMAND ----------

dbutils.widgets.text("date_val","")
date_val = dbutils.widgets.get("date_val")

# COMMAND ----------


date_val= calculate_date(date_val)
print(date_val)


# COMMAND ----------

input_path= f"/mnt/sj-container2/bronze_layer/daily_data/{date_val}/daily_data{date_val}.json"
df = spark.read.json(input_path)
df.printSchema()


# COMMAND ----------

result_df = df.select('metadata.count')
initial_record_count = result_df.collect()[0]['count']
display(initial_record_count)

# COMMAND ----------



df = df.withColumn("feature", explode("features"))
df = df.select("feature.properties")
df.display()  


# COMMAND ----------

col_lst =["alert", "cdi", "code", "detail", "dmin", "felt", "gap", "ids", "mag", "magType", "mmi", "net", "nst", "place", "rms", "sig", "sources", "status", "time", "title", "tsunami", "type", "types", "tz", "updated", "url"
]

for col_name in col_lst:
    df = df.withColumn(col_name, col(f'properties.{col_name}'))
df = df.drop('properties')


# COMMAND ----------

df.display()
df.printSchema()
df.count()

# COMMAND ----------

final_count = df.count()

if initial_record_count != final_count:
    raise ValueError(f"Initial count: {initial_record_count} does not match with final count: {final_count}")


# COMMAND ----------

df = df.withColumn('time_timestamp', from_unixtime(col('time')/1000)).withColumn('updated_timestamp', from_unixtime(col('updated')/1000)).withColumn('injest_ts',current_timestamp())

# COMMAND ----------

df.write.mode('overwrite').format('parquet').save(f'/mnt/sj-container2/silver_layer/{date_val}/earthquake_data')

# COMMAND ----------

display(dbutils.fs.ls(f"/mnt/sj-container2/silver_layer/{date_val}/earthquake_data"))
