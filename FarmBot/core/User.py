# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class User:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def data_all(self):
        try:
            response = self.http.post(url="/user/data/all", data=json.dumps({}))

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get data!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to get data!</r>")
            return None

    def after(self):
        try:
            response = self.http.post(
                url="/user/data/after", data=json.dumps({"lang": "en"})
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get after!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to get after!</r>")
            return None

    def cookie_open(self):
        try:
            response = self.http.post(url="/user/cookie/open", data=json.dumps({}))

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to open cookie!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to open cookie!</r>"
            )
            return None
