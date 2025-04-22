import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from geopy.distance import geodesic
import pydeck as pdk

# Cargar los datos
@st.cache_data
def load_data():
    df = pd.read_csv("base prueba bi mid.csv")
    return df

df = load_data()

st.title("🏠 Dashboard de Propiedades - Equipo de Operaciones")
st.markdown("Este dashboard permite visualizar propiedades a partir de coordenadas específicas, ver estadísticas de precios, y aplicar filtros detallados.")

# Entrada de coordenadas
lat_input = st.number_input("Ingrese latitud", format="%.6f")
lon_input = st.number_input("Ingrese longitud", format="%.6f")

# Calcular distancia entre coordenadas
def distancia(coord1, coord2):
    return geodesic(coord1, coord2).meters

# Filtrar propiedades dentro de 500m
if lat_input != 0 and lon_input != 0:
    df['distancia_m'] = df.apply(lambda row: distancia((lat_input, lon_input), (row['latitud'], row['longitud'])), axis=1)
    df_filtrada = df[df['distancia_m'] <= 500].copy()
    st.success(f"🔍 Propiedades encontradas en un radio de 500m: {len(df_filtrada)}")

    # Mapa con círculo de 500m
    st.subheader("🗺️ Mapa de propiedades cercanas (500m)")
    st.map(df_filtrada.rename(columns={'latitud': 'latitude', 'longitud': 'longitude'}))

    st.caption("El círculo es representativo del área de búsqueda de 500 metros.")

    # Listado de propiedades
    st.dataframe(df_filtrada[['nombre_cliente', 'precio', 'area_m2', 'banios', 'alcobas']])

# ----------------------
# Filtros para análisis
# ----------------------
st.sidebar.header("🎛️ Filtros de búsqueda")
min_area, max_area = int(df['area_m2'].min()), int(df['area_m2'].max())
area_range = st.sidebar.slider("Área (m2)", min_value=min_area, max_value=max_area, value=(min_area, max_area))

banios_unique = sorted(df['banios'].dropna().unique())
banios_filter = st.sidebar.multiselect("Baños", banios_unique, default=banios_unique)

alcobas_unique = sorted(df['alcobas'].dropna().unique())
alcobas_filter = st.sidebar.multiselect("Alcobas", alcobas_unique, default=alcobas_unique)

# Aplicar filtros
df_filtros = df[
    (df['area_m2'] >= area_range[0]) &
    (df['area_m2'] <= area_range[1]) &
    (df['banios'].isin(banios_filter)) &
    (df['alcobas'].isin(alcobas_filter))
]

# Tabla con precios por cliente
st.subheader("📊 Tabla: Precio de venta por cliente")
st.dataframe(df_filtros[['nombre_cliente', 'precio', 'area_m2', 'banios', 'alcobas']])

# Gráfico por zona usando agrupación de coordenadas redondeadas como proxy de zona
st.subheader("📈 Gráfico de precios promedio por zona (aproximada por lat/lon redondeados)")
df_filtros['zona_aprox'] = df_filtros.apply(lambda x: f"({round(x['latitud'], 3)}, {round(x['longitud'], 3)})", axis=1)

zona_group = df_filtros.groupby('zona_aprox')['precio'].mean().reset_index()
fig = px.bar(zona_group, x='zona_aprox', y='precio', title="Precio promedio por zona")
st.plotly_chart(fig)

# Mapa de burbujas por precio
st.subheader("📍 Mapa interactivo de propiedades (tamaño = precio)")
df_filtros = df_filtros.rename(columns={'latitud': 'latitude', 'longitud': 'longitude'})

bubble_map = px.scatter_mapbox(
    df_filtros,
    lat="latitude",
    lon="longitude",
    size="precio",
    hover_name="nombre_cliente",
    color_discrete_sequence=["blue"],
    zoom=12,
    height=500
)
bubble_map.update_layout(mapbox_style="open-street-map")
st.plotly_chart(bubble_map)

st.caption("El tamaño de cada punto representa el precio de la propiedad.")



