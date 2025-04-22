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

