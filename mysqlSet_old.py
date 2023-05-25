"""
    /* ===================================================== 

    * Copyright (c) 2022, Fivecomm - 5G COMMUNICATIONS FOR FUTURE INDUSTRY        VERTICALS S.L. All rights reserved. 

    * File_name scriptRecepcionV33

    * Description:  The main file of the mqtt platform

    * Author:  Alejandro

    * Date:  25-08-21

    * Version:  1.33

    * =================================================== */ 
"""
import mysql.connector
from mysqlConnector import *
from mysql.connector.errors import Error
from conversors import diameterToVolume

def insertBatteryParameters(id,battery,level,balance):
    # level = maxValue(true) or minValue(false)
    # battery =  value to insert
    # id = identifier of the lite
    # balance = balance counter
    try:

        if level:
            string = '`maxValue`='
        else:
            string = '`minValue`='
        mydbConnector7 = mysql.connector.connect(host="172.17.0.2",user="suscriptorPython",password="Rw3X3sZeH6JRXAXPP9pz",database="n8htgo8_fivecomm")
        myCursor7 = mydbConnector7.cursor(buffered=True)
        # 'UPDATE n8htgo8_fivecomm.GATEWAY_PROPERTIES SET balanceCounter=0, `maxValue`=0, `minValue`=0'
        sql = "UPDATE n8htgo8_fivecomm.GATEWAY_PROPERTIES SET balanceCounter=%s,"+string+"%s where id = %s;"
        values = (balance,battery,id)
        myCursor7.execute(sql, values)
        mydbConnector7.commit()        
        myCursor7.close()
        mydbConnector7.close()
        
    except:
        textToWrite = b"Error inserting the battery parameters in the Gateway Properties\n"
        exceptions.exceptionHandler(textToWrite) 

def insertProperties(t1,t2,user,pas,id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]  

        sql = 'INSERT INTO n8htgo8_fivecomm.MQTT_PROPERTIES (txTopic, rxTopic, `user`, password, GATEWAY_PROPERTIES_id) VALUES(%s, %s, %s, %s, %s);'
        val = (t1,t2,user,pas,id)
        myCursor.execute(sql, val)
        mydbConnector.commit()
    except:
            textToWrite = b"Error inserting the mqtt properties\n"
            exceptions.exceptionHandler(textToWrite)
    mysqlClose(mydbConnector,myCursor)

def insertSystem_features(caractSystem, diametro, wakeUpDate, tFuga, volumenLitros, caudalDiametro):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO `SYSTEM_FEATURES`(`id`, `diameter`, `wakeUpDate`, `timeLeak`, `volumeLiters`, `diameterFlow`) VALUES (%s, %s, %s, %s, %s, %s);"
        val = (caractSystem, diametro, wakeUpDate, tFuga, volumenLitros, caudalDiametro)
        myCursor.execute(sql, val)
        mydbConnector.commit()

    except:
        textToWrite = b"Error inserting values on SYSTEM_FEATURES\n"
        exceptions.exceptionHandler(textToWrite)
    mysqlClose(mydbConnector,myCursor)


