import logging

import azure.functions as func
import json
import requests
from mysql.connector import (connection)
import datetime


config = {
  'user': 'jaken',
  'password': 'i_love_cloud1',
  'host': 'sc20jdpn-mysql-db.mysql.database.azure.com',
  'database': 'data',
  'raise_on_warnings': True,
}

def get_val_or_error(request, key):
    val = request.get(key)
    if val is None or val == "":
        raise ValueError(f"Missing required parameter '{key}'")
    return val


def main(req: func.HttpRequest) -> func.HttpResponse:
    # connect to the database
    try:
        cnx = connection.MySQLConnection(**config)
        cursor = cnx.cursor()
    except Exception as e:
        return func.HttpResponse(
            "Failed to connect to the database",
            status_code=500
        )
    # parse the request
    try:
        req = req.get_json()
        city = get_val_or_error(req, "city")
        wind = get_val_or_error(req, "wind")
        temp = get_val_or_error(req, "temp")
        max_temp = get_val_or_error(req, "temp_min")
        min_temp = get_val_or_error(req, "temp_max")
        humidity = get_val_or_error(req, "humidity")
        pressure = get_val_or_error(req, "pressure")
    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

    # get max vals from db
    try:
        query = ("SELECT * FROM red_flags WHERE city_name = %s")
        cursor.execute(query, (city,))
        row = cursor.fetchone()
        if row is not None:
            max_wind = row[0]
            max_temp = row[1]
            max_humidity = row[2]
            max_pressure = row[3]
        else:
            raise ValueError(f"City '{city}' not found in database")
    except Exception as e:
        return func.HttpResponse(
            "Failed to get max vals from db" + str(e),
            status_code=500
        )
    
    # check if any vals are above the max
    returnMsg = ""
    errorFlag = False
    if float(wind) > float(max_wind):
        returnMsg += "Warning: Wind is too high! "
        errorFlag = True
    if float(temp) > float(max_temp):
        returnMsg += "Warning: Temperature is too high! "
        errorFlag = True
    if float(humidity) > float(max_humidity):
        returnMsg += "Warning: Humidity is too high! "
        errorFlag = True
    if float(pressure) > float(max_pressure):
        returnMsg += "Warning: Pressure is too high! "
        errorFlag = True
    
    if errorFlag == False:
        returnMsg = "All values are within the acceptable range."

    # save to reports
    try:
        add_report = ("INSERT INTO reports "
               "(city_name, report_description, report_date)"
               "VALUES (%s, %s, %s)")
        data_report = (city, returnMsg, datetime.datetime.now())
        cursor.execute(add_report, data_report)
        cnx.commit()
    except Exception as e:
        return func.HttpResponse(
            "Failed to save report to db" + str(e),
            status_code=500
        )
    
    return func.HttpResponse(
        returnMsg,
        status_code=200
    )


# print(handle(json.dumps({
#     "city": "London",
#     "wind": 1,
#     "temp": 20,
#     "temp_max": 25,
#     "temp_min": 15,
#     "humidity": 50,
#     "pressure": 1010
# })))