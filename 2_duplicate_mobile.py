from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit
from functools import reduce

spark = SparkSession.builder.appName("duplicate_header")\
    .config("spark.hadoop.fs.s3a.endpoint","http://localhost:9005") \
    .config("spark.hadoop.fs.s3a.access.key","minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key","minioadmin123") \
    .config("spark.hadoop.fs.s3a.impl","org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access","true") \
    .getOrCreate()


df = spark.read.format("csv") \
    .option("header",True)\
    .option("inferSchema",False)\
    .load("s3a://iceberg/warehouse/raw_zone/csv_cases/duplicate_headers.csv")

df.show(truncate=False)

cols = df.columns
condition = ~reduce(lambda acc, c: acc & (col(c).cast("string") == c), cols, lit(True))
df_clean = df.filter(condition)

df_clean.show(truncate=False)