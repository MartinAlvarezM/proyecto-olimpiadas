import pandas as pd
import streamlit as st
import plotly.express as px

st.header('Análisis de los Juegos Olímpicos 🏅')

# Leer el archivo que descargamos
df = pd.read_csv('olympics_data.csv')

st.write('Esta aplicación muestra la relación entre el peso y la altura de los atletas.')

# Crear un botón para mostrar una gráfica
if st.button('Mostrar Gráfico de Dispersión'):
    st.write('Generando gráfica...')
    # Creamos la gráfica de Peso vs Altura
    fig = px.scatter(df.dropna(subset=['height', 'weight']).head(5000), 
                     x="weight", y="height", color="sex",
                     title="Peso vs Altura de Atletas")
    st.plotly_chart(fig, use_container_width=True)

st.set_page_config(page_title="Olympic Data Analytics", page_icon="🥇")
st.header('Análisis Histórico de los Juegos Olímpicos 🏅')

# Cargar los datos (usamos cache para que cargue rápido)
@st.cache_data
def load_data():
    return pd.read_csv('olympics_data.csv')

df = load_data()

st.write('Explora la fisionomía y demografía de los atletas olímpicos a través de los años.')

# --- SECCIÓN 1: HISTOGRAMA (EDADES) ---
st.subheader('¿A qué edad compiten los atletas?')
# Usamos un checkbox como pide el proyecto
show_hist = st.checkbox('Construir histograma de edades')

if show_hist:
    st.write('Distribución de frecuencias por edad de los competidores.')
    fig_hist = px.histogram(df, x="age", nbins=30, color_discrete_sequence=['#D4AF37'],
                           title='Frecuencia de participación por Edad',
                           labels={'age': 'Edad'})
    st.plotly_chart(fig_hist, use_container_width=True)

# --- SECCIÓN 2: GRÁFICO DE DISPERSIÓN (BIOMETRÍA) ---
st.subheader('Relación Altura vs Peso por Deporte')
st.write('Compara cómo cambia el cuerpo de un gimnasta vs un pesista.')

# Botón para generar el gráfico
if st.button('Generar Gráfico de Dispersión'):
    # Filtramos nulos para que el gráfico sea fluido
    df_biometry = df.dropna(subset=['height', 'weight'])
    
    # Creamos el scatter plot
    fig_scatter = px.scatter(df_biometry.head(10000), # Usamos 10k registros para que no pese tanto
                            x="weight", y="height", 
                            color="sport", 
                            hover_name="name",
                            title='Peso vs Altura de Atletas (Top 10,000)',
                            labels={'weight': 'Peso (kg)', 'height': 'Altura (cm)', 'sport': 'Deporte'})
    
    st.plotly_chart(fig_scatter, use_container_width=True)

st.divider()
st.caption('Proyecto desarrollado para el curso de Ingeniería de Datos. Dataset: TidyTuesday Olympics.')