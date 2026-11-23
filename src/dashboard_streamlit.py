import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="¿Dónde poner las próximas Cámaras Salvavidas?", layout="wide")

RUTA = "data/processed/"
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
cuadros_muertos = "muertos"
cuadros_dist = "distancia_min"
cuadros_lat = "latitud"
cuadros_lon = "longitud"
cuadros_dir = "direccion"
cuadros_loc = "localidad"
cuadros_puesto = "puesto"

localidades_nombre = "localidad"
localidades_tasa = "tasa_victimas"
localidades_cam = "camaras"

camaras_lat = "latitud"
camaras_lon = "longitud"
camaras_dir = "direccion"

orden = ["Madrugada (0-5)", "Mañana (6-11)", "Tarde (12-17)", "Noche (18-23)"]

victimas_camaras = pd.read_csv(RUTA + "victimas_camaras.csv.gz")
localidades = pd.read_csv(RUTA + "localidades.csv")
camaras = pd.read_csv(RUTA + "camaras.csv")

fila = np.round(victimas_camaras[victimas_camaras_lat] / TAMANIO_CUADRO).astype(int)
columna = np.round(victimas_camaras[victimas_camaras_lon] / TAMANIO_CUADRO).astype(int)
victimas_camaras[victimas_camaras_cuadro] = fila.astype(str) + "_" + columna.astype(str)

victimas_camaras[victimas_camaras_anio] = victimas_camaras[victimas_camaras_anio].astype(int)

anio_min = 2019
anio_max = int(victimas_camaras[victimas_camaras_anio].max())
tipos = sorted(victimas_camaras[victimas_camaras_tipo].dropna().unique())

st.sidebar.title("Filtros")
anios = st.sidebar.slider("Período", anio_min, anio_max, (anio_min, anio_max))
tipos_sel = st.sidebar.multiselect("Tipo de persona afectada", tipos, default=tipos)
franjas_sel = st.sidebar.multiselect("Franja horaria", orden, default=orden)

victimas_camaras_tipo_franja = victimas_camaras
if len(tipos_sel) < len(tipos):
    victimas_camaras_tipo_franja = victimas_camaras_tipo_franja[victimas_camaras_tipo_franja[victimas_camaras_tipo].isin(tipos_sel)]
if len(franjas_sel) < len(orden):
    victimas_camaras_tipo_franja = victimas_camaras_tipo_franja[victimas_camaras_tipo_franja[victimas_camaras_franja].isin(franjas_sel)]

victimas_camaras_filtradas = victimas_camaras_tipo_franja[
    (victimas_camaras_tipo_franja[victimas_camaras_anio] >= anios[0]) &
    (victimas_camaras_tipo_franja[victimas_camaras_anio] <= anios[1])]

n_filtradas_txt = "{:,}".format(len(victimas_camaras_filtradas)).replace(",", ".")
n_total_txt = "{:,}".format(len(victimas_camaras)).replace(",", ".")
st.sidebar.write("Víctimas en la selección: **{}** de {}".format(n_filtradas_txt, n_total_txt))

st.title("¿Dónde poner las próximas Cámaras Salvavidas?")
st.caption("Pregunta: ¿Cuáles son los puntos de Bogotá con más muertos y heridos en siniestros viales entre 2019 y 2025 que no tienen una Cámara Salvavidas registrada a menos de 300 metros?")
st.write("Datos: siniestros viales 2019–2025 (SIGAT, Secretaría de Movilidad) · cámaras registradas: capa oficial de la Secretaría (febrero de 2024) más las 18 anunciadas en agosto de 2026 · población por localidad (DANE).")
st.write("Analizamos siete años de siniestros viales en Bogotá. De los 50 lugares con más muertos y heridos, 34 no tienen una cámara a menos de 300 metros, y la mitad de las víctimas en esos lugares son motociclistas. Por eso recomendamos que las próximas cámaras empiecen por esos puntos.")

if len(victimas_camaras_filtradas) == 0:
    st.warning("No hay víctimas con la selección actual. Amplíe el período o agregue tipos y franjas.")
    st.stop()

pct_cerca = (victimas_camaras_filtradas[victimas_camaras_dist] <= 300).mean() * 100
pct_lejos = 100 - pct_cerca
pct_cerca_txt = "{:.1f}".format(pct_cerca).replace(".", ",")
pct_lejos_txt = "{:.1f}".format(pct_lejos).replace(".", ",")

dias = (anios[1] - anios[0] + 1) * 365.25
por_dia_txt = "{:.0f}".format(len(victimas_camaras_filtradas) / dias)

