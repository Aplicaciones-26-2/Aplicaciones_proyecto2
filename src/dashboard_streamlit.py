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

orden = ["Madrugada (0-5)", "Mañana (6-11)", "Tarde (12-17)", "Noche (18-23)"]

victimas_camaras = pd.read_csv(RUTA + "victimas_camaras.csv.gz")
cuadros = pd.read_csv(RUTA + "cuadros.csv")
localidades = pd.read_csv(RUTA + "localidades.csv")

fila = np.round(victimas_camaras[victimas_camaras_lat] / TAMANIO_CUADRO).astype(int)
columna = np.round(victimas_camaras[victimas_camaras_lon] / TAMANIO_CUADRO).astype(int)
victimas_camaras[victimas_camaras_cuadro] = fila.astype(str) + "_" + columna.astype(str)

victimas_camaras[victimas_camaras_anio] = victimas_camaras[victimas_camaras_anio].astype(int)

anio_min = int(victimas_camaras[victimas_camaras_anio].min())
anio_max = int(victimas_camaras[victimas_camaras_anio].max())
tipos = sorted(victimas_camaras[victimas_camaras_tipo].dropna().unique())

st.sidebar.title("Filtros")
anios = st.sidebar.slider("Años", anio_min, anio_max, (2019, anio_max))
tipos_sel = st.sidebar.multiselect("Tipo de víctima", tipos, default=tipos)
franjas_sel = st.sidebar.multiselect("Franja horaria", orden, default=orden)
st.sidebar.caption(f"El radio de la cámara es fijo en {RADIO} m en todas las gráficas.")

victimas_camaras_tipo_franja = victimas_camaras
if len(tipos_sel) < len(tipos):
    victimas_camaras_tipo_franja = victimas_camaras_tipo_franja[victimas_camaras_tipo_franja[victimas_camaras_tipo].isin(tipos_sel)]
if len(franjas_sel) < len(orden):
    victimas_camaras_tipo_franja = victimas_camaras_tipo_franja[victimas_camaras_tipo_franja[victimas_camaras_franja].isin(franjas_sel)]

victimas_camaras_filtradas = victimas_camaras_tipo_franja[
    (victimas_camaras_tipo_franja[victimas_camaras_anio] >= anios[0]) &
    (victimas_camaras_tipo_franja[victimas_camaras_anio] <= anios[1])]

st.sidebar.write(f"Víctimas seleccionadas: **{len(victimas_camaras_filtradas):,}** de {len(victimas_camaras):,}")

st.title("Víctimas viales y cámaras de velocidad en Bogotá")

if len(victimas_camaras_filtradas) == 0:
    st.warning("No hay víctimas con los filtros elegidos. Amplía el rango de años o agrega tipos y franjas.")
    st.stop()

st.write("Este dashboard muestra las gráficas que sustentan los dos hallazgos del proyecto. Con los filtros por defecto (2019 a 2025, todos los tipos y franjas) se obtienen los hallazgos originales.")
st.write(f"**Radio de la cámara:** todas las gráficas usan {RADIO} m, que es aproximadamente el alcance de una cámara de velocidad. La comparación con 500 m está aparte, en su propia pestaña.")
st.write("**Distancia:** se mide contra las ubicaciones actuales de las cámaras, porque `camaras.csv` no trae fecha de instalación.")
st.write("**Puntos críticos:** son los 50 primeros de `cuadros.csv` y no cambian con los filtros; los filtros describen a las víctimas que hay en ellos.")

pct_cerca = (victimas_camaras_filtradas[victimas_camaras_dist] <= RADIO).mean() * 100
pct_lejos = 100 - pct_cerca

top50 = cuadros.head(50)
puntos_sin = top50[top50[cuadros_dist] > RADIO]
vic_sin = victimas_camaras_filtradas[victimas_camaras_filtradas[victimas_camaras_cuadro].isin(puntos_sin[cuadros_nombre])]

pct_motos = 0.0
if len(vic_sin) > 0:
    pct_motos = (vic_sin[victimas_camaras_tipo] == "MOTOCICLISTA").mean() * 100

tab_resumen, tab_puntos, tab_sin, tab_loc, tab_tiempo, tab_radio, tab_limites = st.tabs([
    "Resumen", "Puntos con más víctimas", "Puntos críticos sin cámara", "Localidades", "Evolución", "300 m vs 500 m", "Limitaciones"])

col1, col2, col3 = tab_resumen.columns(3)
col1.metric("Víctimas a " + str(RADIO) + " m o menos de una cámara", f"{pct_cerca:.1f}%")
col2.metric("Puntos críticos sin cámara (de 50)", len(puntos_sin))
col3.metric("Motociclistas en esos puntos", f"{pct_motos:.1f}%")

tab_resumen.subheader("Hallazgos")
tab_resumen.write(f"1. De los 50 puntos con más víctimas, {len(puntos_sin)} no tienen una cámara a menos de {RADIO} m, y solo el {pct_cerca:.1f}% de las víctimas ocurrió cerca de una cámara.")
tab_resumen.write(f"2. En esos {len(puntos_sin)} puntos, el {pct_motos:.1f}% de las víctimas seleccionadas son motociclistas.")

