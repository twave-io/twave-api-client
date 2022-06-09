#!/bin/env python

import os
import matplotlib.pyplot as plt
from twave_client import TWaveClient


host = 'api.adif.twave.io'
token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')

asset_id = 'IM2mkWVgGLl'
metric_id = '7PLJmFKUeWf'

api = TWaveClient(host, token)

#  print(api.list_assets())
#  print(api.get_asset(asset_id))

# print(api.get_metrics(asset_id))

print(api.get_metric(asset_id, metric_id))

trend = api.get_trend(asset_id, metric_id, window='5m')

plt.plot(*trend.get_data())
plt.title(trend.meta.name)
plt.show()
