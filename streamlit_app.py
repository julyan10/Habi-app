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

# --- BLOQUE 1: Análisis general y mapa de propiedades ---
st.header("📊 Análisis de propiedades")

# Filtros en barra lateral
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

# --- BLOQUE 2: Propiedades cercanas a coordenadas ---
st.header("🔍 Propiedades en un radio de 500 metros")
col1, col2 = st.columns(2)
with col1:
    lat_input = st.number_input("Latitud", value=4.5997, format="%.6f")
with col2:
    lon_input = st.number_input("Longitud", value=-74.0817, format="%.6f")

# Filtrar propiedades en 500m
df["distancia_m"] = df.apply(lambda row: haversine(lat_input, lon_input, row["latitud"], row["longitud"]), axis=1)
df_cercanas = df[df["distancia_m"] <= 500]

# Mostrar mapa y tabla en columnas
col_mapa, col_tabla = st.columns([2, 1])

with col_mapa:
    st_data = st_folium(m, width=700, height=450)

with col_tabla:
    st.write(f"**Propiedades encontradas:** {len(df_cercanas)}")
    df_cercanas["ciudad"] = df_cercanas.apply(lambda row: get_city(row["latitud"], row["longitud"]), axis=1)
    st.dataframe(df_cercanas[["nombre_cliente", "precio", "area_m2", "banios", "alcobas", "ciudad"]])

