import mysql.connector
import mysqlGet
from mysqlConnector import *

def updateDevice_property(imei,column,value):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE DEVICE_PROPERTIES SET "+ column +" = %s where imei = %s"
        val = (value, imei) 
        myCursor.execute(sql, val)
        
    except Exception as ex:
        textToWrite = b"Error updating values on DEVICE_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)

def updateGreyListProperty(sensor_id, column, value):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE GREY_LIST SET " + column + " = %s where sensor_id = %s"
        val = (value, sensor_id) 
        myCursor.execute(sql, val)
        if myCursor.rowcount == 0:
            raise ValueError("No se ha actualizado ninguna fila")
    except Exception as ex:
        textToWrite = b"Error updating values on DEVICE_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)

def updateDataProperty(id,column,value):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE DATA SET " + column + " = %s where id = %s"
        val = (value, id) 
        myCursor.execute(sql, val)
        if myCursor.rowcount == 0:
            raise ValueError("No se ha actualizado ninguna fila")
        
    except Exception as ex:
        textToWrite = b"Error updating values on DEVICE_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)    

def insertNewDevice(imei, networked, reportTime):
    try:
        # Insertar los valores en device_properties
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = """INSERT INTO DEVICE_PROPERTIES (imei, networked, timestamp, reportTime) 
                SELECT %s, %s, NOW, %s, %s"""
        val = (imei, networked, reportTime)
        myCursor.execute(sql, val)

        
    except Exception as ex:
        textToWrite = b"Error inserting values on MQTT_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def insertNewWhiteList(sensor_id):
    sensor = mysqlGet.getGreyListSensorById(sensor_id)

    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = """INSERT INTO WHITE_LIST (manufacturer, model, vertical, device_id, sensor_id) 
                VALUES (%s, %s, %s, %s, %s)"""
        val = (sensor["manufacturer"], sensor["model"], sensor["vertical"], int(sensor["device_id"]), sensor_id)
        myCursor.execute(sql, val)

        
    except Exception as ex:
        textToWrite = b"Error inserting values on MQTT_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def insertMQTT_properties(imei, user, password, txTopic, rxTopic):
    try:
        # Insertar los valores en mqtt_properties
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = """INSERT INTO MQTT_PROPERTIES (txTopic, rxTopic, user, password, device_id) 
                SELECT %s, %s, %s, %s, dp.id FROM DEVICE_PROPERTIES dp WHERE dp.imei = %s"""
        val = (txTopic, rxTopic, user, password, imei)
        myCursor.execute(sql, val)

        
    except Exception as ex:
        textToWrite = b"Error inserting values on MQTT_PROPERTIES\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def insertDates(imei, timestamp, volume, preassure, temperature, flow, sensor_id ):
    try:
        # Obtener el ID de la fila en device_properties utilizando un JOIN
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = """INSERT INTO DATA (timestamp, volume, preassure, temperature, flow, sensor_id, device_id, received) 
                VALUES( %s, %s, %s, %s, %s, %s,
                        (SELECT dp.id FROM DEVICE_PROPERTIES dp WHERE dp.imei = %s),
                         NOW())"""
        val = (timestamp, volume, preassure, temperature, flow, sensor_id, imei)
        myCursor.execute(sql, val)

        
    except Exception as ex:
        textToWrite = b"Error inserting values on DATA\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def upsertSensorToGraylist(imei, average, rssi, sensor_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = """INSERT INTO GREY_LIST (average, rssi, sensor_id, device_id, timestamp) 
                VALUES (%s, %s, %s, (SELECT dp.id FROM DEVICE_PROPERTIES dp WHERE dp.imei = %s), NOW())
                ON DUPLICATE KEY UPDATE
                average = VALUES(average),
                rssi = VALUES(rssi),
                device_id = VALUES(device_id),
                timestamp = NOW();"""
        val = (average, rssi, sensor_id, imei)
        myCursor.execute(sql, val)
        
        # Commit the transaction
        mydbConnector.commit()
        print("UPSERT executed successfully!")

        
    except Exception as ex:
        textToWrite = b"Error inserting values on DATA\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def insertCoverage(imei, valores_cobertura):
    try:
        # Obtener el ID de la fila en device_properties utilizando un JOIN
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = """INSERT INTO COVERAGE (Cc, Nc, RSRP, RSRQ, TAC, Id_cov, EARFCN, PWD, PAGING, CID, BAND, BW, device_id, timestamp) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                ,(SELECT id FROM DEVICE_PROPERTIES WHERE imei = %s)
                ,NOW()
                );"""
        val = (valores_cobertura["Cc"], valores_cobertura["Nc"], valores_cobertura["RSRP"], valores_cobertura["RSRQ"], 
                valores_cobertura["TAC"], valores_cobertura["Id"], valores_cobertura["EARFCN"], valores_cobertura["PWR"],
                valores_cobertura["PAGING"], valores_cobertura["CID"], valores_cobertura["BAND"], valores_cobertura["BW"],
                imei)
        myCursor.execute(sql, val)
        
    except Exception as ex:
            print(ex)
            textToWrite = b"Error inserting values on COVERAGE\n",ex
            exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)