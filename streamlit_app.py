import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# Título
st.title("Buscador de Ciudad por Coordenadas")

# Inputs
lat = st.number_input("Latitud", value=4.6097, format="%.6f")
lon = st.number_input("Longitud", value=-74.0817, format="%.6f")

# Geolocalizador
geolocator = Nominatim(user_agent="geoapiHabi")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Función
def get_city(lat, lon):
    try:
        location = geocode((lat, lon), exactly_one=True, language='es')
        if location and 'address' in location.raw:
            address = location.raw['address']
            return address.get('city') or address.get('town') or address.get('village')
    except:
        return "No se pudo obtener ciudad"

# Mostrar resultado
if st.button("Buscar ciudad"):
    ciudad = get_city(lat, lon)
    st.success(f"La ciudad es: {ciudad}")
