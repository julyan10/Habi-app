import streamlit as st
import pandas as pd
import plotly.express as px
import folium
import plotly.express as px
from streamlit_folium import st_folium
from folium import Circle
from folium.plugins import MarkerCluster
from math import radians, cos, sin, sqrt, atan2


st.set_page_config(layout="wide")
st.title("\U0001F3E0 Dashboard de Propiedades - Habi")

# --- Función para asignar ciudad basada en coordenadas ---
def asignar_ciudad(lat, lon):
    if 4.4 <= lat <= 4.8 and -74.3 <= lon <= -73.9:
        return "Bogotá"
    elif 6.1 <= lat <= 6.4 and -75.7 <= lon <= -75.4:
        return "Medellín"
    elif 3.3 <= lat <= 3.6 and -76.6 <= lon <= -76.4:
        return "Cali"
    else:
        return "Otra"

# --- Cargar datos ---
@st.cache_data
def load_data():
    df = pd.read_csv("base prueba bi mid.csv")
    df["ciudad"] = df.apply(lambda row: asignar_ciudad(row["latitud"], row["longitud"]), axis=1)
    return df

df = load_data()


# --- Filtros globales ---
st.markdown("""
### 🧠 Contexto del reto

El rendimiento del equipo de Brokers (el equipo encargado de las ventas inmobiliarias) ha disminuido considerablemente desde hace 4 meses. Usted está en el equipo encargado de mejorar la productividad, ¿cuál sería su acción en los dos próximos sprints?

**Solución 1:**

#### Sprint 1: Diagnóstico y análisis  
**Objetivo:** Identificar causas específicas de la baja productividad.

1. **Análisis de datos históricos de desempeño (últimos 6-12 meses):**
   - Ventas por broker, zona y tipo de propiedad.
   - Tiempo promedio de cierre por propiedad.
   - Número de contactos y conversiones.

2. **Entrevistas y focus group con brokers:**
   - Identificar barreras operativas, técnicas o motivacionales.
   - Recoger insumos cualitativos sobre el proceso de ventas.

3. **Revisión de KPIs actuales:**
   - Verificar si están alineados con los objetivos del negocio.
   - Evaluar si los incentivos están bien estructurados.

4. **Mapeo del funnel de ventas:**
   - Identificar puntos críticos donde se pierden oportunidades (p. ej., baja conversión en visitas o negociación).

#### Sprint 2: Implementación de quick wins  
**Objetivo:** Implementar acciones para mejorar productividad mientras se diseña una estrategia a mediano plazo.

1. **Automatización de tareas repetitivas:**
   - Herramientas para agendar visitas o responder preguntas frecuentes.

2. **Capacitación express:**
   - Taller de habilidades blandas (negociación, objeciones).
   - Uso efectivo de herramientas tecnológicas (CRM, dashboards).

3. **Dashboard de desempeño en tiempo real:**
   - Visualización por broker para promover la autogestión del rendimiento.
   - Ranking interno con KPIs claros (visitas, cierres, seguimiento).

4. **Revisión de zonas asignadas:**
   - Redistribuir zonas si hay desequilibrio entre demanda y cobertura.

---

### ⚽ Habi Soccer – Nuevo producto

Habi va a lanzar un nuevo producto **«Habi fútbol»**, en el que la empresa comprará campos sintéticos y los venderá con césped nuevo y buenas gradas. Al tratarse de un nuevo negocio, no disponemos de una estructura de base de datos para medirlo.

#### ¿Qué pasos darías para construir un MVP que permita a los directivos seguir el rendimiento de Habi Soccer?

---

#### Fase 1: Diseño de estructura y captura de datos

1. **Definir los indicadores clave (KPIs):**
   - Nº de campos adquiridos / vendidos.
   - Tiempo promedio de adecuación.
   - Costo total vs precio de venta por campo.
   - Rentabilidad por campo.
   - Ubicación y demanda por zona.
   - % de avance de cada proyecto (compra, adecuación, venta).

2. **Diseñar el modelo de datos inicial (Tablas principales):**
   - **Campos:** ID, dirección, tamaño, zona, estado actual.
   - **Adecuaciones:** fecha inicio/fin, tipo de mejora, proveedor, costo.
   - **Ventas:** comprador, precio, fecha cierre.
   - **Estados del proceso:** pendiente, en adecuación, en venta, vendido.

3. **Definir herramientas de captura:**
   - Formulario interno con Google Forms, Power Apps o Airtable.
   - Almacenamiento temporal en Google Sheets o base SQL ligera.

---

#### Fase 2: Visualización y análisis

1. **Conectar los datos a Power BI / Looker Studio:**
   - Dashboard con filtros por zona, estado y fechas.
   - KPIs en tarjetas: campos activos, vendidos, ingresos totales.
   - Mapa con localización de campos.
   - Gráficos de evolución temporal de ventas y adecuaciones.

2. **Segmentación geográfica:**
   - Análisis de demanda por zona para identificar zonas de oportunidad.

---

#### Fase 3: Validación e iteración

1. **Probar el MVP con los usuarios clave (comercial y directivos):**
   - Obtener feedback para ajustar los datos y visualizaciones.

2. **Iterar sobre el modelo:**
   - Añadir nuevos campos, métricas o integraciones con sistemas existentes (ERP, CRM).
---

### 🧠 Pregunta 3:

> Escriba una sentencia SELECT para recuperar la ciudad, el precio de venta y la fecha de creación de todos los inmuebles que se han publicado por un precio superior al precio medio de venta de todos los inmuebles publicados para Carolina Castro Jaramillo.

**✅ Respuesta en SQL:**

SELECT Ciudad, Precio_venta, Fecha_creacion  
FROM propiedades  
WHERE Publicado_por = 'Carolina Castro Jaramillo'  
AND Precio_venta > (  
    SELECT AVG(Precio_venta)  
    FROM propiedades  
    WHERE Publicado_por = 'Carolina Castro Jaramillo'  
);

---

### 🧠 Pregunta 4:

> ¿Cuál es el promedio de precios de venta por tamaño de propiedad (en metros cuadrados) para propiedades que tienen al menos 3 habitaciones y 2 baños?  
> Considere solo promedio de precio de venta mayor a 80.000.000 y muestre el top 20 ordenado de forma descendente por el promedio del precio de venta.

**✅ Respuesta en SQL:**

SELECT Tamaño,  
    AVG(Precio_venta) AS Promedio_Precio_Venta  
FROM propiedades  
WHERE N_habitaciones >= 3  
    AND N_baños >= 2  
GROUP BY Tamaño  
HAVING AVG(Precio_venta) > 80000000  
ORDER BY Promedio_Precio_Venta DESC  
LIMIT 20;
""")

