from storage import get_attendance, clear_attendance
import pandas as pd
import streamlit as st

df = pd.DataFrame(get_attendance())
st.dataframe(df)
st.button("Clear All", on_click=clear_attendance)