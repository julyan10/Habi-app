import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium
import plotly.express as px

# --- CARGAR DATOS ---
df = pd.read_csv('base prueba bi mid.csv')

# --- GEOCODIFICACIÓN PARA OBTENER CIUDAD ---
geolocator = Nominatim(user_agent="geoapiHabi")
geocode = RateLimiter(geolocator.reverse, min_delay_seconds=1)

def get_city(lat, lon):
    try:
        location = geocode((lat, lon), exactly_one=True, language='es')
        if location and 'address' in location.raw:
            address = location.raw['address']
            return address.get('city') or address.get('town') or address.get('village') or 'Ciudad no encontrada'
        else:
            return 'Ciudad no encontrada'
    except:
        return 'Error al obtener ciudad'

# --- INPUTS DEL USUARIO ---
st.title("Dashboard de Propiedades (radio de 500m)")

st.sidebar.header("Coordenadas")
lat_input = st.sidebar.number_input("Latitud", value=4.5997, format="%.6f")
lon_input = st.sidebar.number_input("Longitud", value=-74.0817, format="%.6f")

# Obtener ciudad
ciudad = get_city(lat_input, lon_input)
st.sidebar.markdown(f"**Ciudad detectada:** {ciudad}")

# --- FILTRO DE RADIO 500M ---
def filtrar_radio(df, lat_centro, lon_centro, radio_metros):
    return df[df.apply(lambda row: geodesic((lat_centro, lon_centro), (row['latitud'], row['longitud'])).meters <= radio_metros, axis=1)]

df_filtrado = filtrar_radio(df, lat_input, lon_input, 500)
df_filtrado = df_filtrado.copy()
df_filtrado['ciudad'] = ciudad

st.subheader(f"Propiedades encontradas en 500m: {len(df_filtrado)}")

# --- MAPA INTERACTIVO ---
mapa = folium.Map(location=[lat_input, lon_input], zoom_start=16)
folium.Circle(location=(lat_input, lon_input), radius=500, color="blue", fill=True, fill_opacity=0.1).add_to(mapa)

for _, row in df_filtrado.iterrows():
    folium.Marker(location=[row['latitud'], row['longitud']],
                  popup=f"{row['nombre_cliente']}<br>Precio: {row['precio']}").add_to(mapa)

st_folium(mapa, width=700)

# --- FILTROS AVANZADOS ---
st.sidebar.header("Filtros adicionales")

alcobas_unique = sorted(df['alcobas'].dropna().unique())
banios_unique = sorted(df['banios'].dropna().unique())

alcobas_sel = st.sidebar.multiselect("Alcobas", alcobas_unique, default=alcobas_unique)
banios_sel = st.sidebar.multiselect("Baños", banios_unique, default=banios_unique)
area_min = st.sidebar.slider("Área mínima (m²)", min_value=0, max_value=500, value=0)

df_filtrado = df_filtrado[
    (df_filtrado['alcobas'].isin(alcobas_sel)) &
    (df_filtrado['banios'].isin(banios_sel)) &
    (df_filtrado['area_m2'] >= area_min)
]

# --- TABLA ---
st.subheader("Tabla de propiedades filtradas")
st.dataframe(df_filtrado[['nombre_cliente', 'precio', 'area_m2', 'banios', 'alcobas', 'ciudad']])

# --- GRÁFICO DE PRECIOS POR CIUDAD ---
st.subheader("Distribución de precios por ciudad")
fig = px.box(df_filtrado, x='ciudad', y='precio', points="all", title="Precios de propiedades por ciudad")
st.plotly_chart(fig)

# --- MAPA DE BURBUJAS POR PRECIO ---
st.subheader("Mapa de propiedades (tamaño por precio)")
mapa_precios = folium.Map(location=[lat_input, lon_input], zoom_start=14)

for _, row in df_filtrado.iterrows():
    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=max(row['precio'] / 1000000, 3),
        popup=f"{row['nombre_cliente']}<br>Precio: {row['precio']}",
        color="green",
        fill=True,
        fill_opacity=0.6
    ).add_to(mapa_precios)

st_folium(mapa_precios, width=700)


