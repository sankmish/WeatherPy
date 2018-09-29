# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time

# Import API key
from api_keys import api_key

# Incorporated citipy to determine city based on latitude and longitude
from citipy import citipy

# Output File (CSV)
output_data_file = "output_data/cities.csv"

# Range of latitudes and longitudes
lat_range = (-90, 90)
lng_range = (-180, 180)

# List for holding lat_lngs and cities
lat_lngs = []
cities = []

# Create a set of random lat and lng combinations
lats = np.random.uniform(low=-90.000, high=90.000, size=1500)
lngs = np.random.uniform(low=-180.000, high=180.000, size=1500)
lat_lngs = zip(lats, lngs)

# Identify nearest city for each lat, lng combination
for lat_lng in lat_lngs:
    city = citipy.nearest_city(lat_lng[0], lat_lng[1]).city_name
    
    # If the city is unique, then add it to a our cities list
    if city not in cities:
        cities.append(city)

# Print the city count to confirm sufficient count
len(cities)

url = "http://api.openweathermap.org/data/2.5/weather?"
query_url = url + api_key + "&q="
cityNames = []
date = []
lat = []
lng = []
cloudiness = []
maxTemp = []
windSpeed = []
country = []
humidity = []


print("Beginning Data Retrieval")
print("-------------------------------------")
for city in cities:
    print("Processing Record of | " + city)
    response = requests.get(query_url + city).json()
    if response['cod'] == '404':
        print("City not found.  Skipping...")
    else:
        cityNames.append(response['name'])
        date.append(response['dt'])
        lat.append(response['coord']['lat'])
        lng.append(response['coord']['lon'])
        cloudiness.append(response['clouds']['all'])
        maxTemp.append(response['main']['temp_max'])
        windSpeed.append(response['wind']['speed'])
        country.append(response['sys']['country'])
        humidity.append(response['main']['humidity'])
print("-------------------------------------")
print("Data Retrieval Complete")
print("-------------------------------------")

weather_dict = {
    "City": cityNames,
    "Cloudiness": cloudiness,
    "Country": country,
    "Date": date,
    "Humidity": humidity,
    "Lat": lat,
    "Long": lng,
    "Max Temp": maxTemp,
    "Wind Speed": windSpeed
}
weather_data = pd.DataFrame(weather_dict)
weather_data.to_csv("Resources/weather.csv", index = False, header = True)
weather_data.head()

weather_data_read = pd.read_csv("Resources/weather.csv")
weather_data_read.head()
plt.scatter(weather_data["Lat"], weather_data["Max Temp"], marker = "o")

plt.title("City Latitude vs. Max Temperature (09/28/18)")
plt.ylabel("Max Temperature (F)")
plt.xlabel("Latitude")
plt.grid()

plt.savefig("LatitudevsTemperature.png")

plt.scatter(weather_data["Lat"], weather_data["Humidity"], marker = "o")

plt.title("City Latitude vs. Humidity (09/28/18)")
plt.ylabel("Humidity (%)")
plt.xlabel("Latitude")
plt.grid()

plt.savefig("LatitudevsHumidity.png")

plt.scatter(weather_data["Lat"], weather_data["Cloudiness"], marker = "o")

plt.title("City Latitude vs. Cloudiness (09/28/18)")
plt.ylabel("Cloudiness (%)")
plt.xlabel("Latitude")
plt.grid()

plt.savefig("LatitudevsCloudiness.png")

plt.scatter(weather_data["Lat"], weather_data["Wind Speed"], marker = "o")

plt.title("City Latitude vs. Wind Speed (09/28/18)")
plt.ylabel("Wind Speed (mph)")
plt.xlabel("Latitude")
plt.grid()

plt.savefig("LatitudevsWind.png")