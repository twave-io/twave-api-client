#!/bin/env python

import os
import pandas as pd
import matplotlib.pyplot as plt
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

spectra = api.list_spectra()

# create a dataframe from the spectra and print it
df = pd.DataFrame(spectra)
print(df.sort_values(by='name'))

# list the snapshots for the first spectrum
spec = spectra[0]
times = api.list_spectrum_data(spec.id)
print("Timestamps:", times)

# get the last snapshot of the spectrum
sp = api.get_spectrum(spec.id, timestamp='last')
print(sp.meta)
print("Created at:", sp.created_at)

plt.plot(*sp.get_data())
plt.xlim([0, sp.max_freq])
plt.ylim(0)
plt.grid(True)
plt.title(sp.meta.name)
plt.ylabel(sp.meta.unit)
plt.show()
