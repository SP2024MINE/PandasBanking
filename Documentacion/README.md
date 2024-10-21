## Predicción de suscripción a deposito

El proyecto que se desarrolla consiste en desarrollar un modelo para predecir si un cliente se suscribirá a un deposito o no y disponibilizar el modelo para relizar predicciones a tráves de un API, utilizando un aplicativo desarrollado en streamlit.

La base de datos utilizada para el desarrollo se extrajo del UC Irvine Machine Learning Repository.

Los pasos ejecutados para el desarrollo del proyecto fueron:

- Creación del repositorio y entorno con la instalación de paquetes y librerías a través de poetry.

##### Construcción del modelo
**Codigo/modelo_bank_mkt.ipynb**
    - Carga, exploración y transformación de datos (Remitase a Codigo/).
    - Construcción de pipeline para preprocesar y entrenar el modelo.
    - Segmentar la base en entrenamiento y prueba.
    - Entrenar el modelo usando el pipeline con la base de entrenamiento.
    - Validar el rendimiento del modelo con la base de prueba.

##### Pipeline
**Datos/bank_mkt_pipeline.pkl**
    - Almacenar el pipeline.

##### Creación del API
**api/main.py**
    - Construcción de un api que recibe como input un json, carga el pipeline y realiza la predicción.
**Codigo/testeo_api.ipynb**
    - Validación de api con datos de prueba que utiliza la URL del endpoint de la API.

##### Creación de la APP
**Codigo/streamlit.iýnb**
    - Construcción de código en notebook para la creación del aplicativo con el formulario en streamlit.
**app/app.py**
    - Aplicativo con el formulario para la captura de información que consume el modelo a través de la API y genera la predicción.
