import requests
from db import messages

session = requests.Session()

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
    test_good()
    test_bad()