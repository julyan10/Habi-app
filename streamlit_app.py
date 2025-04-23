import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Dashboard de Propiedades", layout="wide")

# Cargar archivo CSV
df = pd.read_csv("base prueba bi mid.csv")

# Renombrar columnas si es necesario
df.rename(columns=lambda x: x.strip().lower(), inplace=True)

# Obtener valores únicos para filtros
alcobas_unique = sorted(df['alcobas'].dropna().unique())
banios_unique = sorted(df['banios'].dropna().unique())
area_min, area_max = int(df['area_m2'].min()), int(df['area_m2'].max())

# Barra lateral con filtros
st.sidebar.header("Filtros")
alcobas_filter = st.sidebar.multiselect("Filtrar por Alcobas", alcobas_unique, default=alcobas_unique)
banios_filter = st.sidebar.multiselect("Filtrar por Baños", banios_unique, default=banios_unique)
area_range = st.sidebar.slider("Área (m2)", min_value=area_min, max_value=area_max,
                               value=(area_min, area_max), step=1)

# Filtrar datos
filtered_df = df[
    (df['alcobas'].isin(alcobas_filter)) &
    (df['banios'].isin(banios_filter)) &
    (df['area_m2'] >= area_range[0]) & 
    (df['area_m2'] <= area_range[1])
]

# Inputs para coordenadas (sólo afectan el primer mapa)
st.header("Mapa de Propiedades Cercanas (500m)")
lat = st.number_input("Latitud", value=4.5997, format="%.7f")
lon = st.number_input("Longitud", value=-74.0817, format="%.7f")

# Calcular distancia para propiedades cercanas
from geopy.distance import geodesic

def en_rango(row):
    try:
        return geodesic((lat, lon), (row['latitud'], row['longitud'])).meters <= 500
    except:
        return False

filtered_nearby = df[df.apply(en_rango, axis=1)]

# Crear mapa
m = folium.Map(location=[lat, lon], zoom_start=16)
folium.Marker([lat, lon], popup="Ubicación", icon=folium.Icon(color="red")).add_to(m)
folium.Circle(location=[lat, lon], radius=500, color='blue', fill=True, fill_opacity=0.1).add_to(m)

# Añadir marcadores de propiedades cercanas
for _, row in filtered_nearby.iterrows():
    popup_text = f"{row['nombre_cliente']} - ${row['precio']:,.0f}"
    folium.CircleMarker(location=[row['latitud'], row['longitud']],
                        radius=5,
                        color='green',
                        fill=True,
                        fill_opacity=0.7,
                        popup=popup_text).add_to(m)

st_data = st_folium(m, width=700, height=500)
st.write(f"**Propiedades encontradas:** {len(filtered_nearby)}")

# Visualización: Tabla con datos filtrados
st.header("Listado de Propiedades")
st.dataframe(
    filtered_df[['nombre_cliente', 'precio', 'area_m2', 'banios', 'alcobas']],
    use_container_width=True
)

# Mapa general de propiedades con burbujas por precio
st.header("Mapa de todas las propiedades filtradas")
m2 = folium.Map(location=[df['latitud'].mean(), df['longitud'].mean()], zoom_start=12)

for _, row in filtered_df.iterrows():
    folium.CircleMarker(
        location=[row['latitud'], row['longitud']],
        radius=max(row['precio'] / 50000000, 3),  # Ajusta el tamaño relativo al precio
        color='purple',
        fill=True,
        fill_opacity=0.6,
        popup=f"{row['nombre_cliente']} - ${row['precio']:,.0f}"
    ).add_to(m2)

st_folium(m2, width=700, height=500)



