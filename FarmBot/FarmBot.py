# Developed by: MasterkinG32
# Date: 2024
# Github: https://github.com/masterking32
# Telegram: https://t.me/MasterCryptoFarmBot
import random
import sys
import os
import time

from utilities.utilities import add_account_to_display_data, getConfig
from .core.HttpRequest import HttpRequest
from .core.Auth import Auth
from .core.User import User
from .core.Quests import Quests
from .core.Hero import Hero

MasterCryptoFarmBot_Dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__ + "/../../"))
)
sys.path.append(MasterCryptoFarmBot_Dir)


class FarmBot:
    def __init__(
        self,
        log,
        bot_globals,
        account_name,
        web_app_query,
        proxy=None,
        user_agent=None,
        isPyrogram=False,
        tgAccount=None,
    ):
        self.log = log
        self.bot_globals = bot_globals
        self.account_name = account_name
        self.web_app_query = web_app_query
        self.proxy = proxy
        self.user_agent = user_agent
        self.isPyrogram = isPyrogram
        self.tgAccount = tgAccount

    async def run(self):
        try:
            self.log.info(
                f"<cyan>{self.account_name}</cyan><g> | 🤖 Start farming Hrum ...</g>"
            )

            self.http = HttpRequest(
                log=self.log,
                proxy=self.proxy,
                user_agent=self.user_agent,
                tgWebData=self.web_app_query,
                account_name=self.account_name,
            )

            api_key = None
            try:
                api_key = self.web_app_query.split("&hash=", maxsplit=1)[1]
            except Exception as e:
                self.log.error(
                    f"<r>⭕ <c>{self.account_name}</c> failed to farm! (Invalid TgWebQuery)</r>"
                )
                self.log.error(f"<r>{str(e)}</r>")
                return

            if api_key is None or api_key == "":
                self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to farm!</r>")
                return

            self.http.authToken = api_key

            auth = Auth(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
                web_app_query=self.web_app_query,
            )

            auth_response = auth.auth()
            if auth_response is None:
                add_account_to_display_data(
                    "display_data_bot_issues.json", self.account_name
                )
                return

            if "success" not in auth_response and auth_response["success"] is not True:
                self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to farm!</r>")
                return

            user = User(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
            )

            self.log.info(
                f"<g>🔍 <c>{self.account_name}</c> retrieving user data...</g>"
            )
            user_all_data = user.data_all()

            if user_all_data is None:
                return

            profile = user_all_data.get("data", {}).get("profile", {})
            friends = profile.get("friends", 0)
            registration_date = profile.get("registrationDate", "")
            hero_data = user_all_data.get("data", {}).get("hero", {})
            token = hero_data.get("token", 0)
            cookies = hero_data.get("cookies", 0)

            self.log.info(f"<g>👤 <c>{self.account_name}</c> Info:</g>")
            self.log.info(f"<g>👥 Friends: <c>{friends}</c></g>")
            self.log.info(f"<g>📅 Registration Date: <c>{registration_date}</c></g>")
            self.log.info(f"<g>💰 Tokens: <c>{token}🥠</c></g>")

            user_after_data = user.after()
            if user_after_data is None:
                return

            self.log.info(
                f"<g>❔ <c>{self.account_name}</c> retrieving daily quests...</g>"
            )

            license_key = self.bot_globals.get("license", None)
            quests = Quests(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
                license_key=license_key,
                tgAccount=self.tgAccount,
            )

            daily_quests = quests.daily()
            if daily_quests is None:
                return

            onboarding = hero_data.get("onboarding", [])
            history = user_all_data.get("data", {}).get("history", [])

            hero = Hero(
                log=self.log,
                httpRequest=self.http,
                account_name=self.account_name,
            )

            if len(onboarding) == 0 or len(history) == 0:
                self.log.info(f"<g>🎉 <c>{self.account_name}</c> New account!</g>")
                time.sleep(random.randint(4, 6))
                hero.onboarding_finish()

            if getConfig("auto_prediction", True):
                if cookies > 0:
                    self.log.info(f"<g>🔮 <c>{self.account_name}</c> predicting...</g>")
                    time.sleep(random.randint(2, 5))
                    user.cookie_open()
                else:
                    self.log.info(
                        f"<g>🔮 <c>{self.account_name}</c> predicting is not ready!</g>"
                    )

            if getConfig("claim_daily_reward", True):
                quests.check_daily_reward(daily_quests)

            if getConfig("claim_riddle", True):
                self.log.info(
                    f"<g>🔍 <c>{self.account_name}</c> checking riddle...</g>"
                )
                quests_list = (
                    user_all_data.get("data", {}).get("dbData", []).get("dbQuests", [])
                )
                user_quests = user_after_data.get("data", {}).get("quests", [])
                quests.check_riddle(quests_list, user_quests)

            if getConfig("auto_finish_tasks", True):
                self.log.info(f"<g>🔍 <c>{self.account_name}</c> checking tasks...</g>")
                quests_list = (
                    user_all_data.get("data", {}).get("dbData", []).get("dbQuests", [])
                )
                user_quests = user_after_data.get("data", {}).get("quests", [])
                await quests.check_tasks(quests_list, user_quests)

            self.log.info(
                f"<g>🎉 <c>{self.account_name}</c> finished farming Hrum!</g>"
            )

            add_account_to_display_data(
                "display_data_success_accounts.json",
                self.account_name,
                "Cookies: " + str(cookies),
                token,
            )
        except Exception as e:
            add_account_to_display_data(
                "display_data_bot_issues.json", self.account_name
            )
            self.log.error(f"<r>⭕ <c>{self.account_name}</c> failed to farm!</r>")
            self.log.error(f"<r>{str(e)}</r>")
            return
        finally:
            delay_between_accounts = getConfig("delay_between_accounts", 60)
            random_sleep = random.randint(0, 20) + delay_between_accounts
            self.log.info(
                f"<g>⌛ Farming for <c>{self.account_name}</c> completed. Waiting for <c>{random_sleep}</c> seconds before running the next account...</g>"
            )
            time.sleep(random_sleep)
