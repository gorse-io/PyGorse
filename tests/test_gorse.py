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
from datetime import datetime

import redis

from gorse import Gorse, GorseException

GORSE_ENDPOINT = 'http://127.0.0.1:8088'
GORSE_API_KEY = 'zhenghaoz'


def test_users():
    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    # Insert a user.
    r = client.insert_user({'UserId': '100', 'Labels': ['a', 'b', 'c'], 'Subscribe': ['d', 'e'], 'Comment': 'comment'})
    assert r['RowAffected'] == 1
    # Get this user.
    user = client.get_user('100')
    assert user == {'UserId': '100', 'Labels': ['a', 'b', 'c'], 'Subscribe': ['d', 'e'], 'Comment': 'comment'}
    # Delete this user.
    r = client.delete_user('100')
    assert r['RowAffected'] == 1
    try:
        client.get_user('100')
        assert False
    except GorseException as e:
        assert e.status_code == 404


def test_items():
    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    items = [
        {'ItemId': '100', 'IsHidden': True, 'Labels': ['a', 'b', 'c'], 'Categories': ['d', 'e'], 'Timestamp': timestamp,
         'Comment': 'comment'},
        {'ItemId': '200', 'IsHidden': True, 'Labels': ['b', 'c', 'd'], 'Categories': ['d', 'a'], 'Timestamp': timestamp,
         'Comment': 'comment'},
        {'ItemId': '300', 'IsHidden': True, 'Labels': ['c', 'd', 'e'], 'Categories': ['d', 'j'], 'Timestamp': timestamp,
         'Comment': 'comment'},
        {'ItemId': '400', 'IsHidden': True, 'Labels': ['d', 'e', 'f'], 'Categories': ['d', 'm'], 'Timestamp': timestamp,
         'Comment': 'comment'},
        {'ItemId': '500', 'IsHidden': True, 'Labels': ['e', 'f', 'g'], 'Categories': ['d', 't'], 'Timestamp': timestamp,
         'Comment': 'comment'}
    ]
    # Insert items.
    for item in items:
        r = client.insert_item(item)
        assert r['RowAffected'] == 1
    # Get an item.
    item = client.get_item('100')
    assert item == items[0]
    # Get items
    return_items = []
    part, cursor = client.get_items(3)
    assert len(part) == 3
    assert len(cursor) > 0
    return_items.extend(part)
    part, cursor = client.get_items(3, cursor)
    assert len(part) == 2
    assert len(cursor) == 0
    return_items.extend(part)
    assert return_items == items
    # Update item
    r = client.update_item('100', labels=['x', 'y', 'z'])
    assert r['RowAffected'] == 1
    item = client.get_item('100')
    assert item == {'ItemId': '100', 'IsHidden': True, 'Labels': ['x', 'y', 'z'], 'Categories': ['d', 'e'],
                    'Timestamp': timestamp,
                    'Comment': 'comment'}
    # Delete this item.
    r = client.delete_item('100')
    assert r['RowAffected'] == 1
    try:
        client.get_item('100')
        assert False
    except GorseException as e:
        assert e.status_code == 404


def test_feedback():
    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    timestamp = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Insert a feedback
    r = client.insert_feedback('like', '100', '100', timestamp)
    assert r['RowAffected'] == 1
    # Insert feedbacks
    r = client.insert_feedbacks([
        {'FeedbackType': 'read', 'UserId': '100', 'ItemId': '200', 'Timestamp': timestamp},
        {'FeedbackType': 'read', 'UserId': '100', 'ItemId': '300', 'Timestamp': timestamp}
    ])
    assert r['RowAffected'] == 2
    # List feedbacks
    feedbacks = client.list_feedbacks('read', '100')
    assert feedbacks == [
        {'FeedbackType': 'read', 'UserId': '100', 'ItemId': '200', 'Timestamp': timestamp, 'Comment': ''},
        {'FeedbackType': 'read', 'UserId': '100', 'ItemId': '300', 'Timestamp': timestamp, 'Comment': ''}
    ]


def test_recommend():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.zadd('offline_recommend/100', {'1': 1, '2': 2, '3': 3})

    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    recommend = client.get_recommend('100')
    assert recommend == ['3', '2', '1']


def test_neighbors():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.zadd('item_neighbors/100', {'1': 1, '2': 2, '3': 3})

    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    items = client.get_neighbors('100')
    assert items == [{'Id': '3', 'Score': 3}, {'Id': '2', 'Score': 2}, {'Id': '1', 'Score': 1}]


def test_session_recommend():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.zadd('item_neighbors/1', {"2": 100000, "9": 1})
    r.zadd('item_neighbors/2', {"3": 100000, "8": 1, "9": 1})
    r.zadd('item_neighbors/3', {"4": 100000, "7": 1, "8": 1, "9": 1})
    r.zadd('item_neighbors/4', {"1": 100000, "6": 1, "7": 1, "8": 1, "9": 1})

    client = Gorse(GORSE_ENDPOINT, GORSE_API_KEY)
    recommend = client.session_recommend([
        {"FeedbackType": "like", "UserId": "0", "ItemId": "1",
         "Timestamp": datetime(2010, 1, 1, 1, 1, 1, 1).isoformat()},
        {"FeedbackType": "like", "UserId": "0", "ItemId": "2",
         "Timestamp": datetime(2009, 1, 1, 1, 1, 1, 1).isoformat()},
        {"FeedbackType": "like", "UserId": "0", "ItemId": "3",
         "Timestamp": datetime(2008, 1, 1, 1, 1, 1, 1).isoformat()},
        {"FeedbackType": "like", "UserId": "0", "ItemId": "4",
         "Timestamp": datetime(2007, 1, 1, 1, 1, 1, 1).isoformat()},
    ], 3)
    assert recommend == [{'Id': "9", 'Score': 4}, {'Id': "8", 'Score': 3}, {'Id': "7", 'Score': 2}]
