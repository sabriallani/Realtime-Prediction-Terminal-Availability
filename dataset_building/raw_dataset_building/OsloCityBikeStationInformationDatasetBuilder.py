import requests
import json
import csv

station_info_url = "https://gbfs.urbansharing.com/oslobysykkel.no/station_information.json"

if __name__ == '__main__':
    response = requests.get(station_info_url)
    response_json = json.loads(response.text)
    station_info_json = response_json["data"]["stations"]

    # FOR DEBUG
    for station_info_record in station_info_json:
        print(station_info_record["station_id"] + " --- " +
              station_info_record["name"] + " --- " +
              station_info_record["address"] + " --- " +
              str(station_info_record["lat"]) + " --- " +
              str(station_info_record["lon"]) + " --- " +
              str(station_info_record["capacity"]))
    print(str(len(station_info_json)) + " records")
    #

    # Raw data
    with open('../oslo_citybike_station_information_dataset.csv', 'a', newline='', encoding="UTF-8") \
            as osloCityBikeStationInformationCSV:
        writer = csv.writer(osloCityBikeStationInformationCSV)

        if osloCityBikeStationInformationCSV.tell() == 0:
            writer.writerow(
                ["station_id",
                 "name",
                 "address",
                 "lat",
                 "lon",
                 "capacity"])

        for stationInfoRecord in station_info_json:
            if stationInfoRecord["capacity"] != 0:
                writer.writerow([
                    stationInfoRecord["station_id"],
                    stationInfoRecord["name"],
                    stationInfoRecord["address"],
                    stationInfoRecord["lat"],
                    stationInfoRecord["lon"],
                    stationInfoRecord["capacity"]])
