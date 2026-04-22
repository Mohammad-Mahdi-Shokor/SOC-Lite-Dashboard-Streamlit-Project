import streamlit as st
import pandas as pd
from info import  incidentTypes
from datetime import date
import math
import streamlit as st
from info import incidentTypes ,reports

def parse_report_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)  # expects 'YYYY-MM-DD'

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
if "search" not in st.session_state:
    st.session_state.search = ""


st.text_input(
    "Search by name",
    placeholder="Search By Name",
    label_visibility="collapsed",
    key="search", # connect to session_state :)
)
typeColumn,RatingColumn,DateRange = st.columns([30,40,30])

if "type" not in st.session_state:
    st.session_state.type = []
with typeColumn:
    st.multiselect(
        "Select Type",
        incidentTypes,
        placeholder="type",
        key="type"
    )
   

if "minRating" not in st.session_state:
    st.session_state.minRating = 0.0
if "maxRating" not in st.session_state:
    st.session_state.maxRating = 10.0

with RatingColumn:
    col1, col2 = st.columns([1, 1])

    with col1:
        min_rating = st.number_input(
            "Min rating",
            min_value=0.0,
            max_value=10.0,
            step=0.1,
            format="%.1f",
            key="minRating",
        )

    with col2:
        max_rating = st.number_input(
            "Max rating",
            min_value=min_rating,
            max_value=10.0,
            step=0.1,
            format="%.1f",
            key="maxRating",
        )
if "dateRange" not in st.session_state:
    st.session_state.dateRange = (date(2025, 10, 27), date.today())
with DateRange:
    picked = st.date_input(
    "Select date range",
    value=st.session_state.dateRange,
    format="DD-MM-YYYY",)

if isinstance(picked, (list, tuple)) and len(picked) == 2:
    st.session_state.dateRange = (picked[0], picked[1])

startDate, endDate = st.session_state.dateRange

st.write("\n\n")
searchReports = [
    report
    for report in reports
    if st.session_state.search.lower() in report["name"].lower()
    and (st.session_state.minRating <= float(report["rating"]) <= st.session_state.maxRating)
    and (
        report["type"] in st.session_state.type
        or st.session_state.type == []
    )
    and startDate <= parse_report_date(report["time"]) <= endDate
]


titleCols = st.columns([24,23,10,15,30]) # the percentage of each column (I made 10% for rating and severity cause they are small text :} ) 
rowsPerTable = 10
cols = ["name","type","rating","time","affectedTargets"]
numOfTables = math.ceil(len(searchReports) / rowsPerTable)

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

for i in range((st.session_state.tableNumber - 1) * rowsPerTable, min((st.session_state.tableNumber) * rowsPerTable, len(searchReports))):
    report = searchReports[i]
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
    
    if(i <  min((st.session_state.tableNumber) * rowsPerTable, len(searchReports))-1):
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
