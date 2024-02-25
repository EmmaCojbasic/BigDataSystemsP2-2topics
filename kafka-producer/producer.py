from confluent_kafka import Producer
import csv
import json
import sys 
import time
import datetime

fcd_file = 'sumoTrace.csv'
emission_file = 'my_emission_file.csv'
fcd_topic = 'stockholm-fcd'
emission_topic = 'stockholm-emission'

def receipt(err, msg):
    if err is not None:
        print('Error: {}', format(err))
    else:
        message = 'Produces message on topic {}:{}'.format(msg.topic(), msg.value().decode('utf-8'))
        print(message)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(1)

    csv_file = sys.argv[1]
    producer = Producer({'bootstrap.servers': 'kafka:9092'})
    print('Kafka Producer has been initiated')

    if csv_file == fcd_file:
        with open(fcd_file) as fcd_file:
            lane_data = csv.DictReader(fcd_file, delimiter=';')
            for row in lane_data:
                vehicle_info = {}
                vehicle_info['timestep_time'] = float(row['timestep_time'])
                vehicle_info['vehicle_angle'] = float(row['vehicle_angle']) if row['vehicle_angle'] != "" else 0.0
                vehicle_info['vehicle_id'] = int(row['vehicle_id']) if row['vehicle_id'] != "" else 0
                vehicle_info['vehicle_lane'] = row['vehicle_lane']
                vehicle_info['vehicle_pos'] = float(row['vehicle_pos']) if row['vehicle_pos'] != "" else 0.0
                vehicle_info['vehicle_slope'] = float(row['vehicle_slope']) if row['vehicle_slope'] != "" else 0.0
                vehicle_info['vehicle_speed'] = float(row['vehicle_speed']) if row['vehicle_speed'] != "" else 0.0
                vehicle_info['vehicle_type'] = row['vehicle_type']
                vehicle_info['vehicle_x'] = float(row['vehicle_x']) if row['vehicle_x'] != "" else 0.0
                vehicle_info['vehicle_y'] = float(row['vehicle_y']) if row['vehicle_y'] != "" else 0.0

                producer.produce(fcd_topic, key = 'stockholm', value = json.dumps(vehicle_info), callback = receipt)
                producer.flush()
                time.sleep(0.1)
    else:
        with open(emission_file) as emission_file:
            data = csv.DictReader(emission_file, delimiter=';')
            for row in data:
                emission_info = {}
                emission_info['timestep_time'] = float(row['timestep_time'])
                emission_info['vehicle_CO'] = float(row['vehicle_CO']) if row['vehicle_CO'] != "" else 0.0
                emission_info['vehicle_CO2'] = float(row['vehicle_CO2']) if row['vehicle_CO2'] != "" else 0.0
                emission_info['vehicle_HC'] = float(row['vehicle_HC']) if row['vehicle_HC'] != "" else 0.0
                emission_info['vehicle_NOx'] = float(row['vehicle_NOx']) if row['vehicle_NOx'] != "" else 0.0
                emission_info['vehicle_PMx'] = float(row['vehicle_PMx']) if row['vehicle_PMx'] != "" else 0.0
                emission_info['vehicle_angle'] = float(row['vehicle_angle']) if row['vehicle_angle'] != "" else 0.0
                emission_info['vehicle_eclass'] = row['vehicle_eclass']
                emission_info['vehicle_electricity'] = float(row['vehicle_electricity']) if row['vehicle_electricity'] != "" else 0.0
                emission_info['vehicle_id'] = int(row['vehicle_id']) if row['vehicle_id'] != "" else 0
                emission_info['vehicle_lane'] = row['vehicle_lane']
                emission_info['vehicle_fuel'] = float(row['vehicle_fuel']) if row['vehicle_fuel'] != "" else 0.0
                emission_info['vehicle_noise'] = float(row['vehicle_noise']) if row['vehicle_noise'] != "" else 0.0
                emission_info['vehicle_pos'] = float(row['vehicle_pos']) if row['vehicle_pos'] != "" else 0.0
                emission_info['vehicle_route'] = row['vehicle_route']
                emission_info['vehicle_speed'] = float(row['vehicle_speed']) if row['vehicle_speed'] != "" else 0.0
                emission_info['vehicle_type'] = row['vehicle_type']
                emission_info['vehicle_waiting'] = float(row['vehicle_waiting']) if row['vehicle_waiting'] != "" else 0.0
                emission_info['vehicle_x'] = float(row['vehicle_x']) if row['vehicle_x'] != "" else 0.0
                emission_info['vehicle_y'] = float(row['vehicle_y']) if row['vehicle_y'] != "" else 0.0

                producer.produce(emission_topic, key = 'stockholm', value = json.dumps(emission_info), callback = receipt)
                producer.flush()
                time.sleep(0.1)
    print('Kafka message producer done')