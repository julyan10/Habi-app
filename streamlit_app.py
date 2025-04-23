import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from folium import Circle
from folium.plugins import MarkerCluster
from math import radians, cos, sin, sqrt, atan2

st.set_page_config(layout="wide")

st.title("🏠 Dashboard de Propiedades - Habi")

# Cargar datos
@st.cache_data
def load_data():
    df = pd.read_csv("base prueba bi mid.csv")
    return df

df = load_data()

# Geolocalizador
geolocator = Nominatim(user_agent="geoapiHabi")
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=1)

# Obtener ciudad
@st.cache_data
def get_city(lat, lon):
    try:
        location = reverse((lat, lon), exactly_one=True, language='es')
        if location and 'address' in location.raw:
            address = location.raw['address']
            return address.get('city') or address.get('town') or address.get('village')
    except:
        return None

# Primer Mapa: Propiedades cercanas
st.header("🔍 Propiedades en un radio de 500 metros")
col1, col2 = st.columns(2)
with col1:
    lat_input = st.number_input("Latitud", value=4.5997, format="%.6f")
with col2:
    lon_input = st.number_input("Longitud", value=-74.0817, format="%.6f")

# Función para calcular distancia
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c * 1000

# Filtrar propiedades en 500m
df["distancia_m"] = df.apply(lambda row: haversine(lat_input, lon_input, row["latitud"], row["longitud"]), axis=1)
df_cercanas = df[df["distancia_m"] <= 500]

# Mapa con circunferencia
m = folium.Map(location=[lat_input, lon_input], zoom_start=16)
Circle(location=(lat_input, lon_input), radius=500, color='blue', fill=True, fill_opacity=0.1).add_to(m)
marker_cluster = MarkerCluster().add_to(m)

for _, row in df_cercanas.iterrows():
    folium.Marker(location=[row["latitud"], row["longitud"]],
                  popup=f"{row['nombre_cliente']} - ${row['precio']}").add_to(marker_cluster)

st_data = st_folium(m, width=700)
st.write(f"**Propiedades encontradas:** {len(df_cercanas)}")

# Agregar ciudad a propiedades cercanas
df_cercanas["ciudad"] = df_cercanas.apply(lambda row: get_city(row["latitud"], row["longitud"]), axis=1)

# Tabla con info
st.dataframe(df_cercanas[["nombre_cliente", "precio", "area_m2", "banios", "alcobas", "ciudad"]])

# Segundo bloque - Filtros globales
st.header("📊 Análisis de propiedades")

# Filtros en la barra lateral
with st.sidebar:
    st.markdown("### 🎯 Filtros de Propiedades")

    alcobas_unique = sorted(df['alcobas'].dropna().unique())
    banios_unique = sorted(df['banios'].dropna().unique())

    alcobas_filter = st.multiselect("Filtrar por Alcobas", alcobas_unique, default=alcobas_unique)
    banios_filter = st.multiselect("Filtrar por Baños", banios_unique, default=banios_unique)

    min_area = int(df['area_m2'].min())
    max_area = int(df['area_m2'].max())
    area_min, area_max = st.slider(
        "Filtrar por Área (m2)",
        min_value=min_area,
        max_value=max_area,
        value=(min_area, max_area),
        step=1
    )

# Aplicar filtros a df general
df_filtrado = df[
    df['alcobas'].isin(alcobas_filter) &
    df['banios'].isin(banios_filter) &
    (df['area_m2'] >= area_min) & (df['area_m2'] <= area_max)
]

# Tabla filtrada
st.subheader("📋 Tabla de propiedades filtradas")
st.dataframe(df_filtrado[["nombre_cliente", "precio", "area_m2", "banios", "alcobas"]])

# Gráfico por coordenadas
st.subheader("🗺️ Mapa de propiedades por coordenadas")
fig_map = px.scatter_mapbox(df_filtrado,
                            lat="latitud",
                            lon="longitud",
                            size="precio",
                            color_discrete_sequence=["red"],
                            zoom=10,
                            height=500,
                            hover_name="nombre_cliente",
                            mapbox_style="carto-positron")
st.plotly_chart(fig_map)
