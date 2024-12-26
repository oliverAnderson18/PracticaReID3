import requests

access_token = None

def test_create_user(user_data):
    response = requests.post("http://127.0.0.1:5000/auth/register", json=user_data)
    print("POST Response (Create User):", response.status_code, response.json())


def test_generate_token(user_data):
    global access_token
    response = requests.post("http://127.0.0.1:5000/auth/login", json=user_data)
    if response.status_code == 200:
        access_token = response.json().get("Access Token")
        print("Access Token Obtained:", access_token)
    else:
        print(f"Error (Generate Token): {response.json()}")
    print("POST Response (Login):", response.status_code, response.json())

def generate_gemini(data):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post("http://127.0.0.1:5000/gemini/generate", json=data, headers=headers)
    print("GEMINI response: ", response.status_code, response.json())

def test_envio_normal(data):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post("http://127.0.0.1:5000/texts/send", json=data, headers=headers)
    print("Normal response: ", response.status_code, response.json())

def test_mostrar_mensajes():
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("http://127.0.0.1:5000/texts/messages", headers=headers)
    print("All content: ", response.status_code, response.json())


def test_good_session():
    user_data = {"username": "JoseMa234", "password": "jfasAf34"}
    message = {"content": "Hazme un soneto romántico"}
    test_create_user(user_data)
    test_generate_token(user_data)
    if access_token:  # Verifica que el token se haya obtenido correctamente
        generate_gemini(message)
        test_envio_normal(message)
        test_mostrar_mensajes()
    else:
        print("No access token, skipping authenticated tests.")

if __name__ == "__main__":
    test_good_session()
