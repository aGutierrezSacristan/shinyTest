import streamlit as st
import pandas as pd
import gdown
import plotly.graph_objects as go
import os

# Get file ID from secrets
file_id = st.secrets["gdrive"]["file_id"]
url = f"https://drive.google.com/uc?id={file_id}"
output = "/tmp/students.csv"

# Download only if file doesn't exist
if not os.path.exists(output):
    gdown.download(url, output, quiet=False)

# Load data
df = pd.read_csv(output)

# ---- Streamlit App ----

st.title("Notas de Estudiantes por Año de Ingreso")

st.dataframe(df)

# Pie chart
pie_df = df['año_enrollment'].value_counts().reset_index()
pie_df.columns = ['Año', 'Nº estudiantes']

pie_fig = go.Figure(
    data=[go.Pie(labels=pie_df["Año"], values=pie_df["Nº estudiantes"])],
)
pie_fig.update_layout(title="Distribución por Año de Ingreso")

st.plotly_chart(pie_fig)

# Correlation plot
corr_fig = go.Figure()
corr_fig.add_trace(go.Scatter(x=df["nota1"], y=df["nota2"], mode='markers', name="nota1 vs nota2"))
corr_fig.add_trace(go.Scatter(x=df["nota1"], y=df["nota3"], mode='markers', name="nota1 vs nota3"))
corr_fig.add_trace(go.Scatter(x=df["nota2"], y=df["nota3"], mode='markers', name="nota2 vs nota3"))

corr_fig.update_layout(
    title="Correlación entre Notas",
    xaxis_title="Nota X",
    yaxis_title="Nota Y",
    legend_title="Comparación"
)

st.plotly_chart(corr_fig)
