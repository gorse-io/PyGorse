from datetime import datetime

import redis
from gorse import Gorse, GorseException


def test_users():
    client = Gorse('http://127.0.0.1:8087', 'zhenghaoz')
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
    client = Gorse('http://127.0.0.1:8087', 'zhenghaoz')
    timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Insert an item.
    r = client.insert_item(
        {'ItemId': '100', 'IsHidden': True, 'Labels': ['a', 'b', 'c'], 'Categories': ['d', 'e'], 'Timestamp': timestamp,
         'Comment': 'comment'})
    assert r['RowAffected'] == 1
    # Get this user.
    user = client.get_item('100')
    assert user == {'ItemId': '100', 'IsHidden': True, 'Labels': ['a', 'b', 'c'], 'Categories': ['d', 'e'],
                    'Timestamp': timestamp,
                    'Comment': 'comment'}
    # Delete this user.
    r = client.delete_item('100')
    assert r['RowAffected'] == 1
    try:
        client.get_item('100')
        assert False
    except GorseException as e:
        assert e.status_code == 404


def test_feedback():
    client = Gorse('http://127.0.0.1:8087', 'zhenghaoz')
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

    client = Gorse('http://127.0.0.1:8087', 'zhenghaoz')
    recommend = client.get_recommend('100')
    assert recommend == ['3','2','1']


def test_neighbors():
    r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    r.zadd('item_neighbors/100', {'1': 1, '2': 2, '3': 3})

    client = Gorse('http://127.0.0.1:8087', 'zhenghaoz')
    items = client.get_neighbors('100')
    assert items == [{'Id': '3', 'Score': 3}, {'Id': '2', 'Score': 2}, {'Id': '1', 'Score': 1}]
