from storage import get_attendance, clear_attendance
import pandas as pd
import streamlit as st

st.header("Attendance History")
st.set_page_config(page_title="History")

@st.dialog("Clear all records?")
def clear_dialog():
    submitted = st.button("Clear", on_click=clear_attendance)
    if submitted:
        st.rerun()
        

df = pd.DataFrame(get_attendance())
if not df.empty:
    st.dataframe(df)
    st.button("Clear All", on_click=clear_dialog)
else:
    st.warning("Attendance history is empty.")
