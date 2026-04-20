import streamlit as st 
from PIL import Image
from inputFormsPage import reportPage 
from dashboard import dashboardPage
st.sidebar.title("Control Panel")

screen = st.sidebar.radio(
    "Select Screen",
    ["Report Screen","Dashboard","Search Page"]
)
if screen =="Report Screen":
    reportPage()
elif screen =="Dashboard":
    dashboardPage()