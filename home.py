from pathlib import Path
import streamlit as st


st.set_page_config(layout="centered")

base_dir = Path(__file__).parent
page = st.navigation(
    [
        st.Page(str(base_dir / "welcome.py"), title="Welcome", icon="🏠"),
        st.Page(str(base_dir / "dashboard.py"), title="Dashboard", icon="📊"),
        st.Page(str(base_dir / "search.py"), title="Search", icon="🔎"),
        st.Page(str(base_dir / "inputFormsPage.py"), title="Report An Incident", icon="📝"),
        st.Page(str(base_dir / "chat.py"), title="Chatbot", icon="🤖"),
    ],
    position="top",
)
page.run()