# Databricks notebook source
from datetime import datetime, timedelta
from pyspark.sql.functions import explode, col, from_unixtime, current_timestamp, concat, lit, count, avg, to_date, month, year, trim, split
from pyspark.sql.functions import max as max_
import requests
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType


# COMMAND ----------

def calculate_date(date_val):
    if not date_val:
        yesterday_date = datetime.today() - timedelta(days=1)
        date_val = yesterday_date.strftime("%Y-%m-%d")
    return date_val

