# Databricks notebook source
dbutils.fs.ls("/mnt/silver/Sales/")

# COMMAND ----------

dbutils.fs.ls("/mnt/gold")

# COMMAND ----------

table_name = []

for i in dbutils.fs.ls("/mnt/silver/Sales/"):
    table_name.append(i.name.split('/')[0])

# COMMAND ----------

table_name

# COMMAND ----------

# MAGIC %md
# MAGIC ##Changing Column Names to appropriate format

# COMMAND ----------

for name in table_name:
  path = '/mnt/silver/Sales/' + name
  print(path)
  df = spark.read.format('delta').load(path)

  #to store list of column names
  column_names = df.columns

  for old_col_name in column_names:
    #To convert column name format from ColumnName to Column_Nam
    new_col_name = "".join(["_" + char if char.isupper() and not old_col_name[i-1].isupper() else char for i, char in enumerate(old_col_name)]).lstrip("_")

    #To change column name usin withColumnRenamed and regex_replace
    df = df.withColumnRenamed(old_col_name, new_col_name)

  output_path = '/mnt/gold/Sales/' +name +'/'
  df.write.format('delta').mode("overwrite").save(output_path)

# COMMAND ----------

display(df)
