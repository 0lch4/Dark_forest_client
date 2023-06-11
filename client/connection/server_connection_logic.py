import requests
import json
from typing import Literal, Any
from pathlib import Path


# user have to be always log in if he want connecct to the server
class Connection:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        # everything is in self session for better security
        self.session = requests.session()
        # login flag is for inform user when he was not logged in
        self.logged_in = False

    def login(self) -> str:
        login_link = "https://darkforest.pythonanywhere.com/stats/login"
        self.data = {"username": self.username, "password": self.password}
        if self.username == "" or self.password == "":  # noqa: PLC1901
            return "Enter username and password in text area"
        # logining the user
        self.response = self.session.post(login_link, data=self.data)
        # csrf authorization
        csrftoken = self.response.cookies.get("csrftoken")
        self.session.headers.update({"X-CSRFToken": csrftoken})
        # return info to main app about logging status
        if self.response.status_code == 200 and self.response.url.endswith(
            "login_success"
        ):
            self.logged_in = True
            return "success"
        if self.response.status_code == 200:
            return "Bad username or password"
        return f"Error {self.response.status_code} please contact the administrator at https://github.com/0lch4"

    def register(self) -> str:
        register_link = "https://darkforest.pythonanywhere.com/stats/create_user"
        self.data = {"username": self.username, "password": self.password}
        if self.username == "" or self.password == "":  # noqa: PLC1901
            return "Enter username and password in text area"
        self.response = self.session.post(register_link, data=self.data)

        if self.response.status_code == 200 and self.response.url.endswith(
            "register_success"
        ):
            # when account was created sucessfully register method use login method
            # to login in new account else inform about isuesses
            self.login()
            return "success"
        if self.response.status_code == 200:
            return "User exists"
        return f"Error {self.response.status_code} please contact the administrator at https://github.com/0lch4"

    # send new player best score to server
    def update_best_score(self, username: str) -> str | None:
        if not self.logged_in:
            return "Not logged in"

        link = "https://darkforest.pythonanywhere.com/stats/modify_best_score"
        # score was reading from json file
        new_best_score = load_stats(username)
        self.data = {
            "username": self.username,
            "best_score": new_best_score["best_score"],
        }
        csrftoken = self.session.cookies.get("csrftoken")
        self.session.headers.update({"X-CSRFToken": csrftoken})
        self.session.headers.update(
            {"Referer": "https://darkforest.pythonanywhere.com"}
        )
        self.response = self.session.post(link, data=self.data)
        if self.response.status_code == 200:
            return None
        print(
            f"Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4"
        )
        return None

    # show global best scores
    def show_best_score(self) -> str:
        if not self.logged_in:
            return "Not logged in"

        link = "https://darkforest.pythonanywhere.com/stats/show_best_score"
        self.response = self.session.get(link)

        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            sorted_stats = sorted(
                self.stats, key=lambda x: x["fields"]["best_score"], reverse=True
            )
            output = ""
            for i in sorted_stats:
                output += f"{i['fields']['username']}: {i['fields']['best_score']}\n"
            return output
        return f"Error {self.response.status_code}, please contact the administrator at https://github.com/0lch4"

    # send new player statse to server
    def update_stats(self, username: str) -> str | None:
        if not self.logged_in:
            return "Not logged in"

        link = "https://darkforest.pythonanywhere.com/stats/modify_stats"
        # stats was reading from json file
        new_stats = load_stats(username)
        self.data = {
            "username": self.username,
            "all_levels": new_stats["all_levels"],
            "all_gold": new_stats["all_gold"],
            "enemies_killed": new_stats["enemies_killed"],
            "destroyed_obstacles": new_stats["destroyed_obstacles"],
            "bosses_killed": new_stats["bosses_killed"],
            "devils_killed": new_stats["devils_killed"],
            "fasts_killed": new_stats["fasts_killed"],
            "mutants_killed": new_stats["mutants_killed"],
            "ghosts_killed": new_stats["ghosts_killed"],
        }
        csrftoken = self.session.cookies.get("csrftoken")
        self.session.headers.update({"X-CSRFToken": csrftoken})
        self.session.headers.update(
            {"Referer": "https://darkforest.pythonanywhere.com"}
        )
        self.response = self.session.post(link, data=self.data)
        if self.response.status_code == 200:
            return None
        return f"Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4"

    # show global stats
    def show_stats(self) -> str:
        if not self.logged_in:
            return "Not logged in"

        link = "https://darkforest.pythonanywhere.com/stats/show_stats"
        self.response = self.session.get(link)
        if self.response.status_code == 200:
            self.stats = self.response.json()
            self.stats = json.loads(self.stats)
            output = ""
            # return data to main app
            for i in self.stats:
                output += (
                    f"Username: {i['fields']['username']}\n"
                    f"Levels Compleat: {i['fields']['all_levels']}\n"
                    f"Golds Earned: {i['fields']['all_gold']}\n"
                    f"Enemies Killed: {i['fields']['enemies_killed']}\n"
                    f"Destroyed Obstacles: {i['fields']['destroyed_obstacles']}\n"
                    f"Bosses Killed: {i['fields']['bosses_killed']}\n"
                    f"Devils Killed: {i['fields']['devils_killed']}\n"
                    f"Fasts Killed: {i['fields']['fasts_killed']}\n"
                    f"Mutants Killed: {i['fields']['mutants_killed']}\n"
                    f"Ghosts Killed: {i['fields']['ghosts_killed']}\n\n"
                )

            return output
        return f"Error {self.response.status_code} pleas contact to administrator https://github.com/0lch4"

    # load user data from server to local
    def load_data_to_local(self) -> Literal["Not logged in"] | None:
        if not self.logged_in:
            return "Not logged in"
        # links with user stats and best score
        score_link = "https://darkforest.pythonanywhere.com/stats/show_best_score"
        stats_link = "https://darkforest.pythonanywhere.com/stats/show_stats"
        self.response_score = self.session.get(score_link)
        self.response_stats = self.session.get(stats_link)

        data_stats = {}
        data_score = {}

        if self.response_stats.status_code == 200:
            self.stats = self.response_stats.json()
            self.stats = json.loads(self.stats)
            # import stats data from server
            for entry in self.stats:
                if entry["fields"]["username"] == self.username:
                    data_stats = {
                        "all_levels": entry["fields"]["all_levels"],
                        "all_gold": entry["fields"]["all_gold"],
                        "enemies_killed": entry["fields"]["enemies_killed"],
                        "destroyed_obstacles": entry["fields"]["destroyed_obstacles"],
                        "bosses_killed": entry["fields"]["bosses_killed"],
                        "devils_killed": entry["fields"]["devils_killed"],
                        "fasts_killed": entry["fields"]["fasts_killed"],
                        "mutants_killed": entry["fields"]["mutants_killed"],
                        "ghosts_killed": entry["fields"]["ghosts_killed"],
                    }
                    break
                # if user was created program use this
                data_stats = {
                    "all_levels": 0,
                    "all_gold": 0,
                    "enemies_killed": 0,
                    "destroyed_obstacles": 0,
                    "bosses_killed": 0,
                    "devils_killed": 0,
                    "fasts_killed": 0,
                    "mutants_killed": 0,
                    "ghosts_killed": 0,
                }
        # same to best score
        if self.response_score.status_code == 200:
            self.score = self.response_score.json()
            self.score = json.loads(self.score)
            for entry in self.score:
                if entry["fields"]["username"] == self.username:
                    data_score = {
                        "best_score": entry["fields"]["best_score"],
                    }
                    break
                data_score = {
                    "best_score": 0,
                }
        # join two dicts
        data_combined = {**data_score, **data_stats}
        file_path = Path(f"client/game/stats/{self.username}/stats.json")
        with file_path.open(mode="w") as f:
            json.dump(data_combined, f, indent=4)
            return None


# load data from json file
def load_stats(username: str) -> Any:
    file_path = Path(f"client/game/stats/{username}/stats.json")
    with file_path.open(mode="r") as f:
        return json.load(f)
