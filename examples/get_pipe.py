#!/bin/env python

import os
from twave_client import TWaveClient


HOST = 'api.adif.twave.io'
ASSET_ID = 'IM2mkWVgGLl'

token = os.environ.get('API_TOKEN', 'MY_API_TOKEN')
api = TWaveClient(HOST, token)

pipe_ids = api.list_pipes(ASSET_ID)
print("Pipeline IDs:", pipe_ids)

pipe_id = pipe_ids[0]
print(api.get_pipe_meta(ASSET_ID, pipe_id))

print(api.list_pipe_data(ASSET_ID, pipe_id))
