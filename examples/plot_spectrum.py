#!/bin/env python

import os
import matplotlib.pyplot as plt
from twave_client import TWaveClient


host = 'api.adif.twave.io'
token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')

asset_id = 'IM2mkWVgGLl'
spec_id = '2S5UGhrYvjw'

api = TWaveClient(host, token)

#  print(api.list_spec_data(asset_id, spec_id))

sp = api.get_spectrum(asset_id, spec_id)

plt.plot(*sp.get_data())
plt.xlim([0, sp.meta.max_freq])
plt.ylim(0)
plt.grid(True)
plt.title(sp.meta.name)
plt.ylabel(sp.meta.unit)
plt.show()
