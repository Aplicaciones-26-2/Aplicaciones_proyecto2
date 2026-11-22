import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Víctimas viales y cámaras en Bogotá", layout="wide")

RUTA = "data/processed/"
RADIO = 300
TAMANIO_CUADRO = 0.0027

victimas_camaras_anio = "AA_Acc"
victimas_camaras_dist = "distancia_m"
victimas_camaras_tipo = "Condicion"
victimas_camaras_franja = "franja"
victimas_camaras_lat = "Latitud"
victimas_camaras_lon = "Longitud"
victimas_camaras_cuadro = "cuadro"

cuadros_nombre = "cuadro"
cuadros_nvict = "victimas"
cuadros_dist = "distancia_min"

localidades_nombre = "localidad"
localidades_tasa = "tasa_victimas"
localidades_cam = "camaras"

victimas_camaras = pd.read_csv(RUTA + "victimas_camaras.csv.gz")
cuadros = pd.read_csv(RUTA + "cuadros.csv")
localidades = pd.read_csv(RUTA + "localidades.csv")

fila = np.round(victimas_camaras[victimas_camaras_lat] / TAMANIO_CUADRO).astype(int)
columna = np.round(victimas_camaras[victimas_camaras_lon] / TAMANIO_CUADRO).astype(int)
victimas_camaras[victimas_camaras_cuadro] = fila.astype(str) + "_" + columna.astype(str)

victimas_camaras_2019 = victimas_camaras[victimas_camaras[victimas_camaras_anio] >= 2019]

pct_cerca = (victimas_camaras[victimas_camaras_dist] <= RADIO).mean() * 100
pct_lejos = 100 - pct_cerca

top50 = cuadros.head(50)
puntos_sin = top50[top50[cuadros_dist] > RADIO]
vic_sin = victimas_camaras_2019[victimas_camaras_2019[victimas_camaras_cuadro].isin(puntos_sin[cuadros_nombre])]
pct_motos = (vic_sin[victimas_camaras_tipo] == "MOTOCICLISTA").mean() * 100

st.title("Víctimas viales y cámaras de velocidad en Bogotá")
st.write("Este dashboard muestra las gráficas que sustentan los dos hallazgos del proyecto.")
st.write("**Período:** víctimas de 2019 a 2025 (la gráfica 6 usa todos los años para comparar con el promedio anterior).")
st.write(f"**Radio de la cámara:** todas las gráficas usan {RADIO} m, que es aproximadamente el alcance de una cámara de velocidad. La comparación con 500 m está aparte, en su propia pestaña.")
st.write("**Distancia:** se mide contra las ubicaciones actuales de las cámaras, porque `camaras.csv` no trae fecha de instalación.")

tab_resumen, tab_puntos, tab_sin, tab_loc, tab_tiempo, tab_radio, tab_limites = st.tabs([
    "Resumen", "Puntos críticos", "Sin cámara", "Localidades", "Evolución", "300 m vs 500 m", "Limitaciones"])

col1, col2, col3 = tab_resumen.columns(3)
col1.metric("Víctimas a " + str(RADIO) + " m o menos de una cámara", f"{pct_cerca:.1f}%")
col2.metric("Puntos críticos sin cámara (de 50)", len(puntos_sin))
col3.metric("Motociclistas en esos puntos", f"{pct_motos:.1f}%")

tab_resumen.subheader("Hallazgos")
tab_resumen.write(f"1. De los 50 puntos con más víctimas, {len(puntos_sin)} no tienen una cámara a menos de {RADIO} m, y solo el {pct_cerca:.1f}% de las víctimas ocurrió cerca de una cámara.")
tab_resumen.write(f"2. En esos {len(puntos_sin)} puntos, el {pct_motos:.1f}% de las víctimas son motociclistas.")

g1 = pd.DataFrame([[f"≤ {RADIO} m", pct_cerca], [f"> {RADIO} m", pct_lejos]],
                  columns=["zona", "pct"])

fig1 = px.bar(g1, x="zona", y="pct", text_auto=".1f", color="zona",
              title="Víctimas según distancia a la cámara más cercana")
