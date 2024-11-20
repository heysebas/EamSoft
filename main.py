import csv
import io
import os
import random
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from collections import deque
from typing import List, Dict

# Datos simulados de los archivos CSV
ciudades_data = """id,nombre,departamento_id
1,Bogotá,1
2,Medellín,2
3,Cali,3"""

departamentos_data = """id,nombre,pais_id
1,Cundinamarca,1
2,Antioquia,1
3,Valle del Cauca,1"""

paises_data = """id,nombre
1,Colombia"""

personas_data = """id,tipo_documento,documento,nombre_completo
1,CC,123456789,Juan Perez
2,CC,987654321,María García"""

cotizantes_data = """id,persona_id,ciudad_id,fondo_pensiones
1,1,1,Colpensionex
2,2,2,Porvenir"""

inhabilitacion_cotizante_data = """id,persona_id,fecha_inhabilitacion
1,1,2024-01-01"""

caracterizacion_data = """tipo_documento,documento,nombre_completo,caracterizacion
CC,123456789,Juan Perez,INHABILITAR
CC,987654321,María García,EMBARGAR"""

solicitudes_data = """id,persona_id,fecha_solicitud,estado
1,1,2024-02-01,Generada
2,2,2024-02-01,Generada"""


# Clase base para leer y escribir archivos CSV
class CSVHandler:
    def __init__(self, data_str):  # Corregido de _init_ a __init__
        self.data = self.load_csv_data(data_str)

    def load_csv_data(self, data_str):
        """Carga datos desde una cadena de texto como si fueran un archivo CSV."""
        return list(csv.DictReader(io.StringIO(data_str)))

    def get_all(self):
        """Retorna todas las filas de datos."""
        return self.data


# Clases específicas para cada archivo
class Ciudades(CSVHandler): pass


class Departamentos(CSVHandler): pass


class Paises(CSVHandler): pass


class Personas(CSVHandler): pass


class Cotizantes(CSVHandler): pass


class Inhabilitaciones(CSVHandler): pass


class Caracterizaciones(CSVHandler): pass


class Solicitudes(CSVHandler): pass


# Clase SuperCache para almacenar en caché los datos
class SuperCache:
    def __init__(self):  # Corregido de _init_ a __init__
        self.cache = {
            "ciudades": Ciudades(ciudades_data).get_all(),
            "departamentos": Departamentos(departamentos_data).get_all(),
            "paises": Paises(paises_data).get_all(),
            "personas": Personas(personas_data).get_all(),
            "cotizantes": Cotizantes(cotizantes_data).get_all(),
            "inhabilitaciones": Inhabilitaciones(inhabilitacion_cotizante_data).get_all(),
            "caracterizaciones": Caracterizaciones(caracterizacion_data).get_all(),
            "solicitudes": Solicitudes(solicitudes_data).get_all()
        }

    def get_data(self, key):
        return self.cache.get(key, [])


# Algoritmo de negocio
class Servicio:
    def __init__(self, super_cache):  # Corregido de _init_ a __init__
        self.super_cache = super_cache
        self.lista_negra_inhabilitados = [
            c['documento'] for c in self.super_cache.get_data("caracterizaciones") if c['caracterizacion'] == 'INHABILITAR'
        ]
        self.lista_negra_embargados = [
            c['documento'] for c in self.super_cache.get_data("caracterizaciones") if c['caracterizacion'] == 'EMBARGAR'
        ]
        self.cola_cotizantes = deque()

    def procesar_solicitudes(self):
        for solicitud in self.super_cache.get_data("solicitudes"):
            persona_id = solicitud['persona_id']
            persona = next((p for p in self.super_cache.get_data("personas") if p['id'] == persona_id), None)
            if not persona:
                continue

            # Verificar si la persona está en listas negras
            if persona['documento'] in self.lista_negra_inhabilitados:
                solicitud['estado'] = 'Rechazada'
            elif persona['documento'] in self.lista_negra_embargados:
                solicitud['estado'] = 'Aprobada'
                self.cola_cotizantes.append(solicitud)
            else:
                # Aplicar políticas internas
                edad = random.randint(18, 60)  # Simulación de la edad
                if edad < 35:
                    solicitud['estado'] = 'Aprobada'
                    self.cola_cotizantes.append(solicitud)
                else:
                    solicitud['estado'] = 'Rechazada'


# Interfaz gráfica
class App(tk.Tk):
    def __init__(self, servicio):  # Corregido de _init_ a __init__
        super().__init__()
        self.servicio = servicio
        self.title("Procesamiento de Solicitudes de Cotizantes")
        self.geometry("600x400")

        # Crear la tabla para mostrar las solicitudes
        self.tree = ttk.Treeview(self, columns=("ID", "Persona ID", "Fecha Solicitud", "Estado"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Persona ID", text="Persona ID")
        self.tree.heading("Fecha Solicitud", text="Fecha Solicitud")
        self.tree.heading("Estado", text="Estado")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botón de procesamiento
        btn_procesar = tk.Button(self, text="Procesar Solicitudes", command=self.procesar_solicitudes)
        btn_procesar.pack(pady=10)

        # Cargar solicitudes iniciales en la tabla
        self.cargar_solicitudes()

    def cargar_solicitudes(self):
        for solicitud in self.servicio.super_cache.get_data("solicitudes"):
            self.tree.insert("", tk.END, values=(
                solicitud['id'],
                solicitud['persona_id'],
                solicitud['fecha_solicitud'],
                solicitud['estado']
            ))

    def procesar_solicitudes(self):
        self.servicio.procesar_solicitudes()
        # Limpiar y recargar solicitudes en la tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.cargar_solicitudes()
        messagebox.showinfo("Proceso completado", "Las solicitudes han sido procesadas correctamente.")


# Configuración y ejecución
super_cache = SuperCache()
servicio = Servicio(super_cache)

# Iniciar la aplicación
app = App(servicio)
app.mainloop()
