# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Hero:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def onboarding_finish(self, id=1):
        try:
            response = self.http.post(
                url="/hero/onboarding/finish",
                data=json.dumps({"data": id}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to finish onboarding!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to finish onboarding!</r>"
            )
            return None
