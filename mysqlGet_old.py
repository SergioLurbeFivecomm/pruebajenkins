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
from mysqlConnector import *
import exceptions
import math
import mysqlGet
import mysqlSet
import battery as bat
import random

def getMaxId():
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        myCursor.execute("select max(id) from GATEWAY_PROPERTIES;")
        variables = [""]
        i = 0
        for row in myCursor.fetchall():
            for tmp in row:
                variables[i]=tmp
                i+=1
        mydbConnector.commit()        
            # myCursor.close()
    except:
            textToWrite = b"Error obtaining the last id of GATEWAY_PROPERTIES\n"
            exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return variables

def getCountIdFromImei(imei):

    try:
            
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = "select count(id) from GATEWAY_PROPERTIES where imei = %s;"
        val = (imei,)
        myCursor.execute(sql, val)
        check = []
        for row in myCursor.fetchall():
                print(row)
                check.append(row)

        mysqlClose(mydbConnector,myCursor)

    except:
            textToWrite = b"Error obtaining the count of id from imei\n"
            exceptions.exceptionHandler(textToWrite)
    return check

def getIdFromImei(imei):

    try:

        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]

        sql = "select id from GATEWAY_PROPERTIES where imei = %s;"
        val = (imei,)
        myCursor.execute(sql, val)

        cId = []
        for row in myCursor.fetchall():
            cId.append(row)

        mysqlClose(mydbConnector,myCursor)
    except:
            textToWrite = b"Error obtaining the id from the imei\n"
            exceptions.exceptionHandler(textToWrite)
    return cId

def getMaxIdSystem_features():
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        myCursor.execute("select max(id) from SYSTEM_FEATURES;")
        CARACTERISTICAS_SISTEMA_id = myCursor.fetchone()
        caractSystem = CARACTERISTICAS_SISTEMA_id[0]
        
    except:
        textToWrite = b"Error obtaining the max id from SYSTEM_FEATURES\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return caractSystem

def getUserandPass(cId):

    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select user, password from MQTT_PROPERTIES where GATEWAY_PROPERTIES_id = %s;"
        val = (cId[0][0],)
        myCursor.execute(sql, val)
        CARACTERISTICAS_SISTEMA_id = myCursor.fetchone()
        user = CARACTERISTICAS_SISTEMA_id[0]
        pas = CARACTERISTICAS_SISTEMA_id[1]
    except:
        textToWrite = b"Error obtaining user and pass\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return user,pas

def getSystemFeaturesFromId(cid):
    try:

        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "SELECT SYSTEM_FEATURES_id FROM n8htgo8_fivecomm.GATEWAY_PROPERTIES where id = %s;"
        val = (cid,)
        myCursor.execute(sql, val)

        tmpRemote = myCursor.fetchall()
        systemFeatures = []
        if len(tmpRemote) != 0:
            for row in tmpRemote:
                systemFeatures.append(row)
            cSystemFeatures = systemFeatures[0][0]   
            
    except:
        textToWrite = b"Error obtaining SystemFeatures_id from current id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
    return cSystemFeatures

