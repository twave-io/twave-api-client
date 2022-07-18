#!/bin/env python

import os
import numpy as np
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
ASSET_ID = '46CfUrVW0rt'
METRIC_ID = '57k3sguoBfC'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

#  print(api.list_assets())
#  print(api.get_asset(asset_id))

# print(api.get_metrics(asset_id))

print(api.get_metric(ASSET_ID, METRIC_ID))

trend = api.get_trend(ASSET_ID, METRIC_ID, window='5m')
t, y = trend.get_data()
t = np.array(t, dtype='datetime64[s]')


plt.plot(t, y)
plt.grid(True)
plt.title(trend.meta.name)
plt.show()
