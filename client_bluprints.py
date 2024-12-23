import requests

access_token = None


def test_create_user(user_data):
    response = requests.post("http://127.0.0.1:5000/auth/register", json=user_data)
    print("POST Response (Create User):", response.status_code, response.json())


def test_get_users():
    global access_token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("http://127.0.0.1:5000/auth/users", headers=headers)
    print("GET Response (Get Users):", response.status_code, response.json())


def test_generate_token(user_data):
    global access_token
    response = requests.post("http://127.0.0.1:5000/auth/login", json=user_data)
    if response.status_code == 200:
        access_token = response.json().get("Access Token")
        print("Access Token Obtained:", access_token)
    else:
        print(f"Error (Generate Token): {response.json()}")
    print("POST Response (Login):", response.status_code, response.json())


def test_grant(grant_data):
    global access_token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.post("http://127.0.0.1:5000/admin/grant", json=grant_data, headers=headers)
    print("POST Response (Grant Admin):", response.status_code, response.json())



def test_good_session():
    user_data = {"username": "JoseMa234", "password": "jfasAf34"}
    user_data2 = {"username": "JoseMMsa234", "password": "jfasdAf34", "is_admin": "True"}

    test_create_user(user_data)
    test_create_user(user_data2)
    test_generate_token({"username": "JoseMMsa234", "password": "jfasdAf34"})
    if access_token:  # Verifica que el token se haya obtenido correctamente
        test_get_users()
        test_grant({"username": "JoseMa234"})
        test_get_users()
    else:
        print("No access token, skipping authenticated tests.")




if __name__ == "__main__":
    test_good_session()
