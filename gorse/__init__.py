# Copyright 2022 gorse Project Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List, Tuple

import aiohttp
import requests


class GorseException(Exception):
    """
    Gorse exception.
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message


class Gorse:
    """
    Gorse client.
    """

    def __init__(self, entry_point: str, api_key: str, timeout=None):
        self.entry_point = entry_point
        self.api_key = api_key
        self.timeout = timeout

    def insert_feedback(
            self, feedback_type: str, user_id: str, item_id: str, timestamp: str
    ) -> dict:
        """
        Insert a feedback.
        """
        return self.__request(
            "POST",
            f"{self.entry_point}/api/feedback",
            json=[
                {
                    "FeedbackType": feedback_type,
                    "UserId": user_id,
                    "ItemId": item_id,
                    "Timestamp": timestamp,
                }
            ],
        )

    def list_feedbacks(self, feedback_type: str, user_id: str):
        """
        List feedbacks from a user.
        """
        return self.__request("GET", f"{self.entry_point}/api/user/{user_id}/feedback/{feedback_type}")

    def get_recommend(self, user_id: str, category: str = "", n: int = 10, offset: int = 0, write_back_type: str = None,
                      write_back_delay: str = None) -> List[str]:
        """
        Get recommendation.
        """
        payload = {"n": n, "offset": offset}
        if write_back_type:
            payload["write-back-type"] = write_back_type
        if write_back_delay:
            payload["write-back-delay"] = write_back_delay
        return self.__request("GET", f"{self.entry_point}/api/recommend/{user_id}/{category}", params=payload)

    def session_recommend(self, feedbacks: list, n: int = 10) -> list:
        """
        Get session recommendation.
        """
        return self.__request("POST", f"{self.entry_point}/api/session/recommend?n={n}", json=feedbacks)

    def get_neighbors(self, item_id: str, n: int = 10, offset: int = 0) -> List[str]:
        """
        Get item neighbors.
        """
        return self.__request("GET", f"{self.entry_point}/api/item/{item_id}/neighbors?n={n}&offset={offset}")

    def insert_feedbacks(self, feedbacks: list) -> dict:
        """
        Insert feedbacks.
        """
        return self.__request("POST", f"{self.entry_point}/api/feedback", json=feedbacks)

    def insert_item(self, item) -> dict:
        """
        Insert an item.
        """
        return self.__request("POST", f"{self.entry_point}/api/item", json=item)

    def get_item(self, item_id: str) -> dict:
        """
        Get an item.
        """
        return self.__request("GET", f"{self.entry_point}/api/item/{item_id}")

    def get_items(self, n: int, cursor: str = '') -> Tuple[List[dict], str]:
        """
        Get items.
        :param n: number of returned items
        :param cursor: cursor for next page
        :return: items and cursor for next page
        """
        response = self.__request(
            "GET", f"{self.entry_point}/api/items", params={'n': n, 'cursor': cursor})
        return response['Items'], response['Cursor']

    def update_item(self, item_id: str, is_hidden: bool = None, categories: List[str] = None, labels: List[str] = None,
                    timestamp: str = None,
                    comment: str = None) -> dict:
        """
        Update an item.
        """
        return self.__request("PATCH", f'{self.entry_point}/api/item/{item_id}', json={
            "Categories": categories,
            "Comment": comment,
            "IsHidden": is_hidden,
            "Labels": labels,
            "Timestamp": timestamp
        })

    def delete_item(self, item_id: str) -> dict:
        """
        Delete an item.
        """
        return self.__request("DELETE", f"{self.entry_point}/api/item/{item_id}")

    def insert_user(self, user) -> dict:
        """
        Insert a user.
        """
        return self.__request("POST", f"{self.entry_point}/api/user", json=user)

    def get_user(self, user_id: str) -> dict:
        """
        Get a user.
        """
        return self.__request("GET", f"{self.entry_point}/api/user/{user_id}")

    def delete_user(self, user_id: str) -> dict:
        """
        Delete a user.
        """
        return self.__request("DELETE", f"{self.entry_point}/api/user/{user_id}")

    def __request(self, method: str, url: str, params=None, json=None) -> dict:
        response = requests.request(
            method, url,
            params=params,
            headers={"X-API-Key": self.api_key},
            timeout=self.timeout,
            json=json
        )
        if response.status_code == 200:
            return response.json()
        raise GorseException(response.status_code, response.text)


class AsyncGorse:
    """
    Gorse async client.
    """

    def __init__(self, entry_point: str, api_key: str, timeout=None):
        self.entry_point = entry_point
        self.api_key = api_key
        self.timeout = timeout

    async def insert_feedback(
            self, feedback_type: str, user_id: str, item_id: str, timestamp: str
    ) -> dict:
        """
        Insert a feedback.
        """
        return await self.__request(
            "POST",
            f"{self.entry_point}/api/feedback",
            json=[
                {
                    "FeedbackType": feedback_type,
                    "UserId": user_id,
                    "ItemId": item_id,
                    "Timestamp": timestamp,
                }
            ],
        )

    async def list_feedbacks(self, feedback_type: str, user_id: str):
        """
        List feedbacks from a user.
        """
        return await self.__request("GET", f"{self.entry_point}/api/user/{user_id}/feedback/{feedback_type}")

    async def get_recommend(self, user_id: str, category: str = "", n: int = 10, offset: int = 0, write_back_type: str = None,
                      write_back_delay: str = None) -> List[str]:
        """
        Get recommendation.
        """
        payload = {"n": n, "offset": offset}
        if write_back_type:
            payload["write-back-type"] = write_back_type
        if write_back_delay:
            payload["write-back-delay"] = write_back_delay
        return await self.__request("GET", f"{self.entry_point}/api/recommend/{user_id}/{category}", params=payload)

    async def session_recommend(self, feedbacks: list, n: int = 10) -> list:
        """
        Get session recommendation.
        """
        return await self.__request("POST", f"{self.entry_point}/api/session/recommend?n={n}", json=feedbacks)

    async def get_neighbors(self, item_id: str, n: int = 10, offset: int = 0) -> List[str]:
        """
        Get item neighbors.
        """
        return await self.__request("GET", f"{self.entry_point}/api/item/{item_id}/neighbors?n={n}&offset={offset}")

    async def insert_feedbacks(self, feedbacks: list) -> dict:
        """
        Insert feedbacks.
        """
        return await self.__request("POST", f"{self.entry_point}/api/feedback", json=feedbacks)

    async def insert_item(self, item) -> dict:
        """
        Insert an item.
        """
        return await self.__request("POST", f"{self.entry_point}/api/item", json=item)

    async def get_item(self, item_id: str) -> dict:
        """
        Get an item.
        """
        return await self.__request("GET", f"{self.entry_point}/api/item/{item_id}")

    async def get_items(self, n: int, cursor: str = '') -> Tuple[List[dict], str]:
        """
        Get items.
        :param n: number of returned items
        :param cursor: cursor for next page
        :return: items and cursor for next page
        """
        response = await self.__request(
            "GET", f"{self.entry_point}/api/items", params={'n': n, 'cursor': cursor})
        return response['Items'], response['Cursor']

    async def update_item(self, item_id: str, is_hidden: bool = None, categories: List[str] = None, labels: List[str] = None,
                    timestamp: str = None,
                    comment: str = None) -> dict:
        """
        Update an item.
        """
        return await self.__request("PATCH", f'{self.entry_point}/api/item/{item_id}', json={
            "Categories": categories,
            "Comment": comment,
            "IsHidden": is_hidden,
            "Labels": labels,
            "Timestamp": timestamp
        })

    async def delete_item(self, item_id: str) -> dict:
        """
        Delete an item.
        """
        return await self.__request("DELETE", f"{self.entry_point}/api/item/{item_id}")

    async def insert_user(self, user) -> dict:
        """
        Insert a user.
        """
        return await self.__request("POST", f"{self.entry_point}/api/user", json=user)

    async def get_user(self, user_id: str) -> dict:
        """
        Get a user.
        """
        return await self.__request("GET", f"{self.entry_point}/api/user/{user_id}")

    async def delete_user(self, user_id: str) -> dict:
        """
        Delete a user.
        """
        return await self.__request("DELETE", f"{self.entry_point}/api/user/{user_id}")

    async def __request(self, method: str, url: str, params=None, json=None) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, params=params, json=json, headers={"X-API-Key": self.api_key}) as response:
                if response.status == 200:
                    return await response.json()
                raise GorseException(response.status, await response.text())