st.header("\U0001F4CA Análisis de propiedades")

with st.sidebar:
    st.markdown("### \U0001F3AF Filtros de Propiedades")

    alcobas_unique = sorted(df['alcobas'].dropna().unique())
    banios_unique = sorted(df['banios'].dropna().unique())
    ciudades_unique = sorted(df['ciudad'].dropna().unique())

    alcobas_filter = st.multiselect("Filtrar por Alcobas", alcobas_unique, default=alcobas_unique)
    banios_filter = st.multiselect("Filtrar por Baños", banios_unique, default=banios_unique)
    ciudad_filter = st.multiselect("Filtrar por Ciudad", ciudades_unique, default=ciudades_unique)

    min_area = int(df['area_m2'].min())
    max_area = int(df['area_m2'].max())
    area_min, area_max = st.slider(
        "Filtrar por Área (m2)",
        min_value=min_area,
        max_value=max_area,
        value=(min_area, max_area),
        step=1
    )

# --- Aplicar filtros ---
df_filtrado = df[
    df['alcobas'].isin(alcobas_filter) &
    df['banios'].isin(banios_filter) &
    df['ciudad'].isin(ciudad_filter) &
    (df['area_m2'] >= area_min) & (df['area_m2'] <= area_max)
]

# --- Mostrar tabla filtrada ---
st.subheader("\U0001F4CB Tabla de propiedades filtradas")
st.dataframe(
    df_filtrado[["nombre_cliente", "precio", "area_m2", "banios", "alcobas", "ciudad"]].rename(columns={
        "nombre_cliente": "Cliente",
        "precio": "Precio",
        "banios": "N_Baños",
        "alcobas": "N_Alcobas",
        "area_m2": "Área (m2)",
        "ciudad": "Ciudad"
    })
)

# --- Precio promedio y cantidad de propiedades por ciudad ---
st.subheader("💰 Precio promedio y cantidad de propiedades por ciudad")

# Agrupamos
df_ciudad = df_filtrado.groupby("ciudad").agg(
    Precio_Promedio=("precio", "mean"),
    Cantidad=("nombre_cliente", "count")
).reset_index()

# Redondeamos y preparamos para gráfico
df_ciudad["Precio_Promedio"] = df_ciudad["Precio_Promedio"].round(0).astype(int)

# Derretimos el dataframe para usarlo en plotly express
df_melt = df_ciudad.melt(id_vars="ciudad", value_vars=["Precio_Promedio", "Cantidad"],
                         var_name="Métrica", value_name="Valor")

