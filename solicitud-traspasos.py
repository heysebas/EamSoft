import random
import csv
from datetime import datetime
from faker import Faker

# Función para leer las identificaciones desde el archivo CSV
def leer_identificaciones(archivo):
    identificaciones = []
    with open(archivo, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            identificaciones.append(row['Identificación'])  # Suponiendo que la columna se llama 'Identificación'
    return identificaciones

# Cargar las identificaciones desde el archivo solicitudes_traspaso.csv
identificaciones = leer_identificaciones('solicitudes_traspaso.csv')

# Inicializar Faker para generar nombres aleatorios
fake = Faker()

# Datos adicionales
motivos_traspaso = [
    "Cambio a fondo con mayor rentabilidad",
    "Diversificación de portafolio",
    "Mejor servicio de atención al cliente",
    "Fondo con menor riesgo",
    "Cambio a fondo sostenible o responsable",
    "Bajo rendimiento del fondo actual",
    "Fondo con mejores comisiones",
    "Recomendación de asesor financiero",
    "Cambio por motivos personales",
    "Ajuste de estrategia de inversión"
]


# Función para generar una solicitud
def generar_solicitud():
    solicitud = {
        "Nombre del Cotizante": fake.name(),  # Nombre generado aleatoriamente
        "Identificación": random.choice(identificaciones),  # Identificación aleatoria de la lista cargada
        "Fecha de Solicitud": datetime.now().strftime("%d/%m/%Y"),  # Fecha actual
        "Motivo del Traspaso": random.choice(motivos_traspaso), # Motivo predefinido
        "Estado de la Solicitud": "Generada",  
    }
    return solicitud

# Generar algunas solicitudes de ejemplo
solicitudes = [generar_solicitud() for _ in range(100)]  # Generar 100 solicitudes

# Nombre del archivo CSV para guardar las nuevas solicitudes
nombre_archivo = "solicitudes_traspaso_con_datos.csv"

# Escribir las solicitudes en un archivo CSV
with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Nombre del Cotizante", "Identificación", "Fecha de Solicitud", "Motivo del Traspaso", "Estado de la Solicitud"])
    
    # Escribir la cabecera
    writer.writeheader()
    
    # Escribir las filas de las solicitudes
    writer.writerows(solicitudes)

print(f"Archivo CSV '{nombre_archivo}' generado con éxito.")
