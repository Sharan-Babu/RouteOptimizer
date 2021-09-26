# Import necessary libraries
import streamlit as st
from streamlit_folium import folium_static
import folium
from folium.plugins import MousePosition, Draw
import requests

# Page configs
st.set_page_config(page_title="Route", page_icon="📍")
st.title("Route Optimizer🗺️")

st.markdown("Calculates meetup point for drivers to hand-over deliverables.")

# Location Input Form
st.subheader('Coordinates')
st.caption('Sample data filled')
form = st.form('inputs')

## driver 1
col_1, col_2 = form.columns(2)

d1_lat = col_1.text_input("Driver 1 Latitude 🚴","39.94961")
d1_long = col_2.text_input("Driver 1 Longitude 🚴","-75.15028")

# driver 2
col_3, col_4 = form.columns(2)

d2_lat = col_3.text_input("Driver 2 Latitude 🗾","39.95005")
d2_long = col_4.text_input("Driver 2 Longitude 🗾","-75.16035")

# destination 1
col_5, col_6 = form.columns(2)

dst_lat = col_5.text_input("Destination 1 Latitude 🌏","39.95382")
dst_long = col_6.text_input("Destination 1 Longitude 🌏","-75.15794")

# destination 2
col_7, col_8 = form.columns(2)

dst2_lat = col_7.text_input("Destination 2 Latitude 🗾","39.95497")
dst2_long = col_8.text_input("Destination 2 Longitude 🗾","-75.15273")

# new point
col_A, col_B = form.columns(2)
new_point = [39.94559, -75.15962]
np_lat = col_A.text_input("New Point Latitude 🚴","39.94559")
np_long = col_B.text_input("New Point Longitude 🚴","-75.15962")
new_point[0], new_point[1] = float(np_lat), float(np_long)
form.write("")
submit_button = form.form_submit_button('Get Route')

