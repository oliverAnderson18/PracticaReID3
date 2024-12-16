import requests

access_token = None


def test_create_user(user_data):
    response = requests.post("http://127.0.0.1:5000/register", json=user_data)
    print("POST Response:", response.status_code, response.json())


def test_get_users():
    headers = {"authorization": f"Bearer {access_token}"}
    response = requests.get(f"http://127.0.0.1:5000/users", headers=headers)
    print("GET Response:", response.status_code, response.json())


def test_generate_token(user_data):
    global access_token
    response = requests.post(f"http://127.0.0.1:5000/login", json=user_data)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
    print("POST Response:", response.cookies, response.status_code, response.json())


def test_good_session():
    user_data = {"username": "JoseMa", "password": "Jose1234"}
    test_create_user(user_data)
    test_generate_token(user_data)
    test_get_users()


def test_prueba():
    user_data = {"username": "JoseMa", "password": "Jose1234"}
    test_create_user(user_data)
    test_generate_token(user_data)


if __name__ == "__main__":
    test_good_session()
