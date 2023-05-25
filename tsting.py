import mysqlGet
import mysqlSet
import aesDecoder
from datetime import datetime, timedelta
from narrowSender import *
#from pytz import timezone
#import pytz

imei = 866897040457113
 
sender = narrowSender(imei)
sender.send()