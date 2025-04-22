import streamlit as st
import pandas as pd
from geopy.distance import geodesic
import folium
from streamlit_folium import st_folium

# Cargar datos
@st.cache_data
def cargar_datos():
    return pd.read_csv("base prueba bi mid.csv")

df = cargar_datos()

# Título del dashboard
st.title("Dashboard de Propiedades Cercanas")
st.markdown("Introduce una coordenada para encontrar propiedades en un radio de 500 metros.")

# Entradas del usuario
latitud = st.number_input("Latitud", value=4.599700, format="%f")
longitud = st.number_input("Longitud", value=-74.081700, format="%f")

if st.button("Buscar propiedades cercanas"):
    coordenada_usuario = (latitud, longitud)

    # Calcular distancia de cada propiedad al punto ingresado
    df['distancia_m'] = df.apply(lambda row: geodesic(coordenada_usuario, (row['latitud'], row['longitud'])).meters, axis=1)

    # Filtrar propiedades dentro del radio de 500 metros
    propiedades_cercanas = df[df['distancia_m'] <= 500].copy()

    if not propiedades_cercanas.empty:
        st.success(f"Se encontraron {len(propiedades_cercanas)} propiedades dentro de 500 metros.")

        # Mostrar mapa con propiedades
        mapa = folium.Map(location=[latitud, longitud], zoom_start=15)

        # Marcador del usuario
        folium.Marker([latitud, longitud], popup="Ubicación ingresada", icon=folium.Icon(color='red')).add_to(mapa)

        # Marcadores de propiedades
        for _, row in propiedades_cercanas.iterrows():
            folium.Marker(
                [row['latitud'], row['longitud']],
                popup=f"{row['nombre_cliente']}\nPrecio: ${row['precio']:,.0f}\nÁrea: {row['area_m2']} m²"
            ).add_to(mapa)

        # Mostrar el mapa
        st_data = st_folium(mapa, width=700, height=500)

        # Mostrar tabla de propiedades
        st.markdown("### Características de las propiedades cercanas")
        st.dataframe(propiedades_cercanas[['nombre_cliente', 'precio', 'area_m2', 'banios', 'alcobas', 'latitud', 'longitud']])
    else:
        st.warning("No se encontraron propiedades dentro del radio de 500 metros.")