# Puntos críticos
vic_puntos = victimas_camaras_filtradas.copy()
vic_puntos["muerto"] = vic_puntos["Gravedad_Indicador_30d"] == "MUERTO"

vic_puntos["cerca_oficial"] = (vic_puntos[victimas_camaras_dist] <= 300) & (~vic_puntos["id_camara"].str.startswith("NUEVA"))

puntos = vic_puntos.groupby(victimas_camaras_cuadro).agg(
    victimas=(victimas_camaras_dist, "count"),
    muertos=("muerto", "sum"),
    distancia_min=(victimas_camaras_dist, "min"),
    con_oficial=("cerca_oficial", "max"),
    latitud=(victimas_camaras_lat, "mean"),
    longitud=(victimas_camaras_lon, "mean"),
).reset_index()

puntos = puntos.sort_values([cuadros_nvict, cuadros_muertos, cuadros_nombre], ascending=[False, False, True]).reset_index(drop=True)
puntos[cuadros_puesto] = puntos.index + 1

top50 = puntos.head(50)

# Dirección y localidad más comunes
en_top50 = vic_puntos[vic_puntos[victimas_camaras_cuadro].isin(top50[cuadros_nombre])]
nombres = en_top50.groupby(victimas_camaras_cuadro).agg(
    direccion=("Direccion", lambda x: x.mode()[0]),
    localidad=("Localidad", lambda x: x.mode()[0]),
).reset_index()
top50 = top50.merge(nombres, on=cuadros_nombre, how="left", validate="1:1")

puntos_sin = top50[top50[cuadros_dist] > 300]
vic_sin = victimas_camaras_filtradas[victimas_camaras_filtradas[victimas_camaras_cuadro].isin(puntos_sin[cuadros_nombre])]
n_vic_sin_txt = "{:,}".format(len(vic_sin)).replace(",", ".")

pct_motos_ciudad = (victimas_camaras_filtradas[victimas_camaras_tipo] == "MOTOCICLISTA").mean() * 100
pct_motos = 0.0
if len(vic_sin) > 0:
    pct_motos = (vic_sin[victimas_camaras_tipo] == "MOTOCICLISTA").mean() * 100
pct_motos_txt = "{:.1f}".format(pct_motos).replace(".", ",")
pct_motos_ciudad_txt = "{:.1f}".format(pct_motos_ciudad).replace(".", ",")
dif_motos_txt = "{:+.1f}".format(pct_motos - pct_motos_ciudad).replace(".", ",")

tab_resumen, tab_puntos, tab_perfil, tab_loc, tab_tiempo, tab_radio, tab_alcance = st.tabs([
    "Resumen ejecutivo", "Dónde actuar", "Quiénes y cuándo", "Localidades", "Evolución", "Sensibilidad", "Alcance"])

col1, col2, col3, col4 = tab_resumen.columns(4)
col1.metric("Personas muertas o heridas", n_filtradas_txt)
col1.caption("Aproximadamente {} personas por día".format(por_dia_txt))
col2.metric("Víctimas a 300 m o menos de una cámara", "{} %".format(pct_cerca_txt))
col3.metric("Puntos críticos sin cámara", "{} de 50".format(len(puntos_sin)))
col4.metric("Motociclistas en esos puntos", "{} %".format(pct_motos_txt))

tab_resumen.subheader("Mensajes clave")
tab_resumen.write("1. **{} %** de las víctimas ocurrió a 300 m o menos de una cámara. El {} % restante ocurrió fuera de la red actual.".format(pct_cerca_txt, pct_lejos_txt))
tab_resumen.write("2. **{} de los 50** puntos con más víctimas no tienen una cámara cercana. En ellos hay {} víctimas en el período seleccionado.".format(len(puntos_sin), n_vic_sin_txt))
tab_resumen.write("3. En esos puntos, **{} %** de las víctimas son motociclistas (toda la ciudad: {} %, una diferencia de {} puntos).".format(pct_motos_txt, pct_motos_ciudad_txt, dif_motos_txt))

g1 = pd.DataFrame([["≤ 300 m", pct_cerca], ["> 300 m", pct_lejos]],
                  columns=["zona", "pct"])

fig1 = px.bar(g1, x="zona", y="pct", text_auto=".1f", color="zona",
              color_discrete_map={"≤ 300 m": "#2CA02C", "> 300 m": "#D62728"},
              title="{} % de las víctimas ocurrió cerca de una cámara".format(pct_cerca_txt))
