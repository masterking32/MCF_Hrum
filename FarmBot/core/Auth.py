# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json
from urllib.parse import parse_qs


class Auth:
    def __init__(self, log, httpRequest, account_name, web_app_query):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name
        self.web_app_query = web_app_query

    def auth(self):
        try:
            params = parse_qs(self.web_app_query)
            chat_type = params.get("chat_type", [""])[0]
            chat_instance = params.get("chat_instance", [""])[0]

            device_os = "android" if "Android" in self.http.user_agent else "ios"
            payload = {
                "data": {
                    "chatId": "",
                    "initData": self.web_app_query,
                    "platform": device_os,
                    "startParam": "ref95736407",
                }
            }

            if chat_type:
                payload["data"]["chatType"] = chat_type

            if chat_instance:
                payload["data"]["chatInstance"] = chat_instance

            response = self.http.post(
                url="/telegram/auth",
                data=json.dumps(payload),
                auth_header=False,
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to authenticate!</r>"
                )
                return None

            return response

        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to authenticate!</r>"
            )
            return None

    def register(self, race):
        try:
            response = self.http.post(
                url="/auth/register",
                data=json.dumps({"race": race}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to register!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to register!</r>")
            # self.log.error(f"<r>{e}</r>")
            return None
