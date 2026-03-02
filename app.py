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
    