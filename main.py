# /* =====================================================
# * Copyright (c) 2022, Fivecomm - 5G COMMUNICATIONS FOR FUTURE INDUSTRY
#   VERTICALS S.L. All rights reserved.
# * File_name scriptRecepcionV33
# * Description:  The main file of the mqtt platform
# * Author:  Alvaro
# * Date:  28-04-23
# * Version:  1.33
# * =================================================== */

import time
import os
import threading
# from mysql.connector.errors import Error
from datetime import datetime, timedelta
from paho.mqtt import client as mqtt_client
import jsonSender
import battery as bat
import mysqlGet
import mysqlSet
from timeChecker import *
import mqttConect
import aesDecoder
from jsonFormat import jsonFormat
import replyLite
import crcmod
from binascii import unhexlify
import API

# battery level cnt
minValue = 0
maxValue = 100
changeSpeed = 0.05
balanceCounter = 0
BROKER_INST = 'pablito'
topic = "#"  # topic for sub  of the mqtt suscriptor
BROKER_IP = '192.168.0.20'  # ip or domain of the broker
BROKER_PORT = 1883  # comunication port
# script credentials
BROKER_USR = 'device'
BROKER_PASS = 'device'

BATTERY_THRESHOLD = 0

BAT_REPORT_TIME = 86400
BAT_GRANULARITY = 3600
BAT_VALUES = [86400, 43200, 21700]


def parsePayloadToHexa(payload):
    frame = [hex(byte).split("0x")[1] for byte in payload]
    hex_data = ""
    for i in frame:
        if len(i) == 1:  # if the hex value is only one digit, add a 0 to the left
            i = "0" + i
        hex_data += i
    return hex_data

def segundos_restantes(date):
    ahora = datetime.now()

    dia_siguiente = ahora + timedelta(days=1)
    fecha_siguiente = dia_siguiente.date()

    hora_siguiente = datetime.strptime(f'{fecha_siguiente} {date}', '%Y-%m-%d %H:%M')

    diferencia = hora_siguiente - ahora
    segundos_restantes = diferencia.total_seconds()

    return int(segundos_restantes)

def voltear_bytes(string):
    # Convertir el string en una lista de bytes
    bytes_list = [string[i:i+2] for i in range(0, len(string), 2)]
    # Invertir el orden de los bytes en la lista
    bytes_list.reverse()
    # Unir los bytes en un nuevo string y agregar un 0 al principio si es necesario
    new_string = ''.join(bytes_list)
    if len(new_string) % 2 == 1:
        new_string = '0' + new_string
    return new_string


def makingLogsDir(directory):
    if not os.path.isdir(directory):
        try:
            os.makedirs(directory)
        except OSError:
            pass


def loadImeis() -> list:
    return mysqlGet.getAllIMEIs()
    # return ["866897040488373", "866897040488374", "866897040153126"]


def defaultCase(msg):
    print("warning!")
    # print(msg.payload)
    # print(msg.topic)


def meassureToFloat(code: str, div: int) -> float:
    v_aux = []
    aux_str = ""
    for i in code:
        if len(aux_str) == 2:
            v_aux.append(aux_str)
            aux_str = ""
        aux_str += i
    v_aux.append(aux_str)
    v_aux = v_aux[::-1]
    value = "".join(str(v) for v in v_aux)
    return int(value, 16)/div

def frame50dec(subframe1, subframe2):
    is_crc_ok = crcCheck(subframe1)
    device_sn = str(subframe1[4:-4])
    alarms = str(subframe2[14:-4])
    binary_str = bin(int(alarms, 16))[2:].zfill(16)
    bits = [int(binary_str[i]) for i in range(len(binary_str))]
    bits = bits[::-1]
    data = {
        "crcBool": is_crc_ok,
        "deviceSN": device_sn,
        "alarms": {
            "dry": bits[0],
            "reverse": bits[1],
            "leak": bits[2],
            "burst": bits[3],
            "tamper": bits[4],
            "lowBattery": bits[5],
            "lowTemp": bits[6],
            "highTemp": bits[7],
            "V1AboveV4": bits[8],
            "internalError": bits[9],
            "tamperOnDisplay": bits[15]
        }
    }
    return data


def frame150dec(frame):
    frame = str(frame).replace('-', '')
    is_crc_ok = crcCheck(frame[8:])
    timestamp = int(frame[:8], 16)
    timestamp = datetime.fromtimestamp(timestamp)
    if frame[8:12] == "3f10":
        print("Everything is ok")
    data_order = ["volume", "reverseVolume", "flow",
                  "Batt", "TempAmb", "TempMedia", "Acoustic"]
    cont = 0
    data = {}
    frame_meas = frame[12:-4]
    while len(frame_meas) > 0:
        measure_type = frame_meas[:4]
        units = frame_meas[4:6]
        byteslen = frame_meas[6:8]
        sandexp = frame_meas[8:10]
        multipler = hexSignAndExpToMult(sandexp)
        value = frame_meas[10:10+int(byteslen, 16)*2]
        value = int(value, 16) * multipler
        frame_meas = frame_meas[10+int(byteslen, 16)*2:]
        data[data_order[cont]] = [measure_type,
                                  units, byteslen, multipler, value]
        if len(frame_meas) < 12:
            break
        cont += 1
    data = {
        "crcBool": is_crc_ok,
        "meassure": data_order,
        "data": data,
        "timestamp": timestamp
    }
    return data


