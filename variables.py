import pandas as pd
import os
import sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

local_assets_dir = "assets/styles.css"
docker_assets_dir = "/assets/styles.css"
assets_dir = local_assets_dir

# https://portal.azure.com/#@BupaCore.onmicrosoft.com/resource/subscriptions/ff0c268c-9ffc-4003-8708-108e23191f6e/resourceGroups/rg-ainsten-0001prod/providers/Microsoft.Storage/storageAccounts/stwq3eja2m5mce4prod/storagebrowser
data_dir = "data"
journal_blob_name = "journal.jsonl"
mood_calendar_blob_name = "mood_calendar.jsonl"
anxiety_calendar_blob_name = "anxiety_calendar.jsonl"

colours = [
    "#8DC0E8",
    "#0D1846",
    "#56DBDB",
    "#007D79",
    "#022B30",
    "#9439FE",
    "#D02670",
]