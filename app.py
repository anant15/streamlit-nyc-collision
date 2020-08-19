import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

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
original_data = data

st.header("Where are the most people injured in NYC?")
injured_people = st.slider("No of people injured", 0, 19)
st.map(data.query("injured_persons >= @injured_people")[["latitude", "longitude"]].dropna(how="any"))

st.header("How many collisions occur during a givn time of a day?")
#hour = st.sidebar.slider("Hour to look at", 0, 23)
hour = st.slider("Hour to look at", 0, 23)
data = data[data['date/time'].dt.hour == hour]

midpoint = (np.average(data["latitude"]), np.average(data["longitude"]))

st.markdown("Vehicle collision between %i:00 and and %i:00" % (hour, (hour+1)%24))
st.write(pdk.Deck(
	map_style="mapbox://styles/mapbox/light-v9",
	initial_view_state = {
	"latitude":midpoint[0],
	"longitude":midpoint[1],
	"zoom":11,
	"pitch":50
	},
	layers = [
		pdk.Layer(
		"HexagonLayer",
		data = data[['date/time', 'latitude', 'longitude']],
		get_position = ['longitude', 'latitude'],
		radius = 100,
		extruded = True,
		pickable = True,
		elevation_scale = 4,
		elevation_range=[0, 1000],
		)
	],
))


st.subheader("Breakdown by minute between %i:00 and %i:00 hours" % (hour, (hour+1)%24))
hist = np.histogram(data["date/time"].dt.minute, bins=60, range=(0, 60))[0]
chart_data = pd.DataFrame({'minute': range(0, 60), 'crashes': hist})
fig = px.bar(chart_data, x="minute", y="crashes", hover_data=["minute", "crashes"], height=400)
st.write(fig)

st.header("Top 5 streets by affected type")
select = st.selectbox("Affected type of people", ["Pedestrians", "Cyclists", "Motorists"])

if select == "Pedestrians":
	st.write(original_data.query("injured_pedestrians >= 1") \
	[["on_street_name", "injured_pedestrians"]] \
	.sort_values(by=["injured_pedestrians"], ascending = False) \
	.dropna(how="any")[:5])
if select == "Cyclists":
	st.write(original_data.query("injured_cyclists >= 1") \
	[["on_street_name", "injured_cyclists"]] \
	.sort_values(by=["injured_cyclists"], ascending = False) \
	.dropna(how="any")[:5])
if select == "Motorists":
	st.write(original_data.query("injured_motorists >= 1") \
	[["on_street_name", "injured_motorists"]] \
	.sort_values(by=["injured_motorists"], ascending = False) \
	.dropna(how="any")[:5])

if st.checkbox("Show Raw Data", False):
    st.subheader("Raw Data")
    st.write(data)
