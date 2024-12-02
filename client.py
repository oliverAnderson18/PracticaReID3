import requests

url = "localhost:5000"

url = "http://127.0.0.1:5000"

# POST: Crear un nuevo mensaje
def test_post_message():
    payload = {"content": "Hola desde requests"}
    response = requests.post(BASE_URL, json=payload)
    print("POST Response:", response.status_code, response.json())

# GET: Obtener todos los mensajes
def test_get_messages():
    response = requests.get(BASE_URL)
    print("GET Response:", response.status_code, response.json())

# GET: Obtener un mensaje por ID
def test_get_message_by_id(message_id):
    response = requests.get(f"{BASE_URL}/{message_id}")
    print(f"GET Response (ID {message_id}):", response.status_code, response.json())

# PUT: Actualizar un mensaje por ID
def test_put_message(message_id):
    payload = {"content": "Mensaje actualizado con requests"}
    response = requests.put(f"{BASE_URL}/{message_id}", json=payload)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())

# DELETE: Eliminar un mensaje por ID
def test_delete_message(message_id):
    response = requests.delete(f"{BASE_URL}/{message_id}")
    print(f"DELETE Response (ID {message_id}):", response.status_code, response.json())

# Ejecutar las pruebas
if __name__ == "__main__":
    # Crear un mensaje
    test_post_message()

    # Obtener todos los mensajes
    test_get_messages()

    # Obtener un mensaje por ID (prueba con ID 1)
    test_get_message_by_id(1)

    # Actualizar un mensaje por ID (prueba con ID 1)
    test_put_message(1)

    # Eliminar un mensaje por ID (prueba con ID 1)
    test_delete_message(1)

    # Verificar que el mensaje se eliminó correctamente
    test_get_messages()
