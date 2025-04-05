#!/usr/bin/env python3
import os
import re
import argparse
from tqdm import tqdm
from dataclasses import dataclass
from io import TextIOWrapper
from time import sleep

# Regex de las Líneas
numbers = r"[+-]?(?:(?:\d+(?:\.\d*)?)|\.\d+)(?:[eE][+-]?\d+)?"

SIZE = re.compile(f"Packet Size: ((\\d+) bytes)") #?
MESSAGE = re.compile(f"Received string: (.+:(\\d+))") #?
DATA = re.compile(f"RSSI: ({numbers}) dBm, SNR: ({numbers}) dB") #?


# Clase de lineas csv dataclass
@dataclass
class Row:
    mensaje: str            # *
    numero: int             # *
    rssi: str                # *
    snr: str                # *
    size: str     # *

# Expresión regular para filtrar los archivos
FILE_REGEX = re.compile(r'^(\d+[m])(\d+msps)[.]txt$', re.IGNORECASE)

def set_header(outfile: TextIOWrapper, separator: str):
    """
    Función para establecer el encabezado del archivo CSV.
    
    Parámetros:
      outfile  - Objeto de archivo de salida
      separator - Separador para el archivo CSV
    
    Devuelve:
      None
    """
    # Escribiendo encabezado en el archivo de salida
    outfile.write(f'mensaje{separator}numero{separator}rssi (dBm){separator}snr (dB){separator}size (bytes)\n')

def pre_process(infile: TextIOWrapper, outfile: TextIOWrapper, merged_file: TextIOWrapper| None, separator: str, freq, distance, version):
    """
    Función de pre-procesado (aún sin implementación).
    
    Parámetros:
      infile   - Objeto de archivo de entrada
      outfile  - Objeto de archivo de salida
      freq     - Frecuencia de muestreo (primer grupo de la regex)
      distance - Distancia (segundo grupo de la regex)
      version  - Versión (tercer grupo de la regex)
    
    La función se encargará de leer el contenido del archivo de entrada y escribir
    el resultado en el archivo de salida. Por ahora, simplemente copia el contenido.
    """
    #escribiendo encabezado en el archivo de salida
    set_header(outfile, separator)

    # Función para escribir en el archivo de salida
    def write_row(row: Row):
        # Convertir el dataclass a una cadena CSV
        values = [f'"{row.mensaje}"', str(row.numero), row.rssi, row.snr, row.size]
        outfile.write(separator.join(values) + '\n')
        if merged_file:
            # Escribir en el archivo combinado
            merged_file.write(separator.join(values) + '\n')

        row.mensaje = ""
        row.numero = 0
        row.rssi = ""
        row.snr = ""
        row.size = ""

    # Aquí se implementará el pre-procesado deseado.
    row = Row(mensaje="", numero="", rssi="", snr="", size="")

    for line in infile:
        if match := SIZE.search(line):
            row.size = match.group(2)
        elif match := MESSAGE.search(line):
            row.mensaje = match.group(1)
            row.numero = int(match.group(2))
        elif match := DATA.search(line):
            row.rssi = match.group(1)
            row.snr = match.group(2)
            write_row(row)
        else:
            # Si no hay coincidencias, continuar con la siguiente línea
            continue

def gen_file_name(freq: str, distance: str, version: str, str_format: str):
    """
    Genera un nombre de archivo basado en la frecuencia, distancia y versión.
    
    Parámetros:
      freq     - Frecuencia de muestreo
      distance - Distancia
      version  - Versión
      str_format - Formato de cadena para el nombre del archivo
    
    Devuelve:
      Nombre de archivo generado.
    """
    return str_format.format(freq=freq, distance=distance, version=version)
    

def process_files(input_folder: str, output_folder: str, merge: bool, slow_down: float, separator: str):
    # Asegurarse de que la carpeta de salida exista
    os.makedirs(output_folder, exist_ok=True)
    if merge:
        os.makedirs(os.path.join(output_folder, 'merge'), exist_ok=True)
        # Limpiar la carpeta merge si existe
        merge_folder = os.path.join(output_folder, 'merge')
        for file in os.listdir(merge_folder):
            os.remove(os.path.join(merge_folder, file))
    
    # Listar los archivos que cumplen con la regex en la carpeta de entrada
    files = [f for f in os.listdir(input_folder) if FILE_REGEX.match(f)]
    
    # Barra de carga para el procesamiento de archivos
    for filename in tqdm(files, desc="Procesando archivos"):
        match = FILE_REGEX.match(filename)
        if match:
            freq, distance = match.groups()
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename.replace('.txt', '.csv'))
            if merge:
                merged_file_path = os.path.join(output_folder, 'merge', f'{freq}-{distance}.csv')
            
            with open(input_file_path, 'r', encoding='utf-8', errors='replace') as infile, \
                 open(output_file_path, 'w', encoding='utf-8') as outfile:
                if merge:
                    # Check if merged file exists to write header
                    file_exists = os.path.isfile(merged_file_path)
                    with open(merged_file_path, 'a', encoding='utf-8') as merged_file:
                        # Write header if file is new
                        if not file_exists:
                            set_header(merged_file, separator)
                        pre_process(infile, outfile, merged_file, separator, freq, distance, None)
                else:
                    pre_process(infile, outfile, None, separator, freq, distance, None)
                
            # Opcional: mensaje de confirmación por archivo
            # print(f"Procesado: {filename}")
            sleep(slow_down)  # Simulación de tiempo de procesamiento

def main():
    parser = argparse.ArgumentParser(description="Script para procesar archivos según una regex")
    parser.add_argument("--input_folder", default="base_txt",
                        help="Carpeta de entrada con los archivos (por defecto: base_txt)")
    parser.add_argument("--output_folder", default="preprocessed_csv",
                        help="Carpeta de salida donde se guardarán los resultados (por defecto: preprocessed_csv)")
    parser.add_argument("--slow-down", type=float, default=0.3,
                        help="Tiempo de retardo en segundos durante el procesamiento de cada archivo (por defecto: 0.3)")
    parser.add_argument("--separator", default=",",
                        help="Separador para el archivo CSV (por defecto: ',')")
    parser.add_argument("--merge", action='store_true', default=False,
                        help="Si se establece, fusiona todos los archivos en uno solo")
    
    args = parser.parse_args()
    
    process_files(args.input_folder, args.output_folder, args.merge, args.slow_down, args.separator)

if __name__ == "__main__":
    main()
