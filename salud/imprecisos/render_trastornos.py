import pandas as pd
import streamlit as st
import plotly.express as px

# Cargar datos del CSV
df = pd.read_csv('trastornos_sintomas_estimados.csv', index_col=0)

st.title("Visualización 3D de Trastornos según Síntomas")

st.write("Seleccione tres síntomas del conjunto de datos para graficar en 3D:")

sintomas = df.columns.tolist()

x_sintoma = st.selectbox("Eje X", sintomas, index=0)
y_sintoma = st.selectbox("Eje Y", sintomas, index=1)
z_sintoma = st.selectbox("Eje Z", sintomas, index=2)

st.write("Seleccione los trastornos a mostrar (puede seleccionar varios):")
trastornos_disponibles = df.index.tolist()
trastornos_seleccionados = st.multiselect("Trastornos", trastornos_disponibles, default=trastornos_disponibles)

# Filtrar el DataFrame según los trastornos seleccionados
df_filtrado = df.loc[trastornos_seleccionados]

fig = px.scatter_3d(
    df_filtrado,
    x=x_sintoma,
    y=y_sintoma,
    z=z_sintoma,
    text=df_filtrado.index,
    title="Trastornos según Valores Reales de Síntomas (Filtrables)"
)

fig.update_layout(
    scene = dict(
        xaxis_title=x_sintoma,
        yaxis_title=y_sintoma,
        zaxis_title=z_sintoma
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

fig.update_traces(textposition='top center')

st.plotly_chart(fig, use_container_width=True)

