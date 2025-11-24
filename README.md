# PyGorse

[![CI](https://github.com/gorse-io/PyGorse/actions/workflows/ci.yml/badge.svg)](https://github.com/gorse-io/PyGorse/actions/workflows/ci.yml)
[![](https://img.shields.io/pypi/v/pygorse)](https://pypi.org/project/PyGorse/)
![](https://img.shields.io/pypi/dm/pygorse)

Python SDK for gorse recommender system.

## Install

- Install from PyPI:

```bash
pip install PyGorse
```

- Install from source:

```bash
git clone https://github.com/gorse-io/PyGorse.git
cd PyGorse
pip install .
```

## Usage

Create a client by the entrypoint and api key.

```python
from gorse import Gorse

client = Gorse('http://127.0.0.1:8087', 'api_key')

# Insert a user
client.insert_user({
    'UserId': 'bob',
    'Labels': {
        'gender': 'M',
        'age': 24
    },
    'Comment': 'my user'
})

# Insert items
client.insert_item({
    'ItemId': 'vuejs:vue',
    'IsHidden': False,
    'Labels': {
        'language': 'JavaScript'
    },
    'Categories': ['framework'],
    'Timestamp': '2022-02-24T00:00:00Z',
    'Comment': 'Vue.js framework'
})

# Insert feedbacks
client.insert_feedbacks([
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'vuejs:vue', 'Timestamp': '2022-02-24T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'd3:d3', 'Timestamp': '2022-02-25T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'dogfalo:materialize', 'Timestamp': '2022-02-26T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'mozilla:pdf.js', 'Timestamp': '2022-02-27T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'moment:moment', 'Timestamp': '2022-02-28T00:00:00Z' }
])

# Get recommendation
client.get_recommend('bob', n=10)
```

The Python SDK implements the async client as well:

```python
from gorse import AsyncGorse

client = AsyncGorse('http://127.0.0.1:8087', 'api_key')

# Insert a user
await client.insert_user({
    'UserId': 'bob',
    'Labels': {
        'gender': 'M',
        'age': 24
    },
    'Comment': 'my user'
})

# Insert items
await client.insert_item({
    'ItemId': 'vuejs:vue',
    'IsHidden': False,
    'Labels': {
        'language': 'JavaScript'
    },
    'Categories': ['framework'],
    'Timestamp': '2022-02-24T00:00:00Z',
    'Comment': 'Vue.js framework'
})

# Insert feedbacks
await client.insert_feedbacks([
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'vuejs:vue', 'Timestamp': '2022-02-24T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'd3:d3', 'Timestamp': '2022-02-25T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'dogfalo:materialize', 'Timestamp': '2022-02-26T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'mozilla:pdf.js', 'Timestamp': '2022-02-27T00:00:00Z' },
    { 'FeedbackType': 'star', 'UserId': 'bob', 'ItemId': 'moment:moment', 'Timestamp': '2022-02-28T00:00:00Z' }
])

# Get recommendation
await client.get_recommend('bob', n=10)
```
