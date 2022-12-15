#!/bin/env python

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
METRIC_NAME = 'PT100_1.val'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

# get the first metric with the given name
metrics = api.list_metrics(name=METRIC_NAME)
metric = metrics[0]

print(metric)

# get last year of data
start_time = time.time() - 3600 * 24 * 7 * 52*10
trend = api.get_trend(metric.id, start=start_time, window='5m')
t, y = trend.get_data()
t = np.array(t, dtype='datetime64[s]')

plt.plot(t, y)
plt.grid(True)
plt.title(trend.meta.name)
plt.show()
