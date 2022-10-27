#!/bin/env python

import os
import time
import numpy as np
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
ASSET_ID = '46CfUrVW0rt'
# METRIC_ID = '57k3sguoBfC'
METRIC_ID = '5id7EjsUHOd'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

print(api.get_metric(ASSET_ID, METRIC_ID))

# get last week of data
start_time = time.time() - 3600 * 24 * 7
trend = api.get_trend(ASSET_ID, METRIC_ID, start=start_time, window='5m')
t, y = trend.get_data()
t = np.array(t, dtype='datetime64[s]')

plt.plot(t, y)
plt.grid(True)
plt.title(trend.meta.name)
plt.show()
