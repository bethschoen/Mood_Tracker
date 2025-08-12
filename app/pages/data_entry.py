# optional and required fields 
import streamlit as st
import uuid
import json

import sys
import os
current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', '..')))

import variables as vr
import utils as ut

def data_entry():

    st.set_page_config(layout="wide")

    with st.sidebar:
        st.title("Add a Journal Entry")
        st.markdown('''
        Record your thoughts and feelings here.
        ''')
        st.write('Made with ❤️ by Beth')

    # form for submitting new journal entry
    data = ut.journal_form()
        
    # update project dataset with new submission
    if data:
        entry_id = str(uuid.uuid4())
        # save new data entry to session state
        ut.record_journal_data(entry_id, data)
        # navigate to calendar view
        st.switch_page("pages/data_analysis.py")

data_entry()