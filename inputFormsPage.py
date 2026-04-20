import streamlit as st
from info import incidentTypes ,affectedScopeTemp
st.title("🛡️ SOC Lite Dashboard")
st.subheader("View, Report & Analyse Cybersecurity Incidents.")

if "guest" not in st.session_state:
    st.session_state.guest = False

if  st.session_state.guest:
    name = st.text_input("Full Name:")
else:
    name = "guest"

st.session_state.guest = st.checkbox("Report as a guest")
text = st.text_input("Write a report title")
rating = st.slider("What is the severity?",float(0.0),10.0,step=0.1)
severity = "Low"

if(rating>=9.0):
    severity="Critical"
elif(rating>=7.0):
    severity="High"
elif(rating >=4.0):
    severity= "Medium"

    
type = st.selectbox(
    "What type of incident did you discover?",incidentTypes
)
description = st.text_area(
    "Write a full explanation of the incident below:",
    max_chars=500,
    height=150,
    placeholder="Enter detailed description..."
)
target = st.multiselect(
    "Select affected scope",
    [ item for values in affectedScopeTemp.values() for item in values]
)

datetime=st.date_input("Select the time where this issue was found")
uploaded_info = st.file_uploader("Upload images for clarification (optional)",type=["png","jpg","jpeg"])
if(st.button("Submit")):
    st.write(f"{text} reported successfully :)")
    st.write(f"The severity category is : {severity}")
    st.write(f"The severity type is : {type}")