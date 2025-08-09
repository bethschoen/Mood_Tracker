import pandas as pd
import os
import sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

local_style_dir = "assets/styles.css"
docker_style_dir = "/assets/styles.css"
style_dir = local_style_dir

data_dir = "data"
journal_blob_name = "journal.json"

mood_data_filename = "moods.csv"
mood_col_name = "Mood"
color_col_name = "Color"
sentiment_col_name = "Sentiment"
color_int_col_name = "Color Int"

mood_colors = {
    "Red":"#F08080",
    "Orange":"#FBCEB1",
    "Yellow":"#FFFACD",
    "Green":"#D0F0C0",
    "Blue":"#7C9ED9",
    "Purple":"#CCCCFF",
}