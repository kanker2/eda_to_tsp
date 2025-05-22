import os
import gzip
import tarfile
import requests

DOWNLOAD_URL = "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/tsp/ALL_tsp.tar.gz"
BASE_DIRECTORY = 'ALL_tsp'
UNCOMPRESSED_FILES_DIRECTORY=os.path.join(BASE_DIRECTORY,'tar_gz')
TAR_GZ_FILENAME = os.path.basename(DOWNLOAD_URL)
DOWNLOAD_PATH = os.path.join(UNCOMPRESSED_FILES_DIRECTORY, TAR_GZ_FILENAME)

SOURCE_GZ_DIRECTORY = UNCOMPRESSED_FILES_DIRECTORY
OUTPUT_DIRECTORY = BASE_DIRECTORY

print(f"Iniciando script para descargar y descomprimir archivos TSP...")
print(f"Directorio base: {BASE_DIRECTORY}")

if not os.path.exists(BASE_DIRECTORY):
    os.makedirs(BASE_DIRECTORY, exist_ok=True)
    print(f"Directorio '{BASE_DIRECTORY}' creado.")
if not os.path.exists(UNCOMPRESSED_FILES_DIRECTORY):
    os.makedirs(UNCOMPRESSED_FILES_DIRECTORY, exist_ok=True)
    print(f"Directorio '{UNCOMPRESSED_FILES_DIRECTORY}' creado.")

print(f"\n--- Paso 1: Descargando {TAR_GZ_FILENAME} ---")
if not os.path.exists(DOWNLOAD_PATH):
    try:
        print(f"Descargando de: {DOWNLOAD_URL}")
        response = requests.get(DOWNLOAD_URL, stream=True)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded_size = 0
        
        with open(DOWNLOAD_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded_size += len(chunk)
        print(f"\nArchivo descargado con éxito en: {DOWNLOAD_PATH}")
    except requests.exceptions.RequestException as e:
        print(f"ERROR: No se pudo descargar el archivo de '{DOWNLOAD_URL}': {e}")
        exit(1)
else:
    print(f"El archivo '{DOWNLOAD_PATH}' ya existe. Saltando la descarga.")

print(f"\n--- Paso 2: Descomprimiendo {TAR_GZ_FILENAME} ---")
try:
    print(f"Extrayendo contenido de '{DOWNLOAD_PATH}' a '{UNCOMPRESSED_FILES_DIRECTORY}'...")
    with tarfile.open(DOWNLOAD_PATH, 'r:gz') as tar:
        tar.extractall(path=UNCOMPRESSED_FILES_DIRECTORY)
    print("Extracción del archivo .tar.gz completada.")

except tarfile.ReadError as e:
    print(f"ERROR: '{DOWNLOAD_PATH}' no parece ser un archivo tar.gz válido o está corrupto: {e}")
    exit(1)
except Exception as e:
    print(f"ERROR inesperado al extraer '{DOWNLOAD_PATH}': {e}")
    exit(1)

print(f"\n--- Paso 3: Descomprimiendo archivos .gz individuales ---")
print(f"Buscando archivos .gz en: {SOURCE_GZ_DIRECTORY}")

if not os.path.isdir(SOURCE_GZ_DIRECTORY):
    print(f"Error: El directorio fuente de .gz '{SOURCE_GZ_DIRECTORY}' no fue encontrado después de la extracción.")
    print("Por favor, verifica si la estructura interna del archivo ALL_tsp.tar.gz es diferente y ajusta 'SOURCE_GZ_DIRECTORY'.")
    exit(1)

count_processed = 0
count_decompressed = 0
count_failed = 0

try:
    entries = os.listdir(SOURCE_GZ_DIRECTORY)
except OSError as e:
    print(f"Error al listar archivos en '{SOURCE_GZ_DIRECTORY}': {e}")
    exit(1)

for entry_name in entries:
    full_path_gz = os.path.join(SOURCE_GZ_DIRECTORY, entry_name)

    if os.path.isfile(full_path_gz) and entry_name.lower().endswith('.gz'):
        count_processed += 1

        output_filename = entry_name[:-len('.gz')]
        output_path = os.path.join(OUTPUT_DIRECTORY, output_filename)

        try:
            with gzip.open(full_path_gz, 'rb') as f_in:
                with open(output_path, 'wb') as f_out:
                    f_out.writelines(f_in)
                    count_decompressed += 1

        except gzip.BadGzipFile:
            count_failed += 1
            print(f"  ERROR: '{entry_name}' no parece ser un archivo gzip válido o está corrupto.")
        except IOError as e:
             count_failed += 1
             print(f"  ERROR de E/S al procesar '{entry_name}': {e}")
        except Exception as e:
            count_failed += 1
            print(f"  ERROR inesperado al procesar '{entry_name}': {e}")

print("\n--- Resumen del Proceso de Descompresión Individual ---")
print(f"Archivos encontrados con extensión .gz para procesar: {count_processed}")
print(f"Archivos descomprimidos con éxito: {count_decompressed}")
print(f"Archivos que tuvieron errores: {count_failed}")
print("Proceso de descompresión finalizado.")

print()
print(f"Los archivos finales se encuentran en: {OUTPUT_DIRECTORY}")