def insertgGateway_properties(imei, name, client, device_type, location, description, timestamp, CREDENCIALES_id, caractSystem):

    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO `GATEWAY_PROPERTIES`(`imei`, `name`, `client`, `device_type`, `location`, `description`,`timestamp`, `AUTHORIZATION_id`, `SYSTEM_FEATURES_id`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (imei, name, client, device_type, location, description, timestamp, CREDENCIALES_id, caractSystem) 
        myCursor.execute(sql, val)
        mydbConnector.commit()


    except:
        textToWrite = b"Error inserting values on GATEWAY_PROPERTIES\n"
        exceptions.exceptionHandler(textToWrite)
    mysqlClose(mydbConnector,myCursor)


def updateSystemFeatures(diameter, wakeUpDate, timeLeak,caudalDiametro,cSystemFeatures):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE SYSTEM_FEATURES SET diameter = %s, wakeUpDate = %s, timeLeak = %s, volumeLiters = %s, diameterFlow = %s where id = %s;"
        #cambiar por una tabla y un select#########################################################################################################################################################################################
    
        volumenLitros = diameterToVolume(diameter)
        
        val = (diameter, wakeUpDate, timeLeak, volumenLitros, caudalDiametro,cSystemFeatures)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
    except:
        textToWrite = b"Error updating values on SYSTEM_FEATURES\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def InsertGateway_History(cVectorTimestamps,timestamp,accumulated,CELL_ID,battery,GATEWAY_PROPERTIES_id,value, name, sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO n8htgo8_fivecomm.GATEWAY_HISTORY (timestamp,accumulated,CELL_ID,battery, GATEWAY_PROPERTIES_id, value, name, sigtec, `5G_RSRP`, `5G_RSRQ`,`G5_RSSI` ,`5G_SINR`, `5G_TX_POW`, `4G_RSRP`, `4G_RSRQ`, `4G_SINR`, `4G_RSSI`, `4G_TX_POW`, `3G_RSCP`, `3G_ecio`, t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, t21, t22, t23, t24, t25, t26, t27, t28, t29, t30, t31, t32, t33, t34, t35, t36, t37, t38, t39, t40, t41, t42, t43, t44, t45, t46, t47, t48, t49, t50, t51, t52, t53, t54, t55, t56, t57, t58, t59, t60, t61, t62, t63, t64, t65, t66, t67, t68, t69, t70, t71, t72, t73, t74, t75, t76, t77, t78, t79, t80, t81, t82, t83, t84, t85, t86, t87, t88, t89, t90, t91, t92, t93, t94, t95, t96, t97, t98, t99, t100, t101, t102, t103, t104, t105, t106, t107, t108, t109, t110, t111, t112, t113, t114, t115, t116, t117, t118, t119, t120,alarmKamstrup) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,0);"
        # to check
        
        while len(cVectorTimestamps) != 121:
            cVectorTimestamps.append(0)
        
        val = (timestamp,accumulated,CELL_ID,int(battery),GATEWAY_PROPERTIES_id,str(value), str(name), sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio, cVectorTimestamps[0],cVectorTimestamps[1], cVectorTimestamps[2], cVectorTimestamps[3], cVectorTimestamps[4], cVectorTimestamps[5], cVectorTimestamps[6], cVectorTimestamps[7], cVectorTimestamps[8], cVectorTimestamps[9], cVectorTimestamps[10], cVectorTimestamps[11], cVectorTimestamps[12], cVectorTimestamps[13], cVectorTimestamps[14], cVectorTimestamps[15], cVectorTimestamps[16], cVectorTimestamps[17], cVectorTimestamps[18], cVectorTimestamps[19], cVectorTimestamps[20], cVectorTimestamps[21], cVectorTimestamps[22], cVectorTimestamps[23], cVectorTimestamps[24], cVectorTimestamps[25], cVectorTimestamps[26], cVectorTimestamps[27], cVectorTimestamps[28], cVectorTimestamps[29], cVectorTimestamps[30], cVectorTimestamps[31], cVectorTimestamps[32], cVectorTimestamps[33], cVectorTimestamps[34], cVectorTimestamps[35], cVectorTimestamps[36], cVectorTimestamps[37], cVectorTimestamps[38], cVectorTimestamps[39], cVectorTimestamps[40], cVectorTimestamps[41], cVectorTimestamps[42], cVectorTimestamps[43], cVectorTimestamps[44], cVectorTimestamps[45], cVectorTimestamps[46], cVectorTimestamps[47], cVectorTimestamps[48], cVectorTimestamps[49], cVectorTimestamps[50], cVectorTimestamps[51], cVectorTimestamps[52], cVectorTimestamps[53], cVectorTimestamps[54], cVectorTimestamps[55], cVectorTimestamps[56], cVectorTimestamps[57], cVectorTimestamps[58], cVectorTimestamps[59], cVectorTimestamps[60], cVectorTimestamps[61], cVectorTimestamps[62], cVectorTimestamps[63], cVectorTimestamps[64], cVectorTimestamps[65], cVectorTimestamps[66], cVectorTimestamps[67], cVectorTimestamps[68], cVectorTimestamps[69], cVectorTimestamps[70], cVectorTimestamps[71], cVectorTimestamps[72], cVectorTimestamps[73], cVectorTimestamps[74], cVectorTimestamps[75], cVectorTimestamps[76], cVectorTimestamps[77], cVectorTimestamps[78], cVectorTimestamps[79], cVectorTimestamps[80], cVectorTimestamps[81], cVectorTimestamps[82], cVectorTimestamps[83], cVectorTimestamps[84], cVectorTimestamps[85], cVectorTimestamps[86], cVectorTimestamps[87], cVectorTimestamps[88], cVectorTimestamps[89], cVectorTimestamps[90], cVectorTimestamps[91], cVectorTimestamps[92], cVectorTimestamps[93], cVectorTimestamps[94], cVectorTimestamps[95], cVectorTimestamps[96], cVectorTimestamps[97], cVectorTimestamps[98], cVectorTimestamps[99], cVectorTimestamps[100], cVectorTimestamps[101], cVectorTimestamps[102], cVectorTimestamps[103], cVectorTimestamps[104], cVectorTimestamps[105], cVectorTimestamps[106], cVectorTimestamps[107], cVectorTimestamps[108], cVectorTimestamps[109], cVectorTimestamps[110], cVectorTimestamps[111], cVectorTimestamps[112], cVectorTimestamps[113], cVectorTimestamps[114], cVectorTimestamps[115], cVectorTimestamps[116], cVectorTimestamps[117], cVectorTimestamps[118], cVectorTimestamps[119], cVectorTimestamps[120])
        myCursor.execute(sql, val)
    except Exception as ex:
        print(ex)
        textToWrite = b"Error inserting values on GATEWAY_HISTORY\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def InsertAlarm(alarmName,idCaracteristicas):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO n8htgo8_fivecomm.ALARM (name, SYSTEM_FEATURES_id, alarmType) VALUES(%s, %s, %s);"
        values = alarmName,idCaracteristicas,1
        myCursor.execute(sql, values)

    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error inserting the alarm\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def InsertAlarmHisto(alarmName,stringDate,alarmId,tFuga):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO `ALARM_HISTORY`(`name`, `date`,`ALARM_id`,`timeLeak`) VALUES( %s, %s, %s, %s);"
        values = alarmName,stringDate,alarmId,tFuga
        myCursor.execute(sql, values)

    except:
        print("Error consulta")
        textToWrite = b"Error inserting the alarm history\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def InsertAlarmHistoVolum(alarmName, stringDate,alarmId,volumenLitros):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO ALARM_HISTORY(name, date,ALARM_id,volumeLiters) VALUES(%s, %s,%s, %s);"
        values = alarmName, stringDate,alarmId,volumenLitros
        myCursor.execute(sql, values)
                                

    except:
        print("Error consulta")
        textToWrite = b"Error inserting the alarm history\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def SetAlarmHistoryNoFlow(alarmName, cDate,alarmId):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        alarmId = 3
        sql = "INSERT INTO `ALARM_HISTORY`(`name`, `date`,`ALARM_id`,`noFlow`) VALUES(%s, %s,%s, %s)"
        values = alarmName, cDate,alarmId,1
        myCursor.execute(sql, values)
    except:
        print("Error consulta")
        textToWrite = b"Error inserting into ALARM_HISTORY\n"
        exceptions.exceptionHandler(textToWrite)
    mysqlClose(mydbConnector,myCursor)

def SetRemoteConsoleResponse(response, timestamp, remoteId):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = "INSERT INTO `REMOTE_CONSOLE_RESPONSE`(`response`, `timestamp`, `REMOTE_CONSOLE_id`) VALUES(%s, %s, %s)"
        values = (response, timestamp, remoteId)
        myCursor.execute(sql, values)    
    
    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error inserting into REMOTE_CONSOLE_RESPONSE\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def SetGatewayHistory(timestamp,accumulated,CELL_ID,battery,GATEWAY_PROPERTIES_id,value, name, sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio,counterSerialNumber,divisor):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO n8htgo8_fivecomm.GATEWAY_HISTORY (timestamp,accumulated,CELL_ID,battery, GATEWAY_PROPERTIES_id, value, name, sigtec, `5G_RSRP`, `5G_RSRQ`,`G5_RSSI` ,`5G_SINR`, `5G_TX_POW`, `4G_RSRP`, `4G_RSRQ`, `4G_SINR`, `4G_RSSI`, `4G_TX_POW`, `3G_RSCP`, `3G_ecio`,`counterSerialNumber`,`divisor`) VALUES(%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (timestamp,accumulated,CELL_ID,int(battery),GATEWAY_PROPERTIES_id,str(value), str(name), sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio,counterSerialNumber,divisor)
    except:
        print("Error consulta")
        textToWrite = b"Error inserting into GATEWAY_HISTORY\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def SetRemoteConsole(gateway_id, command, executed,AUTHORIZATION_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = "INSERT INTO `REMOTE_CONSOLE`(`gateway_id`, `command`, `executed`,`AUTHORIZATION_id`) VALUES(%s, %s, %s,%s)"
        values = (gateway_id, command, executed,AUTHORIZATION_id)
        myCursor.execute(sql, values)    
        # print("insert")
    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error inserting into REMOTE_CONSOLE\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def UpdateRemoteConsole(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = "UPDATE `REMOTE_CONSOLE` SET `executed` = 1 WHERE id = %s;"
        values = (id,)
        myCursor.execute(sql, values)    
        print("insert")
    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error inserting into REMOTE_CONSOLE\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def updateTxMode(gateway_id,mode):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE GATEWAY_PROPERTIES SET tx_mode = %s where id = %s;"
            
        val = (mode, gateway_id)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
        flag = True
    except:
        textToWrite = b"Error updating values on GATEWAY_PROPERTIES\n"
        exceptions.exceptionHandler(textToWrite)
        flag = False

    mysqlClose(mydbConnector,myCursor)
    return flag
def updateTxInterval(gateway_id,txInterval):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE GATEWAY_PROPERTIES SET tx_interval = %s where id = %s;"
            
        val = (txInterval, gateway_id)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
        flag = True


    except:
        textToWrite = b"Error updating values on GATEWAY_PROPERTIES\n"
        exceptions.exceptionHandler(textToWrite)
        flag = False

    mysqlClose(mydbConnector,myCursor)
    return flag

def updateTxtime(gateway_id,txTime):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE GATEWAY_PROPERTIES SET tx_time = %s where id = %s;"
            
        val = (txTime, gateway_id)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
        flag = True
    except:
        textToWrite = b"Error updating values on GATEWAY_PROPERTIES\n"
        exceptions.exceptionHandler(textToWrite)
        flag = False

    mysqlClose(mydbConnector,myCursor)
    return flag

def updateAPN(gateway_id,APN):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "UPDATE GATEWAY_PROPERTIES SET APN = %s where id = %s;"
            
        val = (APN, gateway_id)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
        flag = True

    except:
        textToWrite = b"Error updating values on GATEWAY_PROPERTIES\n"
        exceptions.exceptionHandler(textToWrite)
        flag = False

    mysqlClose(mydbConnector,myCursor)
    return flag

def InsertGateway_HistoryKamstrup(cVectorTimestamps,timestamp,alarm,CELL_ID,battery,GATEWAY_PROPERTIES_id,value, name, sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO n8htgo8_fivecomm.GATEWAY_HISTORY (timestamp,accumulated,CELL_ID,battery, GATEWAY_PROPERTIES_id, value, name, sigtec, `5G_RSRP`, `5G_RSRQ`,`G5_RSSI` ,`5G_SINR`, `5G_TX_POW`, `4G_RSRP`, `4G_RSRQ`, `4G_SINR`, `4G_RSSI`, `4G_TX_POW`, `3G_RSCP`, `3G_ecio`, kamstrupPayload,alarmKamstrup) VALUES(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );"
        # to check
        tmpString =  str(cVectorTimestamps)
        val = (timestamp,0,CELL_ID,int(battery),GATEWAY_PROPERTIES_id,str(value), str(name), sigtec, G5_RSRP, G5_RSRQ,G5_RSSI, G5_SINR, G5_TX_POW, G4_RSRP, G4_RSRQ, G4_SINR, G4_RSSI, G4_TX_POW, G3_RSCP, G3_ecio,tmpString,alarm)
        myCursor.execute(sql, val)
        
    except Exception as ex:
        textToWrite = b"Error inserting values on GATEWAY_HISTORY from kamtrup\n",ex
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

def insertDates(temperature, pression, volume):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "INSERT INTO n8htgo8_fivecomm.DATES (Volume, Temperature, Pressure, id_GATEWAY_PROPERTIES) VALUES (%s, %s, %s, %s);"
            
        val = (volume,pression,temperature,22)
        #############################################################################################################################################################################################
        myCursor.execute(sql, val)
        flag = True

    except Exception as ex:
        textToWrite = b"Error inserting values on Dates\n"
        exceptions.exceptionHandler(textToWrite)
        flag = False

    mysqlClose(mydbConnector,myCursor)
    return flag

