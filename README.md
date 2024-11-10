Utilitario Traspaso Colpensionex
Descripción del Proyecto
El Utilitario Traspaso Colpensionex es una aplicación desarrollada en Python para automatizar el traslado de cotizantes desde fondos de pensiones privados al fondo público Colpensionex. Este sistema simplifica y agiliza el proceso mediante la validación de datos y procesamiento en caché de solicitudes, permitiendo un flujo continuo de revisiones y traspasos sin intervención manual.

Estructura del Proyecto

/colpensionex_utilitario/
│
├── README.md                        # Documentación general del proyecto
├── LICENSE.md                       # Información sobre la licencia del proyecto
├── .gitignore                       # Archivos y carpetas a ignorar en el control de versiones
├── requirements.txt                 # Lista de dependencias del proyecto
├── docs/                            # Documentación técnica y de casos de uso
├── src/                             # Código fuente de la aplicación y utilidades
├── data/                            # Archivos CSV y datos de entrada/salida
└── config/                          # Configuración de la aplicación


Funcionalidades
Validación de Archivos CSV: Verifica el formato y contenido de archivos CSV con solicitudes y caracterizaciones de cotizantes.
Carga en Caché: Carga y almacena en caché las solicitudes y datos de caracterización para un procesamiento rápido.
Procesamiento de Solicitudes: Aprueba o rechaza solicitudes basándose en políticas de Colpensionex, moviendo los archivos procesados a carpetas específicas.
Gestión de Listas Negras: Detecta y marca automáticamente a los cotizantes inhabilitados o embargables.
Tareas Programadas: Utiliza cron (Linux) o tareas programadas (Windows) para ejecutar revisiones y procesamientos en intervalos programados.
