# ¿Dónde poner las próximas Cámaras Salvavidas?

Proyecto 2 │ DATA-1002 Aplicaciones en Ciencia de Datos │ Universidad de los Andes │ 2026-2

**Miembros del grupo 8:** 

- Kiary Cardenas Castro
- Jose Alexander Santos Cobos


**Dashboard:** https://aplicacionesproyecto2.streamlit.app/

**Presentación:** `reports/presentacion.pdf`

En pocas palabras: analizamos los muertos y heridos en siniestros viales de Bogotá entre 2019 y 2025 y los comparamos con la ubicación de las Cámaras Salvavidas. De los 50 lugares con más víctimas, 34 no tienen una cámara registrada a 300 metros o menos. Proponemos que la Secretaría Distrital de Movilidad revise primero esos puntos cuando decida dónde poner las próximas cámaras.

---

## 1. ¿De qué trata?

### El problema
En los últimos años, más de 500 personas han muerto cada año en siniestros viales en Bogotá (565 en 2024) y cerca de 20.000 han quedado heridas. Una de las herramientas de la Secretaría Distrital de Movilidad (SDM) para bajar la velocidad son las Cámaras Salvavidas. Queríamos saber si las cámaras están en los lugares donde más gente muere o sale herida, y cuáles de esos lugares no tienen una.

### ¿Por qué ahora?
- En agosto de 2026 la SDM anunció 18 cámaras nuevas en la NQS, la avenida de Las Américas y la calle 26.
- La SDM dice que hay 129 cámaras operando y que salvan 42 vidas al año. En otro comunicado habló de 29 vidas al año.
- En agosto de 2026 el Gobierno nacional ordenó revisar todas las cámaras del país para ver si cumplen su objetivo.
- En septiembre de 2026 un concejal pidió demostrar con cifras qué cambió en cada punto después de instalar las cámaras.
- Según la SDM, entre enero y julio de 2026 las muertes en las vías subieron cerca de 33 % frente al mismo periodo de 2025.

### ¿A quién le sirve y qué decisión apoya?
Le sirve al comité de la SDM que decide dónde instalar las próximas cámaras. El análisis no reemplaza los estudios técnicos de la Secretaría: le entrega una lista ordenada de lugares para revisar primero.

### La pregunta
**¿Cuáles son los puntos de Bogotá con más muertos y heridos en siniestros viales entre 2019 y 2025 que no tienen una Cámara Salvavidas registrada a menos de 300 metros?**

### Cómo medimos cada cosa
- **Víctimas:** personas muertas más personas heridas. Usamos la gravedad a 30 días, que cuenta como muerta a la persona que falleció hasta 30 días después del siniestro. Los muertos también se muestran aparte.
- **Punto:** un cuadro de unos 300 × 300 metros sobre el mapa de la ciudad.
- **Puntos críticos:** los 50 cuadros con más víctimas. Usamos 50 porque es más o menos el número de sitios con cámara (41 sitios de la capa oficial más los 9 puntos nuevos de 2026).
- **Cámaras registradas:** las de la capa oficial de la SDM (actualizada por última vez en febrero de 2024) más las 18 anunciadas en agosto de 2026.
- **Cerca de una cámara:** a 300 metros o menos en línea recta de la cámara más cercana. También lo revisamos con 500 metros.
- **Punto con cámara:** un cuadro donde al menos una víctima ocurrió a 300 metros o menos de una cámara. Esta regla favorece a las cámaras, así que el número de puntos sin cámara no está inflado.
- **Periodo:** siniestros de 2019 a 2025. Los años 2015 a 2018 solo se usan para comparar el antes y el después.

### Preguntas de apoyo
1. ¿Qué porcentaje de las víctimas ocurrió a 300 metros o menos de una cámara? ¿A cuántos puntos críticos llegan las 18 cámaras nuevas de 2026?
2. ¿Qué localidades tienen más víctimas por cada 100.000 habitantes y cuántas cámaras tienen?
3. En los puntos críticos sin cámara, ¿quiénes son las víctimas y a qué horas ocurren los siniestros?
4. ¿Cómo cambiaron las víctimas cerca de las cámaras frente al resto de la ciudad entre 2015-2018 (antes de las cámaras) y 2022-2025?

