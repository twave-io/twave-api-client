#!/bin/env python

import os
import time
from multiprocessing import Pool
import requests
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
WAVE_ID = '1IhCLMgOwoa'
RETRIES = 4

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')

client = TWaveClient(HOST, token, timeout=1)


def download_wave(t):
    # retry if the request times out
    for _ in range(RETRIES):
        try:
            wave = client.get_wave(WAVE_ID, timestamp=t)
        except requests.exceptions.ReadTimeout:
            print("Timeout at", t)
            time.sleep(1)
        else:
            print(f"Downloaded wave at {wave.created_at}")
            return wave

    raise Exception("Timeout")



times = client.list_wave_data(WAVE_ID, start=1693983600, stop=1694070000)
print("Timestamps:", times)

with Pool(10) as p:
    p.map(download_wave, times)
