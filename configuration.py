from pathlib import Path
from storage import load_name_imgpath, remove_image
import streamlit as st 

@st.dialog("Remove student from database?",)
def remove_student(row):
    clicked = st.button("Remove")
    if clicked:
        remove_image(row)
        st.rerun()

st.title("Configuration")
st.set_page_config("Configuration")

st.header("Students")
data = load_name_imgpath()
if not data:
    st.warning("No student images in database.")

imgs = [Path(row["filepath"]) for row in data]


with st.container():
    for row in data:
        col1, col2 = st.columns([3, 1], vertical_alignment="center")
        with col1:
            st.image(Path(row["filepath"]), caption=row["name"], width=100)
        with col2:
            st.button("Remove", key=row["name"], on_click=remove_student, args=(row,))
