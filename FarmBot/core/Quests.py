# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot


import json
import random
import time
from utilities.utilities import getConfig


class Quests:
    def __init__(self, log, httpRequest, account_name, license_key, tgAccount=None):
        self.log = log
        self.http = httpRequest
        self.account_name = account_name
        self.license_key = license_key
        self.tgAccount = tgAccount

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

    async def check_tasks(self, quests, user_quests):
        try:
            self.log.info(f"<g>🔍 <c>{self.account_name}</c> checking quests...</g>")
            for quest in quests:
                checkType = quest.get("checkType", None)
                quest_id = quest.get("key", None)

                if checkType is None or quest_id is None:
                    continue

                task_Title = quest.get("actionText", "")
                is_completed = False
                for user_quest in user_quests:
                    if (
                        user_quest["key"] == quest_id
                        and user_quest["isRewarded"] == True
                    ):
                        is_completed = True
                        break

                if is_completed:
                    continue

                if checkType == "telegramChannel":
                    if (
                        self.tgAccount is None
                        or getConfig("join_channels", True) is False
                    ):
                        continue

                    channel_url = quest.get("actionUrl", None)

                    if channel_url is None or channel_url == "":
                        continue

                    if "+" not in channel_url:
                        channel_url = (
                            channel_url.replace("https://t.me/", "")
                            .replace("@", "")
                            .replace("boost/", "")
                        )

                        channel_url = (
                            channel_url.split("/")[0]
                            if "/" in channel_url
                            else channel_url
                        )

                    self.log.info(
                        f"<g>📝 <c>{self.account_name}</c> | Attempting to join the <c>{channel_url}</c> channel to complete the <c>{task_Title}</c> task</g>"
                    )

                    try:
                        await self.tgAccount.joinChat(channel_url)
                    except Exception as e:
                        pass

                    time.sleep(random.randint(5, 10))

                    self.quest_claim(quest_id)
                    self.log.info(
                        f"<g>✅ <c>{self.account_name}</c> | <c>{task_Title}</c> is completed!</g>"
                    )
                elif checkType in ["fakeCheck"]:
                    self.quest_claim(quest_id)
                    self.log.info(
                        f"<g>✅ <c>{self.account_name}</c> | <c>{task_Title}</c> is completed!</g>"
                    )
                elif checkType == "username":
                    if (
                        self.tgAccount is None
                        or getConfig("change_name", True) is False
                    ):
                        continue

                    checkData = quest.get("checkData", None)
                    if checkData is None:
                        continue

                    tgMe = self.tgAccount.me if self.tgAccount.me else None
                    if tgMe is None:
                        continue

                    try:
                        tgMe.first_name = tgMe.first_name or ""
                        tgMe.last_name = tgMe.last_name or ""

                        if checkData not in [tgMe.first_name, tgMe.last_name]:
                            await self.tgAccount.setName(
                                tgMe.first_name, tgMe.last_name + checkData
                            )

                            self.log.info(
                                f"<g>✅ <c>{self.account_name}</c> | Name changed to <c>{checkData}</c> to complete the <c>{task_Title}</c> task</g>"
                            )
                            self.log.info(
                                f"<g>✅ <c>{self.account_name}</c> | <c>{task_Title}</c> will be completed on the next run!</g>"
                            )
                            continue

                        self.quest_claim(quest_id)
                        self.log.info(
                            f"<g>✅ <c>{self.account_name}</c> | <c>{task_Title}</c> is completed!</g>"
                        )
                    except Exception as e:
                        pass
                else:
                    continue

            self.log.info(
                f"<g>✅ <c>{self.account_name}</c> | All quests are completed!</g>"
            )
        except Exception as e:
            print(e)
            self.log.error(
                f"<r>⭕ <c>{self.account_name}</c> failed to check tasks!</r>"
            )
            return None

    def quest_claim(self, quest_id, quest_answer=None):
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