fig1.update_layout(yaxis_title="% de las víctimas", showlegend=False, title_x=0.5,
                   xaxis_title="Distancia a la cámara más cercana")
tab_resumen.plotly_chart(fig1, width="stretch")

g2 = cuadros.head(10).copy()
g2["Cámara"] = np.where(g2[cuadros_dist] <= RADIO, "Con cámara", "Sin cámara")
g2[cuadros_nombre] = g2[cuadros_nombre].astype(str)

fig2 = px.bar(g2, x=cuadros_nvict, y=cuadros_nombre, color="Cámara", orientation="h",
              title="10 puntos con más víctimas")
fig2.update_yaxes(autorange="reversed")
fig2.update_layout(title_x=0.5)

tab_puntos.write(f"Cada punto se pinta según tenga o no una cámara a {RADIO} m o menos.")
tab_puntos.plotly_chart(fig2, width="stretch")

tab_sin.write(f"Puntos críticos sin cámara: **{len(puntos_sin)} de 50**. Víctimas en esos puntos: **{len(vic_sin)}**.")

g3a = vic_sin[victimas_camaras_tipo].value_counts(normalize=True).mul(100).reset_index()
g3a.columns = ["tipo", "pct"]

fig3a = px.bar(g3a, x="pct", y="tipo", orientation="h",
               title="Tipo de víctima en puntos críticos sin cámara")
fig3a.update_layout(xaxis_title="% de las víctimas", title_x=0.5, yaxis_title="Tipo de víctima")
fig3a.update_yaxes(autorange="reversed")

orden = ["Madrugada (0-5)", "Mañana (6-11)", "Tarde (12-17)", "Noche (18-23)"]
g3b = vic_sin[victimas_camaras_franja].value_counts(normalize=True).reindex(orden).mul(100).reset_index()
g3b.columns = ["franja", "pct"]

fig3b = px.bar(g3b, x="franja", y="pct",
               title="Franja horaria en puntos críticos sin cámara")
fig3b.update_layout(yaxis_title="% de las víctimas", title_x=0.5, xaxis_title="Franja horaria")

col4, col5 = tab_sin.columns(2)
col4.plotly_chart(fig3a, width="stretch")
col5.plotly_chart(fig3b, width="stretch")

g4 = localidades.sort_values(localidades_tasa, ascending=False)

fig4a = px.bar(g4, x=localidades_tasa, y=localidades_nombre, orientation="h",
               title="Víctimas por 100.000 habitantes")
fig4a.update_yaxes(autorange="reversed")
fig4a.update_layout(yaxis_title="Localidad", xaxis_title="Víctimas por 100.000 habitantes",
                    title_x=0.5, height=600)

fig4b = px.bar(g4, x=localidades_cam, y=localidades_nombre, orientation="h",
               title="Número de cámaras por localidad")
fig4b.update_yaxes(autorange="reversed")
fig4b.update_layout(yaxis_title="Localidad", xaxis_title="Cámaras", title_x=0.5, height=600)

tab_loc.write("Las dos gráficas están en el mismo orden para comparar fila por fila si las localidades con más víctimas tienen más o menos cámaras.")
col6, col7 = tab_loc.columns(2)
col6.plotly_chart(fig4a, width="stretch")
col7.plotly_chart(fig4b, width="stretch")

g5 = victimas_camaras_2019.copy()
g5[victimas_camaras_anio] = g5[victimas_camaras_anio].astype(int)
g5["zona"] = np.where(g5[victimas_camaras_dist] <= RADIO, "Cerca de una cámara", "Resto de la ciudad")

por_anio = g5.groupby([victimas_camaras_anio, "zona"]).size().unstack(fill_value=0)

indice = (por_anio / por_anio.loc[2019] * 100).reset_index()
indice = indice.melt(id_vars=victimas_camaras_anio, var_name="zona", value_name="indice")

fig5 = px.line(indice, x=victimas_camaras_anio, y="indice", color="zona", markers=True,
               title="Víctimas por año con respecto a 2019")
