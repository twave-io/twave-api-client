#!/bin/env python

import os
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
ASSET_ID = 'LDzwedpc8t6'
SPEC_ID = '1ZVxCGEOtNS'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

spec_ids = api.list_spectra(ASSET_ID)
print("Spectrum IDs:", spec_ids)
print(api.get_spec_meta(ASSET_ID, SPEC_ID))

times = api.list_spec_data(ASSET_ID, SPEC_ID)

sp = api.get_spectrum(ASSET_ID, SPEC_ID, t=times[0])
print("Created at:", sp.created_at)

plt.plot(*sp.get_data())
plt.xlim([0, sp.meta.max_freq])
plt.ylim(0)
plt.grid(True)
plt.title(sp.meta.name)
plt.ylabel(sp.meta.unit)
plt.show()
