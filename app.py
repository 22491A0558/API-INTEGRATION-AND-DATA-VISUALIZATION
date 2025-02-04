import streamlit as st
import datetime
from utils.api_client import WeatherAPI
from utils.visualizations import WeatherVisualizations

# Page config
st.set_page_config(
    page_title="Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Initialize API client and visualizations
api = WeatherAPI()
viz = WeatherVisualizations()

# Main title
st.title("📊 Weather Data Dashboard")

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    city = st.text_input("Enter City", "London")
    days_range = st.slider("Select Days Range", 1, 7, 5)
    
    # Add dark/light mode toggle
    if st.checkbox("Dark Mode"):
        st.markdown("""
            <style>
                .stApp {
                    background-color: #0E1117;
                    color: #FAFAFA;
                }
            </style>
        """, unsafe_allow_html=True)

# Main content
try:
    # Current weather section
    current_weather = api.get_current_weather(city)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Temperature", f"{current_weather['temp']}°C")
    with col2:
        st.metric("Humidity", f"{current_weather['humidity']}%")
    with col3:
        st.metric("Pressure", f"{current_weather['pressure']} hPa")

    # Historical data section
    st.header("Historical Weather Analysis")
    historical_data = api.get_historical_weather(city, days_range)
    
    # Temperature trend
    st.subheader("Temperature Trends")
    temp_fig = viz.plot_temperature_trend(historical_data)
    st.pyplot(temp_fig)
    
    # Weather conditions distribution
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Weather Conditions Distribution")
        conditions_fig = viz.plot_weather_conditions(historical_data)
        st.pyplot(conditions_fig)
    
    with col2:
        st.subheader("Humidity vs Pressure")
        correlation_fig = viz.plot_humidity_pressure(historical_data)
        st.pyplot(correlation_fig)

except Exception as e:
    st.error(f"Error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data provided by OpenWeatherMap API")
