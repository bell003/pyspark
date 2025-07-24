from pyspark.sql import SparkSession


spark = SparkSession.builder \
    .appName("CSV Dirty Data Practice") \
    .config("spark.hadoop.fs.s3a.endpoint", "http://localhost:9005") \
    .config("spark.hadoop.fs.s3a.access.key", "minioadmin") \
    .config("spark.hadoop.fs.s3a.secret.key", "minioadmin123")\
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .getOrCreate()

df = spark.read.format("csv") \
    .option("header",True)\
    .option("inferSchema",True)\
    .option("delimiter","|")\
    .load("s3a://iceberg/warehouse/raw_zone/csv_cases/pipe_delimiter.csv")


df.show()

df.select("name").show()

print(df.columns)