from pyspark.sql.functions import *
from pyspark.sql.types import FloatType, StringType, TimestampType, IntegerType, DoubleType, StructField, StructType
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os, sys


if __name__ == "__main__":

    appName="StockholmApp"
    kafka_url = os.getenv('KAFKA_URL')
    conf = SparkConf()

    spark = SparkSession.builder.config(conf=conf).appName(appName).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    emission_topic = "stockholm-emission"
    fcd_topic = "stockholm-fcd"
    emission2_topic = "stockholm-emission2"
    fcd2_topic = "stockholm-fcd2"

    # Citanje podataka sa originalnog Kafka topic-a
    emission_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("subscribe", emission_topic) \
        .load()
    
    emission_schema = StructType([
        StructField("timestep_time", FloatType()),
        StructField("vehicle_CO", FloatType()),
        StructField("vehicle_CO2", FloatType()),
        StructField("vehicle_HC", FloatType()),
        StructField("vehicle_NOx", FloatType()),
        StructField("vehicle_PMx", FloatType()),
        StructField("vehicle_angle", FloatType()),
        StructField("vehicle_eclass", StringType()),
        StructField("vehicle_electricity", FloatType()),
        StructField("vehicle_id", IntegerType()),
        StructField("vehicle_lane", StringType()),
        StructField("vehicle_fuel", FloatType()),
        StructField("vehicle_noise", FloatType()),
        StructField("vehicle_pos", FloatType()),
        StructField("vehicle_route", StringType()),
        StructField("vehicle_speed", FloatType()),
        StructField("vehicle_type", StringType()),
        StructField("vehicle_waiting", FloatType()),
        StructField("vehicle_x", FloatType()),
        StructField("vehicle_y", FloatType())
    ])

    emission_df_parsed = emission_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), emission_schema).alias("data")) \
        .select("data.*") \
        .withColumn("timestep_time", to_timestamp(col("timestep_time")))

    window_duration = os.getenv('WINDOW_DURATION')
    
    pollution_data = emission_df_parsed.groupBy(window("timestep_time", window_duration).alias("date"), col("vehicle_lane").alias("laneId")) \
    .agg(
        avg("vehicle_CO").alias("laneCO"),
        avg("vehicle_CO2").alias("laneCO2"),
        avg("vehicle_HC").alias("laneHC"),
        avg("vehicle_NOx").alias("laneNOx"),
        avg("vehicle_PMx").alias("lanePMx"),
        avg("vehicle_noise").alias("laneNoise")
    )

    # query_pollution = pollution_data.writeStream \
    #     .outputMode("complete") \
    #     .format("console") \
    #     .option("truncate", "false") \
    #     .start()
    
    # query_pollution.awaitTermination()

    pollution_data.selectExpr("to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("topic", emission2_topic) \
        .option("checkpointLocation","checkpoint_dir") \
        .outputMode("complete") \
        .start()


    fcd_df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("subscribe", fcd_topic) \
        .load()
    
    fcd_schema = StructType([
        StructField("timestep_time", FloatType()),
        StructField("vehicle_angle", FloatType()),
        StructField("vehicle_id", IntegerType()),
        StructField("vehicle_lane", StringType()),
        StructField("vehicle_pos", FloatType()),
        StructField("vehicle_slope", FloatType()),
        StructField("vehicle_speed", FloatType()),
        StructField("vehicle_type", StringType()),
        StructField("vehicle_x", FloatType()),
        StructField("vehicle_y", FloatType())
    ])

    fcd_df_parsed = fcd_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), fcd_schema).alias("data")) \
        .select("data.*") \
        .withColumn("timestep_time", to_timestamp(col("timestep_time")))


    traffic_data = fcd_df_parsed.groupBy(window("timestep_time", window_duration).alias("date"),
                                        col("vehicle_lane").alias("laneId")) \
        .agg(approx_count_distinct("vehicle_id").alias("vehicleCount"))


    traffic_data.selectExpr("to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("topic", fcd2_topic) \
        .option("checkpointLocation","checkpoint_dir2") \
        .outputMode("complete") \
        .start()


    spark.streams.awaitAnyTermination()

