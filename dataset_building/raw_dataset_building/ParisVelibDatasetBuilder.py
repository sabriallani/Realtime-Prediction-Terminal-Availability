import requests
import json
import csv
from apscheduler.schedulers.blocking import BlockingScheduler

base_api_url = "https://opendata.paris.fr/api/records/1.0/search/"
url_query = "?dataset=velib-disponibilite-en-temps-reel&q=&rows=2000"
url = base_api_url + url_query


def fetch_raw_data():
    response = requests.get(url)
    json_data = json.loads(response.text)
    records = json_data["records"]

    # FOR DEBUG
    for record in records:
        print(record)
    print(str(len(records)) + " records")
    #

    # Raw data
    with open('../paris_velib_dataset.csv', 'a', newline='', encoding="UTF-8") as velibDatasetCSV:
        writer = csv.writer(velibDatasetCSV)

        if velibDatasetCSV.tell() == 0:
            writer.writerow(
                ["dataset_id",
                 "record_id",
                 "ebike",
                 "capacity",
                 "name",
                 "nom_arrondissement_communes",
                 "num_bikes_availabile",
                 "is_installed",
                 "is_renting",
                 "mechanical",
                 "station_code",
                 "num_docks_available",
                 "due_date",
                 "is_returning",
                 "geometry_type",
                 "longitude",
                 "latitude",
                 "record_timestamp"])

        for record in records:
            fields = record["fields"]
            if fields["capacity"] != 0:
                writer.writerow(
                    [record["datasetid"],
                     record["recordid"],
                     fields["ebike"],
                     fields["capacity"],
                     fields["name"],
                     fields["nom_arrondissement_communes"],
                     fields["numbikesavailable"],
                     fields["is_installed"],
                     fields["is_renting"],
                     fields["mechanical"],
                     fields["stationcode"],
                     fields["numdocksavailable"],
                     fields["duedate"],
                     fields["is_returning"],
                     record["geometry"]["type"],
                     record["geometry"]["coordinates"][0],
                     record["geometry"]["coordinates"][1],
                     record["record_timestamp"]
                     ])


scheduler = BlockingScheduler()
scheduler.add_job(fetch_raw_data, 'interval', minutes=30)
scheduler.start()
