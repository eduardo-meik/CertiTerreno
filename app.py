import streamlit as st
import pandas as pd

# Initialize session state to store the form data
if 'form_data' not in st.session_state:
    st.session_state.form_data = pd.DataFrame(columns=[
        'Fecha de Inspección', 'Módulo', 'Tramo', 'Orientación', 
        'Línea', 'Activo Inspeccionado', 'Estado', 'Observaciones', 'Video'
    ])

with st.form("my_form"):
    st.header("Formulario de Terreno")

    fecha_de_inspeccion = st.date_input("Fecha de Inspección")
    modulo = st.selectbox('Selecciona el Módulo', [100, 200, 300])
    tramo = st.selectbox('Selecciona Tramo', ['Tramo 1', 'Tramo 2', 'Tramo 3'])
    orientacion = st.selectbox('Selecciona Orientación', [
        'Norte', 'Sur', 'Este', 'Oeste', 
        'NorteOeste', 'SurOeste', 'NortEste', 'SurEste'
    ])
    linea = st.number_input('Ingresa Línea', min_value=1, max_value=300, step=1)
    activos = st.selectbox('Selecciona Activo Inspeccionado', [
        'Boya 2500 Lts', 'Boya 3000 Lts', 'Grillete', 'Guardacabo', 
        'Cabo', 'Cadena', 'Cable', 'Platos de Distribución', 'Pulieras'
    ])
    estado = st.selectbox('Selecciona Estado', [
        'Sin riesgo', 
        'Riesgo Leve (Una situación con potencial o sospecha de riesgo de paro operacional o siniestro)', 
        'Riesgo Severo (Una situación confirmada de riesgo de paro operacional o siniestro)', 
        'Riesgo Crítico (Una situación en lo inmediato con riesgo de paro operacional o siniestro)'
    ])
    observaciones = st.text_area('Ingresa Observaciones', height=255)
    video = st.file_uploader('Selecciona video de inspección', type=['mp4', 'avi', 'mov'])

    submitted = st.form_submit_button('Previsualizar')

    if submitted:
        if estado != 'Sin riesgo' and not observaciones.strip():
            st.error('Las observaciones son obligatorias cuando el estado es diferente de "Sin riesgo".')
        else:
            # Convert the uploaded file to a safe reference if it exists
            video_ref = video.name if video else None

            new_data = {
                'Fecha de Inspección': fecha_de_inspeccion,
                'Módulo': modulo,
                'Tramo': tramo,
                'Orientación': orientacion,
                'Línea': linea,
                'Activo Inspeccionado': activos,
                'Estado': estado,
                'Observaciones': observaciones,
                'Video': video_ref
            }
            new_row = pd.DataFrame([new_data])
            st.session_state.form_data = pd.concat([st.session_state.form_data, new_row], ignore_index=True)

# Display the form data as a table outside the form if conditions are met
if st.session_state.form_data.empty:
    st.write("No hay datos para mostrar.")
else:
    st.write("Datos del Formulario:")
    dataframe_to_show = st.session_state.form_data.copy()
    # Replace video filenames with clickable links if necessary
    if 'Video' in dataframe_to_show:
        dataframe_to_show['Video'] = dataframe_to_show['Video'].apply(
            lambda x: f"[{x}]" if x else "No video"
        )
    st.dataframe(dataframe_to_show)


