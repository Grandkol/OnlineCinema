import uuid

SEARCH_FILM_DATA = [{
        'id': str(uuid.uuid4()),
        "title": "The Star Maker",
        "imdb_rating": 7.4,
        "description": "\"Dottore\" Joe Moretti travels round Sicily doing screen tests for the big Roman studios. "
                       "He's a conman and takes money or favours for his efforts. Beata, a young illiterate convent "
                       "girl desperately wants to change her life and falls for him, belatedly he realises his feelings "
                       "for her. Their love affair is doomed when he's arrested.",
        "genres": [
            {
                "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                "name": "Romance"
            },
            {
                "id": "1cacff68-643e-4ddd-8f57-84b62538081a",
                "name": "Drama"
            }
        ],
        "actors": [
            {
                "id": "a88f14e6-a8e2-4e05-9744-e89fadf960fb",
                "name": "Franco Scaldati"
            },
            {
                "id": "6d5964ff-e56e-40aa-9e30-6a52ed741e55",
                "name": "Leopoldo Trieste"
            },
            {
                "id": "e1d02f5f-bd47-4eb4-a9c3-1f353ffa9e54",
                "name": "Sergio Castellitto"
            },
            {
                "id": "f142081a-8054-4ec3-ae97-026f8ebdef3e",
                "name": "Tiziana Lodato"
            }
        ],
        "writers": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            },
            {
                "id": "c740cb33-df3a-4aeb-b3ad-7e79581d857c",
                "name": "Fabio Rinaudo"
            }
        ],
        "directors": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            }
        ]
    } for _ in range(60)]

FILM_DATA = [{
        'id': '1acfccf3-c5f5-4b98-9456-24e3d553a604',
        "title": "The Star Maker",
        "imdb_rating": 7.4,
        "description": "\"Dottore\" Joe Moretti travels round Sicily doing screen tests for the big Roman studios. "
                       "He's a conman and takes money or favours for his efforts. Beata, a young illiterate convent "
                       "girl desperately wants to change her life and falls for him, belatedly he realises his feelings "
                       "for her. Their love affair is doomed when he's arrested.",
        "genres": [
            {
                "id": "237fd1e4-c98e-454e-aa13-8a13fb7547b5",
                "name": "Romance"
            },
            {
                "id": "1cacff68-643e-4ddd-8f57-84b62538081a",
                "name": "Drama"
            }
        ],
        "actors": [
            {
                "id": "a88f14e6-a8e2-4e05-9744-e89fadf960fb",
                "name": "Franco Scaldati"
            },
            {
                "id": "6d5964ff-e56e-40aa-9e30-6a52ed741e55",
                "name": "Leopoldo Trieste"
            },
            {
                "id": "e1d02f5f-bd47-4eb4-a9c3-1f353ffa9e54",
                "name": "Sergio Castellitto"
            },
            {
                "id": "f142081a-8054-4ec3-ae97-026f8ebdef3e",
                "name": "Tiziana Lodato"
            }
        ],
        "writers": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            },
            {
                "id": "c740cb33-df3a-4aeb-b3ad-7e79581d857c",
                "name": "Fabio Rinaudo"
            }
        ],
        "directors": [
            {
                "id": "55dc3cfa-0731-42fe-9d7b-6180b00ab712",
                "name": "Giuseppe Tornatore"
            }
        ]
    } for _ in range(3)]