import streamlit as st 
from PIL import Image
from inputFormsPage import reportPage 
# st.sidebar.title("Control Panel")

# screen = st.sidebar.radio(
#     "Select Screen",
#     ["Report Screen","Dashboard","Search Page"]
# )
# if screen =="Report Screen":
#     reportPage()
# elif screen =="Dashboard":
st.set_page_config(layout="centered")
page = st.navigation(
    [
        st.Page("inputFormsPage.py",title="Report An Incident"),
        st.Page("dashboard.py",title="Dashboard"),
        st.Page("search.py",title="Search")
    ],
    position='top'
)
page.run()