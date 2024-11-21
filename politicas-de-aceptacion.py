import csv
import random
from faker import Faker

# Crear una instancia de Faker para generar datos aleatorios
fake = Faker("es_CO")  # Faker configurado para Colombia

# Lista de ciudades colombianas
ciudades_colombianas = [
    "Bogotá",
    "Medellín",
    "Cali",
    "Barranquilla",
    "Cartagena",
    "Cúcuta",
    "Bucaramanga",
    "Pereira",
    "Santa Marta",
    "Ibagué",
    "Manizales",
    "Neiva",
    "Montería",
    "Armenia",
    "Popayán",
    "Valledupar",
    "Sincelejo",
    "Tunja",
    "Villavicencio",
    "Riohacha",
    "Quibdó",
    "Leticia",
    "San Andrés",
    "Yopal",
    "Pasto",
    "Florencia",
    "Sogamoso",
    "Tunja",
    "Cúcuta",
    "Cali",
    "Bello",
    "Soledad",
    "Risaralda",
]


# Función para generar datos de un solicitante
def generar_solicitante():
    identificacion = random.randint(100000000, 999999999)
    lista_negra = random.choice(["S", "N"])
    tiempo_lista_negra = random.randint(1, 12) if lista_negra == "S" else 0
    pre_pensionado = random.choice(["S", "N"])
    pertenece_institucion_publica = random.choice(["S", "N"])

    if pertenece_institucion_publica == "S":
        institucion = random.choice(
            ["Armada", "Inpec", "Policía", "MinSalud", "MinInterior"]
        )
        condecoraciones = (
            random.choice(["S", "N"]) if institucion in ["Armada", "Inpec"] else "N"
        )
        tiene_hijos = random.choice(["S", "N"]) if institucion == "Inpec" else "N"
        tiene_familiares_policia = (
            random.choice(["S", "N"]) if institucion == "Policía" else "N"
        )
        es_mayor_edad = random.choice(["S", "N"]) if institucion == "Policía" else "S"
        observaciones_disciplinarias = (
            random.choice(["S", "N"])
            if institucion in ["MinSalud", "MinInterior"]
            else "N"
        )
        motivo_observacion = fake.text() if observaciones_disciplinarias == "S" else ""
    else:
        institucion = ""
        condecoraciones = ""
        tiene_hijos = ""
        tiene_familiares_policia = ""
        es_mayor_edad = ""
        observaciones_disciplinarias = ""
        motivo_observacion = ""

    # Seleccionar aleatoriamente ciudades colombianas para nacimiento y residencia
    lugar_nacimiento = random.choice(ciudades_colombianas)
    lugar_residencia = random.choice(ciudades_colombianas)

    edad_para_regimen = random.choice(["S", "N"])
    fondo_procedencia = random.choice(
        ["Porvenir", "Protección", "Colfondos", "Old Mutual", "Fondo Extranjero"]
    )
    semanas_cotizadas = random.randint(100, 1000)

    return [
        identificacion,
        lista_negra,
        tiempo_lista_negra,
        pre_pensionado,
        pertenece_institucion_publica,
        institucion,
        condecoraciones,
        tiene_hijos,
        tiene_familiares_policia,
        es_mayor_edad,
        observaciones_disciplinarias,
        motivo_observacion,
        lugar_nacimiento,
        lugar_residencia,
        edad_para_regimen,
        fondo_procedencia,
        semanas_cotizadas,
    ]


# Definir los encabezados del CSV
encabezados = [
    "Identificación",
    "En Lista Negra (S/N)",
    "Tiempo en Lista Negra (meses)",
    "Es Pre-pensionado (S/N)",
    "Pertenece a Institución Pública (S/N)",
    "Institución Pública",
    "Condecoraciones (S/N)",
    "Tiene Hijos (S/N)",
    "Tiene Familiares en la Policía (S/N)",
    "Es Mayor de Edad (S/N)",
    "Observaciones Disciplinarias (S/N)",
    "Motivo de Observación Disciplinaria",
    "Lugar de Nacimiento",
    "Lugar de Residencia",
    "Edad para Régimen de Prima Media (S/N)",
    "Fondo de Procedencia",
    "Semanas Cotizadas",
]

# Nombre del archivo CSV a generar
nombre_archivo = "solicitudes_traspaso.csv"

# Crear el archivo CSV y escribir los datos
with open(nombre_archivo, mode="w", newline="") as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerow(encabezados)  # Escribir los encabezados

    # Generar 100 registros simulados
    for _ in range(100):
        escritor_csv.writerow(generar_solicitante())

print(f"CSV generado correctamente: {nombre_archivo}")
