import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Definir la URL de la API (esto debe reemplazarse con la URL real de la API)
api_url = "http://127.0.0.1:8000/predict"

st.title("Formulario de Datos para Predicción")
st.write('Ingrese la información para determinar si el cliente se suscribirá al depósito o no')

# Preguntas para captura de información personal
st.subheader("Información personal")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Edad", 0, 100, value=30)
    marital = st.selectbox("Estado civil:", ['married', 'single', 'divorced'])

with col2:
    education = st.selectbox("Nivel educativo:", ['primary', 'secondary', 'tertiary'])
    job = st.selectbox("Ocupación:", ['management',  'technician',  'entrepreneur',  'retired',  'admin.',  'services',
                                         'blue-collar',  'self-employed', 'unemployed',  'housemaid',  'student'])

# Preguntas para captura de información financiera
st.subheader("Información finaciera")

# Crear dos columnas
col1, col2, col3 = st.columns(3)

with col1:
    default = st.selectbox('¿Tiene crédito en mora?:', ['yes', 'no'])

with col2:
    housing = st.selectbox('¿Tiene préstamo de vivienda?:', ['yes', 'no'])

with col3:
    loan = st.selectbox('¿Tiene préstamo personal?:', ['yes', 'no'])

balance = st.number_input("Saldo promedio anual:", min_value=0, value=1200)

# Preguntas para captura de información de campaña actual
st.subheader("Información contacto campaña actual")

col1, col2, col3 = st.columns(3)

with col1:
    campaign = st.number_input("Número de contactos:", min_value=1, max_value=60)

with col2:
    day_of_week = st.slider("Día del último contacto", 1, 31)

with col3:
    month = st.selectbox('Mes del último contacto:', ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 
                                                      'nov', 'dec'])

# Preguntas para captura de información de campañas anteriores
st.subheader("Información campañas anteriores")

camp_prev = st.selectbox('¿Contacto en campaña previa?:', ['yes', 'no'], index=1)

if camp_prev == 'yes':
    pdays = st.number_input("Número de días que pasaron después de que el cliente fue contactado por última vez desde una campaña anterior:", min_value=1, max_value=60)
    previous = st.number_input("Número de contactos realizados antes de esta campaña:", min_value=1, max_value=60)
else:
    pdays= -1
    previous = 0 

# Mostrar los datos capturados
if st.button("Mostrar datos"):
    st.write("Datos capturados:")
    st.write(f"Edad: {age}")
    st.write(f"Estado civil: {marital}")
    st.write(f"Nivel educativo: {education}")
    st.write(f"Ocupación: {job}")
    st.write(f"Crédito en mora: {default}")
    st.write(f"Préstamo de vivienda: {housing}")
    st.write(f"Préstamo personal: {loan}")
    st.write(f"Saldo promedio mensual: {balance}")
    st.write(f"Mes de último contacto: {month}")
    st.write(f"Día de último contacto: {day_of_week}")
    st.write(f"Número de contactos realizados: {campaign}")
    st.write(f"Contacto en campaña previa: {camp_prev}")
    if camp_prev == 'yes':
        st.write(f"Número de días que pasaron desde que el cliente fue contactado por última vez en una campaña anterior: {pdays}")
        st.write(f"Número de contactos realizados antes de esta campaña: {previous}")


# Botón para enviar y calcular
if st.button("Calcular resultado"):
    # Crear un diccionario con los datos del formulario
    data = {
        'age': [int(age)],
        'job': [job],
        'marital': [marital],
        'education': [education],
        'default': [default],
        'balance': [int(balance)],
        'housing': [housing],
        'loan': [loan],
        'day_of_week': [int(day_of_week)],
        'month': [month],
        'campaign': [int(campaign)],
        'pdays': [int(pdays)],
        'previous': [int(previous)]
    }

    try:
        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            # Mostrar el resultado de la predicción
            st.write("Resultado de la predicción:")
            st.write(response.json()['prediction'])

            # Extraer las probabilidades del diccionario dentro de 'probabilidad'
            prob_dict = response.json()['probabilidad']

            # Extraer la clave y el valor dentro de 'probabilidad'
            probabilidad_no = float(list(prob_dict.keys())[0])  # La clave representa la probabilidad de "no"
            probabilidad_yes = float(list(prob_dict.values())[0])  # El valor representa la probabilidad de "sí"

            # Crear el gráfico de barras apiladas
            fig, ax = plt.subplots()

            # Barra para "no suscribir" (porcentaje de 100)
            ax.bar('Suscripción', probabilidad_no * 100, label='No suscribe', color='blue')

            # Barra para "sí suscribir" (apilada sobre la de "no", porcentaje de 100)
            ax.bar('Suscripción', probabilidad_yes * 100, bottom=probabilidad_no * 100, label='Sí suscribe', color='green')

            ax.set_ylim(0, 100)  # Limitar el eje y de 0 a 100%
            ax.set_ylabel('Porcentaje (%)')
            ax.set_title('Probabilidad de suscripción a depósito')
            ax.legend()  # Mostrar la leyenda

            # Mostrar el gráfico en Streamlit
            st.pyplot(fig)

        else:
            st.write(f"Error en la solicitud: {response.status_code}")
    except requests.exceptions.RequestException as e:
        st.write(f"Error al conectar con la API: {e}")