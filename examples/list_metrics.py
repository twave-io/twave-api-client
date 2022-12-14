#!/bin/env python

# import os
import pandas as pd
from twave_client import TWaveClient


# HOST = 'api.adif.twave.io'
# token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
# api = TWaveClient(HOST, token)
api = TWaveClient()

assets = api.get_assets()
print(assets)

print(api.get_asset(assets[0].id))

metrics = api.get_metrics()

metric = api.get_metric(metrics[0].id)
print(metric)

assets_df = pd.DataFrame(assets)
df = pd.DataFrame(metrics)

# print the full dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df)
# print(df[['asset_id', 'asset_name', 'device', 'id', 'name']])

pipes = api.list_pipes()
pipes_df = pd.DataFrame(pipes)
print(pipes_df)

pipe = api.get_pipe_meta(pipes[0].id)
print(pipe)

waves = api.list_waves()
waves_df = pd.DataFrame(waves)
print(waves_df)

wave = api.get_wave_meta(waves[0].id)
print(wave)

spectra = api.list_spectra()
spectra_df = pd.DataFrame(spectra)
print(spectra_df)

spectrum = api.get_spec_meta(spectra[0].id)
print(spectrum)
