# Preprocessing TXT Files

Pre-procesamiento de los archivos txt generados durante las distintas simulaciones de Lora usando GNU-Radio

## Tabla de Contenidos

- [Preprocessing TXT Files](#preprocessing-txt-files)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Características](#características)
  - [Requisitos](#requisitos)
  - [Instalación](#instalación)
  - [Uso](#uso)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Licencia](#licencia)
  - [Contacto](#contacto)

## Características

- **Filtrado de archivos:** Solo se procesan aquellos archivos cuyo nombre cumpla con la expresión regular:  
  `^(\d+[mk])-(\d+m)-(\d+)[.]txt$`
  - Primer grupo: Frecuencia de muestreo (ej. "10k" o "50m").
  - Segundo grupo: Distancia (ej. "20m" o "100m").
  - Tercer grupo: Versión (ej. "1" o "2").
- **Pre-procesado modular:** La función `pre_process` se encarga de procesar cada archivo; actualmente es un _stub_ listo para ser personalizado.
- **Procesamiento eficiente:** Los archivos se procesan sin cargar todo el contenido en memoria, pasando directamente los objetos de archivo a la función de pre-procesado.
- **Simulación de retardo:** Opción `--slow-down` para simular un procesamiento más lento, útil para pruebas y simulaciones.
- **Barra de progreso:** Utiliza `tqdm` para mostrar el avance del procesamiento.

## Requisitos

- Python 3.6 o superior.
- Librerías:
  - `tqdm`
- Opcional: si se desea gestionar el entorno con Conda, tener [Anaconda](https://www.anaconda.com/) o [Miniconda](https://docs.conda.io/en/latest/miniconda.html) instalado.

## Instalación

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/tu_usuario/preprocessing-txt-files.git
   cd preprocessing-txt-files
   ```

2. **Crear y activar el entorno (opcional, usando Conda):**

   Crear el entorno:

   ```bash
   conda env create -f environment.yml
   conda activate IoT_txt
   ```

3. **Instalar dependencias (si no usas Conda):**

   Si prefieres usar `pip`, instala las dependencias con:

   ```bash
   pip install -r requirements.txt
   ```

   *Nota:* Asegúrate de tener un archivo `requirements.txt` actualizado con, al menos, `tqdm`.

## Uso

El script se ejecuta desde la línea de comandos. Por defecto, utiliza la carpeta `base_txt` para los archivos de entrada y `preprocessed_csv` para los de salida.

Ejemplo de uso:

```bash
python preprocess.py --input_folder base_txt --output_folder preprocessed_csv_ --slow-down 0.3
```

Parámetros:
- `--input_folder`: Carpeta donde se encuentran los archivos a procesar. Por defecto: `base_txt`.
- `--output_folder`: Carpeta donde se guardarán los archivos procesados. Por defecto: `preprocessed_csv`.
- `--slow-down`: Valor flotante que indica el retardo en segundos después de procesar cada archivo. Por defecto: `0.3`.

## Estructura del Proyecto

```
preprocessing-txt-files/
├── base_txt/                # Carpeta de entrada (archivos originales)
├── preprocessed_csv/        # Carpeta de salida (archivos procesados)
├── preprocess.py            # Script principal de procesamiento
├── README.md                # Este archivo
├── requirements.txt         # Archivo con las dependencias (si se utiliza pip)
└── environment.yml          # Archivo del entorno Conda (opcional)
```

## Licencia

Este proyecto no está licenciado. Es de uso privado para un proyecto de la universidad. Si deseas utilizarlo, por favor contacta al autor.

## Contacto

Si tienes preguntas o sugerencias, por favor crea un _issue_ en el repositorio o contacta a [ldlizcano@uninorte.edu.co](mailto:tu_email@dominio.com).
