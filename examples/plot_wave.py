#!/bin/env python

import os
import pandas as pd
import matplotlib.pyplot as plt
from twave_client import TWaveClient

HOST = 'api.adif.twave.io'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

waves = api.list_waves()

# create a dataframe from the waves and print it
df = pd.DataFrame(waves)
print(df.sort_values(by='name'))

# list the snapshots for the first wave
wave = waves[0]
times = api.list_wave_data(wave.id)
print("Timestamps:", times)

# get the last snapshot of the wave
wf = api.get_wave(wave.id, timestamp='last')
print(wf.meta)
print("Created at:", wf.created_at)
print("Started at:", wf.started_at)

plt.plot(*wf.get_data())
plt.xlim([0, wf.get_duration()])
plt.grid(True)
plt.title(wf.meta.name)
plt.ylabel(wf.meta.unit)
plt.show()
