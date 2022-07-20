from typing import List

import requests


class GorseException(BaseException):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class Gorse:
    def __init__(self, entry_point: str, api_key: str):
        self.entry_point = entry_point
        self.api_key = api_key

    def insert_feedback(
            self, feedback_type: str, user_id: str, item_id: str, timestamp: str
    ) -> dict:
        r = requests.post(
            self.entry_point + "/api/feedback",
            headers={"X-API-Key": self.api_key},
            json=[
                {
                    "FeedbackType": feedback_type,
                    "UserId": user_id,
                    "ItemId": item_id,
                    "Timestamp": timestamp,
                }
            ],
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def list_feedbacks(self, feedback_type: str, user_id: str):
        r = requests.get(self.entry_point + "/api/user/" + user_id + "/feedback/" + feedback_type,
                         headers={"X-API-Key": self.api_key})
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def get_recommend(self, user_id: str, category: str = "", n: int = 10) -> List[str]:
        r = requests.get(
            self.entry_point + "/api/recommend/%s/%s?n=%d" % (user_id, category, n),
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def session_recommend(self, feedbacks: list, n: int = 10) -> list:
        r = requests.post(
            self.entry_point + "/api/session/recommend?n=%d" % n,
            headers={"X-API-Key": self.api_key},
            json=feedbacks,
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def get_neighbors(self, item_id: str, n: int = 3) -> List[str]:
        r = requests.get(
            self.entry_point + "/api/item/%s/neighbors?n=%d" % (item_id, n),
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def insert_feedbacks(self, feedbacks: list) -> dict:
        r = requests.post(
            self.entry_point + "/api/feedback",
            headers={"X-API-Key": self.api_key},
            json=feedbacks,
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def insert_item(self, item) -> dict:
        r = requests.post(
            self.entry_point + "/api/item",
            headers={"X-API-Key": self.api_key},
            json=item,
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def get_item(self, item_id: str) -> dict:
        r = requests.get(
            self.entry_point + "/api/item/%s" % item_id,
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def delete_item(self, item_id: str) -> dict:
        r = requests.delete(
            self.entry_point + "/api/item/%s" % item_id,
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def insert_user(self, user) -> dict:
        r = requests.post(
            self.entry_point + "/api/user",
            headers={"X-API-Key": self.api_key},
            json=user,
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def get_user(self, user_id: str) -> dict:
        r = requests.get(
            self.entry_point + "/api/user/%s" % user_id,
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)

    def delete_user(self, user_id: str) -> dict:
        r = requests.delete(
            self.entry_point + "/api/user/%s" % user_id,
            headers={"X-API-Key": self.api_key},
        )
        if r.status_code == 200:
            return r.json()
        raise GorseException(r.status_code, r.text)
