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
from datetime import datetime, UTC
import unittest

from gorse import Gorse, GorseException, AsyncGorse

GORSE_ENDPOINT = 'http://127.0.0.1:8088'
GORSE_API_KEY = 'zhenghaoz'


class TestGorseClient(unittest.TestCase):

    def test_users(self):
        client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)

        users, cursor = client.get_users(3)
        self.assertGreater(len(cursor), 0)
        self.assertEqual([
            {
                'UserId': '1',
                'Labels': {
                    'age': 24,
                    'gender': 'M',
                    'occupation': 'technician',
                    'zip_code': '85711'
                },
                'Comment': ''
            },
            {
                'UserId': '10',
                'Labels': {
                    'age': 53,
                    'gender': 'M',
                    'occupation': 'lawyer',
                    'zip_code': '90703'
                },
                'Comment': ''
            },
            {
                'UserId': '100',
                'Labels': {
                    'age': 36,
                    'gender': 'M',
                    'occupation': 'executive',
                    'zip_code': '90254'
                },
                'Comment': ''
            }
        ], users)

        user = {
            'UserId': '1000',
            'Labels': {
                'gender': 'M',
                'occupation': 'engineer'
            },
            'Comment': 'zhenghaoz'
        }
        r = client.insert_user(user)
        self.assertEqual(r['RowAffected'], 1)
        resp = client.get_user('1000')
        self.assertEqual(user, resp)

        r = client.delete_user('1000')
        self.assertEqual(r['RowAffected'], 1)
        try:
            client.get_user('1000')
            self.fail()
        except GorseException as e:
            self.assertEqual(e.status_code, 404)

    def test_items(self):
        client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
        items, cursor = client.get_items(3)
        self.assertGreater(len(cursor), 0)
        self.assertEqual('1', items[0]['ItemId'])
        self.assertEqual(['Animation', "Children's", 'Comedy'],
                         items[0]['Categories'])
        self.assertEqual('1995-01-01T00:00:00Z', items[0]['Timestamp'])
        self.assertEqual('Toy Story (1995)', items[0]['Comment'])
        self.assertEqual('10', items[1]['ItemId'])
        self.assertEqual(['Drama', 'War'], items[1]['Categories'])
        self.assertEqual('1996-01-22T00:00:00Z', items[1]['Timestamp'])
        self.assertEqual('Richard III (1995)', items[1]['Comment'])
        self.assertEqual('100', items[2]['ItemId'])
        self.assertEqual(['Crime', 'Drama', 'Thriller'],
                         items[2]['Categories'])
        self.assertEqual('1997-02-14T00:00:00Z', items[2]['Timestamp'])
        self.assertEqual('Fargo (1996)', items[2]['Comment'])

        item = {
            'ItemId': '2000',
            'IsHidden': True,
            'Labels': {
                'embedding': [0.1, 0.2, 0.3]
            },
            'Categories': ['Comedy', 'Animation'],
            'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'Comment': 'Minions (2015)'
        }
        r = client.insert_item(item)
        self.assertEqual(r['RowAffected'], 1)
        resp = client.get_item('2000')
        self.assertEqual(item, resp)

        r = client.update_item('2000', comment='小黄人 (2015)')
        self.assertEqual(r['RowAffected'], 1)
        resp = client.get_item('2000')
        self.assertEqual('小黄人 (2015)', resp['Comment'])

        r = client.delete_item('2000')
        self.assertEqual(r['RowAffected'], 1)
        try:
            client.get_item('2000')
            self.fail()
        except GorseException as e:
            self.assertEqual(e.status_code, 404)

    def test_feedback(self):
        client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
        client.insert_user({'UserId': '2000'})

        feedbacks = [
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '1',
                'Value': 1.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            },
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '1060',
                'Value': 2.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            },
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '11',
                'Value': 3.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            }
        ]
        for fb in feedbacks:
            client.delete_feedback(fb['UserId'], fb['ItemId'])
        r = client.insert_feedbacks(feedbacks)
        self.assertEqual(r['RowAffected'], 3)

        user_feedback = client.list_feedbacks('watch', '2000')
        self.assertEqual(feedbacks, user_feedback)

        r = client.delete_feedback('2000', '1')
        self.assertEqual(r['RowAffected'], 1)
        user_feedback = client.list_feedbacks('watch', '2000')
        self.assertEqual([feedbacks[1], feedbacks[2]], user_feedback)

    def test_item_to_item(self):
        client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
        neighbors = client.get_neighbors('1', 3)
        self.assertEqual('1060', neighbors[0]['Id'])
        self.assertEqual('404', neighbors[1]['Id'])
        self.assertEqual('1219', neighbors[2]['Id'])

    def test_recommend(self):
        client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
        client.insert_user({'UserId': '3000'})
        recommendations = client.get_recommend('3000', n=3)
        self.assertEqual(3, len(recommendations))
        self.assertEqual('315', recommendations[0])
        self.assertEqual('1432', recommendations[1])
        self.assertEqual('918', recommendations[2])


