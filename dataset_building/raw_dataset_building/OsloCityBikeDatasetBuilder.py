import requests
import json
import csv
from apscheduler.schedulers.blocking import BlockingScheduler

availability_url = "https://gbfs.urbansharing.com/oslobysykkel.no/station_status.json"


def fetch_station_info(station_data_csv_content, station_id):
    for station_record in station_data_csv_content:
        if station_record[0] == station_id:
            return station_record


def fetch_raw_data():
    response = requests.get(availability_url)
    response_json = json.loads(response.text)
    availability_json = response_json["data"]["stations"]

    # FOR DEBUG
    for availabilityRecord in availability_json:
        print(availabilityRecord)
    print(str(len(availability_json)) + " records")
    #

    station_data = csv.reader(open('../oslo_citybike_station_information_dataset.csv', "r"), delimiter=",")

    # Raw data
    with open('../oslo_citybike_dataset.csv', 'a', newline='', encoding="UTF-8") as osloCityBikeDatasetCSV:
        writer = csv.writer(osloCityBikeDatasetCSV)

        if osloCityBikeDatasetCSV.tell() == 0:
            writer.writerow(
                ["station_id",
                 "station_name",
                 "station_address",
                 "station_lat",
                 "station_lon",
                 "station_capacity",
                 "is_installed",
                 "is_renting",
                 "num_bikes_available",
                 "num_docks_available",
                 "is_returning",
                 "last_reported"])

        for record in availability_json:
            station_id = record["station_id"]
            station_info = fetch_station_info(station_data, station_id)
            writer.writerow(
                [station_id,
                 station_info[1],
                 station_info[2],
                 station_info[3],
                 station_info[4],
                 station_info[5],
                 record["is_installed"],
                 record["is_renting"],
                 record["num_bikes_available"],
                 record["num_docks_available"],
                 record["is_returning"],
                 record["last_reported"],
                 ])

scheduler = BlockingScheduler()
scheduler.add_job(fetch_raw_data, 'interval', minutes=30)
scheduler.start()
