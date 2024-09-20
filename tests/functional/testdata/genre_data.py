import uuid

GENRE_DATA = [
    {"id": str(uuid.uuid4()), "name": "Biography", "description": "hello", "movies": []}
    for _ in range(10)
]
