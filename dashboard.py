import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from info import severityKeys, reporters,reports



# just to be clear, I love writing comments :)
st.title("🛡️ SOC Lite Dashboard")
st.subheader("View, Report & Analyse Cybersecurity Incidents.")

start = datetime(2025, 10, 27)
end = datetime.now()
reportsDf = pd.DataFrame(reports)
reportsDf["time"] = pd.to_datetime(reportsDf["time"])
dailyCounts = reportsDf.groupby("time").size().reset_index(name="count")
allDates = pd.DataFrame({
    "time": pd.date_range(
        start=pd.to_datetime("2025-10-27"), #start date of line graph
        end=pd.Timestamp.today().normalize(), # end date of line graph
        freq="D" # steps (1 day)
    )
})
dailyFull = allDates.merge(dailyCounts, on="time", how="left")
dailyFull["count"] = dailyFull["count"].fillna(0).astype(int)
#heatmap realted content (view commented code on line 94 for more info)
heatmapData = dailyFull.copy()
heatmapData["week"] = heatmapData["time"].dt.strftime("%Y-%U")
heatmapData["weekday"] = heatmapData["time"].dt.day_name().str[:3]
weekdayOrder = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
heatmapData["month"] = heatmapData["time"].dt.strftime("%b")
heatmapData["day"] = heatmapData["time"].dt.day
reportersStats = {name: {s: 0 for s in severityKeys} for name in reporters}
for report in reports:
    reporterName = report["name"]
    sev = report["severity"]
    if sev in reportersStats[reporterName]:
        reportersStats[reporterName][sev] += 1
reportersStatsDf = pd.DataFrame.from_dict(reportersStats, orient="index")
reportersStatsDf = reportersStatsDf.reset_index().rename(columns={"index": "Reporter"})
severityColors = ["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"] # colors for each severity (Low to Critical)
chartData = reportersStatsDf.melt(
    id_vars="Reporter",
    value_vars=[sev for sev in severityKeys if sev in reportersStatsDf.columns],
    var_name="Severity",
    value_name="Count"
) 

chart = alt.Chart(chartData).mark_bar().encode( # Here I had to use ai cause it was complex to do by my own lol (I know how to make a normal bar chart but not like this)
    x=alt.X("Reporter:N", title="Reporter"),
    y=alt.Y("Count:Q", title="Incidents"),
    color=alt.Color(
        "Severity:N",
        scale=alt.Scale(domain=severityKeys, range=severityColors),
        sort=severityKeys,
        legend=alt.Legend(title="Severity")
    ),
    order=alt.Order("Severity:N", sort="ascending")
) # untill here, I know what code is doing but I can't write it by my own
pieData = reportsDf["severity"].value_counts().reindex(severityKeys, fill_value=0).reset_index()
pieData.columns = ["severity", "count"]
# Pie chart with Altair
pieChart = alt.Chart(pieData).mark_arc().encode(
    theta="count:Q",
    color=alt.Color("severity:N", scale=alt.Scale(domain=["Low", "Medium", "High", "Critical"], 
                                                     range=["#2ecc71", "#f1c40f", "#e67e22", "#e74c3c"])),
    tooltip=["severity:N", "count:Q"]
).properties(width=280, height=280)

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Reporters Stats")
    st.altair_chart(chart, use_container_width=True)
with col2:
    st.subheader("Severity Pie")
    st.altair_chart(pieChart, use_container_width=False)
# st.subheader("Incidents Per Day")
# st.line_chart(dailyFull.set_index("time")["count"])
# tis was a heatmap that I don;t know how to make, but I vibecoded it, uncomment underneath code to view it :) (it is like the commit heatmap of github)
st.subheader("Incident Activity Heatmap")
heatmapChart = alt.Chart(heatmapData).mark_rect(cornerRadius=2).encode(
    x=alt.X("week:N", title="Week", axis=alt.Axis(labelAngle=0, labelPadding=4)),
    y=alt.Y("weekday:N", sort=weekdayOrder, title="Day"),
    color=alt.Color("count:Q", title="Incidents", scale=alt.Scale(scheme="greens")),
    tooltip=[
        alt.Tooltip("time:T", title="Date"),
        alt.Tooltip("count:Q", title="Incidents")
    ]
).properties(height=220)

st.altair_chart(heatmapChart, use_container_width=True)