### Lo que este análisis no dice
No mide si las cámaras bajan los siniestros, las cámaras se ponen donde ya había muchos siniestros, 2020 y 2021 fueron años de pandemia, la ciudad cambia de un año a otro y no tenemos la fecha en que empezó a funcionar cada cámara. Por eso no confirmamos ni negamos la cifra de 42 vidas al año. Lo que sí mostramos es dónde ocurren las víctimas y dónde están las cámaras.

---

## 2. ¿Qué datos usamos?

| Fuente | Quién la publica | Periodo que usamos | Qué es una fila | Tamaño | Consulta |
|---|---|---|---|---|---|
| Siniestros viales (SIGAT), archivo "2024" | Secretaría Distrital de Movilidad, en Datos Abiertos Bogotá | 2015-2024 (el archivo trae todos esos años) | hoja Siniestros: un siniestro · hoja Actor_vial: una persona involucrada | 278.614 siniestros y 608.155 personas | 18 nov 2026 |
| Siniestros viales (SIGAT), archivo 2025 | Observatorio de Movilidad de Bogotá (SDM) | 2025 | igual, pero con otros nombres de columnas | 11.573 siniestros y 28.029 personas | 18 nov 2026 |
| Cámaras Salvavidas, capa oficial | SDM (la misma capa del mapa de fotodeteccionbogota.com) | actualizada hasta febrero de 2024 | una cámara o un gabinete | 143 filas: 93 cámaras y 50 gabinetes | 21 nov 2026 |
| Cámaras nuevas de 2026 | Alcaldía de Bogotá (25 de agosto de 2026) | anunciadas en agosto de 2026 | un punto y sentido | 9 filas que suman 18 cámaras en 6 cruces | 21 nov 2026 |
| Población por localidad | DANE, proyecciones de población de Bogotá 2018-2035 | 2018-2025 | una localidad en un año | 160 filas (20 localidades × 8 años) | 21 nov 2026 |

Links:
- SIGAT 2015-2024: https://datosabiertos.bogota.gov.co/dataset/anuario-siniestralidad
- SIGAT 2025: https://observatorio.movilidadbogota.gov.co/publicaciones/anuarios
- Capa de cámaras: https://services2.arcgis.com/NEwhEo9GGSHXcRXV/ArcGIS/rest/services/Camaras_Salvavidas_5Feb2020/FeatureServer/2
- Cámaras nuevas: https://bogota.gov.co/mi-ciudad/movilidad/ubicaciones-de-las-nuevas-camaras-salvavidas-de-bogota-2026
- Población: https://www.dane.gov.co/index.php/estadisticas-por-tema/demografia-y-poblacion/proyecciones-de-poblacion/proyecciones-de-poblacion-bogota

### Limitaciones de cada fuente
- **SIGAT:** solo trae los siniestros que reporta la autoridad de tránsito, así que faltan casos, sobre todo de heridos leves. 15.065 siniestros de 2015 a 2020 no tienen coordenadas. El archivo 2025 solo trae la gravedad a 30 días y los siniestros con víctimas.
- **Capa de cámaras:** se actualizó por última vez en febrero de 2024 y no dice desde cuándo funciona cada cámara ni si estaba funcionando.
- **Cámaras nuevas:** la Alcaldía publicó los cruces, no las coordenadas. Las calculamos nosotros (ver más abajo).
- **Población:** es la gente que vive en cada localidad, no la que pasa por ella. Es una proyección y empieza en 2018.

