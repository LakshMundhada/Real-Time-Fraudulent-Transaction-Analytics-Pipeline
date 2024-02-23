from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col,lit, when
from pyspark.sql.types import StructType, StringType , StructField , DecimalType 
from pyspark.sql import functions as F
from pyspark.sql.window import Window


# Create a SparkSession
spark = SparkSession.builder \
    .appName("Structured_Redpanda_WordCount") \
    .config("spark.jars", "s3://requiredfiles2323/spark-sql-kafka-0-10_2.12-3.2.1.jar,s3://requiredfiles2323/kafka-clients-2.1.1.jar") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")




class DistanceCalculator:
    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians using Spark SQL functions
        lat1_rad = F.radians(lat1)
        lon1_rad = F.radians(lon1)
        lat2_rad = F.radians(lat2)
        lon2_rad = F.radians(lon2)

        # Difference in latitude and longitude
        d_lat = lat2_rad - lat1_rad
        d_lon = lon2_rad - lon1_rad

        # Haversine formula using Spark SQL functions
        a = F.sin(d_lat / 2)*2 + F.cos(lat1_rad) * F.cos(lat2_rad) * F.sin(d_lon / 2)*2
        c = 2 * F.atan2(F.sqrt(a), F.sqrt(1 - a))

        # Distance in kilometers
        distance = R * c
        return distance






histdf=spark.read.csv("s3://credit-project-data-80-percent/part-00000-5c9dab29-f21f-4f32-821a-4c9d76f329e8-c000.csv",header=True)
histdf.cache()
# Define the schema for your JSON data
schema = StructType([
    StructField("_c0", StringType(), True),
    StructField("ssn", StringType(), True),
    StructField("cc_num", StringType(), True),
    StructField("first", StringType(), True),
    StructField("last", StringType(), True),
    StructField("gender", StringType(), True),
    StructField("street", StringType(), True),
    StructField("city", StringType(), True),
    StructField("state", StringType(), True),
    StructField("zip", DecimalType(5, 0), True),
    StructField("lat", DecimalType(9, 6), True),
    StructField("long", DecimalType(9, 6), True),
    StructField("city_pop", StringType(), True),
    StructField("job", StringType(), True),
    StructField("dob", StringType(), True),
    StructField("acct_num", StringType(), True),
    StructField("profile", StringType(), True),
    StructField("trans_num", StringType(), True),
    StructField("trans_date", StringType(), True),
    StructField("trans_time", StringType(), True),
    StructField("unix_time", StringType(), True),
    StructField("category", StringType(), True),
    StructField("amt", DecimalType(9, 2), True),
    StructField("is_fraud", DecimalType(9, 0), True),
    StructField("merchant", StringType(), True),
    StructField("merch_lat", DecimalType(9, 6), True),
    StructField("merch_long", DecimalType(9, 6), True)
])

# Read streaming data from Kafka topic

df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "pkc-p11xm.us-east-1.aws.confluent.cloud:9092") \
    .option("subscribe", "new") \
    .option("kafka.security.protocol", "SASL_SSL") \
    .option("kafka.sasl.mechanism", "PLAIN") \
    .option("kafka.sasl.jaas.config", 
            "org.apache.kafka.common.security.plain.PlainLoginModule required " + \
            "username='NQUVTTMSN2ZERMOC' " + \
            "password='H5D3zLCvpITwlG+erBnSp1uVtQkjYeZpFqoQ38XdO0lHymht4ny68cCZ7KT++S36';") \
    .load()


# Assuming your Kafka messages have key and value columns (you can adjust as needed)
df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")

# Apply the specified schema to the JSON data
df = df.select(from_json(col("value"), schema).alias("data")).select("data.*")




jdbc_url = "jdbc:mysql://grouptwo.cq7tmru9zell.us-east-1.rds.amazonaws.com/customer"
table_name = "customer_details"
connection_properties = {
    "user": "admin",
    "password": "Group_two",
    "driver": "com.mysql.jdbc.Driver" 
}

# Read data from the RDS table into a DataFrame
rds_df = spark.read.jdbc(jdbc_url, table=table_name, properties=connection_properties)





window_spec = Window.partitionBy("cc_num").orderBy(F.col("unix_time").desc())

# Filter the historical transactions DataFrame to get the last 10 transactions for each cc_num
last_10_transactions = histdf \
    .withColumn("row_num", F.row_number().over(window_spec)) \
    .filter(F.col("row_num") <= 10) \
    .drop("row_num")

# Calculate the average transaction amount for the last 10 transactions of each cc_num
average_transaction_amount = last_10_transactions \
    .groupBy("cc_num") \
    .agg(F.avg("amt").alias("avg_transaction_amt"))

# Filter the streaming DataFrame to include only the cc_num present in histdf
filtered_df = df.join(average_transaction_amount, "cc_num", "inner")

# Add a status column based on the condition
result = filtered_df.withColumn("distance",DistanceCalculator.calculate_distance(col("lat"), col("long"), col("merch_lat"), col("merch_long"))) \
                   .withColumn("status",F.when((F.col("distance") > 1500) &(F.col("amt") > F.col("avg_transaction_amt") + 500), "fraud").otherwise("genuine"))

def write_to_jdbc_micro_batch(df, epoch_id):
   

    # Check if there are any unique records before writing
    if not df.isEmpty():
        # Write unique records to JDBC table
        df.select("ssn", "cc_num", "first", "last", "gender", "city", "state", "dob", "acct_num", "is_fraud") \
                  .write.jdbc(jdbc_url, table=table_name, mode="append", properties=connection_properties)

        # Append the unique cc_num values to rds_df
        global rds_df
        rds_df = rds_df.union(df.select("ssn", "cc_num", "first", "last", "gender", "city", "state", "dob", "acct_num", "is_fraud"))


# Write the streaming DataFrame to JDBC using foreachBatch
query1 = df.select("ssn", "cc_num", "first", "last", "gender", "city", "state", "dob", "acct_num", "is_fraud").writeStream.foreachBatch(write_to_jdbc_micro_batch).start()


histdf=histdf.union(df)



#histdf=histdf.union(df)
#histdf.write.csv("s3://fraud-detection-project-data/buday/", mode="append", header=True)



query = result.writeStream \
    .outputMode("append") \
    .foreachBatch(lambda df, epoch_id: (df.drop("first", "last", "job", "profile").write.mode("append").format("parquet").save("s3://athenabucket-231/final.parquet/"))) \
    .start()


# Wait for the query to terminate
query1.awaitTermination()
query.awaitTermination()