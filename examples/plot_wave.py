#!/bin/env python

import os
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
ASSET_ID = '46CfUrVW0rt'
WAVE_ID = 'GG3apjmArtm'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

wave_ids = api.list_waves(ASSET_ID)
print("Wave IDs:", wave_ids)
print(api.get_wave_meta(ASSET_ID, WAVE_ID))

wf = api.get_wave(ASSET_ID, WAVE_ID)
print(wf.meta)
print("Created at:", wf.created_at)
print("Started at:", wf.started_at)

plt.plot(*wf.get_data())
plt.xlim([0, wf.get_duration()])
plt.grid(True)
plt.title(wf.meta.name)
plt.ylabel(wf.meta.unit)
plt.show()
