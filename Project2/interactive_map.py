import pandas as pd
import os
import plotly.express as px
from plotly.offline import plot

folder_path = r"C:\Users\hassa\Documents\GitHub\AER817_Project_Cursor"

data = []


for file in os.listdir(folder_path):
    if file.endswith(".CSV"):
        file_path = os.path.join(folder_path, file)
        try:
            
            df = pd.read_csv(file_path, header=None, engine='python')
            df.columns = ["Longitude", "Latitude", "Temperature", "Humidity", "CO2", "CO", "Time", "Date"]
            df["Longitude"] = df["Longitude"].str.split(":").str[1].astype(float)
            df["Latitude"] = df["Latitude"].str.split(":").str[1].astype(float)
            df["Temperature"] = df["Temperature"].str.split(":").str[1].str.replace("C", "").astype(float)
            df["Humidity"] = df["Humidity"].str.split(":").str[1].str.replace("%", "").astype(float)
            df["CO2"] = df["CO2"].str.split(":").str[1].str.replace("ppm", "").astype(float)
            df["CO"] = df["CO"].str.split(":").str[1].str.replace("ppm", "").astype(float)
            df["Time"] = df["Time"].str.split(":").str[1] + ":" + df["Time"].str.split(":").str[2]
            df["Date"] = df["Date"].str.split(":").str[1]

            
            data.append(df)
        except Exception as e:
            print(f"Error processing file {file}: {e}")


combined_data = pd.concat(data, ignore_index=True)


combined_data["HoverText"] = (
    "Time: " + combined_data["Time"] +
    "<br>Date: " + combined_data["Date"] +
    "<br>Temperature: " + combined_data["Temperature"].astype(str) + "°C" +
    "<br>Humidity: " + combined_data["Humidity"].astype(str) + "%" +
    "<br>CO2: " + combined_data["CO2"].astype(str) + " ppm" +
    "<br>CO: " + combined_data["CO"].astype(str) + " ppm"
)


fig = px.scatter_mapbox(
    combined_data,
    lat="Latitude",
    lon="Longitude",
    hover_name="HoverText",
    zoom=2.5,  
    center={"lat": combined_data["Latitude"].mean(), "lon": combined_data["Longitude"].mean()},
    mapbox_style="open-street-map"
)


fig.update_layout(
    title="Interactive Environmental Data Map",
    hovermode="closest"
)


plot(fig, filename="interactive_map.html", auto_open=True)
