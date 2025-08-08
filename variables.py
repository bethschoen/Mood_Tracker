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
journal_blob_name = "journal.json"
mood_calendar_blob_name = "mood_calendar.jsonl"
anxiety_calendar_blob_name = "anxiety_calendar.jsonl"

mood_colors = {
    "Red":"#F08080",
    "Orange":"#FBCEB1",
    "Yellow":"#FFFACD",
    "Green":"#D0F0C0",
    "Blue":"#7C9ED9",
    "Purple":"#CCCCFF",
}

mood_data_filename = "moods.csv"