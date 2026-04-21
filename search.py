import streamlit as st
import pandas as pd
from info import reports, incidentTypes
import math

header_divider = """
<hr style="
    border: none;
    height: 2px;
    background: linear-gradient(90deg, #a5b4fc 0%, #60a5fa 45%, #38bdf8 100%);
    border-radius: 999px;
    margin: 8px 0 10px 0;
">
"""

row_divider = """
<hr style="
    border: none;
    border-top: 1px dashed #d1d5db;
    margin: 8px 0;
    opacity: 0.9;
">
"""

severity_color_map = {
    "Low": "#22c55e",
    "Medium": "#eab308",
    "High": "#f97316",
    "Critical": "#ef4444",
}

st.title("Incidents Reports")
search = st.text_input("",placeholder="Search By Name")
typeColumn,RatingColumn = st.columns(2)
with typeColumn:
    st.selectbox(
        "Select Type",
        incidentTypes,
        index=None,
        placeholder="type"
    )
with RatingColumn:
    col1, col2 = st.columns([1, 1])

    with col1:
        min_rating = st.number_input("Min rating", 0.0, 10.0, 0.0, 0.1)

    with col2:
        max_rating = st.number_input("Max rating", min_rating, 10.0, 10.0, 0.1)

st.write("\n\n")
titleCols = st.columns([24,23,10,15,30]) # the percentage of each column (I made 10% for rating and severity cause they are small text :} ) 
rowsPerTable = 12
cols = ["name","type","rating","time","affectedTargets"]
numOfTables = math.ceil(len(reports) / rowsPerTable)

if "tableNumber" not in st.session_state:
    st.session_state.tableNumber = 1

#shape one : each column has a divider under it 
# for i in range(len(cols)):
#     with titleCols[i]:
#         st.markdown(f"**{cols[i]}**")
#         st.markdown(header_divider, unsafe_allow_html=True)
#         for b in range((st.session_state.tableNumber - 1) * rowsPerTable, min((st.session_state.tableNumber) * rowsPerTable, len(reports))):
#             if cols[i] == "affectedTargets":
#                 st.markdown(" ".join([
#                     f'<span style="background:#eef2ff;color:#3730a3;padding:4px 10px;border-radius:999px;margin-right:6px;font-size:12px;">{t}</span>'
#                     for t in reports[b][cols[i]]
#                 ]), unsafe_allow_html=True)

#             elif cols[i]=="rating":
#                 severity = reports[b]["severity"]
#                 rating_value = reports[b][cols[i]]
#                 st.markdown(
#                     f'<span style="background:{severity_color_map.get(severity, "#9ca3af")};color:white;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;">{rating_value}</span>',
#                     unsafe_allow_html=True
#                 )
                
#             else:
#                 st.write(reports[b][cols[i]])
            
#             if(b <  min((st.session_state.tableNumber) * rowsPerTable, len(reports))-1):
#                 st.markdown(row_divider, unsafe_allow_html=True)

#shape two: whole row have one divider under it
for i in range(len(cols)):
    with titleCols[i]:
        st.markdown(f"**{cols[i]}**")
    
st.markdown(header_divider, unsafe_allow_html=True)

for i in range((st.session_state.tableNumber - 1) * rowsPerTable, min((st.session_state.tableNumber) * rowsPerTable, len(reports))):
    report = reports[i]
    contentCols = st.columns([24,23,10,15,30])
    for j in range(len(cols)):
        with contentCols[j]:
            if cols[j] == "affectedTargets":
                st.markdown(" ".join([
                    f'<span style="background:#eef2ff;color:#3730a3;padding:4px 10px;border-radius:999px;margin-right:6px;font-size:12px;">{t}</span>'
                    for t in report[cols[j]]
                ]), unsafe_allow_html=True)
            elif cols[j] == "rating":
                severity = report["severity"]
                rating_value = report[cols[j]]
                st.markdown(
                    f'<span style="background:{severity_color_map.get(severity, "#9ca3af")};color:white;padding:4px 10px;border-radius:999px;font-size:12px;font-weight:600;">{rating_value}</span>',
                    unsafe_allow_html=True
                )
            else:
                st.write(report[cols[j]])
    
    if(i <  min((st.session_state.tableNumber) * rowsPerTable, len(reports))-1):
        st.markdown(row_divider, unsafe_allow_html=True)


st.write("\n\n")
maxPerRow = 10
numberOfRows = math.ceil(numOfTables/10)
tablesNums = st.columns(maxPerRow, gap="small")
for i in range(numOfTables):
    pageNumber = i + 1
    with tablesNums[i%10]:
        if st.button(
                str(pageNumber),
                key=f"{pageNumber}",
                type="primary" if st.session_state.tableNumber == pageNumber else "secondary"
            ):
                st.session_state.tableNumber = pageNumber
                st.rerun()
    # st.rerun()
