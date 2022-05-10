"""
Class: CS230--Section 3
Name: Samantha Duong
Description: Final Project: Fast Food Restaurants in the United States
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk

st.title("CS 230 Final Project")

import time
my_bar = st.progress(0)
for percent_complete in range(100):
    time.sleep(0.1)
    my_bar.progress(percent_complete + 1)

from PIL import Image
image = Image.open('unhealthiest-fast-food-2020.webp')
st.image(image, caption='')

with st.sidebar:
    your_name = st.text_input("Enter name: ", "")
st.write(f"Hello {your_name}! Here is some information about fast food restaurants in the United States.")

# first chart
df = pd.read_csv("Fast Food Restaurants.csv",
                 header=0,
                 names=["ID", "Added", "Updated", "Address", "Categories", "City", "Country", "Keys", "Latitude", "Longitude", "Name", "Postal Code", "State", "SourceURLS", "Websites"])

df2 = df.groupby('State').count()['Name']
st.subheader('Number of Fast Food Restaurants in Each State')
st.bar_chart(df2)

# second chart
with st.sidebar:
    options = st.multiselect('State',
        (["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]))

newdf = pd.DataFrame()
for o in options:
    newdf = newdf.append(df[df['State']==o])

df3 = newdf.groupby('State').count()['Name']
st.subheader('Number of Fast Food Restaurants in the Selected States')
st.bar_chart(df3)


# third chart
def names(df):
    names_list = []
    for ind, row in df.iterrows():
        if row['Name'] not in names_list:
            names_list.append(row["Name"])
    names_list.sort()
    return names_list


names_list = names(df)
with st.sidebar:
    option2 = st.selectbox('Restaurant Name', names_list)

df5 = df[df['Name'] == option2]
df4 = df5.groupby('State').count()['Name']
st.subheader('Number of Selected Fast Food Restaurant Name in Each State')
st.bar_chart(df4)


# map
locations = [("Milk Street Cafe", 42.357, -71.057588),
             ("McDonald's", 42.338242, -71.106394),
             ('B.GOOD', 42.357762, -71.058363),
             ("Panda Express", 42.348883, -71.081814),
             ("Raising Cane's", 42.351916, -71.118713),
             ("Burger King", 42.386021, -71.008839),
             ("Wendy's", 42.354092, -71.058994),
             ("Dunkin' Donuts", 42.272674, -71.0692),
             ("Dunkin' Donuts", 42.337545, -71.108778),
             ("Domino's Pizza", 42.363053, -71.064517),
             ("Dairy Queen", 42.338891, -71.107222),
             ("Hilton Boston Logan Airport", 42.378136, -71.02868),
             ("Raising Cane's Chicken Fingers", 42.35197, -71.11869),
             ("Dunkin Donuts", 42.35143, -71.12163),
             ("Chipotle Mexican Grill", 42.35067, -71.04644),
             ("b.good", 42.34033, -71.08965)
             ]

df1 = pd.DataFrame(locations, columns=["NAME", "LATITUDE", "LONGITUDE"])

st.subheader("Map Showing the Locations of Fast Food Restaurants in the United States")

map_df = df.filter(['Name','Latitude','Longitude'])

view_state = pdk.ViewState(
    latitude=map_df['Latitude'].mean(),#df1["LATITUDE"].mean(),
    longitude=map_df['Longitude'].mean(), #df1["LONGITUDE"].mean(),
    zoom=5,
    pitch=20)

layer1 = pdk.Layer('ScatterplotLayer',
                  data = map_df,#df1,
                  get_position = '[Longitude, Latitude]',
                  get_radius = 5000,
                  get_color = [0,0,255],
                  pickable = True)

tool_tip = {"html": "NAME:<br/> <b>{Name}</b> ",
            "style": {"backgroundColor": "green",
                        "color": "white"}}

map = pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[layer1],
    tooltip=tool_tip)

st.pydeck_chart(map)

# common restaurant names
st.subheader("The Most Common Word in Restaurant Names Are: ")
st.write(pd.Series(' '.join(df["Name"]).lower().split()).value_counts()[:10])

word = ["mcdonald's", "taco", "bell", "burger", "king", "subway", "arby's", "wendy's", "pizza", "in"]
frequency = [1904, 1229, 1035, 906, 840, 833, 666, 629, 549, 465]
x = word
y = frequency
fig, ax = plt.subplots()
ax.scatter(x, y)
ax.grid(True)
plt.xticks(rotation=90)
plt.ylabel("Frequency")
plt.xlabel("Word")
plt.title("Frequency of Common Words in Restaurant Names")
plt.show()
st.pyplot(fig)
