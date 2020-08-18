import streamlit as st
import pandas as pd
import numpy as np

#st.title("Hello World!")
#st.markdown("### This is my first streamlit application")
DATA_URL = (
"Motor_Vehicle_Collisions_-_Crashes.csv"
)

st.title("Motor Vehicle Collision in NYC")
st.markdown("This application is a streamlit dashboard that can be used to check collisions in NYC city."
" Add some emoji here.")

@st.cache(persist=True)
def get_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[["CRASH_DATE", "CRASH_TIME"]])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis="columns", inplace=True)
    data.rename(columns={"crash_date_crash_time":"date/time"}, inplace=True)
    return data

data = get_data(100000)


st.header("Where are the most people injured in NYC?")
injured_people = st.slider("No of people injured", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a givn time of a day?")
hour = st.selectbox("Hour to look at", range(0, 24), 1)
data = data[data['date/time'].dt.hour == hour]


if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
