import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from info import affectedTargetsTypes , incidentTypes,affectedTargetsTypes,ratingToSeverity


def dashboardPage():
    start = datetime(2025, 10, 27)
    end = datetime.now()
    tempRating =round(np.random.uniform(0, 10), 1)
    reports = [{"name":"guest",
                "title":"",
                "type":incidentTypes[0],
                "rating":tempRating,
                "severity":ratingToSeverity(tempRating),
                "description":"",
                "time":start + timedelta( seconds=np.random.randint(0, int((end - start).total_seconds())))
                }] #first one is sample so I understand how the list of maps would look like
    
    
    st.write (reports)

 
    
    
