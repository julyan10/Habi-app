import streamlit as st
import pandas as pd
from geopy.distance import geodesic

# Título del dashboard
st.title("Dashboard de Propiedades Cercanas")

# Instrucciones
st.write("Introduce una coordenada para encontrar propiedades en un radio de 500 metros.")

# Campos para introducir latitud y longitud
lat = st.number_input("Latitud", format="%.10f", value=4.5997)
lon = st.number_input("Longitud", format="%.10f", value=-74.0817)

# Botón para activar la búsqueda
if st.button("Buscar propiedades cercanas"):
    try:
        # Cargar datos
        df = pd.read_csv("base prueba bi mid.csv")

        # Verificar si hay columnas necesarias
        if 'latitud' in df.columns and 'longitud' in df.columns:
            # Coordenadas del usuario
            user_coords = (lat, lon)

            # Función para calcular distancia
            def calcular_distancia(row):
                return geodesic(user_coords, (row['latitud'], row['longitud'])).meters

            # Calcular distancia y filtrar
            df['distancia_m'] = df.apply(calcular_distancia, axis=1)
            propiedades_cercanas = df[df['distancia_m'] <= 500]

            # Mostrar resultados
            if not propiedades_cercanas.empty:
                st.success(f"Se encontraron {len(propiedades_cercanas)} propiedades en un radio de 500 metros.")
                st.map(propiedades_cercanas[['latitud', 'longitud']])
                st.dataframe(propiedades_cercanas[['area_m2', 'precio', 'banios', 'alcobas', 'nombre_cliente']])
            else:
                st.warning("No se encontraron propiedades en un radio de 500 metros.")
        else:
            st.error("El archivo no contiene columnas 'latitud' y 'longitud'.")

    except FileNotFoundError:
        st.error("El archivo 'base prueba bi mid.csv' no fue encontrado.")
    except Exception as e:
        st.error(f"Ocurrió un error: {e}")
