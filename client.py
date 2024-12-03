import requests
from db import messages

url = "http://127.0.0.1:5000"


def test_post_message():
    data = {"content": "Hola desde requests"}
    response = requests.post(f"http://127.0.0.1:5000/send", json=data)
    print("POST Response:", response.status_code, response.json())

def test_get_messages():
    response = requests.get(f"http://127.0.0.1:5000/receive")
    print("GET Response:", response.status_code, response.json())

def test_put_message(message_id):
    payload = {"content": "Mensaje actualizado con requests"}
    response = requests.put(f"http://127.0.0.1:5000/modify/{message_id}", json=payload)
    print(f"PUT Response (ID {message_id}):", response.status_code, response.json())

def test_delete_message(message_id):

    response = requests.delete(f"http://127.0.0.1:5000/delete/{message_id}")
    print(f"DELETE Response (ID {message_id}):", response.status_code, response.json())

if __name__ == "__main__":

    test_post_message()

    test_get_messages()

    test_put_message('dec1d104fe034c11b05d7b4a132d4825')