### Licencias
- **SIGAT:** Secretaría Distrital de Movilidad, Anuario de Siniestralidad Vial, publicado en Datos Abiertos Bogotá con licencia Creative Commons Atribución-CompartirIgual 4.0 (CC BY-SA 4.0). Los archivos de `data/processed` salen de estos datos, así que los compartimos con la misma licencia.
- **Población:** Fuente: Departamento Administrativo Nacional de Estadística: www.dane.gov.co. Proyecciones de población de Bogotá por localidad 2018-2035. Los términos de uso del DANE permiten usar y transformar la información si se cita así.
- **Cámaras Salvavidas:** Secretaría Distrital de Movilidad, capa "Camaras_Salvavidas_5Feb2020" de ArcGIS, consultada el 21 de noviembre de 2026. La capa no dice qué licencia tiene; por eso citamos la fuente y la fecha de consulta.
- **Cámaras nuevas de 2026:** Alcaldía de Bogotá, "Ubicaciones de las nuevas Cámaras Salvavidas de Bogotá 2026", 25 de agosto de 2026.

### ¿De dónde salen los datos de las cámaras?
La página oficial de las cámaras, fotodeteccionbogota.com, muestra un mapa hecho en ArcGIS, el programa de mapas que usa la SDM. Para llegar a los datos de ese mapa hicimos esto:

1. En fotodeteccionbogota.com abrimos el código de la página (Ctrl + U) y buscamos la palabra "arcgis". Ahí está la dirección del mapa: `https://movilidadbogota.maps.arcgis.com/apps/webappviewer/index.html?id=aaff947d4c8343eb800bf23cbb80b613`
2. ArcGIS deja ver en texto cómo está armado cada mapa. Abrimos el del mapa de las cámaras: `https://movilidadbogota.maps.arcgis.com/sharing/rest/content/items/aaff947d4c8343eb800bf23cbb80b613/data?f=pjson`. Ahí dice que el mapa se llama "Dispositivos de Control" y que usa otro mapa por debajo, con el código `d63cde2290994f8c94682511f373dbe5`.
3. Abrimos ese segundo mapa: `https://movilidadbogota.maps.arcgis.com/sharing/rest/content/items/d63cde2290994f8c94682511f373dbe5/data?f=pjson`. Ahí aparece la capa "Cámara aprobada por el Ministerio de Transporte" y su dirección: `https://services2.arcgis.com/NEwhEo9GGSHXcRXV/ArcGIS/rest/services/Camaras_Salvavidas_5Feb2020/FeatureServer/2`
4. Bajamos esa capa por su API en el notebook `01b_camaras.ipynb` el 21 de noviembre de 2026, sin filtros (`where=1=1`, todos los campos). Trae 143 filas: 93 cámaras y 50 gabinetes (el gabinete es la caja donde se conectan las cámaras de cada sitio).

El "5Feb2020" del nombre es la fecha en que se creó la capa. La última vez que le cambiaron datos fue el 13 de febrero de 2024.

### Las 18 cámaras nuevas de 2026
La Alcaldía anunció 18 cámaras en 9 puntos: NQS con calle 25A, NQS con calle 9 (dos sentidos), NQS con calle 47A (dos sentidos), avenida de Las Américas con carrera 58 (dos sentidos), calle 26 con carrera 17 y calle 26 con carrera 25. Son 6 cruces. Las guardamos a mano en `data/raw/Camaras/camaras_nuevas.csv`, una fila por punto y sentido. Como la Alcaldía no publicó coordenadas, para cada cruce usamos la mediana de las coordenadas de los siniestros del SIGAT registrados en ese cruce, y como localidad la que más se repite ahí.

---

## 3. ¿Cómo unimos los datos?

```
Actor_vial (1 fila = 1 persona) ──muchos a uno──> Siniestros (1 fila = 1 siniestro)   [código del siniestro]
        │
        └─> víctimas con fecha, hora, localidad y coordenadas
                │
                ├── × Cámaras (cada siniestro con cada cámara) → distancia → cámara más cercana
                │        resultado: 1 fila por siniestro y 1 fila por víctima
                │
                ├── cuadros de 300 m → víctimas por cuadro → 50 puntos críticos
                │
                └── víctimas por localidad y año ──uno a uno──> Población DANE   [localidad + año]
```

