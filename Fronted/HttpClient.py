import json

import requests
import logging

# Configura logging una sola vez (en la app principal idealmente)
logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

class HttpClient:
    def __init__(self):
        self.url = "http://127.0.0.1:5000/execute_sql"

    def make_get_request(self, url):
        try:
            response = requests.get(url)
            if response.status_code == 200:
                logging.debug(f"Respuesta GET exitosa: {response.text}")
                return response.json().get("data")
            else:
                logging.error(f"Error GET {response.status_code}: {response.text}")
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            logging.critical(f"Fallo de conexión en GET: {e}")
            return f"Error al conectar: {str(e)}"

    def make_post_request(self, params):
        try:
            if params is None:
                logging.error("Los parámetros no pueden ser None en POST")
                return None

            headers = {'Content-Type': 'application/json'}
            logging.debug(f"Haciendo POST a: {self.url} con parámetros: {params}")
            params=json.dumps(params)
            response = requests.post(self.url, json=params, headers=headers)

            if response.status_code == 200:
                logging.info(f"POST exitoso a:{self.url}")
                return {"response":response.json(),"status": response.status_code}
            else:
                logging.error(f"Error POST {response.status_code}: {response.text}")
                return {"error": response.text, "status": response.status_code}

        except requests.exceptions.RequestException as e:
            logging.critical(f"Fallo de conexión en POST: {e}")
            return f"Error al conectar: {str(e)}"