fig1.update_layout(yaxis_title="% de las víctimas", showlegend=False, title_x=0.5,
                   xaxis_title="Distancia a la cámara más cercana", separators=",.")
tab_resumen.plotly_chart(fig1, width="stretch")

tab_resumen.subheader("Siguiente paso propuesto")
tab_resumen.write("Priorizar la evaluación de cámaras en los puntos sin cobertura con más víctimas:")

tabla_prioridad = puntos_sin.head(5)[[cuadros_puesto, cuadros_dir, cuadros_loc, cuadros_nvict, cuadros_muertos]].copy()
tabla_prioridad.columns = ["Puesto", "Ubicación", "Localidad", "Víctimas", "Muertos"]
tab_resumen.dataframe(tabla_prioridad, hide_index=True, width="stretch")

mapa_puntos = top50.copy()
mapa_puntos["color"] = np.where(mapa_puntos[cuadros_dist] <= 300, "#2CA02C", "#D62728")
mapa_puntos["tamanio"] = mapa_puntos[cuadros_nvict] * 0.7
mapa_puntos = mapa_puntos[[cuadros_lat, cuadros_lon, "color", "tamanio"]]
mapa_puntos.columns = ["lat", "lon", "color", "tamanio"]

mapa_camaras = camaras[[camaras_lat, camaras_lon]].copy()
mapa_camaras.columns = ["lat", "lon"]
# Las cámaras de la capa oficial en azul y las 18 nuevas de 2026 en naranja
mapa_camaras["color"] = np.where(camaras["id_camara"].str.startswith("NUEVA"), "#FF8C00", "#138AD9")
mapa_camaras["tamanio"] = 70

mapa = pd.concat([mapa_puntos, mapa_camaras], ignore_index=True)

g2 = top50.head(10).copy()
g2["Cámara"] = np.where(g2[cuadros_dist] <= 300, "Con cámara", "Sin cámara")
g2["Punto"] = g2[cuadros_puesto].astype(str) + ". " + g2[cuadros_dir]

fig2 = px.bar(g2, x=cuadros_nvict, y="Punto", color="Cámara", orientation="h",
              color_discrete_map={"Con cámara": "#2CA02C", "Sin cámara": "#D62728"},
              category_orders={"Punto": g2["Punto"].tolist()},
              title="{} de los 10 puntos con más víctimas no tienen cámara".format((g2["Cámara"] == "Sin cámara").sum()))
fig2.update_yaxes(autorange="reversed")
fig2.update_layout(title_x=0.5, xaxis_title="Víctimas", yaxis_title="", separators=",.")

tab_puntos.subheader("{} de los 50 puntos con más víctimas no tienen una cámara a 300 m o menos".format(len(puntos_sin)))
tab_puntos.write(":red[●] Punto crítico sin cámara · :green[●] Punto crítico con cámara · :blue[●] Cámara de la capa oficial · :orange[●] Cámara nueva de 2026 (el tamaño del punto crítico crece con las víctimas)")
tab_puntos.map(mapa, latitude="lat", longitude="lon", color="color", size="tamanio")
# Cuántos puntos críticos quedarían sin cámara si no contamos las de 2026
n_sin_oficial = int((~top50["con_oficial"]).sum())
tab_puntos.write("Sin las 18 cámaras de 2026 serían **{}** puntos críticos sin cámara; con ellas son **{}**.".format(n_sin_oficial, len(puntos_sin)))
tab_puntos.plotly_chart(fig2, width="stretch")

g3a = vic_sin[victimas_camaras_tipo].value_counts(normalize=True).mul(100).reset_index()
g3a.columns = ["tipo", "pct"]

fig3a = px.bar(g3a, x="pct", y="tipo", orientation="h", text_auto=".1f",
               title="Quiénes: {} % son motociclistas".format(pct_motos_txt))
fig3a.update_layout(xaxis_title="% de las víctimas", title_x=0.5, yaxis_title="", separators=",.")
fig3a.update_yaxes(autorange="reversed")

g3b = vic_sin[victimas_camaras_franja].value_counts(normalize=True).reindex(orden).mul(100).reset_index()
g3b.columns = ["franja", "pct"]

pct_noche = g3b[g3b["franja"].isin(["Noche (18-23)", "Madrugada (0-5)"])]["pct"].sum()
pct_noche_txt = "{:.1f}".format(pct_noche).replace(".", ",")
fig3b = px.bar(g3b, x="franja", y="pct", text_auto=".1f",
               title="Cuándo: {} % fue de noche o de madrugada".format(pct_noche_txt))
