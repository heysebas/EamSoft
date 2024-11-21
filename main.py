import os
import csv
import shutil
from datetime import datetime
from collections import deque
import tkinter as tk
from tkinter import ttk, messagebox

# --- Configuración del sistema ---
BASE_PATH = "./data"
ENTRANTES = os.path.join(BASE_PATH, "SolicitudesEntrantes")
EN_PROCESO = os.path.join(BASE_PATH, "SolicitudesEnProcesamiento")
PROCESADAS = os.path.join(BASE_PATH, "SolicitudesProcesadas")
CARACTERIZACIONES = os.path.join(BASE_PATH, "Caracterizaciones")

os.makedirs(ENTRANTES, exist_ok=True)
os.makedirs(EN_PROCESO, exist_ok=True)
os.makedirs(PROCESADAS, exist_ok=True)
os.makedirs(CARACTERIZACIONES, exist_ok=True)


# --- Funciones auxiliares ---
def cargar_csv(filepath, columnas_requeridas=None):
    """Carga un archivo CSV y verifica las columnas requeridas."""
    try:
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r", encoding="utf-8") as f:
            data = list(csv.DictReader(f))
            if columnas_requeridas:
                for col in columnas_requeridas:
                    if col not in data[0]:
                        return []
            return data
    except Exception as e:
        print(f"Error al cargar {filepath}: {e}")
        return []


