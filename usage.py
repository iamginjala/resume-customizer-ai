import pandas as pd
import os
import streamlit as st



PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))        # .../Job application assistant
db_path = os.path.join(PROJECT_ROOT, "DATA", "resume.db")


conn  = st.connection("resume_db",type="sql",url=f'sqlite:///{db_path}')

usage_df = conn.query("select * from usage_records;",ttl=0)

st.dataframe(usage_df)