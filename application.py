import pandas as pd
import os
import streamlit as st
from sqlalchemy import text


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))        # .../Job application assistant
db_path = os.path.join(PROJECT_ROOT, "DATA", "resume.db")


conn  = st.connection("resume_db",type="sql",url=f'sqlite:///{db_path}')


apps_df = conn.query("select id,company,role,status,applied_at,notes from applications order by applied_at desc;",ttl=0)

st.dataframe(apps_df)

if apps_df.empty:
    st.info("No applications yet.")
    st.stop()

apps_df["label"] = apps_df["company"] + " — " + apps_df["role"]
selected_label = st.selectbox("Select an application", apps_df["label"])
selected_row = apps_df[apps_df["label"] == selected_label].iloc[0]

STATUS_OPTIONS = ["applied","recruiter_ping","interview","offer","closed","rejected"]

with st.form("edit_application"):
    company = st.text_input("Company",value=selected_row["company"])
    role = st.text_input("Role",value=selected_row["role"])
    status = st.selectbox("Status",STATUS_OPTIONS,index=STATUS_OPTIONS.index(selected_row["status"]))
    notes = st.text_area("Notes",value=selected_row["notes"] or "")
    if st.form_submit_button("Save Changes"):
        with conn.session as s:
            s.execute(
                text("UPDATE applications SET company=:company,role=:role,status=:status,notes=:notes WHERE id =:id"),
                {"company":company,"role":role,"status": status, "notes":notes,"id":int(selected_row["id"])}
            )

            s.commit()
        st.success("Updated.")
        st.rerun()


st.divider()
confirm = st.checkbox("Confirm delete this also deletes linked resume versions")
if st.button("Delete this application", type="secondary", disabled=not confirm):
    with conn.session as s:
        s.execute(text("DELETE FROM resume_versions WHERE application_id=:id"), {"id": int(selected_row["id"])})
        s.execute(text("DELETE FROM applications WHERE id=:id"), {"id": int(selected_row["id"])})
        s.commit()
    st.success("Deleted.")
    st.rerun()
