'''
NOTE: UNUSED AND INCOMPLETE SCRIPT. 
FOR BAYAESIAN BLEND, THE CSV DATA WAS DOWNLOADED MANUALLY FROM THE WEB PAGE
'''

import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("CM_KEY")
if not TOKEN:
    raise RuntimeError("CM_KEY missing in environment (.env)")

API = "https://api.carbonmapper.org/api/v1/catalog/plumes/annotated"
params = {
    "gas": "CO2",
    "bbox": "49.33,25.62,49.44,25.70",
    "start": "2024-01-01T00:00:00Z",
    "end":   "2025-12-31T23:59:59Z",
    "quality[]": ["good","questionable"],
    "sort": "desc",
    "limit": 200
}

r = requests.get(API, headers={"Authorization": f"Bearer {TOKEN}"}, params=params, timeout=60)
r.raise_for_status()
items = r.json()["items"]
df = pd.json_normalize(items)
# Columns you'll want:
# df[["scene_timestamp","gas","emission_auto","emission_uncertainty_auto",
#     "plume_quality","wind_speed_avg_auto","wind_direction_avg_auto","plume_id"]]
