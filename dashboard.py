import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime, timedelta
from info import affectedTargetsTypes, severityKeys, reporters, incidentTypes, ratingToSeverity


def dashboardPage():
    start = datetime(2025, 10, 27)
    end = datetime.now()
    reports = []
    for _ in range(250):
        tempRating = round(np.random.uniform(0, 10), 1)
        reports.append({
                "name": reporters[np.random.randint(0, len(reporters))],
                "title": "",
                "type": incidentTypes[0],
                "rating": tempRating,
                "severity": ratingToSeverity(tempRating),
                "description": "",
                "time":  (start + timedelta(seconds=np.random.randint(0, int((end - start).total_seconds())))).date(), # random date between 27 of october 2025 (the date I started bughunting) and today's date
                "affectedTargets": np.random.choice(
                    affectedTargetsTypes,
                    size=np.random.randint(1, len(affectedTargetsTypes) + 1),
                    replace=False
                ).tolist()
        })

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
  
    chart = alt.Chart(chartData).mark_bar().encode( # Here I had to use ai cause it was complex to do by my own lol 
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


    st.title("Incidents Dashboard")
    st.subheader("Reporters Stats")
    st.altair_chart(chart, use_container_width=True)

 
def getDateList(reports):
    datelist = []
    for report in reports:
        datelist.append(report["time"])
    return datelist
