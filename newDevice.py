    # /* ===================================================== 
    # 
    # * Copyright (c) 2022, Fivecomm - 5G COMMUNICATIONS FOR FUTURE INDUSTRY        VERTICALS S.L. All rights reserved. 
    # 
    # * File_name scriptRecepcionV33
    # 
    # * Description:  The main file of the mqtt platform
    # 
    # * Author:  Alejandro
    # 
    # * Date:  25-08-21
    # 
    # * Version:  1.33
    # 
    # * =================================================== */ 
import mysql.connector
import random
import string
import os
import sys
import time
from datetime import datetime
import exceptions
import mysqlGet
import mysqlSet
import timeHandler
import mqttConect


def setDevice(msg,length_of_string, vectorTopicTx,vectorTopicRx):
    """This is an fuction that sets the board in to the vectors and in tot the
        database.
        For that purpose the board must be registered on the mqtt broker
        Args:
            msg(mqtt object)
            length_of_string(int) 
            vectorTopicTx(Vector of strings)
            vectorTopicRx(Vector of strings)

        Returns:
            vectorTopic(Tuple of two vectors of strings)
        Raises:
            Exception: Error handling topic Vectors
            This error should appear if the value of the database is wrong 
            i.e. is a string
    """

    # default values
    name = 't1'
    client = 't1'
    device_type = "FIVECOMM LITE 5G"
    location = "default"
    description = "default"
    CREDENTIALS_id = 1 # increase if other client is using the code
    diameter = 15
    tLeak = 1 #temporal values
    volumeLiters = 15 #temporal values
    flowdiameter = 15 #temporal values

    try:

        try:
            messageReceivedDecoded = msg.payload.decode()
            mqttRecieved = messageReceivedDecoded.split(";") 
        except:
            textToWrite = b"Error decoding the a1 topic message\n"
            exceptions.exceptionHandler(textToWrite)

        try:

            if mqttRecieved[0] != None and str(mqttRecieved[0]).isnumeric():
                imei = str(mqttRecieved[0])
            if mqttRecieved[1] != None:
                tim = mqttRecieved[1]
            
            check = mysqlGet.getCountIdFromImei(imei)
            if int(check[0][0]) > 0:
                properties = mysqlGet.getAllFromImei(imei)
                networked = check[2][0]
                id = check[0][0]
            else:
                print("Incorrect IMEI from the device")
                vectorTopicTx = 0
                vectorTopicRx = 0

            if check[0][0] == 0:

                    ########################################################################## It can be optimized by generating a default username and password at startup and if it is used it is regenerated
                    user = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)) # random string generator, should obtain it from DB
                    pas = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string)) #random string generator
                    user = "PMhEI6OEn1"
                    pas = "2lLsOQRuVI"
                    ############################################################################################################################
                    t1 = "t"+str(imei) 
                    t2 = "r"+str(imei)
                    #check no more than 10 characters if so, change the letter
                    msg2 = {'user': user, 'pass':pas,'timestamp':'120','topic1':t1,'topic2':t2}
                    client3 =  mqttConect.mqttConect("p3")
                    result = client3.publish(t2, str(msg2)) 

                    # print(f"sended")
                    # os.system(f'docker exec app_mqtt_1 rabbitmqctl add_user {user} {pas}')
                    # os.system(f'docker exec app_mqtt_1 rabbitmqctl set_permissions -p / {user} ".*" ".*" ".*"')
                    # os.system(f'docker exec app_mqtt_1 rabbitmqctl set_user_tags {user} management')
                        
                    #########################################################################################################
                    ################### From here the information of the database is created and stored #####################
                    mysqlSet.insertMQTT_properties(id, user, pas, t1, t2)
                    ##### INSERT TO GATEWAY_PROPERTIES ##########cId############################################################
                    timestamp = datetime.utcnow()
                    mysqlSet.insertDevice_properties(imei, networked, timestamp)
                    #########################################################################################################
                    #########################################################################################################
                    vectorTopicTx.append(t1)
                    vectorTopicRx.append(t2)
            else:
                # t1 = "t"+str(imei) 
                # t2 = "r"+str(imei)
                # cTime = int(tim)
                # cDate = datetime.utcnow()
                # cWakeUp = int(datetime.timestamp(cDate.replace(hour=12,minute=30)))      
                # if(cTime>cWakeUp):
                #     cWakeUp = timeHandler.obtainWakeUp()                        
                    
                # user,pas = mysqlGet.getUserandPass(cId)
                # msg2 = '{"user": {user},"pass":{pass},"timestamp":{timestamp},"topic1":{topic1},"topic2":{topic2}}'
                # # msg2 = {'user': user, 'pass':pas,'timestamp':str(int(cWakeUp-cTime)),'topic1':t1,'topic2':t2}
                # msg2 = {'user': user, 'pass':pas,'timestamp':'120','topic1':t1,'topic2':t2}

                # client2 =  mqttConect.mqttConect("p3")
                # result = client2.publish(t2, str(msg2)) 
                # time.sleep(0.01)

                # print("result",result)
                None
            
        except mysql.connector.Error as e:
            try:
                print ("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
            except IndexError:
                print ("MySQL Error: %s" % str(e))
                
            except TypeError as e:
                print(e)
            except ValueError as e:
                print(e)
        except:
            print(sys.exc_info() )
            print("other kind of error")

        return vectorTopicTx,vectorTopicRx

    except:
        textToWrite = b"Error with a1\n"
        exceptions.exceptionHandler(textToWrite)     