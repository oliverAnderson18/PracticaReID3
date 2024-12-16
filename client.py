import requests
from db import messages

session = requests.Session()
access_token = None


def test_post_message():
    data = {"content": "Hola desde requests"}
    response = requests.post(f"http://127.0.0.1:5000/send", json=data)
    print("POST Response:", response.status_code, response.json())
    return list(response.json())


def test_get_messages():
    response = requests.get(f"http://127.0.0.1:5000/messages")
    print("GET Response:", response.status_code, response.json())


def test_put_message(message_id):
    payload = {"content": "Mensaje actualizado con requests"}
    response = requests.put(f"http://127.0.0.1:5000/modify/{message_id}", json=payload)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())


def test_delete_message(message_id):
    response = requests.delete(f"http://127.0.0.1:5000/delete/{message_id}")
    print(f"DELETE Response (ID {message_id}):", response.status_code, response.json())


def test_bad_post():
    data = {}
    response = requests.post(f"http://127.0.0.1:5000/send", json=data)
    print("POST Response:", response.status_code, response.json())
    return list(response.json())


def test_bad_put(message_id):
    payload = {}
    response = requests.put(f"http://127.0.0.1:5000/modify/{message_id}", json=payload)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())


def test_create_user(user_data):
    response = session.post("http://127.0.0.1:5000/register", json=user_data)
    print("POST Response:", response.status_code, response.json())


def test_get_users():
    response = session.get(f"http://127.0.0.1:5000/users")
    print("GET Response:", response.status_code, response.json())


def test_generate_cookie(user_data):
    global access_token
    response = session.post(f"http://127.0.0.1:5000/login", json=user_data)
    if response.status_code() == 200:
        access_token = response.json.get("access_token")
    print("POST Response:", response.status_code, response.json())


def test_delete_user(user_data):
    response = session.delete(f"http://127.0.0.1:5000/logout", json=user_data)
    print("DELETE Response:", response.status_code, response.json())


def test_good_session():
    user_data = {"username": "JoseMa", "password": "miMa2dresita"}
    test_create_user(user_data)
    test_get_users()
    test_generate_cookie(user_data)
    test_delete_user(user_data)


def test_bad_session():
    test_get_users()
    user_data1 = {"username": "", "password": "miMa2dresita"}
    user_data2 = {"username": "JoseMa", "password": ""}
    user_data3 = {"username": "Josa", "password": "sdla23nkvf"}
    user_data4 = {"username": "Jos a", "password": "sdla23nkvf"}
    user_data5 = {"username": "JoseMa", "password": "sd"}
    user_data6 = {"username": "JoseMa", "password": "151221342341"}
    user_data7 = {"username": "JoseMa", "password": "jasldfjasldf"}
    test_create_user(user_data1)
    test_generate_cookie(user_data1)
    test_delete_user(user_data1)

    test_create_user(user_data2)
    test_generate_cookie(user_data2)
    test_delete_user(user_data2)

    test_create_user(user_data3)
    test_generate_cookie(user_data3)
    test_delete_user(user_data3)

    test_create_user(user_data4)
    test_generate_cookie(user_data4)
    test_delete_user(user_data4)

    test_create_user(user_data5)
    test_generate_cookie(user_data5)
    test_delete_user(user_data5)

    test_create_user(user_data6)
    test_generate_cookie(user_data6)
    test_delete_user(user_data6)

    test_create_user(user_data7)
    test_generate_cookie(user_data7)
    test_delete_user(user_data7)

def test_good():
    values = test_post_message()
    test_get_messages()
    test_put_message(values[0])
    test_delete_message(values[0])


def test_bad():
    test_get_messages() #Nothing in db so it must be 404
    test_bad_post()
    values = test_post_message()
    test_put_message(1341)
    test_bad_put(values[0])
    test_delete_message(234)


if __name__ == "__main__":
    #test_good()
    #test_bad()
    test_good_session()
