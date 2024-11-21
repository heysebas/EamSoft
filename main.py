import tkinter as tk
from tkinter import ttk
import csv

# Función para cargar los datos desde un archivo CSV
def cargar_datos(archivo):
    datos = []
    with open(archivo, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            datos.append(row)
    return datos

# Función para mostrar la tabla de solicitudes en la ventana
def mostrar_tabla(archivo, tree):
    # Cargar los datos del archivo CSV
    datos = cargar_datos(archivo)
    
    # Limpiar la tabla anterior
    for item in tree.get_children():
        tree.delete(item)
    
    # Insertar los nuevos datos en la tabla
    for solicitud in datos:
        tree.insert("", tk.END, values=[solicitud["Nombre del Cotizante"], solicitud["Identificación"], 
                                       solicitud["Fecha de Solicitud"], solicitud["Motivo del Traspaso"], 
                                       solicitud["Estado de la Solicitud"]])

# Función para crear la ventana de Tkinter y mostrar la tabla
def crear_ventana():
    # Crear ventana principal
    ventana = tk.Tk()
    ventana.title("Solicitudes de Traspaso")

    # Crear el Treeview para mostrar las filas y columnas
    columnas = ["Nombre del Cotizante", "Identificación", "Fecha de Solicitud", "Motivo del Traspaso", "Estado de la Solicitud"]
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    
    # Definir las columnas y sus encabezados
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=150)  # Ajustar el ancho de las columnas
    
    # Empacar el Treeview en la ventana
    tree.pack(expand=True, fill=tk.BOTH)

    # Cargar la primera tabla (solicitudes_traspaso_con_datos.csv)
    mostrar_tabla("solicitudes_traspaso_con_datos.csv", tree)

    # Función para mostrar la tabla de solicitudes validadas
    def mostrar_solicitudes_validas():
        mostrar_tabla("solicitudes_validada.csv", tree)

    # Botón para mostrar las solicitudes validadas
    boton_mostrar_validas = tk.Button(ventana, text="Mostrar Solicitudes Validadas", command=mostrar_solicitudes_validas)
    boton_mostrar_validas.pack(pady=10)

    # Ejecutar la ventana
    ventana.mainloop()

# Crear y mostrar la ventana
crear_ventana()
