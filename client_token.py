import requests

access_token = None


def test_post_message(data):
    headers = {"Authorization": f"Bearer {"access_token"}"}
    response = requests.post(f"http://127.0.0.1:5000/send", json=data, headers=headers)
    print("POST Response:", response.status_code, response.json())
    if response.status_code == 200:
        return list(response.json())
    return []



def test_get_messages():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://127.0.0.1:5000/messages", headers=headers)
    print("GET Response:", response.status_code, response.json())
    if response.status_code == 200:
        return response.json()  # Devuelve la lista de mensajes
    return []



def test_put_message(message_id, data):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.put(f"http://127.0.0.1:5000/modify/{message_id}", json=data, headers=headers)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())


def test_delete_message(message_id):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(f"http://127.0.0.1:5000/delete/{message_id}", headers=headers)
    print(f"DELETE Response (ID {message_id}):", response.status_code, response.json())


def test_create_user(user_data):
    response = requests.post("http://127.0.0.1:5000/register", json=user_data)
    print("POST Response:", response.status_code, response.json())


def test_get_users():
    headers = {
    "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(f"http://127.0.0.1:5000/users", headers=headers)
    print("GET Response:", response.status_code, response.json())


def test_generate_token(user_data):
    global access_token
    response = requests.post(f"http://127.0.0.1:5000/login", json=user_data)
    if response.status_code == 200:
        access_token = response.json().get("Access Token")
    else:
        print(f"Error: {response.json()}")  # Imprime el error si no se obtiene el token
    print("POST Response:", response.status_code, response.json())


def test_good_session():
    user_data = {"username": "JoseMa", "password": "miMa2dresita"}
    data1 = {"content": "1"}
    data2 = {"content": "2"}
    data3 = {"content": "3"}
    payload = {"content": "Mensaje actualizado con requests"}
    
    test_create_user(user_data)
    test_generate_token(user_data)

    if access_token:  # Verifica que el token se haya obtenido correctamente
        test_get_users()
        values1 = test_post_message(data1)
        values2 = test_post_message(data2)
        values3 = test_post_message(data3)
        test_get_messages()
        test_put_message(values1[0], payload)
        test_get_messages()
        test_delete_message(values3[0])
        test_get_messages()
    else:
        print("No access token, skipping authenticated tests.")




if __name__ == "__main__":
    test_good_session()
