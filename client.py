import requests
from db import messages

url = "http://127.0.0.1:5000"

# POST: Crear un nuevo mensaje
def test_post_message():
    data = {"content": "Hola desde requests"}
    response = requests.post(f"http://127.0.0.1:5000/send", json=data)
    print("POST Response:", response.status_code, response.json())

# GET: Obtener todos los mensajes
def test_get_messages():
    response = requests.get(f"http://127.0.0.1:5000/receive")
    print("GET Response:", response.status_code, response.json())


# PUT: Actualizar un mensaje por ID
def test_put_message(message_id):
    payload = {"content": "Mensaje actualizado con requests"}
    response = requests.put(f"{url}/{message_id}", json=payload)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())

# DELETE: Eliminar un mensaje por ID
def test_delete_message(message_id):
    response = requests.delete(f"{url}/{message_id}")
    print(f"DELETE Response (ID {message_id}):", response.status_code, response.json())

# Ejecutar las pruebas
if __name__ == "__main__":
    # Crear un mensaje
    test_post_message()

    # Obtener todos los mensajes
    test_get_messages()

    test_put_message('dec1d104fe034c11b05d7b4a132d4825')