# What is the typical difference between the input and output pressure of the compressor?

import os
import pandas as pd
from cognite.client import CogniteClient

os.environ['COGNITE_API_KEY'] = 'MmM5NGUxYzQtOGE1Ny00ZDJkLWEzYTItMGQ4ZjM0NTFkZTAw' 
os.environ['COGNITE_CLIENT_NAME'] = 'Denis' 
os.environ['COGNITE_PROJECT'] = 'publicdata' 

c = CogniteClient()
c.login.status()

# 23-FCV-96193: VRD - PH PURGE 1 ST.COMP. MOTOR
asset_id = 2209766572772321
comp_motor = c.assets.retrieve(id=asset_id)

time_series = comp_motor.time_series() 
