# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json
import random
import time


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
                    return None

            self.log.info(
                f"<y>🟡 <c>{self.account_name}</c> daily reward is not available!</y>"
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

    def check_riddle(self, quests, user_quests):
        try:
            riddle_quest = None
            for quest in quests:
                if quest["key"].startswith("riddle_"):
                    riddle_quest = quest
                    break

            if riddle_quest is None:
                self.log.info(
                    f"<y>🟡 <c>{self.account_name}</c> | Riddle is not available!</y>"
                )
                return None

            quest_id = riddle_quest.get("key", None)
            quest_answer = riddle_quest.get("checkData", None)

            if quest_id is None or quest_answer is None:
                return None

            for quest in user_quests:
                if quest["key"] == quest_id and quest["isRewarded"] == True:
                    self.log.info(
                        f"<g>✅ <c>{self.account_name}</c> | Riddle already claimed!</g>"
                    )
                    return None

            answer_check = self.check_riddle_answer(quest_id, quest_answer)
            if (
                answer_check is None
                or "success" not in answer_check
                and not answer_check["success"]
            ):
                return None

            self.log.info(
                f"<g>📝 <c>{self.account_name}</c> | Riddle answer is correct, Calming ...</g>"
            )

            time.sleep(random.randint(2, 5))

            claim = self.quest_claim(quest_id, quest_answer)
            if claim is None or "success" not in claim and not claim["success"]:
                return None

            self.log.info(f"<g>✅ <c>{self.account_name}</c> | Riddle claimed!</g>")

        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to check riddle!</r>"
            )
            return None

    def quest_claim(self, quest_id, quest_answer):
        try:
            response = self.http.post(
                url="/quests/claim",
                data=json.dumps({"data": [quest_id, quest_answer]}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to claim quest!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to claim quest!</r>"
            )
            return None

    def check_riddle_answer(self, quest_id, quest_answer):
        try:
            response = self.http.post(
                url="/quests/check",
                data=json.dumps({"data": [quest_id, quest_answer]}),
            )

            if response is None:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to check riddle answer!</r>"
                )
                return None

            return response
        except Exception as e:
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to check riddle answer!</r>"
            )
            return None
