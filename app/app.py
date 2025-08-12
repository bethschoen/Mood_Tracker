import streamlit as st
import pandas as pd
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import variables as vr

# Page Navigation
pages = [    
    st.Page("pages/data_analysis.py", title="Home", icon="📅", default=True),
    st.Page("pages/data_entry.py", title="Journal Entry", icon="📝"),
    st.Page("pages/journal.py", title="Journal View", icon="📖"),
    st.Page("pages/data_edit.py", title="Edit", icon="📝")
]

pg = st.navigation(pages)

# Running the app
pg.run()