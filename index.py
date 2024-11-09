import os
import requests
import streamlit as st
import google.auth
import google_auth_oauthlib.flow
from google.oauth2.credentials import Credentials
import google.generativeai as genai
import speech_recognition as sr
from langdetect import detect
import pyttsx3
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

# Configura Streamlit
st.set_page_config(page_title="Asistente de Comunicación para Dislexia", layout="centered")

# Establece tu API key de Gemini
API_KEY = "AIzaSyD4NP35vvgCzw2AoD0Shds8KIRs6XijswM"

# Función para obtener credenciales de OAuth 2.0
def obtener_credenciales():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', ['https://www.googleapis.com/auth/userinfo.profile'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(requests)
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'client_secret_907441065113-s84h2jnq4ts0cn9hu2j4ntj8b4cojio0.apps.googleusercontent.com.json',
                ['https://www.googleapis.com/auth/userinfo.profile']
            )
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

# Función para corregir el texto usando la API de Gemini
def corregir_texto_gemini(texto, idioma):
    try:
        # Detectar idioma
        if idioma == "es":
            prompt = f"Por favor, corrige el siguiente texto para dislexia: {texto}"
        elif idioma == "en":
            prompt = f"Please correct the following text for dyslexia: {texto}"
        else:
            prompt = f"Please correct the following text for dyslexia in {idioma}: {texto}"

        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")  # Usa el modelo adecuado
        response = model.generate_content(prompt)
        if response:
            return response.text
        else:
            st.error("Error al generar la corrección de texto.")
            return texto
    except Exception as e:
        st.error(f"Error al llamar a la API de Gemini: {str(e)}")
    return texto

# Función para capturar texto por voz
def capturar_voz():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Por favor, habla ahora.")
        audio = r.listen(source)
    try:
        texto = r.recognize_google(audio, language='es-ES')
        st.write("Texto reconocido: ", texto)
        return texto
    except sr.UnknownValueError:
        st.error("No se pudo reconocer el audio.")
        return ""
    except sr.RequestError as e:
        st.error(f"Error con el servicio de Google Speech Recognition: {e}")
    return ""

# Función para leer el texto en voz alta
def leer_en_voz(texto):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Velocidad de la voz
    engine.setProperty('volume', 1)  # Volumen máximo
    engine.say(texto)
    engine.runAndWait()

# Función para cargar datos de progreso desde un archivo CSV
def cargar_datos():
    if os.path.exists("progreso.csv"):
        return pd.read_csv("progreso.csv")
    else:
        return pd.DataFrame(columns=["Fecha", "Ejercicios completados"])

# Función para agregar los datos de práctica diaria
def agregar_progreso(ejercicios):
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    st.session_state.data = st.session_state.data.append({"Fecha": fecha_actual, "Ejercicios completados": ejercicios}, ignore_index=True)

# Función para guardar los datos de progreso en un archivo CSV
def guardar_datos():
    st.session_state.data.to_csv("progreso.csv", index=False)

# Configuración inicial de los datos de progreso
if 'data' not in st.session_state:
    st.session_state.data = cargar_datos()

# Interfaz de Streamlit para ingresar el texto de forma manual o por voz
st.title("Asistente de Comunicación para Dislexia")

# Estilo dinámico para los botones
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        font-size: 18px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Opciones para elegir entre escribir o hablar
opcion = st.selectbox("Elige cómo deseas ingresar el texto:", ["Escribir", "Hablar"])

if opcion == "Escribir":
    # Entrada de texto
    texto_usuario = st.text_area("Escribe el texto a corregir", height=200, placeholder="Escribe aquí tu texto...")
elif opcion == "Hablar":
    # Capturar texto por voz
    texto_usuario = capturar_voz()

# Detectar el idioma del texto (por defecto en español)
if texto_usuario:
    idioma = detect(texto_usuario)
    st.write(f"Idioma detectado: {idioma}")

    with st.spinner('Corrigiendo el texto...'):
        texto_corregido = corregir_texto_gemini(texto_usuario, idioma)
    
    # Mostrar el resultado con retroalimentación visual
    if texto_corregido:
        st.success("Texto corregido exitosamente.")
        st.markdown(f"### Texto corregido: \n{texto_corregido}")
        # Leer el texto corregido en voz alta
        if st.button("Escuchar el texto corregido"):
            leer_en_voz(texto_corregido)
    else:
        st.error("Hubo un problema al corregir el texto.")
else:
    st.warning("Por favor, ingresa un texto para corregir.")

# Actividades personalizadas para mejorar la comprensión lectora
st.subheader("Actividad recomendada: Leer en voz alta")

actividad = st.radio("Elige una actividad para mejorar la comprensión lectora", 
                     ("Leer el texto en voz alta", "Responde preguntas sobre el texto"))

if actividad == "Leer el texto en voz alta":
    st.write("Por favor, lee el siguiente texto en voz alta para mejorar tu fluidez lectora:")
    st.markdown(f"**Texto a leer:** {texto_usuario}")
    if st.button("Escuchar el texto para practicar"):
        leer_en_voz(texto_usuario)
elif actividad == "Responde preguntas sobre el texto":
    st.write("¿Qué crees que significa el texto que has leído? Haz una breve reflexión.")
    st.text_area("Escribe tu reflexión aquí:", height=100)

# Simulando el progreso del usuario (en una aplicación real, este dato puede ser almacenado en un archivo o base de datos)
# Guardando el progreso de manera diaria
ejercicios = st.number_input("¿Cuántos ejercicios completaste hoy?", min_value=0, step=1)
if st.button("Registrar Progreso"):
    agregar_progreso(ejercicios)
    st.success("¡Progreso registrado!")

# Mostrar los datos de progreso
st.write("### Progreso Diario")
st.write(st.session_state.data)

# Mostrar el gráfico del progreso
fig, ax = plt.subplots()
ax.bar(st.session_state.data["Fecha"], st.session_state.data["Ejercicios completados"])
ax.set_xlabel("Fecha")
ax.set_ylabel("Ejercicios Completados")
ax.set_title("Progreso Diario de Ejercicios")
plt.xticks(rotation=45)
st.pyplot(fig)

# Guardar los datos al finalizar la aplicación
st.button("Guardar Progreso", on_click=guardar_datos)
