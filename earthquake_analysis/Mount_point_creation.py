# Databricks notebook source
configs = {
    "fs.azure.account.auth.type": "SAS",
    "fs.azure.sas.token.provider.type": "org.apache.hadoop.fs.azurebfs.sas.FixedSASTokenProvider",
    "fs.azure.sas.fixed.token": "sp=racwdlmeop&st=2025-05-11T05:32:21Z&se=2025-05-11T13:32:21Z&sv=2024-11-04&sr=c&sig=URE2zUv9S9Kybf9LvOTNIwFtL8Sl%2BeQ5%2FV1gaklrWXY%3D"
}

# Mount the ADLS container to Databricks file system (DBFS)
dbutils.fs.mount(
    source="abfss://sj-container2@storage5845.dfs.core.windows.net/",
    mount_point="/mnt/sj-container2",
    extra_configs=configs
)

# COMMAND ----------

dbutils.fs.ls("/mnt/sj-container2/bronze_layer/")
