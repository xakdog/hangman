Hangman game
============

Web version of Hangman. Based on Django and Riot.js.

Local development
-----------------

Create virtual env and install dependencies.

```bash
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

Run server

```bash
python manage.py runserver
```

Run tests

```bash
python manage.py test
```

Architectural questions
-----------------------

[Principles and tasks](TASKS.md)

### Why Riot.js

The first version of front-end was vanilla.
But to bring more order and make support easier I decided
to use library instead of manipulating DOM manually.

1. Compiler + riot is tiny (14KB)
2. It uses component approach
3. It's simple and minimalistic

### Why Fetch API

1. It's reduce code amount and easier to support
2. Supported by 87.25% users natively
3. You can easily extend browser support by using polyfill 

### Why I use flexboxes

1. It's an MVP and our goal is to ship product ASAP
2. They actually well-supported (94.42% browsers)
3. Flex-boxes can help us fit into small smartphones screens

### RESTful API vs WebSockets

Our game mostly use single requests. These requests are one directional.
WebSockets are 29% faster on single requests. But main source of delay
is actual RTT to client. With RESTful API it's easier to recover from errors
due to idempotency of requests. And it's faster to implement and make changes
to a RESTful API if we use Django.

https://blog.feathersjs.com/http-vs-websockets-a-performance-comparison-da2533f13a77
