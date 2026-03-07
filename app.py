import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Olympic Data Analytics", layout="wide")

# pre-procesamiento de datos

@st.cache_data
def load_data():
    df = pd.read_csv('olympics_data.csv')

    # --- Tratamiento de nulos ---
    df['medal'] = df['medal'].fillna('No Medal')

    # --- Eliminar duplicados y resetear índice ---
    df = df.drop_duplicates().reset_index(drop=True)

    # --- Normalización de columnas de texto ---
    for col in ['event', 'sport', 'name', 'team', 'games']:
        df[col] = df[col].str.strip().str.replace(r'\s+', ' ', regex=True)

    return df


df = load_data()

st.title('Dashboard Olímpico')
st.markdown("---")

# 1
st.header('1. Distribución de Edades')
deportes = sorted(df['sport'].unique())
deporte_sel = st.selectbox('Selecciona un Deporte para ver las edades:', ['Todos'] + deportes)

df_edad = df if deporte_sel == 'Todos' else df[df['sport'] == deporte_sel]

fig_hist = px.histogram(
    df_edad, x="age", nbins=30,
    color_discrete_sequence=['#D4AF37'],
    title=f'Edades en: {deporte_sel}',
    labels={'age': 'Edad'}
)
st.plotly_chart(fig_hist, use_container_width=True)

# 2
st.header('2. Ranking de Medallas por País')
col1, col2 = st.columns([1, 3])

with col1:
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    años_rango = st.slider('Selecciona el rango de años:', min_year, max_year, (min_year, max_year))

df_medals = df[
    (df['year'] >= años_rango[0]) &
    (df['year'] <= años_rango[1]) &
    (df['medal'] != 'No Medal')
]
top_paises = (
    df_medals.groupby('noc')['medal']
    .count()
    .reset_index()
    .sort_values(by='medal', ascending=False)
    .head(15)
)

with col2:
    fig_paises = px.bar(
        top_paises, x='noc', y='medal',
        title=f'Top 15 Países con más medallas ({años_rango[0]} - {años_rango[1]})',
        labels={'noc': 'País (NOC)', 'medal': 'Total Medallas'},
        color='medal', color_continuous_scale='Viridis'
    )
    st.plotly_chart(fig_paises, use_container_width=True)

# 3.
st.header('3. Hall de la Fama por Deporte')

col_gen, col_dep = st.columns([1, 2])

with col_gen:
    genero_top = st.radio("Género:", ('M', 'F'), horizontal=True, key="gen_top")

with col_dep:
    deporte_top = st.selectbox('Selecciona el Deporte:', ['Todos'] + deportes, key="dep_top")

df_top = df[(df['sex'] == genero_top) & (df['medal'] != 'No Medal')]

if deporte_top != 'Todos':
    df_top = df_top[df_top['sport'] == deporte_top]

ranking_individual = (
    df_top.groupby('name')['medal']
    .count()
    .reset_index()
    .sort_values(by='medal', ascending=False)
    .head(10)
)

if not ranking_individual.empty:
    fig_top_10 = px.bar(
        ranking_individual,
        x='medal', y='name', orientation='h',
        title=f'Top 10 Medallistas en {deporte_top} ({genero_top})',
        labels={'medal': 'Total de Medallas', 'name': 'Atleta'},
        color='medal',
        color_continuous_scale='Oryel' if genero_top == 'F' else 'Ice'
    )
    fig_top_10.update_yaxes(autorange="reversed")
    st.plotly_chart(fig_top_10, use_container_width=True)
else:
    st.warning(f"No se encontraron medallistas para {deporte_top} con este filtro.")

# 4
st.header('4. Dominancia: Verano vs Invierno')

paises_disponibles = sorted(df['noc'].unique())
# Buscar NOR de forma segura en lugar de usar índice fijo
default_idx = paises_disponibles.index('NOR') if 'NOR' in paises_disponibles else 0
pais_comp = st.selectbox('Selecciona un país para comparar temporadas:', paises_disponibles, index=default_idx)

df_season = df[(df['noc'] == pais_comp) & (df['medal'] != 'No Medal')]
resumen_season = df_season.groupby('season')['medal'].count().reset_index()

fig_season = px.pie(
    resumen_season, values='medal', names='season',
    title=f'Distribución de Medallas Verano vs Invierno: {pais_comp}',
    color_discrete_map={'Summer': 'orange', 'Winter': 'blue'}
)
st.plotly_chart(fig_season, use_container_width=True)

st.divider()
st.caption('Herramientas de desarrollo de software - Martin: Designer & Data Scientist.')