# Creamos el gráfico
fig = px.bar(
    df_melt,
    x="ciudad",
    y="Valor",
    color="Métrica",
    barmode="group",
    text_auto=True,
    title="Precio promedio y cantidad de propiedades por ciudad",
    labels={"ciudad": "Ciudad", "Valor": "Valor", "Métrica": "Métrica"}
)

fig.update_layout(yaxis_tickformat=",", height=500)
st.plotly_chart(fig, use_container_width=True)

with st.expander("🧠 Ver análisis del gráfico"):
    st.markdown("""
- **Medellín presenta el precio promedio más alto** entre todas las ciudades, lo que sugiere una mayor valorización del mercado inmobiliario.
- **Bogotá y Cali tienen precios promedio más moderados**, pero también concentran un mayor número de propiedades publicadas.
- La categoría **“Otra” representa propiedades fuera de las 3 ciudades principales** y muestra un precio promedio alto, lo que indica que pueden ubicarse en zonas de alta valorización o baja oferta.
- **La diferencia de escala entre precio y cantidad** resalta la necesidad de observar ambas métricas en conjunto al tomar decisiones estratégicas.
    """)

# --- Línea: evolución del precio promedio según el área por ciudad ---
st.subheader("📈 Tendencia de precio según área por ciudad")

# Agrupamos área en bins para mayor legibilidad
df_filtrado["area_bin"] = pd.cut(df_filtrado["area_m2"], bins=10)

# Calculamos el precio promedio por ciudad y rango de área
df_line = df_filtrado.groupby(["ciudad", "area_bin"]).agg(
    Precio_Promedio=("precio", "mean")
).reset_index()

# Convertimos los bins en strings ordenadas
df_line["area_bin"] = df_line["area_bin"].astype(str)

# Gráfico de líneas
fig_line = px.line(
    df_line,
    x="area_bin",
    y="Precio_Promedio",
    color="ciudad",
    markers=True,
    title="Tendencia de precio promedio según área (agrupada) por ciudad",
    labels={"area_bin": "Área (rangos)", "Precio_Promedio": "Precio Promedio"}
)
fig_line.update_layout(yaxis_tickformat=",", xaxis_tickangle=-45)
st.plotly_chart(fig_line, use_container_width=True)

with st.expander("🧠 Ver análisis del gráfico"):
    st.markdown("""
- Existe una **relación positiva entre el área y el precio promedio**: a mayor tamaño, mayor valor del inmueble.
- **Medellín mantiene los precios promedio más altos** en todos los rangos de área, lo que sugiere un mayor valor del m² o una oferta más premium.
- **Bogotá y Cali presentan precios más equilibrados**, especialmente en rangos intermedios.
- Se observa un **salto notable en los precios** a partir de propiedades con más de 150 m², lo que podría indicar una categoría distinta de inmuebles (por ejemplo, casas o propiedades de lujo).
    """)

# --- Mapa de propiedades por coordenadas ---
st.subheader("\U0001F5FA️ Mapa de propiedades por zona")
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

# --- Mapa por coordenadas ingresadas ---
st.header("\U0001F50D Propiedades en un radio de 500 metros")
st.markdown(
    "\U0001F50E *Ingresa una latitud y longitud para identificar propiedades publicadas dentro de un radio de 500 metros.*"
)
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

# Calcular distancia y filtrar cercanas
df["distancia_m"] = df.apply(lambda row: haversine(lat_input, lon_input, row["latitud"], row["longitud"]), axis=1)
df_cercanas = df[df["distancia_m"] <= 500]

# Mapa y tabla en columnas
col_mapa, col_tabla = st.columns([2, 1])

with col_mapa:
    m = folium.Map(location=[lat_input, lon_input], zoom_start=16)
    Circle(location=(lat_input, lon_input), radius=500, color='blue', fill=True, fill_opacity=0.1).add_to(m)
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in df_cercanas.iterrows():
        folium.Marker(
            location=[row["latitud"], row["longitud"]],
            popup=f"{row['nombre_cliente']} - ${row['precio']}"
        ).add_to(marker_cluster)

    st_data = st_folium(m, width=700, height=450)

with col_tabla:
    st.write(f"**Propiedades encontradas:** {len(df_cercanas)}")

    columnas_mostrar = ["nombre_cliente", "precio", "area_m2", "banios", "alcobas", "ciudad"]
    columnas_presentes = [col for col in columnas_mostrar if col in df_cercanas.columns]

    st.dataframe(
        df_cercanas[columnas_presentes].rename(columns={
            "nombre_cliente": "Cliente",
            "precio": "Precio",
            "banios": "N_Baños",
            "alcobas": "N_Alcobas",
            "area_m2": "Área (m2)",
            "ciudad": "Ciudad"
        })
    )
