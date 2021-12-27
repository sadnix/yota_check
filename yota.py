import os
import uuid
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import logging
import logging.handlers
from datetime import datetime
from pytz import timezone
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(__file__, '../'))

ylog = logging.getLogger('ylogger')
ylog.setLevel(logging.DEBUG)

def timetz(*args):
    return datetime.now(tz).timetuple()

tz = timezone('Europe/Moscow')

logging.Formatter.converter = timetz

handler = logging.handlers.TimedRotatingFileHandler(os.path.join(BASE_DIR, 'yota.log'), when="midnight", interval=1, backupCount=30)
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(filename)s %(lineno)d %(threadName)s - %(message)s"))
ylog.addHandler(handler)

s = requests.Session()
try:
    resp = s.get("http://ya.ru", allow_redirects=False)
    ylog.debug('Connection established')
except Exception as e:
    # Modem not found or not connected
    ylog.debug('Connection error: %s'%(e))
    exit()

# if redirect from http to https then connection established
if resp.headers['Location'] != 'https://ya.ru/':

    # generate transaction number for header
    transaction = str(uuid.uuid4())

    headers = {
        'User-agent':       'Mozilla/5.0 (Windows NT 6.1; WOW64) ApaymentIdleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'x-transactionid':  transaction,
        'Content-Type':     'application/json',
    }

    url = "https://hello.yota.ru/wa/v1/service/temp"

    # two variants:
    # first: if device on free tariff then restart once per day
    data = '{"serviceCode":"light"}'
    try:
        resp = s.post(url, data=data, headers=headers)
        ylog.debug([url, data, resp.status_code, resp.text, resp.headers])
    except Exception as e:
        ylog.debug('Error: POST not sended %s: %s'%(data, e))

    if resp.status_code != 200:
        # second: if not free tariff and not money on account
        # restart once per 2 hours
        data='{"serviceCode":"sa"}'
        try:
            resp = s.post(url, data=data, headers=headers)
            ylog.debug([url, data, resp.status_code, resp.text, resp.headers])
        except Exception as e:
            ylog.debug('Error: POST not sended %s: %s'%(data, e))
