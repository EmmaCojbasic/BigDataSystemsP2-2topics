export SPARK_MASTER_URL=spark://${SPARK_MASTER_NAME}:${SPARK_MASTER_PORT}
export SPARK_HOME=/opt/bitnami/spark

echo "Submit application ${SPARK_APPLICATION_PYTHON_LOCATION} to Spark master ${SPARK_MASTER_URL}"
echo "Passing arguments ${SPARK_APPLICATION_ARGS}"
echo $(ls)
spark-submit --master ${SPARK_MASTER_URL} ${SPARK_SUBMIT_ARGS} ${SPARK_APPLICATION_PYTHON_LOCATION} 