g1 = pd.DataFrame([[f"≤ {RADIO} m", pct_cerca], [f"> {RADIO} m", pct_lejos]],
                  columns=["zona", "pct"])

fig1 = px.bar(g1, x="zona", y="pct", text_auto=".1f", color="zona",
              title="Víctimas según distancia a la cámara más cercana")
fig1.update_layout(yaxis_title="% de las víctimas", showlegend=False, title_x=0.5,
                   xaxis_title="Distancia a la cámara más cercana")
tab_resumen.plotly_chart(fig1, width="stretch")

g2 = victimas_camaras_filtradas[victimas_camaras_cuadro].value_counts().head(10).reset_index()
g2.columns = [cuadros_nombre, cuadros_nvict]
g2 = g2.merge(cuadros[[cuadros_nombre, cuadros_dist]], on=cuadros_nombre, how="left")
g2["Cámara"] = np.where(g2[cuadros_dist] <= RADIO, "Con cámara", "Sin cámara")
g2[cuadros_nombre] = g2[cuadros_nombre].astype(str)

fig2 = px.bar(g2, x=cuadros_nvict, y=cuadros_nombre, color="Cámara", orientation="h",
              title="10 puntos con más víctimas")
fig2.update_yaxes(autorange="reversed")
fig2.update_layout(title_x=0.5)

tab_puntos.write(f"Se cuentan las víctimas seleccionadas por punto. Cada punto se pinta según tenga o no una cámara a {RADIO} m o menos.")
tab_puntos.plotly_chart(fig2, width="stretch")

tab_sin.write(f"Puntos críticos sin cámara: **{len(puntos_sin)} de 50**. Víctimas seleccionadas en esos puntos: **{len(vic_sin)}**.")

g3a = vic_sin[victimas_camaras_tipo].value_counts(normalize=True).mul(100).reset_index()
g3a.columns = ["tipo", "pct"]

fig3a = px.bar(g3a, x="pct", y="tipo", orientation="h",
               title="Tipo de víctima en puntos críticos sin cámara")
fig3a.update_layout(xaxis_title="% de las víctimas", title_x=0.5, yaxis_title="Tipo de víctima")
fig3a.update_yaxes(autorange="reversed")

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

tab_loc.write("Estas gráficas no cambian con los filtros, porque `localidades.csv` ya trae la tasa calculada con todas las víctimas. Están en el mismo orden para comparar fila por fila si las localidades con más víctimas tienen más o menos cámaras.")
col6, col7 = tab_loc.columns(2)
col6.plotly_chart(fig4a, width="stretch")
col7.plotly_chart(fig4b, width="stretch")

g5 = victimas_camaras_filtradas.copy()
g5["zona"] = np.where(g5[victimas_camaras_dist] <= RADIO, "Cerca de una cámara", "Resto de la ciudad")

por_anio = g5.groupby([victimas_camaras_anio, "zona"]).size().unstack(fill_value=0)
por_anio = por_anio.reindex(range(anios[0], anios[1] + 1), fill_value=0)

base = por_anio.loc[anios[0]].replace(0, np.nan)
indice = (por_anio / base * 100).reset_index()
indice = indice.melt(id_vars=victimas_camaras_anio, var_name="zona", value_name="indice")

fig5 = px.line(indice, x=victimas_camaras_anio, y="indice", color="zona", markers=True,
               title=f"Víctimas por año con respecto a {anios[0]}")
fig5.update_layout(yaxis_title=f"Índice ({anios[0]} = 100)", xaxis_title="Año", title_x=0.5)
fig5.update_xaxes(dtick=1)
fig5.add_hline(y=100, line_dash="dash", line_color="gray",
               annotation_text=f"{anios[0]} = 100", annotation_position="bottom right")

tab_tiempo.write(f"Cada año se divide entre el valor de {anios[0]} (primer año del rango) de su misma zona, para comparar el cambio relativo y no el tamaño de cada grupo.")
tab_tiempo.plotly_chart(fig5, width="stretch")

g6 = victimas_camaras_tipo_franja.copy()

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
tab_tiempo.write("Esta gráfica aplica los filtros de tipo y franja, pero no el de años, porque necesita todos los años para comparar el antes y el después.")
tab_tiempo.plotly_chart(fig6, width="stretch")

radios = [300, 500]
filas = []

for r in radios:
    pct = (victimas_camaras_filtradas[victimas_camaras_dist] <= r).mean() * 100
    sin_r = top50[top50[cuadros_dist] > r]
    vic_r = victimas_camaras_filtradas[victimas_camaras_filtradas[victimas_camaras_cuadro].isin(sin_r[cuadros_nombre])]
    motos = 0.0
    if len(vic_r) > 0:
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
tab_limites.write("- Con filtros muy estrechos (pocos años, un solo tipo o una sola franja) las cifras se calculan con pocas víctimas y varían mucho.")