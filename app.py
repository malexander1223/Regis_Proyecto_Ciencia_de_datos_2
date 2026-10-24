# REGIS | Aplicación Streamlit multipágina, metodología CRISP-DM
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import unicodedata

st.set_page_config(
    page_title="Regis | Inteligencia Comercial",
    page_icon="📦",
    layout="wide"
)

BASE = Path(".")

def leer_csv(nombre):
    ruta = BASE / nombre
    if ruta.exists():
        return pd.read_csv(ruta)
    return None

# Inicializar base de datos
BASE_TOTAL = leer_csv("Regis_1000_segmentado.csv")
DICCIONARIO = leer_csv("Regis_diccionario_opciones.csv")

if BASE_TOTAL is not None:
    MASCARA_REAL = BASE_TOTAL["origen"].str.lower().eq("real")
    BASE_REALES = BASE_TOTAL.loc[MASCARA_REAL].copy()
else:
    BASE_REALES = pd.DataFrame()

def titulo_seccion(numero, titulo, subtitulo):
    st.title(f"{numero} · {titulo}")
    st.markdown(f"*{subtitulo}*")
    st.markdown("---")

def aviso_limitacion(texto):
    st.warning(f"⚠️ **Limitación metodológica:** {texto}")

def ayuda_defensa(explicacion, palabras_clave):
    with st.expander("💡 Ayuda para la Defensa del Proyecto"):
        st.markdown(explicacion)
        st.caption(f"**Palabras clave:** {palabras_clave}")

def pct_texto(valor):
    return f"{valor:.1f}%"

def es_interes_directo(df):
    if df.empty or 'interes' not in df.columns:
        return 0.0
    return df['interes'].str.lower().eq('si').mean() * 100

def es_condicionado(df):
    if df.empty or 'interes' not in df.columns:
        return 0.0
    return df['interes'].str.lower().str.contains('prueba').mean() * 100

def es_tradicional(df):
    if df.empty or 'metodo_control' not in df.columns:
        return 0.0
    return df['metodo_control'].str.lower().isin(['tradicional', 'ninguno']).mean() * 100

def pagina_intro_negocio():
    titulo_seccion("01", "Introducción y negocio", "¿Qué necesita conocer Regis antes de diseñar y comercializar su software?")
    st.markdown("**REGIS** es una propuesta de software de gestión de inventarios bajo suscripción (SaaS) para comerciantes de Centro y Max Paredes, La Paz.")
    
    st.subheader("Objetivo central")
    st.write("Identificar qué segmentos de comerciantes presentan mayor potencial comercial para la implementación de un software de gestión de inventarios.")
    
    st.subheader("Las ocho preguntas de negocio")
    preguntas = [
        "¿Existe una necesidad real de una solución de gestión de inventarios?",
        "¿Qué segmentos presentan mayor necesidad potencial?",
        "¿Qué perfiles demográficos y económicos declaran mayor interés?",
        "¿En qué sectores comerciales se concentran las dificultades potenciales?",
        "¿Qué segmentos parecen más atractivos comercialmente?",
        "¿Qué funcionalidades del software conviene priorizar?",
        "¿Qué facilita la adopción y reduce la curva de aprendizaje?",
        "¿Qué rangos de precio mensual prefieren los distintos segmentos?"
    ]
    for i, q in enumerate(preguntas, 1):
        st.markdown(f"**P{i}.** {q}")

    st.subheader("Indicadores base (Comerciantes Reales)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Interés directo", pct_texto(es_interes_directo(BASE_REALES)))
    col2.metric("Condicionado a prueba", pct_texto(es_condicionado(BASE_REALES)))
    col3.metric("Control tradicional/ninguno", pct_texto(es_tradicional(BASE_REALES)))
    
    aviso_limitacion("No existen mediciones directas de pérdidas de inventario o ventas efectivas en el conjunto de variables de la encuesta.")
    ayuda_defensa("El problema era decidir a qué comerciantes dirigirnos, qué funciones construir primero y bajo qué condiciones lanzar Regis.", "SaaS, KPI, CRISP-DM, OSEMN")

def pagina_comprension_datos():
    titulo_seccion("02", "Comprensión de datos", "Procedencia, estructura, calidad y alcance de la información.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Encuestas reales", len(BASE_REALES))
    col2.metric("Registros sintéticos", len(BASE_TOTAL) - len(BASE_REALES) if BASE_TOTAL is not None else 0)
    col3.metric("Base consolidada", len(BASE_TOTAL) if BASE_TOTAL is not None else 0)
    st.info("La ampliación sintética sirve para fines experimentales, no representan nuevos comerciantes encuestados en el trabajo de campo.")

def pagina_preparacion_eda():
    titulo_seccion("03", "Preparación y EDA", "Procesamiento y análisis exploratorio inicial de los registros.")
    st.write("Limpieza de espacios, transformación de formatos y normalización de variables multirrespuesta.")

def pagina_modelado():
    titulo_seccion("04", "Modelado", "Resultados de segmentación (K-Means) y clasificación supervisada.")
    st.write("Modelos generados y evaluados: K-Means, Regresión Logística y Árboles de Decisión.")

def pagina_evaluacion():
    titulo_seccion("05", "Evaluación del Negocio", "Respuestas empíricas sustentadas en datos para la toma de decisiones.")
    st.write("En base a los clusters y las métricas obtenidas se evalúa la viabilidad del software Regis.")

def pagina_simulador():
    titulo_seccion("06", "Simulador de Mercado", "Evaluación de escenarios comerciales y potencial de mercado.")
    st.write("Simulador interactivo para estimar la captación en base a las variables ajustadas.")

def pagina_conclusiones():
    titulo_seccion("07", "Conclusiones", "Directrices estratégicas para el lanzamiento y próximos pasos.")
    st.write("Recomendaciones clave basadas en la metodología analítica CRISP-DM.")

# Configuración de navegación multipágina
PAGINAS = {
    "PROYECTO": [
        st.Page(pagina_intro_negocio, title="1. Introducción y negocio", icon="💼", default=True),
        st.Page(pagina_comprension_datos, title="2. Comprensión de datos", icon="📊"),
        st.Page(pagina_preparacion_eda, title="3. Preparación y EDA", icon="🔧"),
        st.Page(pagina_modelado, title="4. Modelado y evaluación", icon="🧠"),
        st.Page(pagina_evaluacion, title="5. Evaluación", icon="📈"),
        st.Page(pagina_simulador, title="6. Implementación - Simulador", icon="🧮"),
        st.Page(pagina_conclusiones, title="7. Conclusiones", icon="🏁"),
    ]
}

st.navigation(PAGINAS, position="sidebar", expanded=True).run()
