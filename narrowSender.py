import mysqlGet
import mysqlSet
import datetime
import requests
import json
from datetime import timedelta, datetime
import datetime

class narrowSender:
    
    def __init__(self, imei):

        json_data = {
            "sn": "",
            "data_received": "",
            "data_wl": {},
            "data_gl": {}
        }
        self.json_data = json_data
        self.url = "http://192.168.0.141:8000"
        self.bearer = ""
        self.headers = ""
        self.imei = imei
        self.hour = 0

    def get_json(self):
        self.setDeviceData()
        sensors = mysqlGet.getWhiteListBySn("sensor_id", self.get_value("sn"))
        while self.hour < 24:
            self.json_data["data_wl"][str(self.hour)] = {}
            for s in sensors:
                self.setSensor(s)
            self.hour += 1
        grey_list_ids = mysqlGet.getGreyListBySn("sensor_id", self.get_value("sn"))
        for s_id in grey_list_ids:
            self.setSensorGreyList(s_id)
        #print(json.dumps(self.json_data))
        return(json.dumps(self.json_data))
        
    def set_value(self, key, value):
        self.json_data[key] = value
        
    def get_value(self, key):
        return self.json_data[key]

    def setSensor(self, sensor_id):
        try:
            data = mysqlGet.getDataBySensorIdAndHour(sensor_id, self.hour)
        except Exception:
            data = {"data":""}
        try:
            data_grey_list = mysqlGet.getGreyListSensorProperties("sensor_id", sensor_id)
            rssi = data_grey_list["rssi"]
        except Exception:
            rssi = "Null"
        data_to_json = {"data":data["data"], "rssi":rssi}
        #mysqlSet.updateDataProperty(data["id"], "sent", 1)
        self.json_data["data_wl"][str(self.hour)][str(sensor_id)] = data_to_json

    def setSensorGreyList(self, sensor_id):
        try:
            data_grey_list = mysqlGet.getGreyListSensorProperties("sensor_id", sensor_id)
            rssi = data_grey_list["rssi"]
        except Exception:
            rssi = "Null"
        data_to_json = {"num_veces":data_grey_list["average"], "rssi":rssi}
        self.json_data["data_gl"][str(sensor_id)] = data_to_json

    def setDeviceData(self):
        try:
            data = mysqlGet.getDeviceProperties("imei", self.imei)
            self.set_value("sn",data["sn"])
            self.json_data["data_received"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:  
            print("error")
            print(e)

    def send(self):
        json_send = json.dumps(self.json_data)
        print(json_send)
        self.bearer = "none"
        self.headers = {"accept": "application/json",
            "authorization": self.bearer, "content-type": "application/json"}
        response = requests.post(self.url, headers=self.headers, json=json_send)
        print(response)