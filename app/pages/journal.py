import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime
import os, sys
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def show_slider_visual(value, min_val=0, max_val=100):
    fig, ax = plt.subplots(figsize=(6, 1))
    ax.plot([min_val, max_val], [0, 0], 'k-', lw=2)
    ax.plot(value, 0, 'ro', markersize=10)
    ax.set_xlim(min_val, max_val)
    ax.axis('off')
    ax.annotate(value, xy=(0, value))
    ax.annotate(value, xy=(-10, value))
    st.pyplot(fig)

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
            label_visibility="collapsed"
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
            element_text = event_info[element].split("\n")
            element_bullet_points = ut.convert_list_to_bullet_points(element_text)
            element_container = st.container(border=None, height=300)
            element_container.markdown(element_bullet_points, unsafe_allow_html=True)
    

def journal():

    st.set_page_config(layout="wide")
    with st.sidebar:
        st.title("Journal")
        st.markdown('''
        "First of all, let me get something straight: This is a JOURNAL, not a diary."
        ''')

        st.markdown("## Filters")
        # TODO: option for ordering diary
        # option for search

    for event_id in st.session_state["journal_data"].keys():
        display_diary_entry(event_id)
        # whitespace
        st.container(height=3, border=False)

journal()