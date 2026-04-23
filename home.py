import streamlit as st 
st.set_page_config(layout="centered")
page = st.navigation(
    [
        st.Page("welcome.py", title="Welcome", icon="🏠"),
        st.Page("dashboard.py", title="Dashboard", icon="📊"),
        st.Page("search.py", title="Search", icon="🔎"),
        st.Page("inputFormsPage.py", title="Report An Incident", icon="📝")
    ],
    position='top'
)
page.run()