| Unión | Llave | Tipo | Filas antes → después | Qué revisamos |
|---|---|---|---|---|
| SIGAT 2015-2024 + SIGAT 2025 | se apilan | `pd.concat` | 278.614 + 11.573 → 290.187 siniestros | 3 siniestros estaban en los dos archivos: dejamos uno → 290.184 |
| Personas + siniestros | código del siniestro | muchos a uno (`validate="m:1"`) | 205.182 víctimas → 198.030 con su siniestro | `indicator=True`: 7.152 sin pareja (7.143 heridos y 9 muertos), porque su siniestro no tenía coordenadas o tenía la coordenada de relleno |
| Siniestros × cámaras | coordenadas | todos con todos (`how="cross"`), año por año | 125.154 siniestros × 102 cámaras ≈ 12,8 millones de pares → 125.154 | nos quedamos con la cámara más cercana: exactamente una fila por siniestro (`validate="1:1"`) y ninguno sin distancia |
| Víctimas + distancia | código del siniestro | muchos a uno (`validate="m:1"`) | 198.030 → 198.030 | ninguna víctima quedó sin distancia |
| Víctimas por localidad y año + población | localidad + año | uno a uno (`validate="1:1"`) | 139 → 139 | las 139 filas encontraron pareja |

**Cómo se mide la distancia.** En Bogotá, un grado de latitud o de longitud mide casi lo mismo: unos 111.000 metros. Multiplicamos la diferencia de coordenadas por 111.000 y usamos el teorema de Pitágoras. Es una distancia en línea recta. Lo comparamos con la fórmula exacta para distancias sobre la Tierra y solo 20 de 138.178 víctimas cambian de grupo.

**Por qué año por año.** Unir todos los siniestros con todas las cámaras de una vez daba casi 13 millones de filas. Por partes es más liviano y el resultado es el mismo.

**Cómo se arman los cuadros.** 300 metros son unos 0,0027 grados. Dividimos la latitud y la longitud entre 0,0027 y redondeamos. Todas las víctimas con el mismo par de números quedan en el mismo cuadro.

---

## 4. Decisiones de limpieza

| Decisión | Por qué | Filas antes | Filas después |
|---|---|---|---|
| Juntar el archivo 2024 (trae 2015-2024) con el de 2025, después de igualar los nombres de las columnas | el 2025 viene aparte y con otros nombres | 278.614 + 11.573 | 290.187 |
| Pasar a número las coordenadas de 2025 | venían como texto con coma ("4,58") | | |
| Quitar 3 siniestros repetidos entre 2024 y 2025 (dejamos la versión de 2025) | el mismo código estaba en los dos archivos | 290.187 | 290.184 |
| Dejar solo siniestros con heridos o muertos, con la gravedad a 30 días | la pregunta es sobre víctimas; los "solo daños" casi no se registran desde 2023; la gravedad a 30 días es la única que trae 2025 | 290.184 | 130.018 |
| Quitar los siniestros sin coordenadas (todos de 2015 a 2020) | sin coordenadas no se puede medir la distancia a una cámara | 130.018 | 125.446 |
| Quitar 292 siniestros de 2022 con la coordenada 4.619318, -74.097908 | tenían 287 direcciones distintas de toda la ciudad: era una coordenada de relleno | 125.446 | 125.154 |
| Crear la franja horaria (madrugada 0-5, mañana 6-11, tarde 12-17, noche 18-23) | para ver a qué horas ocurren | | |
| Juntar las personas de 2015-2024 y 2025 y quitar 5 repetidas | eran las de los 3 siniestros repetidos | 636.184 | 636.179 |
| Dejar solo las personas muertas o heridas | ilesos no son víctimas | 636.179 | 205.182 |
| Dejar las víctimas cuyo siniestro quedó después de la limpieza | sin siniestro no hay coordenadas | 205.182 | 198.030 |
| No guardar edad ni sexo | no los usamos y así protegemos la privacidad | | |
| Cámaras: quitar los gabinetes | el gabinete es la caja, no la cámara | 143 | 93 |
| Agregar las 9 filas de las cámaras de 2026 | la capa oficial llega a febrero de 2024 | 93 | 102 |
| Población: área total de cada localidad, de 2018 a 2025 | el archivo trae cabecera, rural y total | 1.080 | 160 |
| Igualar los nombres de las localidades (mayúsculas, LA CANDELARIA → CANDELARIA, CIUDAD BOLIVAR → CIUDAD BOLÍVAR) | para unir la población con el SIGAT | | |
| Usar solo 2019-2025 para la pregunta | la red de cámaras funciona desde 2019 y 2025 es el último año con datos | 198.030 | 138.178 |

