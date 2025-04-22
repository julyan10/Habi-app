import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Título de la app
st.title("Dashboard de Propiedades Cercanas")
st.write("Introduce una coordenada para encontrar propiedades en un radio de 500 metros.")

# Carga de datos
@st.cache_data
def load_data():
    return pd.read_csv("base prueba bi mid.csv")

df = load_data()

# Inputs de usuario
lat = st.number_input("Latitud", value=4.5997, format="%.7f")
lon = st.number_input("Longitud", value=-74.0817, format="%.7f")

# Botón para buscar
if st.button("Buscar propiedades cercanas"):
    punto_usuario = (lat, lon)

    # Calcular distancia para cada propiedad
    def calcular_distancia(row):
        punto_propiedad = (row['latitud'], row['longitud'])
        return geodesic(punto_usuario, punto_propiedad).meters

    df['distancia_m'] = df.apply(calcular_distancia, axis=1)

    # Filtrar propiedades dentro de 500 metros
    propiedades_cercanas = df[df['distancia_m'] <= 500].copy()

    if propiedades_cercanas.empty:
        st.warning("No se encontraron propiedades en un radio de 500 metros.")
    else:
        # Crear columnas compatibles con st.map
        propiedades_cercanas['latitude'] = propiedades_cercanas['latitud']
        propiedades_cercanas['longitude'] = propiedades_cercanas['longitud']

        # Mostrar mapa
        st.subheader("📍 Mapa de propiedades cercanas")
        st.map(propiedades_cercanas[['latitude', 'longitude']])

        # Mostrar tabla con características
        st.subheader("📋 Listado de propiedades encontradas")
        st.dataframe(propiedades_cercanas.drop(columns=['latitude', 'longitude']), use_container_width=True)

import plotly.express as px

# Crear una columna para "zona aproximada" agrupando lat/lon
df['zona_aprox'] = df['latitud'].round(2).astype(str) + "_" + df['longitud'].round(2).astype(str)

st.subheader("📊 Dashboard de precios por cliente y por zona")

# Selector de cliente
clientes = df['nombre_cliente'].dropna().unique()
cliente_seleccionado = st.selectbox("Selecciona un cliente", sorted(clientes))

# Filtrar datos del cliente
df_cliente = df[df['nombre_cliente'] == cliente_seleccionado]

# Gráfico de precios por zona aproximada
zona_agrupada = df_cliente.groupby('zona_aprox')['precio'].mean().reset_index()

fig = px.bar(zona_agrupada, x='zona_aprox', y='precio',
             labels={'zona_aprox': 'Zona Aproximada', 'precio': 'Precio Promedio'},
             title=f'Precios promedio por zona para {cliente_seleccionado}')

st.plotly_chart(fig)

# Mostrar tabla
st.write("Detalle de propiedades:")
st.dataframe(df_cliente[['latitud', 'longitud', 'precio']])