def guardar_csv(filepath, data, columnas):
    """Guarda los datos en un archivo CSV. Si el archivo existe, agrega los datos."""
    mode = "w" if not os.path.exists(filepath) else "a"
    with open(filepath, mode, encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        if mode == "w":
            writer.writeheader()
        writer.writerows(data)


# --- Clases para manejo de datos ---
class SuperCache:
    def __init__(self):
        self.cache = {}
        self._cargar_datos_base()

    def _cargar_datos_base(self):
        """Carga los datos base en memoria."""
        self.cache["ciudades"] = cargar_csv(os.path.join(BASE_PATH, "ciudades.csv"),
                                            ["id", "nombre", "departamento_id"])
        self.cache["departamentos"] = cargar_csv(os.path.join(BASE_PATH, "departamentos.csv"),
                                                 ["id", "nombre", "pais_id"])
        self.cache["paises"] = cargar_csv(os.path.join(BASE_PATH, "paises.csv"), ["id", "nombre"])
        self.cache["personas"] = cargar_csv(os.path.join(BASE_PATH, "personas.csv"),
                                            ["id", "tipo_documento", "documento", "nombre_completo"])
        self.cache["cotizantes"] = cargar_csv(os.path.join(BASE_PATH, "cotizantes.csv"),
                                              ["id", "persona_id", "ciudad_id", "fondo_pensiones"])

    def get_data(self, key):
        return self.cache.get(key, [])


class Servicio:
    def __init__(self, super_cache):
        self.super_cache = super_cache
        self.lista_negra_inhabilitados = set()
        self.lista_negra_embargados = set()
        self.cola_prioritaria = deque()

    def validar_archivo(self, filepath, columnas_requeridas):
        """Valida el contenido de un archivo CSV."""
        data = cargar_csv(filepath, columnas_requeridas)
        if not data:
            print(f"Archivo inválido o vacío: {filepath}")
        return data

    def cargar_caracterizaciones(self):
        """Carga las caracterizaciones de los archivos correspondientes."""
        for filename in os.listdir(CARACTERIZACIONES):
            filepath = os.path.join(CARACTERIZACIONES, filename)
            data = self.validar_archivo(filepath, ["tipo_documento", "documento", "nombre_completo", "caracterizacion"])
            for row in data:
                if row["caracterizacion"] == "INHABILITAR":
                    self.lista_negra_inhabilitados.add(row["documento"])
                elif row["caracterizacion"] == "EMBARGAR":
                    self.lista_negra_embargados.add(row["documento"])

    def procesar_solicitudes(self):
        """Procesa solicitudes desde la carpeta ENTRANTES."""
        solicitudes_procesadas = []
        for filename in os.listdir(ENTRANTES):
            filepath = os.path.join(ENTRANTES, filename)
            solicitudes = self.validar_archivo(filepath, ["id", "persona_id", "fecha_solicitud", "estado"])
            if not solicitudes:
                continue

            for solicitud in solicitudes:
                persona = next((p for p in self.super_cache.get_data("personas") if p["id"] == solicitud["persona_id"]),
                               None)
                if not persona:
                    continue

                # Verificar estado de la persona contra listas negras
                if persona["documento"] in self.lista_negra_inhabilitados:
                    solicitud["estado"] = "Rechazada"
                elif persona["documento"] in self.lista_negra_embargados:
                    solicitud["estado"] = "Aprobada - Embargado"
                else:
                    solicitud["estado"] = "Aprobada"
                    self.cola_prioritaria.append(solicitud)

                # Asociar información adicional del cotizante (ciudad y fondo)
                cotizante = next(
                    (c for c in self.super_cache.get_data("cotizantes") if c["persona_id"] == solicitud["persona_id"]),
                    None)
                if cotizante:
                    solicitud["ciudad"] = next((ciudad["nombre"] for ciudad in self.super_cache.get_data("ciudades") if
                                                ciudad["id"] == cotizante["ciudad_id"]), "Desconocida")
                    solicitud["fondo"] = cotizante["fondo_pensiones"]
                solicitudes_procesadas.append(solicitud)

            shutil.move(filepath, os.path.join(EN_PROCESO, filename))

        # Guardar las solicitudes procesadas
        now = datetime.now().strftime("%Y_%m_%d")
        procesadas_path = os.path.join(PROCESADAS, f"SolicitudesProcesadas_{now}.csv")
        guardar_csv(procesadas_path, solicitudes_procesadas,
                    ["id", "persona_id", "fecha_solicitud", "estado", "ciudad", "fondo"])
        return solicitudes_procesadas


class App(tk.Tk):
    def __init__(self, servicio):
        super().__init__()
        self.servicio = servicio
        self.title("Gestión de Solicitudes Colpensionex")
        self.geometry("800x600")

        # Tabla principal
        self.tree = ttk.Treeview(self, columns=("ID", "Persona ID", "Fecha Solicitud", "Estado", "Ciudad", "Fondo"),
                                 show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Persona ID", text="Persona ID")
        self.tree.heading("Fecha Solicitud", text="Fecha Solicitud")
        self.tree.heading("Estado", text="Estado")
        self.tree.heading("Ciudad", text="Ciudad")
        self.tree.heading("Fondo", text="Fondo")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Botones
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        btn_procesar = tk.Button(btn_frame, text="Procesar Solicitudes", command=self.procesar_solicitudes)
        btn_procesar.pack(side=tk.LEFT, padx=5)

        # Buscador por ID
        tk.Label(btn_frame, text="Buscar Persona ID:").pack(side=tk.LEFT)
        self.entry_busqueda = tk.Entry(btn_frame)
        self.entry_busqueda.pack(side=tk.LEFT, padx=5)
        btn_buscar = tk.Button(btn_frame, text="Buscar", command=self.buscar_persona)
        btn_buscar.pack(side=tk.LEFT)

        self.cargar_datos_iniciales()

    def cargar_datos_iniciales(self):
        """Carga las solicitudes procesadas previamente."""
        now = datetime.now().strftime("%Y_%m_%d")
        procesadas_path = os.path.join(PROCESADAS, f"SolicitudesProcesadas_{now}.csv")
        solicitudes_procesadas = cargar_csv(procesadas_path, ["id", "persona_id", "fecha_solicitud", "estado", "ciudad",
                                                              "fondo"]) if os.path.exists(procesadas_path) else []
        self.cargar_datos(solicitudes_procesadas)

    def cargar_datos(self, datos):
        """Carga datos en la tabla."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for dato in datos:
            self.tree.insert("", tk.END, values=(
            dato["id"], dato["persona_id"], dato["fecha_solicitud"], dato["estado"], dato.get("ciudad", ""),
            dato.get("fondo", "")))

    def procesar_solicitudes(self):
        """Procesa las solicitudes y actualiza la tabla."""
        self.servicio.cargar_caracterizaciones()
        solicitudes = self.servicio.procesar_solicitudes()
        self.cargar_datos(solicitudes)
        messagebox.showinfo("Proceso Completado", "Las solicitudes fueron procesadas correctamente.")

    def buscar_persona(self):
        """Busca una persona por ID o documento."""
        criterio = self.entry_busqueda.get().strip()
        if not criterio:
            messagebox.showwarning("Advertencia", "Por favor ingresa un ID o documento de persona.")
            return

        # Buscar por ID en la lista de personas
        persona = next((p for p in self.servicio.super_cache.get_data("personas") if
                        p["id"] == criterio or p["documento"] == criterio), None)
        if persona:
            # Buscar el estado en las solicitudes procesadas
            now = datetime.now().strftime("%Y_%m_%d")
            procesadas_path = os.path.join(PROCESADAS, f"SolicitudesProcesadas_{now}.csv")
            solicitudes_procesadas = cargar_csv(procesadas_path, ["id", "persona_id", "estado"]) if os.path.exists(
                procesadas_path) else []

            solicitud = next((s for s in solicitudes_procesadas if s["persona_id"] == persona["id"]), None)
            estado = solicitud["estado"] if solicitud else "Sin procesar"

            info = (
                f"ID: {persona['id']}\n"
                f"Tipo Documento: {persona['tipo_documento']}\n"
                f"Documento: {persona['documento']}\n"
                f"Nombre: {persona['nombre_completo']}\n"
                f"Estado: {estado}"
            )
            messagebox.showinfo("Persona Encontrada", info)
        else:
            messagebox.showerror("Error", "No se encontró ninguna persona con el ID o documento proporcionado.")


# --- Inicialización de la aplicación ---
cache = SuperCache()
servicio = Servicio(cache)
app = App(servicio)
app.mainloop()
