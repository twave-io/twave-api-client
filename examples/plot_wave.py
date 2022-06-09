#!/bin/env python

import os
import matplotlib.pyplot as plt
from twave_client import TWaveClient


host = 'api.adif.twave.io'
token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')

asset_id = 'IM2mkWVgGLl'
wave_id = 'CIMuCiALPZx'

api = TWaveClient(host, token)

#  print(api.list_wave_data(asset_id, wave_id))

wf = api.get_wave(asset_id, wave_id)

plt.plot(*wf.get_data())
plt.xlim([0, wf.get_duration()])
plt.grid(True)
plt.title(wf.meta.name)
plt.ylabel(wf.meta.unit)
plt.show()
