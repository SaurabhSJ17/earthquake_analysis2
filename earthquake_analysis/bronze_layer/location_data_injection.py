# Databricks notebook source
# MAGIC %run ../utils

# COMMAND ----------

dbutils.widgets.text("date_val","")
date_val = dbutils.widgets.get("date_val")


# COMMAND ----------

date_val= calculate_date(date_val)
print(date_val)

# COMMAND ----------

input_location = f"/mnt/sj-container2/silver_layer/{date_val}/earthquake_data"
df = spark.read.parquet(input_location)

df.display()


# COMMAND ----------

print(df.columns)

# COMMAND ----------

df = df.select('net','code','updated')

df = df.withColumn("location_url", concat(lit('https://earthquake.usgs.gov/realtime/product/nearby-cities/'),col('net'),col('code'),lit('/'),col("net"),lit('/'),col('updated'),lit('/nearby-cities.json'))).withColumn("row_id",concat(col("net"),col("code")))



# COMMAND ----------

location_url_id_list = [
    {'location_url': x["location_url"], 'row_id': x["row_id"]}
    for x in df.select("location_url", "row_id").collect()
]


print(location_url_id_list)

# COMMAND ----------

result_lst = []
cnt = 0

for x in location_url_id_list:
    location_url= x['location_url']
    row_id = x['row_id']
    request_res = requests.get(location_url)
    if request_res.status_code ==200:
        if cnt<=10:
            for val in request_res.json():
                val['row_id'] = row_id
                result_lst.append(val)
            else:
                break
        cnt +=1

# COMMAND ----------

print(result_lst)

# COMMAND ----------

location_schema = StructType([
    StructField("distance", IntegerType()),
    StructField("direction", StringType()),
    StructField("name", StringType()),
    StructField("longitude", FloatType()),
    StructField("latitude", FloatType()),
    StructField("population", IntegerType()),
    StructField("row_id", StringType())
])

df = spark.createDataFrame(result_lst, location_schema)
# df.display()

df.write.mode("overwrite").format("parquet").save(f"/mnt/sj-container2/bronze_layer/daily_data/{date_val}/earthquake_nearby_cities")

# COMMAND ----------

df.display()
