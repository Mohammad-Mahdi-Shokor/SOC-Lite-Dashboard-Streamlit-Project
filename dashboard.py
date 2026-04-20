import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from info import affectedTargetsTypes , incidentTypes,affectedTargetsTypes,ratingToSeverity


def dashboardPage():
    start = datetime(2025, 10, 27)
    end = datetime.now()
    reports = [] 
    for _ in range(100):
        tempRating =round(np.random.uniform(0, 10), 1)
        reports.append ({"name":"guest",
                "title":"",
                "type":incidentTypes[0],
                "rating":tempRating,
                "severity":ratingToSeverity(tempRating),
                "description":"",
                "time":start + timedelta( seconds=np.random.randint(0, int((end - start).total_seconds())))
        })
    st.write (reports)

 
    
    
