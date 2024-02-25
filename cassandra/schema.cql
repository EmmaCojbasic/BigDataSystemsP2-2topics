SELECT * FROM system_schema.keyspaces WHERE keyspace_name = 'bigdata';

DROP KEYSPACE IF EXISTS bigdata;

CREATE KEYSPACE bigdata WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1};

USE bigdata;

DROP TABLE IF EXISTS bigdata.pollution;

CREATE TABLE bigdata.pollution (
  date TIMESTAMP PRIMARY KEY,
  laneId text,
  laneCO double,
  laneCO2 double,          
  laneHC double,
  laneNOx double,
  lanePMx double,
  laneNoise double
);

DROP TABLE IF EXISTS bigdata.traffic;

CREATE TABLE bigdata.traffic (
  date TIMESTAMP PRIMARY KEY,
  laneId text,
  vehicleCount int
);