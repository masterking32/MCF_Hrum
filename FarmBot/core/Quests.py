# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json


class Quests:
    def __init__(self, log, httpRequest, account_name):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name

    def daily(self):
        try:
            response = self.http.post(url="/quests/daily", data=json.dumps({}))

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to get daily quests!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to get daily quests!</r>"
            )
            return None

    def check_daily_reward(self, daily_quests):
        try:
            self.log.info(
                f"<g>🔍 <c>{self.account_name}</c> checking daily reward...</g>"
            )
            if daily_quests is None or "data" not in daily_quests:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to claim daily reward!</r>"
                )
                return None

            daily_rewards = daily_quests["data"]
            for day, state in daily_rewards.items():
                if state == "canTake":
                    self.log.info(
                        f"<g>🪙 daily reward for <c>{self.account_name}</c> is available</g>"
                    )

                    self.claim_daily_reward(id=day)
                    self.log.info(
                        f"<g>✅ daily reward for <c>{self.account_name}</c> claimed</g>"
                    )

        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to claim daily reward!</r>"
            )
            return None

    def claim_daily_reward(self, id=1):
        try:
            response = self.http.post(
                url="/quests/daily/claim",
                data=json.dumps({"data": id}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to claim daily reward!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to claim daily reward!</r>"
            )
            return None
