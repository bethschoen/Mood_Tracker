import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def initialise_session_state() -> None:

    if "frequent_words" not in st.session_state:
        frequent_words = ut.analyse_word_frequency(st.session_state["journal_data"], vr.custom_stop_words)
        st.session_state["frequent_words"] = frequent_words

def display_diary_entry(event_id):
    # get event info
    event_info = st.session_state["journal_data"][event_id]

    # datetime title
    event_datetime = datetime.strptime(event_info["datetime"], "%Y-%m-%dT%H:%M:%S")
    event_datetime_str = event_datetime.strftime("%d %B %Y %H:%M")
    st.markdown(f"# {event_datetime_str}")
    
    # anxiety and mood
    anxiety_mood_cols = st.columns([2, 0.2, 1])
    with anxiety_mood_cols[0]:
        ## anxiety slider
        st.markdown("### Anxiety")
        anxiety = st.select_slider(
            "Anxiety", 
            options=vr.anxiety_strings, 
            value=vr.anxiety_strings[event_info["anxiety"]-1],
            label_visibility="collapsed",
            key=event_id+"anxiety_slider"
        )
    with anxiety_mood_cols[2]:
        ## mood cards
        st.markdown("### Mood")
        ut.create_mood_tags(event_info['mood'], display=True)

    # context comments
    st.markdown("### Context and Comments")
    context_container = st.container(border=None, height=100)
    context_container.markdown(event_info["comments"])

    # thoughts, feelings, triggers
    tft_cols = st.columns(3)
    for i, element in enumerate(["thoughts", "feelings", "triggers"]):
        with tft_cols[i]:
            st.markdown(f"### {element.capitalize()}")
            element_text = event_info[element]
            # check text is not empty
            if len(element_text) > 0:
                element_text_list = element_text.split("\n")
                element_bullet_points = ut.convert_list_to_bullet_points(element_text_list)
            else:
                element_bullet_points = ""
            element_container = st.container(border=None, height=300)
            element_container.markdown(element_bullet_points, unsafe_allow_html=True)

def get_min_and_max_datetimes_recorded():

    journal_entries = st.session_state["journal_data"].values()
    datetimes = [datetime.strptime(i["datetime"], "%Y-%m-%dT%H:%M:%S") for i in journal_entries]
    oldest_date = min(datetimes).replace(hour=0, minute=0)
    newest_date = max(datetimes).replace(hour=23, minute=59)

    return (oldest_date, newest_date)

def journal():

    st.set_page_config(layout="wide")
    initialise_session_state()
    with st.sidebar:
        st.title("Journal")
        st.markdown('''
        "First of all, let me get something straight: This is a JOURNAL, not a diary."
        ''')

        st.markdown("## Filters")
        # sort all events
        ascending = "Oldest first"
        descending = "Newest first"
        ordering = st.selectbox(
            "Sort by",
            (descending, ascending),
        )

        # whitespace
        st.container(height=4, border=False)

        min_date, max_date = get_min_and_max_datetimes_recorded()
        date_range = st.slider(
            "Date filter",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD/MM/YY HH:MM",
        )
        
        # TODO: key word search
        print(st.session_state["frequent_words"])

    # get ID and datetime of all events
    all_events = []
    for event_id, event_data in st.session_state["journal_data"].items():
        # convert recorded datetime to a datetime object
        datetime_obj = datetime.strptime(event_data["datetime"], "%Y-%m-%dT%H:%M:%S")
        # check event falls within the selected date range
        if datetime_obj >= date_range[0] and datetime_obj <= date_range[1]:
            all_events.append((event_id, event_data["datetime"]))

    # sort all entries by datetime 
    ordering_map = {
        ascending: False,
        descending: True,
    }
    reverse = ordering_map[ordering]
    all_events.sort(key=lambda tup: tup[1], reverse=reverse) 
    sorted_events = [x[0] for x in all_events]    

    # display sorted, filtered events
    for event_id in sorted_events:
        display_diary_entry(event_id)
        # whitespace between entries
        st.container(height=1, border=False)
        st.divider() 
        st.container(height=1, border=False)

journal()