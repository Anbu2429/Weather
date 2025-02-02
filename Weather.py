import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


API_KEY = '8fc16d826adcbe0ac926ffcaae4b2ef6'
GEOCODING_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_current_weather(city):
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'  
    }
    
    response = requests.get(GEOCODING_URL, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to retrieve weather data: {response.status_code} - {response.text}")
        print(f"Error: {response.status_code} - {response.text}")

    return None

st.title('Current Weather Data')

city = st.text_input("Enter city name:", "New York")

if city:
    
    weather_data = get_current_weather(city)

    if weather_data:
        
        temp = weather_data['main']['temp']
        humidity = weather_data['main']['humidity']
        weather_desc = weather_data['weather'][0]['description']
        wind_speed = weather_data['wind']['speed']
        
        
        rain_amount = weather_data.get('rain', {}).get('1h', 0)  
        rain_cm = rain_amount * 0.1  

        
        st.write(f"**Current weather in {city}:**")
        st.metric("Temperature (°C)", temp)
        st.metric("Humidity (%)", humidity)
        st.metric("Wind Speed (m/s)", wind_speed)
        st.write(f"Weather Description: {weather_desc.capitalize()}")

        if rain_amount > 0:
            st.metric("Rainfall in last hour (cm)", round(rain_cm, 2))
        else:
            st.write("No rainfall in the last hour.")


        data = {
            'Metric': ['Temperature (°C)', 'Humidity (%)', 'Wind Speed (m/s)', 'Rainfall (cm)'],
            'Value': [temp, humidity, wind_speed, rain_cm]
        }
        df = pd.DataFrame(data)

        
        st.write("Current Weather Metrics:")
        fig, ax = plt.subplots()
        df.plot(kind='bar', x='Metric', y='Value', ax=ax, color=['blue', 'green', 'orange', 'purple'])
        plt.title(f"Current Weather Metrics for {city}")
        plt.ylabel('Value')
        plt.xticks(rotation=0)
        st.pyplot(fig)

    else:
        st.write("Failed to retrieve weather data.")
