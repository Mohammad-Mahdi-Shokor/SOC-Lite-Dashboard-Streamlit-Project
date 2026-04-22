
import streamlit as st
from info import incidentTypes, affectedTargetsTypes, ratingToSeverity, addReport

@st.dialog("Thanks for reporting!")
def submitAReport():
    st.subheader("Your report has been added to the reports list :)")

st.title("Report an Incident")

if "isGuest" not in st.session_state:
    st.session_state.isGuest = False

is_guest = st.checkbox("Report as a guest", key="isGuest")

if isinstance(affectedTargetsTypes, dict):
    affected_options = [item for values in affectedTargetsTypes.values() for item in values]
else:
    affected_options = affectedTargetsTypes

with st.form("Report an Incident"):
    name = st.text_input(
        "Full Name:",
        placeholder="guest" if is_guest else "Enter your full name"
    )

    title = st.text_input("Write a report title")
    rating = st.slider("What is the severity?", 0.0, 10.0, step=0.1)
    severity = ratingToSeverity(rating)
    incident_type = st.selectbox("What type of incident did you discover?", incidentTypes)

    description = st.text_area(
        "Write a full explanation of the incident below:",
        max_chars=500,
        height=150,
        placeholder="Enter detailed description..."
    )

    targets = st.multiselect("Select affected scope", affected_options)

    found_date = st.date_input("Select the time where this issue was found")
    uploaded_info = st.file_uploader(
        "Upload images for clarification (optional)",
        type=["png", "jpg", "jpeg"]
    )

    submitted = st.form_submit_button("Submit")

if submitted:
    effective_name = "guest" if is_guest else name.strip()
    if (not is_guest) and (len(effective_name) < 3):
        st.error("Name should be at least 3 characters")
    elif(len(title.strip())<3):
        st.error("Title should be at least 3 characters")
    elif  description.strip()=="":
        st.error("Description is incorrect format")
    elif   targets==[]:
        st.error("Please select at least one affected target")
    else:
        addReport(
    name="guest" if is_guest else name,
    title=title,
    type=incident_type,
    rating=rating,
    severity=severity,
    description=description,
    time=str(found_date),
    affectedTargets=targets,
)
        st.success("Report submitted.")
        submitAReport()

