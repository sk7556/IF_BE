from django.test import TestCase, Client
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async

User = get_user_model()

email = "test12@test12.com"
password = "testpw123"
loginurl = "/accounts/login/"
room_create_url = "/chat/roomcreate/"
room_list_url = "/chat/roomlist/"
room_invisible_url = "/chat/roominvisible/"
testmessage = "hello world"


class MyTests(TestCase):
    def setUp(self):
        print("----------유저 생성-----------")
        self.user = User.objects.create_user(
            email=email,
            password=password,
            gender="Male",
            nickname="test",
            birth="2023-11-11",
        )
        self.user2 = User.objects.create_user(
            email="test222@test22.com",
            password="testpassword2222",
            gender="Male",
            nickname="test",
            birth="2023-11-11",
        )
        client = Client()
        login = client.login(email=email, password=password)
        self.assertTrue(login)

    @database_sync_to_async
    def login_user(self, client):
        response = client.post(loginurl, {"email": email, "password": password})
        access_token = response.data.get("access")
        return client

    @database_sync_to_async
    def create_room(self, client, user_id):
        response = client.post(room_create_url, {"user": user_id})
        room_name = response.data.get("room")["room_name"]

        return room_name

    @database_sync_to_async
    def room_invisible(self, client, room_name):
        response = client.get(f"{room_invisible_url}{room_name}/")
        return response

    @database_sync_to_async
    def load_message(self, client, room_name):
        response = client.get(f"/chat/{room_name}/?page=1")
        return response

    @database_sync_to_async
    def load_rooms(self, client):
        response = client.get(f"{room_list_url}")
        return response

    def test_room_create(self):
        print("----------채팅방 생성 테스트-----------")
        client = Client()
        client.post(loginurl, {"email": email, "password": password})
        response = client.post(room_create_url, {"user": "2"})
        room_name = response.data.get("room")["room_name"]

        print("room_name:", room_name)
        self.assertTrue(room_name)
        self.assertEqual(len(room_name), 20)

        print("----------채팅방 생성 테스트 완료-----------")

    async def test_my_consumer(self):
        print("----------채팅방 접속 테스트-----------")

        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "")
        client = Client()
        client = await self.login_user(client)
        room_name = await self.create_room(client, "2")
        print("room_name:", room_name)
        self.assertTrue(room_name)
        self.assertEqual(len(room_name), 20)

        communicator.scope["url_route"] = {
            "args": (),
            "kwargs": {"room_name": room_name},
        }

        cookies = client.cookies.output(header="", sep=";").strip().split("; ")
        communicator.scope["cookies"] = {}
        for cookie in cookies:
            key, value = cookie.split("=")
            communicator.scope["cookies"][key] = value

        connected, subprotocol_ = await communicator.connect()
        self.assertTrue(connected)

        print("----------메세지 전송 테스트-----------")

        await communicator.send_json_to({"message": testmessage})
        response = await communicator.receive_json_from()
        print("받은 메세지:", response)
        assert response["message"]["message"] == testmessage

        await communicator.disconnect()
        print("----------메세지 전송 테스트 완료-----------")

        print("----------메세지 불러오기 테스트 -----------")

        response = await self.load_message(client, room_name)
        print(response.data)
        assert response.status_code == 200

        print("----------메세지 불러오기 테스트 완료 -----------")

        print("----------채팅 목록 불러오기 테스트 -----------")

        response = await self.load_rooms(client)
        print(response.data)
        assert response.status_code == 200

        print("----------채팅 목록 불러오기 테스트 완료 -----------")

        print("----------메세지 숨기기 테스트-----------")

        response = await self.room_invisible(client, room_name)
        print(response.data)
        assert response.status_code == 200

        print("----------메세지 숨기기 테스트 완료 -----------")
