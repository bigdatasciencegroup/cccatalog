import logging
import os
import re
import requests
import time
import json
import argparse
import random
from datetime import datetime, timedelta

PATH    = os.environ['OUTPUT_DIR']

def writeToFile(_data, _name):
    outputFile = '{}{}'.format(PATH, _name)

    if len(_data) < 1:
        return None

    logging.info('Writing to file => {}'.format(outputFile))

    with open(outputFile, 'a') as fh:
        for line in _data:
            if line:
                fh.write('\t'.join(line) + '\n')


def sanitizeString(_data):
    if _data is None:
        return ''

    _data = _data.strip()
    _data = _data.replace('"', "'")
    _data = re.sub(r'\n|\r', ' ', _data)

    return re.sub(r'\s+', ' ', _data)


def delayProcessing(_startTime, _maxDelay):
    minDelay = 1.0

    #subtract time elapsed from the requested delay
    elapsed       = float(time.time()) - float(_startTime)
    delayInterval = round(_maxDelay - elapsed, 3)
    waitTime      = max(minDelay, delayInterval) #time delay between requests.

    logging.info('Time delay: {} second(s)'.format(waitTime))
    time.sleep(waitTime)


def requestContent(_url):
    logging.info('Processing request: {}'.format(_url))

    try:
        response = requests.get(_url)

        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            logging.warning('Unable to request URL: {}. Status code: {}'.format(url, response.status_code))
            return None

    except Exception as e:
        logging.error('There was an error with the request.')
        logging.info('{}: {}'.format(type(e).__name__, e))
        return None
