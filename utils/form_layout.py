import streamlit as st
from datetime import datetime
import json

import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..')))

import variables as vr
import utils as ut

def journal_form(journal_entry:dict=None):
    
    if journal_entry is None:
        journal_entry = {}

    datetime_str = journal_entry.get("datetime")
    if datetime_str:
        default_date = datetime.strptime(datetime_str, vr.datetime_str_format).date()
        default_time = datetime.strptime(datetime_str, vr.datetime_str_format).time()
    else:
        default_date = "today"
        default_time = "now"

    default_moods = journal_entry.get("mood", None)
    default_anxiety = journal_entry.get("anxiety", 5)
    default_comments = journal_entry.get("comments", "")
    default_thoughts = journal_entry.get("thoughts", "")
    default_feelings = journal_entry.get("feelings", "")
    default_triggers = journal_entry.get("triggers", "")

    # form for editing information - existing values will already be present in the text boxs/information submission boxes to maintain existing details
    with st.form(border=True, key="info_change"):
        cols = st.columns(2)
        # DATE AND TIME
        with cols[0]:
            datetime_cols = st.columns([0.6, 0.4])
            with datetime_cols[0]:
                date = st.date_input("Date & Time", default_date)
            with datetime_cols[1]:
                time = st.time_input("time", default_time, label_visibility="hidden")

        # MOOD(S)
        with cols[1]:
            moods = st.multiselect(
                "Mood", 
                st.session_state["positive_tags"] + st.session_state["negative_tags"], 
                default=default_moods
            )

        # ANXIETY
        def stringify(i:int = 0) -> str:
            return vr.anxiety_strings[i-1]
        
        anxiety = st.select_slider(
            "Anxiety", 
            options=list(range(1, 11)), 
            value=default_anxiety,
            format_func=stringify
        )
        
        # COMMENTS
        comments = st.text_area(
            "Context and Comments", 
            default_comments,
            help="What situation are you in that is influencing your mood?"
        )
        
        # THOUGHTS
        thoughts = st.text_area(
            "Thoughts",             
            default_thoughts,
            help="What's running through your mind?\nUse a new line to separate bullet points."
        )

        # FEELINGS
        feelings = st.text_area(
            "Feelings", 
            default_feelings,
            help="How are these thoughts and stimuli making you feel?\nUse a new line to separate bullet points."
        )

        # TRIGGERS
        triggers = st.text_area(
            "Triggers", 
            default_triggers,
            help="What external stimuli are influencing your thoughts and feelings?\nUse a new line to separate bullet points."
        )

        # with submit, create ID
        submit = st.form_submit_button(label = 'Save')
        if submit:
            date_str = date.strftime("%Y-%m-%d")
            time_str = time.strftime("%H:%M:00")
            data = {
                "datetime":date_str + "T" + time_str,
                "mood":moods,
                "anxiety":anxiety,
                "thoughts":thoughts.strip(),
                "feelings":feelings.strip(),
                "triggers":triggers.strip(),
                "comments":comments.strip()
            }
        
            return data

def save_json_data_locally():
    # update local file
    data_loc = os.path.join(vr.data_dir, vr.journal_blob_name)
    with open(data_loc, 'w') as f:
        json.dump(st.session_state["journal_data"], f)

def record_journal_data(entry_id: str, data: dict) -> None:

    # save new data entry to session state
    st.session_state["journal_data"][entry_id] = data
    # update recorded moods in session state
    st.session_state["recorded_moods"] = list(set(st.session_state["recorded_moods"] + data["mood"]))
    # update local file
    save_json_data_locally()

    return None