def getCommandFromGatewayId(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select command, gateway_id,id FROM REMOTE_CONSOLE WHERE id = (select min(id) from REMOTE_CONSOLE where executed = 0 and gateway_id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)

        vectorRemote = [] # duplicamos el tamaño para transmision y recepcion y le sumamos 2 porque es de 0 a Y * 2
        i=0
        tmpRemote = myCursor.fetchall() # posible fetchone() ?

    except:
        textToWrite = b"Error obtaining SystemFeatures_id from current id\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
    if tmpRemote == []:
        tmpRemote = "0"
    else:
        tmpRemote = tmpRemote[0][0]
    return tmpRemote

def getTimeLeakFromGateway(gateway_id):
    tmp = mysqlConnect()
    try:

        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select diameterFlow from SYSTEM_FEATURES where id=(select SYSTEM_FEATURES_id from GATEWAY_PROPERTIES where id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)
        fuga = True #leak check
        tFuga = myCursor.fetchall()# Obtain the leak time from the database based on the gateway id
        for row in tFuga:
            tmp = row
            tFuga = tmp[0]

    except:
        textToWrite = b"Error obtaining diameterFlow from system features id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return tFuga
    
def getNumberOfPulsesFromGateway(gateway_id):
    
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select ((volumeLiters)/(diameterFlow))*100 from SYSTEM_FEATURES where id = (select SYSTEM_FEATURES_id from GATEWAY_PROPERTIES where id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)
        cal = myCursor.fetchall()
        for row in cal:
            tmp = row
        nPulsos = tmp

    except:
        textToWrite = b"Error obtaining the number of pulses from system features id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return nPulsos

def getTLeakFromGateway(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select SYSTEM_FEATURES_id from GATEWAY_PROPERTIES JOIN SYSTEM_FEATURES on SYSTEM_FEATURES.id=GATEWAY_PROPERTIES.SYSTEM_FEATURES_id where GATEWAY_PROPERTIES.SYSTEM_FEATURES_id = %s;"
        values = gateway_id
        myCursor.execute(sql,(values,))
        cal = myCursor.fetchall()
        i = 0
        tmp = []
        for row in cal:
            tmp.append(row)
            i = i+1
        if tmp != []:    
            idCaracteristicas = tmp[0][0]
            tFuga = 0
        else:
            idCaracteristicas = 0
            tFuga = 0

    except Exception as ex:
        print(ex)
        textToWrite = b"Error obtaining the number of pulses from system features id leak\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return idCaracteristicas,tFuga

def getTLeakFromSystem_Features_Id(idCaracteristicas):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select name,id from ALARM where alarmType = 1 and SYSTEM_FEATURES_id = %s;"
        values = idCaracteristicas
        myCursor.execute(sql, (values,))# alarm type -> 1 for leak, 2 -> for subdimension and 3 -> for no flow                   
        cal = myCursor.fetchall()
        for row in cal:
            tmp.append(row)


    except:
        textToWrite = b"Error obtaining the alarm and id with system features id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return tmp

def getAlarmName(type):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select max(name) from ALARM where alarmType = %s;"
        val = (type,)
        myCursor.execute(sql, val)# alarm type -> 1 for leak, 2 -> for subdimension and 3 -> for no flow                   
        cal = myCursor.fetchone()
        tmp = []
        for row in cal:
            tmp.append(row)
        alarmName = tmp[0][0]

    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error obtaining the name of the alarm\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return alarmName
                           
def getAlarmId():
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        myCursor.execute("select max(id) from ALARM where alarmType = 1;")
        cal = myCursor.fetchall()
        tmp = []
        for row in cal:
            tmp.append(row)
            alarmId = tmp[0][0]
    except:
        textToWrite = b"Error obtaining the id of the alarm\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return alarmId

def GetVolumeliters(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select SYSTEM_FEATURES_id,volumeLiters from GATEWAY_PROPERTIES JOIN SYSTEM_FEATURES on SYSTEM_FEATURES.id=GATEWAY_PROPERTIES.SYSTEM_FEATURES_id where GATEWAY_PROPERTIES.id =%s;"
        val = (gateway_id,)
        myCursor.execute(sql, val)
        cal = myCursor.fetchall()
        tmp = []
        for row in cal:
            tmp.append(row) 
        idCaracteristicas = tmp[0][0]
        volumenLitros = tmp[0][1]
    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error obtaining the volumeLiters from Gateway_Properties\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return idCaracteristicas, volumenLitros

def GetIdFromSystem_Features_Id(idCaracteristicas):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select id from ALARM where SYSTEM_FEATURES_id= %s;"
        val = (idCaracteristicas,)
        myCursor.execute(sql, val)
        aId = myCursor.fetchall()
        if len(aId)!=0:
            alarmId = aId[0][0]
        else:
            alarmId = 1
    except:
        textToWrite = b"Error obtaining the alarm id from SYSTEM_FEATURES_id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return alarmId

def GetCountFromGatewayHistoryTwo(stringDate,gateway_id):
    try:
        
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "SELECT count(*) FROM GATEWAY_HISTORY where t0 = 0 and t1 = 0 and t2 = 0 and t3 = 0 and t4 = 0 and t5 = 0 and t6 = 0 and t7 = 0 and t8 = 0 and t9 = 0 and t10 = 0 and t11 = 0 and t12 = 0 and t13 =0 and t14 = 0 and t15 = 0 and t16 = 0 and t17 = 0 and t18 = 0 and t19 = 0 and t20 = 0 and t21 = 0 and t22 = 0 and t23 = 0 and t24 = 0 and timestamp >= %s and GATEWAY_PROPERTIES_id = %s"
        val = (stringDate,gateway_id)
        myCursor.execute(sql, val)
        coun = myCursor.fetchall()
        count = coun[0]


    except Exception as ex:
        print("Error consulta",ex)
        textToWrite = b"Error obtaining the alarm id from SYSTEM_FEATURES_id\n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return count

def GetSystemFeaturesIdFromGatewayHistory(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select SYSTEM_FEATURES_id from GATEWAY_PROPERTIES JOIN SYSTEM_FEATURES on SYSTEM_FEATURES.id=GATEWAY_PROPERTIES.SYSTEM_FEATURES_id where GATEWAY_PROPERTIES.id = %s;"
        val = (gateway_id,)
        myCursor.execute(sql, (val,))

        cal = myCursor.fetchall()
        del tmp
        tmp = []
        for row in cal:
            tmp.append(row)



    except:
        textToWrite = b"Error obtaining the alarm id from SYSTEM_FEATURES_id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return tmp

def GetMaxIdRemote():
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        myCursor.execute("SELECT MAX(id) FROM REMOTE_CONSOLE")
        REMOTE_CONSOLE_id = myCursor.fetchone()
        remoteId = REMOTE_CONSOLE_id[0]

    except:
        textToWrite = b"Error obtaining the max id from REMOTE_CONSOLE\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return remoteId

def GetDiamterFlowFromGatewayHistory(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select diameterFlow from SYSTEM_FEATURES where id=(select SYSTEM_FEATURES_id from GATEWAY_PROPERTIES where id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, (val,))
        fuga = True #leak check
        tFuga = myCursor.fetchall()# Obtain the leak time from the database based on the gateway id
        for row in tFuga:
            tmp = row
        tFuga = tmp[0]
    except:
        textToWrite = b"Error obtaining the diameterFlow from id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)
    return tFuga

def getLastDayReadingDates(stringDatePrevious,stringDate):
    try:
        tmp2 = mysqlConnect()
        myCursor = tmp2[1]
        mydbConnector = tmp2[0]
        tmp = []
        print(f"SELECT count(*) FROM GATEWAY_HISTORY where timestamp like '{stringDate}' order by id desc limit 1;")
        ########@####################################@#############################################################
        myCursor.execute(f"SELECT count(*) FROM GATEWAY_HISTORY where timestamp like '{stringDate}' order by id desc limit 1;")                        
        count = myCursor.fetchone()
        checkCount = count[0]
        if checkCount != 0:
        ####################################################################@#######################################
            #print(stringDate)
            # print(f"SELECT t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23 FROM GATEWAY_HISTORY where timestamp like '{stringDate}' order by id desc limit 1;")
            myCursor.execute(f"SELECT t0,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23 FROM GATEWAY_HISTORY where timestamp like '{stringDate}' order by id desc limit 1;")
            cal = myCursor.fetchone()
            i = 0   
            for row in cal:
                tmp.append(row)
                i = i+1
            # print(f"SELECT t24 FROM GATEWAY_HISTORY where timestamp like '{stringDatePrevious}' order by id desc limit 1;")
            myCursor.execute(f"SELECT t24 FROM GATEWAY_HISTORY where timestamp like '{stringDatePrevious}' order by id desc limit 1;")
            REMOTE_CONSOLE_id = myCursor.fetchone()
            if REMOTE_CONSOLE_id != None:
                t24 = REMOTE_CONSOLE_id[0]
                tmp[0] = str(int(tmp[0])+int(t24))
            else:
                t24 = 0
                tmp[0] = str(int(tmp[0])+int(t24))
                print("no tiene valor del dia anterior")
            # print(tmp)
    except:
        textToWrite = b"Error obtaining the 24 elements \n"
        exceptions.exceptionHandler(textToWrite)

    mysqlClose(mydbConnector,myCursor)

    return tmp

def getLastDayReading(serialNumber):

    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        vol = []
        myCursor.execute(f"select diameterFlow from SYSTEM_FEATURES WHERE ID = (SELECT SYSTEM_FEATURES_id from GATEWAY_PROPERTIES where id = {serialNumber});")
        cal = myCursor.fetchone()
        if cal != None and len(cal) != 0:
            for row in cal:
                vol.append(row)
        else:
            vol = 0
    except Exception as ex:
        print(ex)
        textToWrite = b"Error obtaining the volume liters\n"
        exceptions.exceptionHandler(textToWrite)
        
    mysqlClose(mydbConnector,myCursor)

    return vol

def getIdCommandFromGatewayId(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select id FROM REMOTE_CONSOLE WHERE id = (select min(id) from REMOTE_CONSOLE where executed = 0 and gateway_id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)

        vectorRemote = [] # duplicamos el tamaño para transmision y recepcion y le sumamos 2 porque es de 0 a Y * 2
        i=0
        tmpRemote = myCursor.fetchone() # posible fetchone() ?

    except:
        textToWrite = b"Error obtaining SystemFeatures_id from current id\n"
        print(textToWrite)
        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
    if tmpRemote == []:
        tmpRemote = -1
    else:
        tmpRemote = tmpRemote[0]
    return tmpRemote

def getCommandIdFromGatewayId(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select command, gateway_id,id FROM REMOTE_CONSOLE WHERE id = (select max(id) from REMOTE_CONSOLE where executed = 0 and gateway_id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)

        vectorRemote = [] # duplicamos el tamaño para transmision y recepcion y le sumamos 2 porque es de 0 a Y * 2
        i=0
        tmpRemote = myCursor.fetchall() # posible fetchone() ?

    except:
        textToWrite = b"Error obtaining SystemFeatures_id from current id\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
    if tmpRemote == []:
        tmpRemote = "0"
    else:
        tmpRemote = tmpRemote[0][2]
    return tmpRemote

# def getAllUsersPassword(gateway_id): TO DELETE?
#     try:
#         tmp = mysqlConnect()
#         myCursor = tmp[1]
#         mydbConnector = tmp[0]
#         sql= "SELECT `user`, password, GATEWAY_PROPERTIES_id FROM n8htgo8_fivecomm.MQTT_PROPERTIES;"
#         val = (gateway_id,)
#         myCursor.execute(sql, val)

#         vectorRemote = [] # duplicamos el tamaño para transmision y recepcion y le sumamos 2 porque es de 0 a Y * 2
#         i=0
#         tmpRemote = myCursor.fetchall() # posible fetchone() ?

#     except:
#         textToWrite = b"Error obtaining all the users and passwords\n"
#         print(textToWrite)

#         exceptions.exceptionHandler(textToWrite)
    
#     mysqlClose(mydbConnector,myCursor)
   
#     return tmpRemote
    
def getLastTimestamp(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "SELECT max(`timestamp`) FROM n8htgo8_fivecomm.GATEWAY_HISTORY WHERE GATEWAY_PROPERTIES_id=%s;"
        val = (gateway_id,)
        myCursor.execute(sql, val)
        tmp_return = myCursor.fetchone()

    except:
        textToWrite = b"Error obtaining all the users and passwords\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
   
    return tmp_return

def getCommandExecutedFromGatewayId(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql= "select command FROM REMOTE_CONSOLE WHERE id = (select max(id) from REMOTE_CONSOLE where executed = 1 and gateway_id = %s);"
        val = (gateway_id,)
        myCursor.execute(sql, val)

        vectorRemote = [] # duplicamos el tamaño para transmision y recepcion y le sumamos 2 porque es de 0 a Y * 2
        i=0
        tmpRemote = myCursor.fetchone() # posible fetchone() ?

    except:
        textToWrite = b"Error obtaining the command from current id\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)
    
    mysqlClose(mydbConnector,myCursor)
    return tmpRemote

def getLocationFromGatewayId(gateway_id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        vol = []
        sql= "select location from GATEWAY_PROPERTIES where id = %s;"
        val = (gateway_id,)
        myCursor.execute(sql, val)
        locationRemote = myCursor.fetchone() # posible fetchone() ?


    except Exception as ex:
        print(ex)
        textToWrite = b"Error obtaining location from current id\n"
        print(textToWrite)

        exceptions.exceptionHandler(textToWrite)    

    mysqlClose(mydbConnector,myCursor)
    return locationRemote

def getBatteryFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select battery from GATEWAY_HISTORY where GATEWAY_PROPERTIES_id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        values = myCursor.fetchone()
        tmpBattery = values[0]    
    except Exception as ex:
        print(ex)
        textToWrite = b"Error obtaining the battery parameters from Gateway Properties\n"
        exceptions.exceptionHandler(textToWrite)
        tmpBattery = 0

    mysqlClose(mydbConnector,myCursor)
    return tmpBattery

def getIMEIFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select IMEI from GATEWAY_PROPERTIES where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()
    except:
        textToWrite = b"Error obtaining the IMEI from Gateway Properties\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite

    mysqlClose(mydbConnector,myCursor)
    return value

def getLastConnectionFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select timestamp from REMOTE_CONSOLE_RESPONSE where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()
    except:
        textToWrite = b"Error obtaining last connection from Gateway Properties\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite

    mysqlClose(mydbConnector,myCursor)
    return value

def getSignalPowerFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select G5_RSSI from GATEWAY_HISTORY where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()
    except:
        textToWrite = b"Error obtaining signal power from Gateway Properties\n"
        exceptions.exceptionHandler(textToWrite)
        value = None
    mysqlClose(mydbConnector,myCursor)
    return value

def getHWversionFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select HWversion from GATEWAY_PROPERTIES where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()

    except:
        textToWrite = b"Error obtaining HW version from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = None

    mysqlClose(mydbConnector,myCursor)
    return value
def getFWversionFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select FWversion from GATEWAY_PROPERTIES where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()
        return value
    except:
        textToWrite = b"Error obtaining FW version from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = None

    mysqlClose(mydbConnector,myCursor)
    return value

def getBatteryStatusFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select battery from GATEWAY_HISTORY where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        values = myCursor.fetchone()
        tmpBattery = values[0]
        battery = int(tmpBattery)/100.0
        battery = math.ceil(battery)/10.0
        battery = bat.batteryConversion(battery,id)
        
        if battery <38000:
            value = "inactive"
        else:
            value = "active"
    except:
        textToWrite = b"Error obtaining battery status from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = None

    mysqlClose(mydbConnector,myCursor)
    return value

def getStatusFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select id from GATEWAY_HISTORY where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        values = myCursor.fetchone()
        
        if values != None:
            value = "active"
        else:
            value = "inactive"
    except:
        textToWrite = b"Error obtaining battery status from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite

    mysqlClose(mydbConnector,myCursor)
    return value

def getTxModeFromGatewayId(id):
    try:
        value = "Fixed time transmission"
    except:
        textToWrite = b"Error obtaining battery status from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite
    
    return value

def getTxIntervalFromGatewayId(id):
    try:
        value = "24 hours"
    except:
        textToWrite = b"Error obtaining battery status from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite
    return value

def getTxTimeFromGatewayId(id):
    try:
        tmp = mysqlConnect()
        myCursor = tmp[1]
        mydbConnector = tmp[0]
        sql = "select timestamp from GATEWAY_HISTORY where id = %s;"
        values = id
        myCursor.execute(sql, (values,))
        value = myCursor.fetchone()
    except:
        textToWrite = b"Error obtaining battery status from Gateway History\n"
        exceptions.exceptionHandler(textToWrite)
        value = textToWrite
    mysqlClose(mydbConnector,myCursor)
    return value

def getAllData(id):
    try:
        # tmp = mysqlConnect()
        # myCursor = tmp[1]
        # mydbConnector = tmp[0]
        # sql = "select timestamp from GATEWAY_HISTORY where id = %s;"
        # values = id
        # myCursor6.execute(sql, (values,))
        # values = myCursor6.fetchone()
        # mydbConnector6.commit()        
        # myCursor6.close()
        # mydbConnector6.close()
        volumen = random.randint(20, 50)
        presion = random.randint(30, 80)
        temperatura = random.randint(0, 100)
        values = {"Volume":volumen, "Pressure":presion, "Temperature":temperatura}
        return values
       
    except:
        textToWrite = b"Error obtaining all dates\n"
        exceptions.exceptionHandler(textToWrite)

