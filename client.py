import requests
from db import messages

session = requests.Session()
access_token = None


def test_post_message(data):
    response = requests.post(f"http://127.0.0.1:5000/send", json=data)
    print("POST Response:", response.status_code, response.json())
    return list(response.json())


def test_get_messages():
    response = requests.get(f"http://127.0.0.1:5000/messages")
    print("GET Response:", response.status_code, response.json())


def test_put_message(message_id, data):
    response = requests.put(f"http://127.0.0.1:5000/modify/{message_id}", json=data)
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
    print("POST Response:", response.cookies, response.status_code, response.json())
    #if response.status_code() == 200:
    #    access_token = response.json.get("access_token")
    #print("POST Response:", response.status_code, response.json())



def test_delete_user(user_data):
    response = session.delete(f"http://127.0.0.1:5000/logout", json=user_data)
    print("DELETE Response:", response.status_code, response.json())


def test_good_session():
    user_data = {"username": "JoseMa", "password": "miMa2dresita"}
    data1 = {"content": "1"}
    data2 = {"content": "2"}
    data3 = {"content": "3"}
    payload = {"content": "Mensaje actualizado con requests"}
    test_create_user(user_data)
    test_generate_cookie(user_data)
    test_get_users()
    values1 = test_post_message(data1)
    values2 = test_post_message(data2)
    values3 = test_post_message(data3)
    test_get_messages()
    test_put_message(values1[0], payload)
    test_get_messages()
    test_delete_message(values3[0])
    test_get_messages()
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
    data = {"content": "Hola desde requests"}
    values = test_post_message(data)
    payload = {"content": "Mensaje actualizado con requests"}
    test_get_messages()
    test_put_message(values[0], payload)
    test_delete_message(values[0])


def test_prueba():
    user_data = {"username": "JoseMa", "password": "miMa2dresita"}
    test_create_user(user_data)
    test_generate_cookie(user_data)
    test_delete_user(user_data)

def test_bad():
    data = {"content": "Hola desde requests"}
    test_get_messages() #Nothing in db so it must be 404
    test_bad_post()
    values = test_post_message(data)
    test_put_message(1341)
    test_bad_put(values[0])
    test_delete_message(234)

def test_get_session():
    user_data = {"username": "JoseMa", "password": "miMa2dresita"}
    response1 = session.post("http://127.0.0.1:5000/register", json=user_data)
    print("Register Response:", response1.json())
    response2 = session.post("http://127.0.0.1:5000/login", json=user_data)
    print("Login Response:", response2.json())
    response3 = session.get("http://127.0.0.1:5000/get_session")
    print("Session Content after login:", response3.json())
    data = {"content": "Hola desde requests"}
    response4 = session.post("http://127.0.0.1:5000/send", json=data)
    print("Send Message Response:", response4.json())
    response5 = session.get("http://127.0.0.1:5000/messages")
    print("Messages:", response5.json())
    response6 = session.get("http://127.0.0.1:5000/get_session")
    print("Session Content after sending a message:", response6.json())
    response7 = session.post("http://127.0.0.1:5000/logout", json=user_data)
    print("Logout Response:", response7.json())
    response8 = session.get("http://127.0.0.1:5000/get_session")
    print("Session Content after logout:", response8.json())

if __name__ == "__main__":
    #test_good()
    #test_bad()
    #test_good_session()
    #test_bad_session()
    #test_prueba()
    test_get_session()