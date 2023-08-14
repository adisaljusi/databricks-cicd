# Databricks notebook source
dbutils.widgets.text("catalog", "default")
dbutils.widgets.text("schema", "public")
dbutils.widgets.text(
    "base_path", "abfss://container@storageaccount.dfs.core.windows.net/"
)
dbutils.widgets.text("table", "table")
dbutils.widgets.text("file_format", "parquet")

# COMMAND ----------

catalog = dbutils.widgets.get("catalog")
schema = dbutils.widgets.get("schema")
base_path = dbutils.widgets.get("base_path")
table = dbutils.widgets.get("table")
file_format = dbutils.widgets.get("file_format")

# COMMAND ----------

folder_suffix = "*/*/*"
file_path = f"{base_path}/{table}/{folder_suffix}"
checkpoint_path = f"{base_path}/{table}/_checkpoint/"

# COMMAND ----------

sql(f"USE CATALOG `{catalog}`;")
sql(f"CREATE SCHEMA IF NOT EXISTS {schema};")
sql(f"USE SCHEMA {schema};")

# COMMAND ----------

df_raw = (
    spark.readStream.format("cloudFiles")
    .option("cloudFiles.format", file_format)
    .option("cloudFiles.schemaLocation", checkpoint_path)
    .load(file_path)
    .writeStream.option("checkpointLocation", checkpoint_path)
    .trigger(availableNow=True)
    .toTable(f"`{catalog}`.{schema}.{table}")
)