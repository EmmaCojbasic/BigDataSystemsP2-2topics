from pyspark.sql.functions import *
from pyspark.sql.types import FloatType, StringType, TimestampType, IntegerType, DoubleType, StructField, StructType, DateType
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import os
from cassandra.cluster import Cluster


keyspace = "bigdata"
pollution_table = "pollution"
traffic_table = "traffic"


def writePollutionToCassandra(writeDF, epochId):
    writeDF.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table=pollution_table, keyspace=keyspace) \
        .save()
    print("Data written to Cassandra for pollution table")

def writeTrafficToCassandra(writeDF, epochId):
    writeDF.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table=traffic_table, keyspace=keyspace) \
        .save()
    print("Data written to Cassandra for traffic table")
    
def create_database(cassandra_session):

    cassandra_session.execute("""
        CREATE KEYSPACE IF NOT EXISTS bigdata
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': 1 }
        """)

    cassandra_session.set_keyspace(keyspace)

    cassandra_session.execute("DROP TABLE IF EXISTS bigdata.pollution")
    cassandra_session.execute("""
        CREATE TABLE bigdata.pollution (
            date TIMESTAMP PRIMARY KEY,
            laneId text,
            laneCO double,
            laneCO2 double,
            laneHC double,
            laneNOx double,
            lanePMx double,
            laneNoise double
        )
    """)
    
    cassandra_session.execute("DROP TABLE IF EXISTS bigdata.traffic")
    cassandra_session.execute("""
        CREATE TABLE bigdata.traffic (
            date TIMESTAMP PRIMARY KEY,
            laneId text,
            vehicleCount int
        )
    """)


if __name__ == "__main__":

    cassandra_host = "cassandra" #os.getenv('CASSANDRA_HOST')
    cassandra_port = 9042 #int(os.getenv('CASSANDRA_PORT'))
    kafka_url = "kafka:9092" #os.getenv('KAFKA_URL')
    #topic = os.getenv('KAFKA_TOPIC')
    fcd_topic = 'stockholm-fcd2'
    emission_topic = 'stockholm-emission2'
    
    window_duration = "1 minute" #os.getenv('WINDOW_DURATION')
    N = int(os.getenv('N'))

    cassandra_cluster = Cluster([cassandra_host], port=cassandra_port)
    cassandra_session = cassandra_cluster.connect()
    create_database(cassandra_session)

    vehicleSchema = StructType([
        StructField("Date", TimestampType()),
        StructField("LaneId", StringType()),
        StructField("VehicleCount", IntegerType())
    ])

    emissionSchema = StructType([
        StructField("Date", TimestampType()),
        StructField("LaneId", StringType()),
        StructField("LaneCO", FloatType()),
        StructField("LaneCO2", FloatType()),
        StructField("LaneHC", FloatType()),
        StructField("LaneNOx", FloatType()),
        StructField("LanePMx", FloatType()),
        StructField("LaneNoise", FloatType())
    ])

    appName = "Stockholm2App"
    
    conf = SparkConf()
    conf.set("spark.cassandra.connection.host", cassandra_host)
    conf.set("spark.cassandra.connection.port", cassandra_port)
    #spark = SparkSession.builder.config(conf=conf).appName(appName).config("spark.ui.port", "4041").getOrCreate()
    spark = SparkSession.builder.config(conf=conf).appName(appName).getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")

    dfEmission = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("subscribe", emission_topic) \
        .load()
    
    #dfEmission.printSchema()
    
    dfFcd = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_url) \
        .option("subscribe", fcd_topic) \
        .load()
    
    #dfFcd.printSchema()

    dfEmissionParsed = dfEmission.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), emissionSchema).alias("data")).select("data.*")

    dfFcdParsed = dfFcd.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), vehicleSchema).alias("data")).select("data.*")
    
    ########## BITNO

    dfEmissionParsed = dfEmissionParsed.withColumn("Date", to_timestamp("Date", "MMM dd, yyyy, hh:mm:ss a"))
    dfFcdParsed = dfFcdParsed.withColumn("Date", to_timestamp("Date", "MMM dd, yyyy, hh:mm:ss a"))


    dfEmissionParsed = dfEmissionParsed.withColumnRenamed("Date", "date") \
                         .withColumnRenamed("LaneId", "laneId") \
                         .withColumnRenamed("LaneCO", "laneCO") \
                         .withColumnRenamed("LaneCO2", "laneCO2") \
                         .withColumnRenamed("LaneHC", "laneHC") \
                         .withColumnRenamed("LaneNOx", "laneNOx") \
                         .withColumnRenamed("LanePMx", "lanePMx") \
                         .withColumnRenamed("LaneNoise", "laneNoise")

    dfFcdParsed = dfFcdParsed.withColumnRenamed("Date", "date") \
                                .withColumnRenamed("LaneId", "laneId") \
                                .withColumnRenamed("VehicleCount", "vehicleCount")

    query_pollution2 = dfEmissionParsed.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()
    
    query_pollution2.awaitTermination()

    query_traffic = dfFcdParsed.writeStream \
        .foreachBatch(writeTrafficToCassandra) \
        .outputMode("append") \
        .start()

    query_pollution = dfEmissionParsed.writeStream \
        .foreachBatch(writePollutionToCassandra) \
        .outputMode("append") \
        .start()

    # print("PRINTING TRAFFIC DATA")
    # query_traffic2 = grouped_data_traffic.writeStream \
    # .outputMode("complete") \
    # .format("console") \
    # .option("truncate", "false") \
    # .start()

    query_traffic.awaitTermination()
    query_pollution.awaitTermination()

    spark.stop()   