fig3b.update_layout(yaxis_title="% de las víctimas", title_x=0.5, xaxis_title="", separators=",.")

tab_perfil.write("Puntos críticos sin cámara: **{} de 50** · Víctimas en esos puntos: **{}**".format(len(puntos_sin), n_vic_sin_txt))
col5, col6 = tab_perfil.columns(2)
col5.plotly_chart(fig3a, width="stretch")
col6.plotly_chart(fig3b, width="stretch")

g4 = localidades.sort_values(localidades_tasa, ascending=False)

loc_top = g4.iloc[0]
loc_top_tasa_txt = "{:.1f}".format(loc_top[localidades_tasa]).replace(".", ",")
n_loc_sin_camara = int((localidades[localidades_cam] == 0).sum())

fig4a = px.bar(g4, x=localidades_tasa, y=localidades_nombre, orientation="h",
               title="{} tiene la tasa más alta: {} por 100.000 habitantes".format(loc_top[localidades_nombre].title(), loc_top_tasa_txt))
fig4a.update_yaxes(autorange="reversed")
fig4a.update_layout(yaxis_title="", xaxis_title="Víctimas por 100.000 habitantes al año",
                    title_x=0.5, height=600, separators=",.")

fig4b = px.bar(g4, x=localidades_cam, y=localidades_nombre, orientation="h",
               title="{} localidades no tienen ninguna cámara".format(n_loc_sin_camara))
fig4b.update_yaxes(autorange="reversed")
fig4b.update_layout(yaxis_title="", xaxis_title="Cámaras", title_x=0.5, height=600)

tab_loc.write("**{}** tiene la tasa más alta ({} víctimas por 100.000 habitantes al año) y {} cámaras. {} localidades no tienen ninguna cámara.".format(
    loc_top[localidades_nombre].title(), loc_top_tasa_txt, int(loc_top[localidades_cam]), n_loc_sin_camara))
tab_loc.caption("Esta pestaña usa todas las víctimas de 2019 a 2025 y no cambia con los filtros.")
col7, col8 = tab_loc.columns(2)
col7.plotly_chart(fig4a, width="stretch")
col8.plotly_chart(fig4b, width="stretch")

g5 = victimas_camaras_tipo_franja.copy()
# En el antes y después no contamos las cámaras de 2026 porque entre 2015 y 2025 todavía no existían
nueva = g5["id_camara"].str.startswith("NUEVA")
g5["zona"] = np.where((g5[victimas_camaras_dist] <= 300) & (~nueva), "Cerca de una cámara", "Resto de la ciudad")

por_anio = g5.groupby([victimas_camaras_anio, "zona"]).size().unstack(fill_value=0)

base = por_anio[por_anio.index <= 2018].mean().replace(0, np.nan)
despues = por_anio[por_anio.index >= 2022].mean()
cambio = (despues - base) / base * 100
cambio_cerca_txt = "{:.1f}".format(cambio["Cerca de una cámara"]).replace(".", ",")
cambio_resto_txt = "{:.1f}".format(cambio["Resto de la ciudad"]).replace(".", ",")
cambio_cerca_signo = "{:+.1f}".format(cambio["Cerca de una cámara"]).replace(".", ",")
cambio_resto_signo = "{:+.1f}".format(cambio["Resto de la ciudad"]).replace(".", ",")

indice = (por_anio / base * 100).reset_index()
indice = indice.melt(id_vars=victimas_camaras_anio, var_name="zona", value_name="indice")

fig5 = px.line(indice, x=victimas_camaras_anio, y="indice", color="zona", markers=True,
               title="Cambio frente a 2015-2018: {} % cerca de las cámaras y {} % en el resto".format(cambio_cerca_signo, cambio_resto_signo))
fig5.update_layout(yaxis_title="Índice (promedio 2015-2018 = 100)", xaxis_title="Año", title_x=0.5,
                   legend_title_text="", separators=",.")
fig5.update_xaxes(dtick=1)
fig5.add_hline(y=100, line_dash="dash", line_color="gray")

g6 = victimas_camaras_tipo_franja.copy()

por_anio_total = g6.groupby(victimas_camaras_anio).size().reset_index()
por_anio_total.columns = ["anio", "victimas"]
por_anio_total["Período"] = np.where(por_anio_total["anio"] < 2019, "2015-2018", "2019-2025")

