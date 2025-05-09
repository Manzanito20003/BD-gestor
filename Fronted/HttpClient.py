import requests

class HttpClient:
    def __init__(self):
        pass

    def make_get_request(self, url):
        try:
            # Hacer una solicitud GET
            response = requests.get(url)

            # Verificar el estado de la respuesta
            if response.status_code == 200:
                print(response.text)
                response= response.json()
                return response["data"]
            else:
                return f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error al conectar: {str(e)}"

    def make_post_request(self, url, params):
        try:
            # Convertir los parámetros a JSON (si son diccionario o estructura similar)
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, json=params, headers=headers)

            # Verificar el estado de la respuesta
            if response.status_code == 200:
                return response.json()  # Si la respuesta es JSON
            else:
                return f"Error: {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Error al conectar: {str(e)}"