def hexSignAndExpToMult(hex: str) -> float:
    sandexp = bin(int(hex, base=16)).replace("0b", "").zfill(16)[::-1]
    multipler = pow(-1, (int(sandexp[7], 2))) * pow(10,
                                                    (pow(-1, (int(sandexp[6], 2)))*int(sandexp[:5][::-1], 2)))
    return multipler

def crcCheck(frame: str) -> bool:
    crc = frame[-4:]
    sub = frame[:-4]
    crc16 = crcmod.predefined.Crc('xmodem')
    crc16.update(unhexlify(sub))
    return crc16.hexdigest().lower() == crc.lower()

def calculate_crc16_xmodem(data):
    crc = 0
    for b in data:
        crc = crc ^ b << 8
        for i in range(8):
            if crc & 0x8000:
                crc = crc << 1 ^ 0x1021
            else:
                crc = crc << 1
    return crc & 0xFFFF

def calcular_porcentaje_bateria(voltaje_actual):
    voltaje_minimo = 3.27
    voltaje_maximo = 4.2
    rango_voltaje = voltaje_maximo - voltaje_minimo
    porcentaje_bateria = ((voltaje_actual - voltaje_minimo) / rango_voltaje) * 100
    return max(min(porcentaje_bateria, 100), 0)

def frameSelectorType(payload) -> str:
    # The current frame types are:
    # - sigtec -> str
    # - wm_bus, 50_bytes, 150_bytes -> bytes
    try:
        dec_payload = payload.decode()
    except:  # If it's not a string, it's bytes tuple
        dec_payload = ""
    a = dec_payload[:6]
    if dec_payload[:6] == "sigtec":
        frame_type = "sigtec"
    elif dec_payload[:8] == "greylist":
        frame_type = "greyList"
    else:  # All frames inside this else are bytes, so we need to parse them
        # hex_data = parsePayloadToHexa(payload)
        hex_data = payload
        print(len(hex_data))
        print(hex_data)
        a = len(hex_data)
        if len(hex_data) == 150:
            frame_type = "wm_bus"
        else:
            frame_type = "unknown"
    print("Frame type: " + frame_type)
    return frame_type

def json_real_time(imei):
    js = jsonFormat()
    js.send_realTime(imei)

def getWhiteList(imei):
    device = mysqlGet.getDeviceProperties("imei", imei)
    return mysqlGet.getWhiteListBySn("sensor_id", device["sn"])


