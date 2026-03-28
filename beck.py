# import json
#
# from aiohttp import request
#
#
# class Chat:
#     def __init__(self, user_id: int = None):
#         self.user_id = user_id
#
#     bot_token = "8133134761:AAFi7aTDD3vCM78LhVKUqaK05kT7Avcsnmo"
#     basic_url = f"https://api.telegram.org/bot>{bot_token}/"
#
#     def get_massage(self):
#         url = self.basic_url + "getUpdates"
#         from urllib import request
#         response = request.get(url)
#         response_data = json.loads(response.text)
#         messages = response_data.get("result")
#         res = []
#         for message in messages:
#             print(message.get("message"))
#             text = messages.get("message").get("text")
#             user_id = messages.get("message").get("from").get("id")
#             username = messages.get("message").get("from").get("username")
#             text = f"{username} ({user_id}): {text})"
#             res.append({"massage: ": text, "user_id": user_id, "username": username})
#         return res
#
#     def send_massage(self, text):
#         user_id = self.user_id
#         url = f"{self.basic_url}/sendMessage?chat_id={user_id} , text={text}"
#         request.get(url)
#
#     def all_user_id(self):
#         message = self.get_massage()
#         users_id = []
#         for message in message:
#             _, user_id, _ = message.values()
#             user_id.append(users_id)
#         return set(users_id)
#
#     def send_ads(self, message):
#         user_id = self.all_user_id()
#         for id in user_id:
#             Chat(user_id=id).send_massage(message)
#
#