# Get routes
if submit_button:
	# Center Map
	st.title("Directions")
	with st.spinner("Getting directions..."):

		# Create Map objects
		m = folium.Map(location=[float(d1_lat), float(d1_long)], zoom_start=15)
		m2 = folium.Map(location=[float(d1_lat), float(d1_long)], zoom_start=15)

		# Coordinates on hover
		MousePosition().add_to(m)
		MousePosition().add_to(m2)

		# Draw on map
		Draw().add_to(m)
		Draw().add_to(m2)

		# Add Driver 1 Marker
		folium.Marker(
		    [float(d1_lat), float(d1_long)], popup="Driver 1", tooltip="Driver 1", icon=folium.Icon(color='green')
		).add_to(m)

		folium.Marker(
		    [float(d1_lat), float(d1_long)], popup="Driver 1", tooltip="Driver 1", icon=folium.Icon(color='green')
		).add_to(m2)

		# Add Destination 1 marker
		folium.Marker(
		    [float(dst_lat), float(dst_long)], popup="Destination 1", tooltip="Destination 1"
		).add_to(m)

		folium.Marker(
		    [float(dst_lat), float(dst_long)], popup="Destination 1", tooltip="Destination 1"
		).add_to(m2)

		# Add Destination 2 marker
		folium.Marker(
		    [float(dst2_lat), float(dst2_long)], popup="Destination 2", tooltip="Destination 2", icon=folium.Icon(color='green')
		).add_to(m)

		folium.Marker(
		    [float(dst2_lat), float(dst2_long)], popup="Destination 2", tooltip="Destination 2", icon=folium.Icon(color='green')
		).add_to(m2)

		# Get directions
		def get_directions(d1_lat,d1_long,d2_lat,d2_long):
			URL = "https://atlas.microsoft.com/route/directions/json?subscription-key=vxBYJRnuVWb9WErEip_dx2WkD8DJhl1ji4LLsCF_lec&api-version=1.0&query={},{}:{},{}".format(d1_lat, d1_long, d2_lat, d2_long)
			response = requests.get(URL)
			response = response.json()
			#st.json(response)

			# Decode json
			# route coordinates
			base = response["routes"][0]
			points = base["legs"][0]["points"]
			distance = base["summary"]["lengthInMeters"]
			duration = round((base["summary"]["travelTimeInSeconds"]/60),3)

			# coordinates array
			coords = [[float(d1_lat), float(d1_long)]]

			for x in points:
				coords.append([float(x["latitude"]), float(x["longitude"])])

			coords.append([float(d2_lat), float(d2_long)])

			# meet point coordinates
			midpoint = coords[len(coords)//2]

			# meet duration
			half_duration = duration / 2

			return coords, midpoint, distance, duration, half_duration

		# driver1 to driver2
		coords, midpoint1, distance1, duration1, half_duration1 = get_directions(d1_lat,d1_long,d2_lat,d2_long)	

		# driver1 to midpoint
		coords2, midpoint2, distance2, duration2, half_duration2 = get_directions(d1_lat,d1_long,midpoint1[0],midpoint1[1])	
		folium.PolyLine(coords2, color="lightgreen", popup="Route 1", tooltip="Route 1", weight=4.5, opacity=1).add_to(m)

		# driver2 to midpoint
		coords3, midpoint3, distance3, duration3, half_duration3 = get_directions(d2_lat,d2_long,midpoint1[0],midpoint1[1])	
		folium.PolyLine(coords3, color="red", popup="Route 2", tooltip="Route 2", weight=3.5, opacity=0.5).add_to(m)
		

		# Destination marker
		folium.Marker(
		    [float(d2_lat), float(d2_long)], popup="Driver 2", tooltip="Driver 2"
		).add_to(m)

		folium.Marker(
		    [float(d2_lat), float(d2_long)], popup="Driver 2", tooltip="Driver 2"
		).add_to(m2)

		# Meet point Marker
		folium.Marker(
		    midpoint1, popup="Meet Point", tooltip="Meetup point", icon=folium.Icon(color='pink')
		).add_to(m)

		# New delivery/destination point
		# Replace with Desirable location in the form [latitude,longitude]
		#new_point = [39.94559, -75.15962]
		
		folium.Marker(
		    new_point, popup="New Point", tooltip="New Point", icon=folium.Icon(color='orange')
		).add_to(m)

		folium.Marker(
		    new_point, popup="New Point", tooltip="New Point", icon=folium.Icon(color='orange')
		).add_to(m2)


		# midpoint to destination 1
		coords4, midpoint4, distance4, duration4, half_duration4 = get_directions(midpoint1[0],midpoint1[1],dst_lat,dst_long)	
		folium.PolyLine(coords4, color="green", popup="Route 3", tooltip="Route 3", weight=4.5, opacity=1).add_to(m)

		# destination 1 to destination 2
		coords5, midpoint5, distance5, duration5, half_duration5 = get_directions(dst_lat,dst_long, dst2_lat, dst2_long)	
		folium.PolyLine(coords5, color="green", popup="Route 4", tooltip="Route 4", weight=4.5, opacity=1).add_to(m)

		# driver2 to destination 1
		coords6, midpoint6, distance6, duration6, half_duration6 = get_directions(d2_lat,d2_long, dst_lat, dst_long)
		folium.PolyLine(coords6, color="blue", popup="Route 1", tooltip="Route 1", weight=3.5, opacity=1).add_to(m2)

		# driver1 to destination 2
		coords7, midpoint7, distance7, duration7, half_duration7 = get_directions(d1_lat,d1_long, dst2_lat, dst2_long)
		folium.PolyLine(coords7, color="green", popup="Route 2", tooltip="Route 2", weight=3.5, opacity=1).add_to(m2)

		# destination1 to new point
		coords8, midpoint8, distance8, duration8, half_duration8 = get_directions(dst_lat,dst_long, new_point[0], new_point[1])
		folium.PolyLine(coords8, color="blue", popup="Route 3", tooltip="Route 3", weight=4.5, opacity=0.5).add_to(m2)

		# midpoint to new point
		coords9, midpoint9, distance9, duration9, half_duration9 = get_directions(midpoint1[0],midpoint1[1], new_point[0], new_point[1])
		folium.PolyLine(coords9, color="red", popup="Route 5", tooltip="Route 5", weight=4.5, opacity=0.2).add_to(m)

		# Render map
		st.header("Classic")
		folium_static(m2)

		st.write("")

		st.header("Meet Approach")
		folium_static(m)


		st.write("")
		st.write("")

		# Display Metrics
		col_9, col_10, col_11 = st.columns(3)

		# Classic Approach Metrics
		col_9.markdown("#### Classic Approach:")
		classic_distance = distance6+distance7+distance8
		classic_duration = round((duration6+duration7+duration8),3)
		col_9.markdown(f"**Distance**: {classic_distance} meters")
		col_9.markdown(f"**Duration**: {classic_duration} minutes")

		# Optimized Approach Metrics
		col_10.markdown("#### Optimized Approach:")
		optimized_distance = distance2+distance3+distance4+distance5+distance9
		optimized_duration = round((duration2+duration3+duration4+duration5+duration9),3)
		col_10.markdown(f"**Distance**: {optimized_distance} meters")
		col_10.markdown(f"**Duration**: {optimized_duration} minutes")

		# Cost of meeting Metrics
		col_11.markdown("#### Cost of Meeting:")
		meet_distance = distance2 + distance3
		meet_duration = round((duration1 + duration2),3)
		col_11.markdown(f"**Meet Distance**: {meet_distance} meters")
		col_11.markdown(f"**Meet Duration**: {meet_duration} minutes")

		# Analysis
		if optimized_distance < classic_distance:
			st.success(f"{classic_distance-optimized_distance} meters saved 🚲")
			st.success("Drivers should meet! 🤝")
		else:
			st.info("Classic Approach is better")	