#!/bin/env python

import os
import pandas as pd
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
# ASSET_ID = 'Cl8xACci15o'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

asset_ids = api.list_assets()
print(asset_ids)

all_metrics = []
assets_by_id = {}

for asset_id in asset_ids:
    asset = api.get_asset(asset_id)
    assets_by_id[asset_id] = asset
    print(f"Asset: {asset.id} ({asset.description})")

    metrics = api.get_metrics(asset_id)
    all_metrics.extend(metrics)


df = pd.DataFrame(all_metrics)
df['asset_name'] = df['asset_id'].apply(lambda x: assets_by_id[x].name)
df['device'] = df['asset_id'].apply(lambda x: assets_by_id[x].description)

# print the full dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df[['asset_id', 'asset_name', 'device', 'id', 'name']])
