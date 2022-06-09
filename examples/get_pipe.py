#!/bin/env python

import os
from twave_client import TWaveClient


host = 'api.adif.twave.io'
token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')

asset_id = 'IM2mkWVgGLl'

api = TWaveClient(host, token)

pipe_ids = api.list_pipes(asset_id)
print("Pipeline IDs:", pipe_ids)

pipe_id = pipe_ids[0]
print(api.get_pipe_meta(asset_id, pipe_id))

print(api.list_pipe_data(asset_id, pipe_id))
