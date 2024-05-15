import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import urljoin, urlparse

# URL de la página inicial
start_url = "https://es.wikipedia.org/wiki/Pok%C3%A9mon"

# Hacer una solicitud HTTP GET a la URL inicial
response = requests.get(start_url)

# Comprobar si la solicitud fue exitosa
if response.status_code == 200:
    # Analizar el contenido HTML de la página
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extraer todas las etiquetas <a> y sus enlaces
    a_tags = soup.find_all('a')
    links = [urljoin(start_url, a.get('href')) for a in a_tags if a.get('href')]

    # Filtrar enlaces que sean válidos y relevantes
    filtered_links = []
    for link in links:
        parsed_link = urlparse(link)
        if parsed_link.scheme in ['http', 'https'] and 'wikipedia.org' in parsed_link.netloc:
            filtered_links.append(link)
    
    # Limitar el número de enlaces para evitar demasiadas solicitudes
    filtered_links = filtered_links[:10]  # Limita a los primeros 10 enlaces

    # Crear un diccionario para almacenar los datos
    data = {}

    # Recorrer cada enlace filtrado
    for link in filtered_links:
        try:
            # Hacer una solicitud HTTP GET a cada enlace
            link_response = requests.get(link)
            
            # Comprobar si la solicitud fue exitosa
            if link_response.status_code == 200:
                # Analizar el contenido HTML de la página enlazada
                link_soup = BeautifulSoup(link_response.content, 'html.parser')

                # Extraer todas las etiquetas <h1> y <p>
                h1_tags = link_soup.find_all('h1')
                p_tags = link_soup.find_all('p')

                # Crear una lista para almacenar las etiquetas encontradas
                tags = [str(tag) for tag in h1_tags + p_tags]
            else:
                # Si la solicitud no fue exitosa, la lista de etiquetas estará vacía
                tags = []
        except requests.RequestException as e:
            # Si hay un error en la solicitud, imprimir el error y continuar
            print(f"Error al acceder a {link}: {e}")
            tags = []

        # Añadir las etiquetas encontradas al diccionario
        data[link] = tags

    # Guardar el diccionario en un archivo JSON
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

    print("Datos guardados en 'output.json'")
else:
    print("Error al acceder a la página inicial")
