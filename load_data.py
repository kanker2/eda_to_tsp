import os
import pandas as pd
from bs4 import BeautifulSoup

DOWNLOAD_SOLUTIONS_URL = "http://comopt.ifi.uni-heidelberg.de/software/TSPLIB95/STSP.html"
SYMMETRIC_TSP_SOLUTIONS_FILENAME='optimal_symmetric_tsp_solutions.html'
ALL_TSP_FOLDER='ALL_tsp'

def symmetric_tsp_solutions():
    """
    Descarga el archivo HTML de soluciones óptimas TSP, lo guarda localmente
    y luego parsea el contenido para extraer los nombres de los problemas
    y sus valores óptimos.
    """
    local_html_path = SYMMETRIC_TSP_SOLUTIONS_FILENAME

    if not os.path.exists(local_html_path):
        print(f"\nDescargando las soluciones TSP óptimas de '{DOWNLOAD_SOLUTIONS_URL}'...")
        try:
            response = requests.get(DOWNLOAD_SOLUTIONS_URL)
            response.raise_for_status()

            with open(local_html_path, 'w', encoding='iso-8859-1') as f:
                f.write(response.text)
            print(f"Descarga de soluciones completada en: {local_html_path}")
        except requests.exceptions.RequestException as e:
            print(f"ERROR: No se pudo descargar el archivo de soluciones de '{DOWNLOAD_SOLUTIONS_URL}': {e}")
            return pd.Series()
    else:
        print(f"\nEl archivo '{local_html_path}' ya existe. Saltando la descarga.")

    try:
        with open(local_html_path, 'r', encoding='iso-8859-1') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{local_html_path}' no fue encontrado después de intentar descargarlo.")
        return pd.Series()
    except Exception as e:
        print(f"Error al leer el archivo '{local_html_path}': {e}")
        return pd.Series()

    soup = BeautifulSoup(html_content, 'html.parser')

    list_items = soup.find_all('li')
    problem_solutions = []

    for item in list_items:
        text = item.get_text()
        parts = text.split(': ', 1)

        if len(parts) == 2:
            problem_name = parts[0].strip()
            solution_string = parts[1].strip()

            solution_value_part = solution_string.split('(')[0].strip()
            try:
                solution_value = int(solution_value_part)
                problem_solutions.append((problem_name, solution_value))
            except ValueError:
                print(f"Advertencia: No se pudo convertir el valor '{solution_value_part}' a entero para '{problem_name}'.")
        else:
            pass

    problem_solutions = pd.Series(dict(problem_solutions))
    problem_solutions.index.name = 'problem_name'
    problem_solutions.name = 'optimal_cost'
    return problem_solutions


def read_tsp_files_from_folder(tsp_folder):
    file_names=pd.Series(os.listdir(tsp_folder))
    file_paths=file_names.apply(lambda x: os.path.join(tsp_folder,x))
    file_paths=file_paths[file_paths.apply(os.path.isfile)].reset_index(drop=True)
    file_paths.name='file_paths'

    problems=pd.DataFrame(file_paths)
    intermediate_result_name_sol_type=problems['file_paths'].str.split('\\').apply(lambda x: (x[:1]+x[1].split('.'))[1:])
    problems['name']=intermediate_result_name_sol_type.apply(lambda x: x[0])
    problems['type']=intermediate_result_name_sol_type.apply(lambda x: x[-1])
    problems=problems.iloc[1:].reset_index(drop=True)
    regex_pattern = r'(\d+)$'
    numeric_suffix_str = problems.name.str.extract(regex_pattern, expand=False)
    numeric_suffix = pd.to_numeric(numeric_suffix_str, errors='coerce')
    problems['size']=numeric_suffix

    return problems

def load_problems(tsp_folder=ALL_TSP_FOLDER):
    tsp_files=read_tsp_files_from_folder(tsp_folder)
    problems=tsp_files[tsp_files.type=='tsp']
    return problems.reset_index(drop=True)

def load_solutions(tsp_folder=ALL_TSP_FOLDER):
    tsp_files=read_tsp_files_from_folder(tsp_folder)
    solutions=tsp_files[tsp_files.type=='tour']
    return solutions.reset_index(drop=True)