Con estas decisiones trabajamos con el 98,7 % de las víctimas de 2019 a 2025. En 2015-2018 se pierde más (8,2 %), porque ahí están casi todos los siniestros sin coordenadas. Por eso no comparamos números totales entre esos periodos, solo cuánto cambió cada zona.

Para revisar que los datos cuadran, comparamos 2024 con el anuario oficial de la SDM: el anuario reporta 565 muertos y 22.593 heridos; nosotros tenemos 565 muertos y 22.589 heridos.

---

## 5. Indicadores

| Indicador | Cómo se calcula | Unidad |
|---|---|---|
| Víctimas | muertos + heridos | personas |
| Muertos | personas que murieron hasta 30 días después del siniestro | personas |
| % de víctimas cerca de una cámara | víctimas a 300 m o menos de una cámara ÷ víctimas totales × 100 | % |
| Puntos críticos sin cámara | de los 50 cuadros con más víctimas, cuántos no tienen una cámara a 300 m o menos | cuadros |
| % de motociclistas en esos puntos | motociclistas ÷ víctimas en los puntos críticos sin cámara × 100 | % |
| Víctimas por 100.000 habitantes | víctimas de la localidad en 2019-2025 ÷ suma de su población en esos años × 100.000 (promedio por año) | víctimas por 100.000 habitantes al año |
| Cámaras por localidad | filas de la tabla de cámaras en cada localidad | cámaras |
| Cambio antes y después | (promedio anual 2022-2025 − promedio anual 2015-2018) ÷ promedio anual 2015-2018 × 100, por separado para las víctimas cerca de las cámaras de la capa oficial y para el resto | % |

Todos los indicadores del dashboard se recalculan con los filtros (años, tipo de persona y franja horaria), con dos excepciones: la pestaña de localidades usa siempre 2019-2025 y todas las víctimas, y la pestaña de evolución no usa el filtro de años porque necesita 2015-2018.


---

## 6. ¿Cómo está organizado el repo?

- `data/raw`: datos originales, sin cambios.
- `data/processed`: tablas limpias que salen de los notebooks.
- `notebooks`: el análisis, en orden del 01 al 08.
- `src`: el dashboard (`dashboard_streamlit.py`) y el script que pasa el Excel 2024 a `.csv.gz`.
- `outputs`: carpetas para gráficas y tablas (por ahora vacías; las gráficas están en el notebook 07 y en el dashboard).
- `reports`: la presentación.

El Excel 2024 del SIGAT pesa 121 MB y GitHub no deja subir archivos de más de 100 MB, así que no está en el repo. Lo pasamos a `.csv.gz` con `src/convertir_2024.py`.

## 7. ¿Cómo correr el proyecto?

1. `git clone https://github.com/Aplicaciones-26-2/Aplicaciones_proyecto2.git`
2. `pip install -r requirements.txt` (Python 3.12 o más reciente)
3. Correr los notebooks en orden, del 01 al 07. El 01b no hace falta: la capa de cámaras ya está guardada.
4. Desde la carpeta principal del repo: `streamlit run src/dashboard_streamlit.py`

---
## 8. Resultados

Todo es de 2019 a 2025, salvo el antes y después. Las gráficas están en el dashboard y en el notebook 07.

Víctimas: 138.178 muertos y heridos (unos 54 por día); 3.504 murieron.

