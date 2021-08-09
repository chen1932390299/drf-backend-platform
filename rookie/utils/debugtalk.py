import  string
import  random
from random import randrange
import time
import datetime
import uuid
import  base64


def __RandomString(string_type:string,range_start,range_end):
        length = random.randint(range_start,range_end)
        if  not length or  not isinstance(length,int):
            length = 8
        samples =  string.ascii_letters+string.digits
        if string_type == 'letters':
            samples = string.ascii_letters
        if string_type == 'digits':
            samples = string.digits
        return  ''.join(random.sample(samples,length))

def  __RandomInt(start,end):
   samples =  string.digits
   return  int(''.join(random.sample(samples,random.randint(start,end))))

def __RandomTimeStamp(start_date,end_date):
    """
    :param start_date: 2021-7-4 11:22:11
    :param end_date: 2021-7-22 11:22:11
    :return:
    """
    start_timestamp = time.mktime(time.strptime(start_date, '%Y-%m-%d %H:%M:%S'))
    end_timestamp = time.mktime(time.strptime(end_date, '%Y-%m-%d %H:%M:%S'))
    time_gen =  time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(randrange(start_timestamp, end_timestamp)))
    return datetime.datetime.strptime(time_gen, '%Y-%m-%d %H:%M:%S').timestamp()

def __Time(decimal_max_places=3):
    timestamp =  time.time()
    if not isinstance(decimal_max_places,int):
        decimal_max_places = 3
    if decimal_max_places:
        timestamp =  int(time.time()*10**decimal_max_places)
    return timestamp


def  __UUID1():

    return  uuid.uuid1().hex

def __Base64(string):
    byte = bytes(str(string),encoding='utf-8')
    data = base64.b64encode(byte)
    return data