class TestAsyncGorseClient(unittest.IsolatedAsyncioTestCase):

    async def test_users(self):
        client = AsyncGorse(GORSE_ENDPOINT, GORSE_API_KEY)
        users, cursor = await client.get_users(3)
        self.assertGreater(len(cursor), 0)
        self.assertEqual([
            {
                'UserId': '1',
                'Labels': {
                    'age': 24,
                    'gender': 'M',
                    'occupation': 'technician',
                    'zip_code': '85711'
                },
                'Comment': ''
            },
            {
                'UserId': '10',
                'Labels': {
                    'age': 53,
                    'gender': 'M',
                    'occupation': 'lawyer',
                    'zip_code': '90703'
                },
                'Comment': ''
            },
            {
                'UserId': '100',
                'Labels': {
                    'age': 36,
                    'gender': 'M',
                    'occupation': 'executive',
                    'zip_code': '90254'
                },
                'Comment': ''
            }
        ], users)
        user = {
            'UserId': '1000',
            'Labels': {
                'gender': 'M',
                'occupation': 'engineer'
            },
            'Comment': 'zhenghaoz'
        }
        r = await client.insert_user(user)
        self.assertEqual(r['RowAffected'], 1)
        resp = await client.get_user('1000')
        self.assertEqual(user, resp)
        r = await client.delete_user('1000')
        self.assertEqual(r['RowAffected'], 1)
        try:
            await client.get_user('1000')
            self.fail()
        except GorseException as e:
            self.assertEqual(e.status_code, 404)

    async def test_items(self):
        client = AsyncGorse(GORSE_ENDPOINT, GORSE_API_KEY)
        items, cursor = await client.get_items(3)
        self.assertGreater(len(cursor), 0)
        self.assertEqual('1', items[0]['ItemId'])
        self.assertEqual(['Animation', "Children's", 'Comedy'], items[0]['Categories'])
        self.assertEqual('1995-01-01T00:00:00Z', items[0]['Timestamp'])
        self.assertEqual('Toy Story (1995)', items[0]['Comment'])
        self.assertEqual('10', items[1]['ItemId'])
        self.assertEqual(['Drama', 'War'], items[1]['Categories'])
        self.assertEqual('1996-01-22T00:00:00Z', items[1]['Timestamp'])
        self.assertEqual('Richard III (1995)', items[1]['Comment'])
        self.assertEqual('100', items[2]['ItemId'])
        self.assertEqual(['Crime', 'Drama', 'Thriller'], items[2]['Categories'])
        self.assertEqual('1997-02-14T00:00:00Z', items[2]['Timestamp'])
        self.assertEqual('Fargo (1996)', items[2]['Comment'])
        item = {
            'ItemId': '2000',
            'IsHidden': True,
            'Labels': {'embedding': [0.1, 0.2, 0.3]},
            'Categories': ['Comedy', 'Animation'],
            'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'Comment': 'Minions (2015)'
        }
        r = await client.insert_item(item)
        self.assertEqual(r['RowAffected'], 1)
        resp = await client.get_item('2000')
        self.assertEqual(item, resp)
        r = await client.update_item('2000', comment='小黄人 (2015)')
        self.assertEqual(r['RowAffected'], 1)
        resp = await client.get_item('2000')
        self.assertEqual('小黄人 (2015)', resp['Comment'])
        r = await client.delete_item('2000')
        self.assertEqual(r['RowAffected'], 1)
        try:
            await client.get_item('2000')
            self.fail()
        except GorseException as e:
            self.assertEqual(e.status_code, 404)

    async def test_feedback(self):
        client = AsyncGorse(GORSE_ENDPOINT, GORSE_API_KEY)
        await client.insert_user({'UserId': '2000'})
        feedbacks = [
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '1',
                'Value': 1.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            },
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '1060',
                'Value': 2.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            },
            {
                'FeedbackType': 'watch',
                'UserId': '2000',
                'ItemId': '11',
                'Value': 3.0,
                'Timestamp': datetime.now(UTC).strftime('%Y-%m-%dT%H:%M:%SZ'),
                'Comment': ''
            }
        ]
        for fb in feedbacks:
            await client.delete_feedback(fb['UserId'], fb['ItemId'])
        r = await client.insert_feedbacks(feedbacks)
        self.assertEqual(r['RowAffected'], 3)
        user_feedback = await client.list_feedbacks('watch', '2000')
        self.assertEqual(feedbacks, user_feedback)
        r = await client.delete_feedback('2000', '1')
        self.assertEqual(r['RowAffected'], 1)
        user_feedback = await client.list_feedbacks('watch', '2000')
        self.assertEqual([feedbacks[1], feedbacks[2]], user_feedback)

    async def test_item_to_item(self):
        client = AsyncGorse(GORSE_ENDPOINT, GORSE_API_KEY)
        neighbors = await client.get_neighbors('1', 3)
        self.assertEqual('1060', neighbors[0]['Id'])
        self.assertEqual('404', neighbors[1]['Id'])
        self.assertEqual('1219', neighbors[2]['Id'])

    async def test_recommend(self):
        client = AsyncGorse(GORSE_ENDPOINT, GORSE_API_KEY)
        await client.insert_user({'UserId': '3000'})
        recommendations = await client.get_recommend('3000', n=3)
        self.assertEqual(3, len(recommendations))
        self.assertEqual('315', recommendations[0])
        self.assertEqual('1432', recommendations[1])
        self.assertEqual('918', recommendations[2])