def subscribe(client: mqtt_client, vectorIMEIs: list):
    def on_message(client, userdata, msg: mqtt_client.MQTTMessage):
        nonlocal vectorIMEIs
        if msg.topic == "a1":
            # Replace here New function check IMEI dev_imeicheck
            if msg.payload.decode().split(";")[0] in vectorIMEIs:
                print("Device already registered")
                
                usr, passwrd = mysqlGet.getUserAndPassFromImei(
                    msg.payload.decode().split(";")[0])
                fw = msg.payload.decode().split(";")[3]
                hw = msg.payload.decode().split(";")[2]
                apn = msg.payload.decode().split(";")[4]
                mysqlSet.updateDevice_property(msg.payload.decode().split(";")[0],"fw",fw)
                mysqlSet.updateDevice_property(msg.payload.decode().split(";")[0],"hw",hw)
                mysqlSet.updateDevice_property(msg.payload.decode().split(";")[0],"apn",apn)

                client = replyLite.send("a1",
                                        [msg.payload.decode().split(";")[0], usr, passwrd, None], client)
            else:
                print("Device NOT registered")
        elif msg.topic[0] == "t" and msg.topic[1:] in vectorIMEIs:
            print("\033[96m=========================================\033[0m")
            frame_type = frameSelectorType(msg.payload)
            if frame_type == "sigtec":
                frame_battery = msg.payload.decode().split(";")[-1]
                frame_coverage = msg.payload.decode().split(";")[-2]

                properties = mysqlGet.getDeviceProperties('imei',msg.topic[1:])
                
                # Dividir los valores por el carácter " "
                valores = frame_coverage.split(" ")
                
                # Crear un diccionario para almacenar los valores
                resultados = {}
                
                # Iterar sobre los valores y extraer los datos necesarios
                for valor in valores:
                    if ":" in valor:
                        clave, valor = valor.split(":")
                        resultados[clave.strip()] = valor.strip()
                
                # Crear variables para los valores obtenidos
                # for clave, valor in resultados.items():
                #     globals()[clave] = valor

                # seconds = segundos_restantes(properties['wake_up'])

                # client = replyLite.send(
                #     "sigtech", [msg.topic[1:], seconds, int(granularity), properties['signal_threshold']], client)
                client = replyLite.send(
                    "sigtech", [msg.topic[1:], 86400, 900, -120], client)
                
                mysqlSet.updateDevice_property(msg.topic[1:], "battery", frame_battery)
                mysqlSet.insertCoverage(
                        msg.topic[1:], resultados)
                #send json
                # sender = wmbusSender(msg.topic[1:])
                # sender.send()
            elif frame_type == "greyList":
                list =  msg.payload.decode().split(";")[1].split(',')[:-1]
                for i in list:
                    # sólo hay que voltear, no pasar a HEXADECIMAL

                    #############################################
                    str_id = voltear_bytes(i[:8])
                    sen_id = int(str_id,16)
                    #############################################
                    # sen_id = int(str_id)
                    rssi = int(i[8:10],16)
                    average = int(i[10:12],16)
                    mysqlSet.upsertSensorToGraylist(msg.topic[1:], average, rssi, sen_id)
                white_list = getWhiteList(msg.topic[1:])
                white_list.insert(0, msg.topic[1:])
                if len(white_list) > 1:
                    client = replyLite.send(
                        "whitelist", white_list, client)
                else:
                    print("no hay white list")
                               
            elif frame_type == "wm_bus":
                properties = mysqlGet.getDeviceProperties('imei',msg.topic[1:])
                hex_data = parsePayloadToHexa(msg.payload)
                print("\033[93mRaw frame:\033[97m  " + hex_data)
                hex_data = '-'.join(a+b for a,
                                    b in zip(hex_data[::2], hex_data[1::2]))
                hex_data = hex_data.lower().replace("-", "").rstrip('0')[2:-2]
                msgCod = hex_data[8:]
                print("\033[93mClean frame:\033[97m  " + msgCod)
                msgDec = aesDecoder.aesSingleDecoder(msgCod, properties['key'])
                # msgDec = [{'units': '13', 'value': '11170000'}, {'units': '3b', 'value': '00000000'}, {'units': '5a', 'value': '23a6'}]
                meassures = []
                for i in msgDec:
                    my_bytes = i["value"]
                    if i["units"] == "13" or i["units"] == "3b":
                        div = 1000
                    else:
                        div = 10
                    meassures.append(meassureToFloat(my_bytes, div))
                print(meassures)
                # jsonSender.wmBus(meassures[0])
                sensor_id = voltear_bytes(msgCod[-102:-94])
                mysqlSet.insertDates(msg.topic[1:],datetime.fromtimestamp(int(hex_data[:8],16)).strftime("%Y-%m-%d %H:%M:%S"), meassures[0], meassures[3],
                                                meassures[2], meassures[1], sensor_id)
                mysqlSet.updateDevice_property(msg.topic[1:], 'last_mssg_send', datetime.now() + timedelta(hours=2))
            else:
                print("Unknown frame type")
            gateway_id = msg.topic[0:len(msg.topic)]
            # except Exception as ex:
            #     textToWrite = b"Error decoding the topic message\n", ex
            #     exceptions.exceptionHandler(textToWrite)
            print("\033[96m=========================================\033[0m")
        elif msg.topic[0] == "r" and msg.topic[1:] in vectorIMEIs:
            print("My message")
            print("info: " + str(msg.info) + " | mid: " + str(msg.mid) +
                  " | qos: " + str(msg.qos) + " | retain: " + str(msg.retain) +
                  " | state: " + str(msg.state) + " | timestamp: " + str(msg.timestamp))
        else:
            defaultCase(msg)
    client.subscribe(topic)
    client.on_message = on_message

def run():
    directory = "logs"  # directory for the logs
    makingLogsDir(directory)
    while True:
        try:
            client = mqttConect.mqttConect(
                BROKER_INST, BROKER_IP, BROKER_PORT, BROKER_USR, BROKER_PASS)
            vectorIMEIs = loadImeis()
            # mysqlSet.insertMQTT_properties(866897040488373,"device","device","t866897040488373","r866897040488373")
            # user, password = mysqlGet.getUserAndPassFromImei(866897040488373)
            # connects to broker, deberiamos cambiar el nombre de la fnc
            subscribe(client, vectorIMEIs)
            #replyLite.pubTest(client)
            client.loop_forever()
        except KeyboardInterrupt:
            res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
            if res == 'y':
                exit(0)
        except Exception as ex:
            logFile = open("logs/backendErrors.txt", "ab")
            cDate = datetime.utcnow()
            stringDate = str(cDate.year) + "-" + str(cDate.month) + "-" + str(cDate.day) + \
                " " + str(cDate.hour) + ":" + str(cDate.minute) + \
                ":" + str(cDate.second)
            textToWrite = b"Principal thread error\n"+str.encode(str(ex))
            logFile.write(bytes(stringDate, 'ascii') +
                          bytes(" : ", 'ascii')+textToWrite)
            logFile.close()
            print(textToWrite.decode('ASCII'))

def main_run():
    threads = []
    x = threading.Thread(target=run)
    threads.append(x)
    # x = threading.Thread(target=API.server_run)
    # threads.append(x)
    for i in threads:
        i.start()


if __name__ == "__main__":
    main_run()