fig5.update_layout(yaxis_title="Índice (2019 = 100)", xaxis_title="Año", title_x=0.5)
fig5.add_hline(y=100, line_dash="dash", line_color="gray",
               annotation_text="2019 = 100", annotation_position="bottom right")

tab_tiempo.write("Cada año se divide entre el valor de 2019 de su misma zona, para comparar el cambio relativo y no el tamaño de cada grupo.")
tab_tiempo.plotly_chart(fig5, width="stretch")

g6 = victimas_camaras.copy()
g6[victimas_camaras_anio] = g6[victimas_camaras_anio].astype(int)

por_anio_total = g6.groupby(victimas_camaras_anio).size().reset_index()
por_anio_total.columns = ["anio", "victimas"]
por_anio_total["Período"] = np.where(por_anio_total["anio"] < 2019, "Antes de 2019", "Desde 2019")

promedio_antes = por_anio_total[por_anio_total["anio"] < 2019]["victimas"].mean()
promedio_despues = por_anio_total[por_anio_total["anio"] >= 2019]["victimas"].mean()

fig6 = px.bar(por_anio_total, x="anio", y="victimas", color="Período", text_auto=True,
              title="Víctimas por año en toda la ciudad")
fig6.update_layout(xaxis_title="Año", yaxis_title="Víctimas", title_x=0.5)
fig6.update_xaxes(dtick=1)

tab_tiempo.write(f"Promedio anual antes de 2019: **{promedio_antes:,.0f}** | Desde 2019: **{promedio_despues:,.0f}**")
tab_tiempo.plotly_chart(fig6, width="stretch")

radios = [300, 500]
filas = []

for r in radios:
    pct = (victimas_camaras[victimas_camaras_dist] <= r).mean() * 100
    sin_r = top50[top50[cuadros_dist] > r]
    vic_r = victimas_camaras_2019[victimas_camaras_2019[victimas_camaras_cuadro].isin(sin_r[cuadros_nombre])]
    motos = (vic_r[victimas_camaras_tipo] == "MOTOCICLISTA").mean() * 100
    filas.append([r, pct, len(sin_r), motos])

comparacion = pd.DataFrame(filas, columns=["radio", "pct_cerca", "puntos_sin_camara", "pct_motos"])

tab_radio.write("Se repiten los tres números clave con cada radio. Esta comparación no cambia las demás gráficas, que siempre usan 300 m.")

col8, col9 = tab_radio.columns(2)
col8.subheader("Radio de 300 m")
col8.metric("Víctimas cerca de una cámara", f"{comparacion.loc[0, 'pct_cerca']:.1f}%")
col8.metric("Puntos críticos sin cámara (de 50)", int(comparacion.loc[0, "puntos_sin_camara"]))
col8.metric("Motociclistas en esos puntos", f"{comparacion.loc[0, 'pct_motos']:.1f}%")
col9.subheader("Radio de 500 m")
col9.metric("Víctimas cerca de una cámara", f"{comparacion.loc[1, 'pct_cerca']:.1f}%")
col9.metric("Puntos críticos sin cámara (de 50)", int(comparacion.loc[1, "puntos_sin_camara"]))
col9.metric("Motociclistas en esos puntos", f"{comparacion.loc[1, 'pct_motos']:.1f}%")

tab_radio.write("Con 500 m el porcentaje de víctimas cerca de una cámara aumenta y bajan los puntos sin cámara, pero la conclusión se mantiene: la mayoría de los puntos críticos sigue sin cámara y cerca de la mitad de las víctimas son motociclistas.")
tab_radio.dataframe(comparacion.round(1), hide_index=True)

tab_limites.write("- `camaras.csv` no tiene fechas de instalación, así que no se puede saber qué cámaras existían en cada año. Incluye además 9 cámaras de agosto de 2026.")
tab_limites.write("- Las gráficas 5 y 6 muestran cómo cambian las víctimas en el tiempo, pero no prueban por sí solas que las cámaras sean la causa del cambio.")