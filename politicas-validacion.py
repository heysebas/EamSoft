import pandas as pd
from concurrent.futures import ThreadPoolExecutor

# Función que realiza las validaciones para cada solicitud
def validar_solicitud(solicitud, caracterizacion):
    # Inicializamos el estado de la solicitud
    estado = 'APROBADA'

    # Verificamos si la solicitud está en lista negra por los últimos 6 meses
    if caracterizacion['En Lista Negra (S/N)'] == 'S':
        if caracterizacion['Tiempo en Lista Negra (meses)'] > 6:
            estado = 'RECHAZADA'
    elif caracterizacion['Es Pre-pensionado (S/N)'] == 'S':
        estado = 'RECHAZADA'
    elif caracterizacion['En Lista Negra (S/N)'] == 'N' and caracterizacion['Es Pre-pensionado (S/N)'] == 'N':
        # Verificación para quienes no son pre-pensionados y no están en lista negra
        if caracterizacion['Pertenece a Institución Pública (S/N)'] == 'N':  # Si no pertenece a institución pública
            if caracterizacion['Lugar de Nacimiento'] in ['Bogotá', 'Medellín', 'Cali'] and caracterizacion['Lugar de Residencia'] in ['Bogotá', 'Medellín', 'Cali']:
                estado = 'RECHAZADA'
            elif (caracterizacion['Lugar de Nacimiento'] not in ['Bogotá', 'Cali', 'Medellín']) and \
                (caracterizacion['Lugar de Residencia'] not in ['Bogotá', 'Cali', 'Medellín']) and \
                (caracterizacion['Edad para Régimen de Prima Media (S/N)'] == 'N'):

                # Más reglas dependiendo de las condiciones específicas
                if caracterizacion['Fondo de Procedencia'] == 'Protección' and caracterizacion['Semanas Cotizadas'] < 590:
                    estado = 'APROBADA'
                elif caracterizacion['Fondo de Procedencia'] == 'Porvenir' and caracterizacion['Semanas Cotizadas'] < 800:
                    estado = 'APROBADA'
                elif caracterizacion['Fondo de Procedencia'] == 'Colfondos' and caracterizacion['Semanas Cotizadas'] < 300:
                    estado = 'APROBADA'
                elif caracterizacion['Fondo de Procedencia'] == 'Old Mutual' and caracterizacion['Semanas Cotizadas'] < 100:
                    estado = 'APROBADA'
                
                # Agregar más condiciones según las reglas que has proporcionado...

        elif caracterizacion['Pertenece a Institución Pública (S/N)'] == 'S':
            # Validación si pertenece a alguna institución pública como la Armada, INPEC, Policía, Mininterior, Minsalud
            if caracterizacion['Institución Pública'] == 'Armada' and caracterizacion['Condecoraciones (S/N)'] == 'S':
                estado = 'APROBADA'
            elif caracterizacion['Institución Pública'] == 'INPEC' and caracterizacion['Tiene Hijos (S/N)'] == 'S':
                estado = 'APROBADA'
            elif caracterizacion['Institución Pública'] == 'Policía' and caracterizacion['Tiene Familiares en la Policía (S/N)'] == 'S' and caracterizacion['Es Mayor de Edad (S/N)'] == 'S':
                estado = 'APROBADA'
            elif caracterizacion['Institución Pública'] in ['Minsalud', 'Mininterior'] and caracterizacion['Observaciones Disciplinarias (S/N)'] == 'S':
                estado = 'RECHAZADA'
            

    return estado

# Función para procesar el archivo de solicitudes y validarlas
def procesar_solicitudes(solicitudes_file, caracterizacion_file):
    # Cargamos los datos desde los CSVs
    solicitudes = pd.read_csv(solicitudes_file)
    caracterizacion = pd.read_csv(caracterizacion_file)

    # Creamos una lista para los resultados
    resultados = []

    # Creamos un ThreadPoolExecutor para realizar las validaciones en paralelo
    with ThreadPoolExecutor() as executor:
        # Para cada solicitud, buscaremos su caracterización y aplicamos la validación
        for index, solicitud in solicitudes.iterrows():
            caracterizacion_row = caracterizacion[caracterizacion['Identificación'] == solicitud['Identificación']].iloc[0]
            estado = executor.submit(validar_solicitud, solicitud, caracterizacion_row)
            resultados.append((solicitud['Nombre del Cotizante'], solicitud['Identificación'], solicitud['Fecha de Solicitud'], solicitud['Motivo del Traspaso'], estado.result()))

    # Crear el DataFrame con los resultados
    df_resultados = pd.DataFrame(resultados, columns=["Nombre del Cotizante", "Identificación", "Fecha de Solicitud", "Motivo del Traspaso", "Estado de la Solicitud"])

    # Guardar el archivo con los resultados
    df_resultados.to_csv('solicitudes_validada.csv', index=False)

# Llamamos la función para procesar las solicitudes
procesar_solicitudes('solicitudes_traspaso_con_datos.csv', 'solicitudes_traspaso.csv')
