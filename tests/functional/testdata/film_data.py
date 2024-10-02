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
    },
    {
          "id": "fda827f8-d261-4c23-9e9c-e42787580c4d",
          "title": "A Star Is Born",
          "imdb_rating": 7.7,
          "description": "Jackson Maine (Cooper), a country music star on the brink of decline, discovers a talented unknown named Ally (Germanotta). As the two begin a passionate love affair, Jackson coaxes Ally into the spotlight, catapulting her to stardom. But as Ally's career quickly eclipses his own, Jack finds it increasingly hard to handle his fading glory.",
          "genres": [
            {
              "id": "56b541ab-4d66-4021-8708-397762bff2d4",
              "name": "Music"
            },
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
              "id": "fe2b0699-b5ac-437a-9a69-e747b11eb641",
              "name": "Andrew Dice Clay"
            },
            {
              "id": "77789b44-e734-4fa6-91e8-212a09fa4a32",
              "name": "Lady Gaga"
            },
            {
              "id": "e52627f7-a659-476a-b415-e58e6bebe824",
              "name": "Sam Elliott"
            },
            {
              "id": "5c360057-c51f-4376-bdf5-049b87fa853b",
              "name": "Bradley Cooper"
            }
          ],
          "writers": [
            {
              "id": "f24f3fa4-2e42-4dde-be8c-2aba541a593b",
              "name": "Joan Didion"
            },
            {
              "id": "2b0f84fb-416b-4c30-80db-69478bf872be",
              "name": "John Gregory Dunne"
            },
            {
              "id": "5ac68e18-a84c-4a98-a2ba-85d1bc85e0a4",
              "name": "William A. Wellman"
            },
            {
              "id": "e259d88e-b693-436a-9fed-a10204b8fd91",
              "name": "Robert Carson"
            },
            {
              "id": "e31f6518-6f0a-4738-a224-211eb4150e13",
              "name": "Frank Pierson"
            },
            {
              "id": "5c360057-c51f-4376-bdf5-049b87fa853b",
              "name": "Bradley Cooper"
            },
            {
              "id": "39276c87-27ec-42f3-a573-e0184fc463a7",
              "name": "Eric Roth"
            },
            {
              "id": "7fb9ae3d-aeac-40a9-aa25-cd6992be16a6",
              "name": "Moss Hart"
            },
            {
              "id": "dd0d82d8-1c95-4bb9-b9c6-d707773aa4db",
              "name": "Will Fetters"
            }
          ],
          "directors": [
            {
              "id": "5c360057-c51f-4376-bdf5-049b87fa853b",
              "name": "Bradley Cooper"
            }
          ]
        }, {
          "id": "46f15353-2add-415d-9782-fa9c5b8083d5",
          "title": "Star Wars: Episode IX - The Rise of Skywalker",
          "imdb_rating": 6.7,
          "description": "The surviving members of the resistance face the First Order once again, and the legendary conflict between the Jedi and the Sith reaches its peak bringing the Skywalker saga to its end.",
          "genres": [
            {
              "id": "6c162475-c7ed-4461-9184-001ef3d9f26e",
              "name": "Sci-Fi"
            },
            {
              "id": "3d8d9bf5-0d90-4353-88ba-4ccc5d2c07ff",
              "name": "Action"
            },
            {
              "id": "120a21cf-9097-479e-904a-13dd7198c1dd",
              "name": "Adventure"
            },
            {
              "id": "b92ef010-5e4c-4fd0-99d6-41b6456272cd",
              "name": "Fantasy"
            }
          ],
          "actors": [
            {
              "id": "2d6f6284-13ce-4d25-9453-c4335432c116",
              "name": "Adam Driver"
            },
            {
              "id": "26e83050-29ef-4163-a99d-b546cac208f8",
              "name": "Mark Hamill"
            },
            {
              "id": "7026c3f4-d7b8-414a-99d5-06de1788a0ee",
              "name": "Daisy Ridley"
            },
            {
              "id": "b5d2b63a-ed1f-4e46-8320-cf52a32be358",
              "name": "Carrie Fisher"
            }
          ],
          "writers": [
            {
              "id": "a5a8f573-3cee-4ccc-8a2b-91cb9f55250a",
              "name": "George Lucas"
            },
            {
              "id": "a1758395-9578-41af-88b8-3f9456e6d938",
              "name": "J.J. Abrams"
            },
            {
              "id": "cdf3ace6-802d-4620-b875-809e6318a493",
              "name": "Chris Terrio"
            },
            {
              "id": "5623ae85-91ff-44f1-b46d-21c9d1d0d7f6",
              "name": "Colin Trevorrow"
            },
            {
              "id": "26e020b4-98d9-4c78-b85a-0570eb19d9bc",
              "name": "Derek Connolly"
            }
          ],
          "directors": [
            {
              "id": "a1758395-9578-41af-88b8-3f9456e6d938",
              "name": "J.J. Abrams"
            }
          ]
        }, ]