promedio_antes = por_anio_total[por_anio_total["anio"] < 2019]["victimas"].mean()
promedio_despues = por_anio_total[por_anio_total["anio"] >= 2019]["victimas"].mean()
promedio_antes_txt = "{:,.0f}".format(promedio_antes).replace(",", ".")
promedio_despues_txt = "{:,.0f}".format(promedio_despues).replace(",", ".")

fig6 = px.bar(por_anio_total, x="anio", y="victimas", color="Período", text_auto=",d",
              title="Víctimas por año en toda la ciudad")
fig6.update_layout(xaxis_title="Año", yaxis_title="Víctimas", title_x=0.5, separators=",.")
fig6.update_xaxes(dtick=1)

tab_tiempo.write("Lectura descriptiva: no mide el efecto de las cámaras. Esta pestaña no usa el filtro de período, porque necesita los años de antes de las cámaras (2015-2018).")
tab_tiempo.write("Entre 2015-2018 y 2022-2025 las víctimas cambiaron **{} %** cerca de las cámaras y **{} %** en el resto de la ciudad.".format(cambio_cerca_txt, cambio_resto_txt))
tab_tiempo.plotly_chart(fig5, width="stretch")
tab_tiempo.write("Promedio anual: **{}** víctimas en 2015-2018 y **{}** en 2019-2025. Ojo: en 2015-2018 faltan más siniestros sin coordenadas, por eso esos años se ven más bajos de lo que fueron.".format(promedio_antes_txt, promedio_despues_txt))
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

pct_300_txt = "{:.1f}".format(comparacion.loc[0, "pct_cerca"]).replace(".", ",")
pct_500_txt = "{:.1f}".format(comparacion.loc[1, "pct_cerca"]).replace(".", ",")
motos_300_txt = "{:.1f}".format(comparacion.loc[0, "pct_motos"]).replace(".", ",")
motos_500_txt = "{:.1f}".format(comparacion.loc[1, "pct_motos"]).replace(".", ",")
puntos_300 = int(comparacion.loc[0, "puntos_sin_camara"])
puntos_500 = int(comparacion.loc[1, "puntos_sin_camara"])

col9, col10 = tab_radio.columns(2)
col9.subheader("Alcance de 300 m")
col9.metric("Víctimas cerca de una cámara", "{} %".format(pct_300_txt))
col9.metric("Puntos críticos sin cámara", "{} de 50".format(puntos_300))
col9.metric("Motociclistas en esos puntos", "{} %".format(motos_300_txt))
col10.subheader("Alcance de 500 m")
col10.metric("Víctimas cerca de una cámara", "{} %".format(pct_500_txt))
col10.metric("Puntos críticos sin cámara", "{} de 50".format(puntos_500))
col10.metric("Motociclistas en esos puntos", "{} %".format(motos_500_txt))

tab_radio.write("Con un alcance de 500 m, las víctimas cerca de una cámara pasan de {} % a {} % y los puntos críticos sin cámara bajan de {} a {}. La conclusión se mantiene: la mayoría de las víctimas sigue fuera de la red.".format(
    pct_300_txt, pct_500_txt, puntos_300, puntos_500))

tab_alcance.write("- Se mide contra las cámaras registradas: la capa oficial de la Secretaría (febrero de 2024) más las 18 cámaras anunciadas en agosto de 2026, que están en 9 ubicaciones. No hay fechas de instalación y pudo faltar alguna cámara instalada entre 2024 y 2026.")
tab_alcance.write("- La distancia es en línea recta y se toma contra la cámara más cercana.")
tab_alcance.write("- Un punto crítico es un cuadro de 300 m dentro de los 50 con más víctimas según la selección (sin filtros: 2019-2025). Entre 2019-2022 y 2023-2025 coinciden 24 de los 50.")
tab_alcance.write("- Los siniestros sin coordenadas (todos de 2015 a 2020) no se incluyen, por lo que los primeros años quedan con menos víctimas.")
tab_alcance.write("- La evolución en el tiempo es descriptiva y no prueba que las cámaras sean la causa del cambio.")
tab_alcance.write("- Con períodos cortos o un solo tipo de víctima, las cifras se calculan con pocos casos y varían mucho.")
tab_alcance.write("- La población del DANE es la que vive en cada localidad, no la que pasa por ella.")
tab_alcance.caption("Fuentes: Secretaría Distrital de Movilidad, Anuario de Siniestralidad Vial (Datos Abiertos Bogotá, licencia CC BY-SA 4.0) · Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co · Secretaría Distrital de Movilidad, capa de Cámaras Salvavidas (ArcGIS) · Alcaldía de Bogotá, ubicaciones de las nuevas Cámaras Salvavidas 2026.")