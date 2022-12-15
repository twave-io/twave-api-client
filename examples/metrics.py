#!/bin/env python

import os
from twave_client import TWaveClient

HOST = 'api.adif.twave.io'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

# get all assets
assets = api.list_assets()
print(assets)

# get the first asset
print(api.get_asset(assets[0].id))

# get all metrics
metrics = api.list_metrics()

# get the first metric
print(api.get_metric(metrics[0].id))
