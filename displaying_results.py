import matplotlib.pyplot as plt
import math

def drawing_tour(name, cities, tour, show_edge_weights=False,ax=None):
    """
    Visualiza el tour de TSP.

    Args:
        name (str): Nombre del problema TSP (usado en el título).
        cities (dict): Diccionario {ID_ciudad: [x, y]} con las coordenadas.
        tour (list): Lista ordenada de IDs de ciudades en el tour.
        show_edge_weights (bool): Si es True, muestra la distancia en cada arista.
                                   Por defecto es False (recomendado para muchos nodos).
    """

    def calculate_distance(coord1, coord2):
        """Calcula la distancia euclidiana entre dos puntos [x, y]."""
        return math.sqrt((coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2)

    # --- Preparar datos para plotear ---
    # Usamos (X, Y) donde X es el primer elemento y Y el segundo
    x_coords = [coord[0] for coord in cities.values()]
    y_coords = [coord[1] for coord in cities.values()]
    #city_ids = list(cities.keys()) # No necesitamos la lista completa si no etiquetamos todos

    # --- Crear la figura y los ejes del plot ---
    # Aumentamos un poco el tamaño para más puntos
    if ax is None:
        fig, ax = plt.subplots(figsize=(14, 12))

    # --- Plotear los puntos de las ciudades (muy pequeños) ---
    # Usamos un color claro para los puntos generales
    ax.scatter(x_coords, y_coords, color='lightgray', s=10, zorder=5, label='Ciudades') # s=3 tamaño muy pequeño

    # --- Opcional: Añadir etiquetas a *pocos* puntos (ej. el primero) ---
    # Para 1000+ puntos, etiquetar todos hace el gráfico ilegible.
    # Solo etiquetamos el punto de inicio para referencia.
    if tour: # Asegurarse de que el tour no esté vacío
        start_city_id = tour[0]
        start_coord = cities[start_city_id]

        # Etiqueta de texto para el inicio/fin
        ax.annotate(f'Inicio/Fin ({start_city_id})', (start_coord[0], start_coord[1]),
                    textcoords="offset points", xytext=(5,5), ha='left', fontsize=10, color='darkgreen')

        # Señalar el punto inicial/final con un marcador distinto
        ax.scatter(start_coord[0], start_coord[1], color='green', s=50, zorder=7, marker='*', label=f'Inicio/Fin ({start_city_id})') # zorder más alto
    else:
        print("Advertencia: El tour está vacío, no se puede identificar el punto de inicio/fin.")


    # --- Plotear el tour y mostrar costos de segmento (opcionalmente) ---
    total_cost = 0
    num_cities = len(tour)

    # Preparamos las coordenadas del tour para plotear una única línea
    tour_x = []
    tour_y = []

    # Asegurarse de que hay al menos 2 ciudades en el tour para dibujar segmentos
    if num_cities > 1:
        for i in range(num_cities):
            city1_id = tour[i]
            city2_id = tour[(i + 1) % num_cities] # Conecta el último con el primero

            coord1 = cities[city1_id]
            coord2 = cities[city2_id]

            tour_x.append(coord1[0])
            tour_y.append(coord1[1])

            # Calcular distancia del segmento
            distance = calculate_distance(coord1, coord2)
            total_cost += distance

            # Mostrar el coste de la arista en el punto medio - SÓLO SI show_edge_weights es True
            if show_edge_weights:
                mid_x = (coord1[0] + coord2[0]) / 2
                mid_y = (coord1[1] + coord2[1]) / 2
                # Reducir aún más el tamaño de la fuente si se activan los pesos
                ax.text(mid_x, mid_y, f'{distance:.1f}', fontsize=6, color='green', ha='center', va='bottom', alpha=0.8) # Formatear a 1 decimal, color verde, texto pequeño

        # Añadir el primer punto de nuevo al final para cerrar el ciclo en el plot
        # Esto solo si num_cities > 0 (lo cual ya está implícito en el bucle si num_cities > 1)
        tour_x.append(cities[tour[0]][0])
        tour_y.append(cities[tour[0]][1])

        # Plotear el tour como una única línea azul
        ax.plot(tour_x, tour_y, color='blue', linestyle='-', linewidth=1, zorder=3, label='Ruta del Tour') # zorder intermedio
    elif num_cities == 1:
         # Si solo hay una ciudad, no hay tour, solo se plotea el punto
         print("Advertencia: El tour contiene solo una ciudad. No se dibujará ninguna ruta.")
         # El punto ya se plotea en la sección de 'Ciudades' y 'Inicio/Fin'
    else:
         print("Advertencia: El tour está vacío.")


    # --- Configurar el gráfico ---
    ax.set_title(f'Visualización del Tour para {name}\nCoste Total del Tour: {total_cost:.2f}', fontsize=14)
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    # Desactivar la cuadrícula para evitar que sature el gráfico con muchos puntos/líneas
    ax.grid(False) # Opcional: puedes probar True si prefieres, pero para 1000+ puntos suele ser mejor False

    # Asegurarse de que los ejes se ajustan a los datos
    ax.autoscale_view()
    ax.set_aspect('equal', adjustable='box') # Intenta mantener proporciones si las unidades son las mismas en X e Y

    ax.legend()