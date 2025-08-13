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

mood_colors_v1 = {
    "Red":"#F08080",
    "Orange":"#FBCEB1",
    "Yellow":"#FFFACD",
    "Green":"#D0F0C0",
    "Blue":"#7C9ED9",
    "Purple":"#CCCCFF",
}

light_text = "#f7f7f7"
dark_text = "#2F4F4F"

mood_colors_v2 = {
    "Positive":{
        "Red":{
            "background":"#FF6F61",
            "text":dark_text
        },
        "Orange":{
            "background":"#FFA07A",
            "text":dark_text
        },
        "Yellow":{
            "background":"#FFFF99",
            "text":dark_text
        },
        "Green":{
            "background":"#98FB98",
            "text":dark_text
        },
        "Blue":{
            "background":"#ADD8E6",
            "text":dark_text
        },
        "Purple":{
            "background":"#E6E6FA",
            "text":dark_text
        },
    },
    "Negative":{
        "Red":{
            "background":"#B22222",
            "text":light_text
        },
        "Orange":{
            "background":"#D2691E",
            "text":light_text
        },
        "Yellow":{
            "background":"#FFD700",
            "text":dark_text
        },
        "Green":{
            "background":"#556B2F",
            "text":light_text
        },
        "Blue":{
            "background":"#4682B4",
            "text":light_text
        },
        "Purple":{
            "background":"#800080",
            "text":light_text
        },
    }
}

anxiety_strings = [
    "1: Relaxed and calm",
    "2: Slight tension",
    "3: Noticeable but manageable",
    "4: Midly distracted",
    "5: Aware of myself and surroundings",
    "6: Heightened alertness",
    "7: Impaired concentration",
    "8: Significant intrusive thoughts",
    "9: Difficulty functioning in the moment",
    "10: Urgent need to escape"
]

anxiety_colors = [
    "#b3ebff",
    "#94e2ff",
    "#75daff",
    "#38caff",
    "#00a1db",
    "#008abd",
    "#005e80",
    "#004761",
    "#003142",
    "#001b24"
]

mood_calendar_key = "Mood"
anxiety_calendar_key = "Anxiety"

datetime_str_format = "%Y-%m-%dT%H:%M:%S"

# word_frequency.py
custom_stop_words = ["feel"]
text_fields = ["comments", "triggers", "feelings", "thoughts"]
word_col_name = "word"
word_count_col_name = "word_count"