Cerca de una cámara: solo el 8,8 % de las víctimas ocurrió a 300 m o menos de una cámara (17,6 % con 500 m). Las cámaras sí están en zonas con muchas víctimas, pero son pocas para todos los puntos críticos.

Puntos críticos: 34 de los 50 cuadros con más víctimas no tienen una cámara registrada cerca (25 de 50 con 500 m). Ahí hubo 7.114 víctimas y 210 muertos. El primero es la avenida de Las Américas con carrera 53: 260 víctimas y sin cámara.

Cámaras nuevas de 2026: llegan a 4 de los 50 puntos críticos. Sin ellas serían 38 sin cámara; con ellas, 34.

Quiénes y cuándo: en los 34 puntos, el 50,2 % de las víctimas son motociclistas (46,4 % en toda la ciudad) y el 44,6 % fue de noche o de madrugada.

Localidades: Los Mártires tiene la tasa más alta (817,5 víctimas por 100.000 habitantes al año) y ninguna cámara.

Antes y después: entre 2015-2018 y 2022-2025 las víctimas subieron 40,2 % cerca de las cámaras de la capa oficial y 48,3 % en el resto. Es una comparación descriptiva: no prueba que las cámaras funcionen.

Recomendación. Que la Secretaría incluya estos 34 puntos en el próximo estudio técnico para ubicar cámaras, empezando por los 16 que se repiten en 2019-2022 y 2023-2025. El siguiente paso es medir la velocidad en esos puntos y conseguir la fecha de instalación de cada cámara.

---

## 9. Limitaciones

El SIGAT solo trae los siniestros que se reportan.

Quitamos los siniestros sin coordenadas y una coordenada de relleno; en 2019-2025 quedó el 98,7 % de las víctimas.

La capa de cámaras llega a febrero de 2024, así que pudo faltar alguna (por eso decimos "registrada"). Tampoco sabemos desde cuándo funciona cada cámara ni si estaba prendida.

Las coordenadas de las cámaras nuevas son aproximadas y la distancia es en línea recta.

Los resultados dependen del radio de 300 m y del tamaño de los cuadros; por eso repetimos el análisis con 500 m.

No tenemos la causa de cada siniestro ni el tráfico de cada vía.

La población es la que vive en cada localidad, no la que pasa por ella.

El antes y después es descriptivo y no mide el efecto de las cámaras.

---

## 10. Fuentes de contexto

Ubicaciones de las 18 cámaras nuevas y cómo se escogieron (Alcaldía de Bogotá, 25 de agosto de 2026): https://bogota.gov.co/mi-ciudad/movilidad/ubicaciones-de-las-nuevas-camaras-salvavidas-de-bogota-2026

129 cámaras y 42 vidas al año (Semana, agosto de 2026): https://www.semana.com/vehiculos/articulo/en-donde-quedan-todas-las-camaras-de-fotomultas-en-bogota/202640/

29 vidas al año (Alcaldía de Bogotá): https://bogota.gov.co/mi-ciudad/movilidad/los-mitos-y-verdades-de-las-camaras-de-fotodeteccion-en-bogota

Revisión nacional de las cámaras (Vanguardia, agosto de 2026): https://www.vanguardia.com/colombia/2026/08/23/de-la-espriella-ordena-revisar-las-fotomultas-en-colombia-cuestiona-su-uso-para-recaudar-dinero/

El Concejo pide cifras por punto (Noticias RCN, septiembre de 2026): https://www.noticiasrcn.com/colombia/casi-nueve-de-cada-diez-pesos-recaudados-por-las-camaras-salvavidas-en-bogota-provienen-de-una-misma-infraccion-1060641

Aumento de muertes en 2026 (Enter.co): https://www.enter.co/?p=586129

Resultados del Anuario de Siniestralidad Vial 2024 (La República, abril de 2025): https://www.larepublica.co/economia/bogota-tuvo-la-tasa-de-mortalidad-mas-baja-en-siniestros-viales-en-2024-cerro-en-7-1-4106829