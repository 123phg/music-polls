# About
This is a simple project that I am writing for training: music quiz service.\
How will it work?
- The user begins to interact with the service using one of the interfaces: telegram or http web api
- The service prompts the user to log to Spotify
- The service loads data from user's Spotify recommendations and create questions for quiz based on recomendations info.
- After that service send a question to user and handle answer

The main idea is that recommendations will lead to good questions.\
The recommendations do not contain the tracks that the user has listened to.\
However, the recommendations contain information about tracks that are similar \
to the ones the user has listened to.

Examples of questions:
- Who is the author of the album?
- What year was the album released?
- Which label released the album?
- What is the genre of the album?

Each question will contain an album cover

Question telegram example \
\
![image_of_question_example](https://i.ibb.co/3Njmd63/demo-question.png)

# Roadmap & current status
The project is new and in the stage of active development.
Steps:
- Create Question model with required methods & Question http api
- Create Question writer \
  It is needed to load questions to the database for the user.
- Create telegram bot & auth mechanism **<- I'm here**
- Create demo data and release it to AWS \
  I am planning to create an internal database of questions that I will
  use instead of questions from Spotify.
  Of course, this is only to speed up the release.
- Add Spotify API client and use it to get music data for each user. 
# How to install
```bash
docker-compose up -d --build
docker-compose run web python manage.py migrate
```

# How to run
```bash
docker-compose up -d
```

# How to run tests
```bash
docker-compose run --rm web sh
pytest
```
# Http API description
**Get quesions list**\
Type: GET\
Path: '/api/v1/genres-polls/questions/' \
Response: 
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "image_url": "https://example_image_url/1.jpg",
            "options": [
                "ambient",
                "dub step"
            ]
        },
        {
            "id": 3,
            "image_url": "http://www.image.com/2.jpg",
            "options": [
                "kek"
            ]
        }
    ]
}
```
**Question Detail** \
Type: GET\
Path: '/api/v1/genres-polls/questions/{question_id}/' \
Response: 
```json
{
    "id": 1,
    "image_url": "https://i.scdn.co/image/ab67616d00001e02872772e0b165e57a104fd37a",
    "options": [
        "ambient",
        "dub step"
    ]
}
```
**Answer the question** \
Type: PATCH\
Path: '/api/v1/genres-polls/questions/1/answer/' \
Content: \
```json
{
    "selected_answer": "ambient"
}
```
Response: \
```json
{
    "id": 1,
    "image_url": "https://i.scdn.co/image/ab67616d00001e02872772e0b165e57a104fd37a",
    "options": [
        "ambient",
        "dub step"
    ],
    "selected_answer": "ambient",
    "correct_answer": "ambient"
}
```

# Components

## Question model
Question model - standard Django ORM data model. \
Model has some data validations.\
Has custom object manager to provide actual for user questions.\
path: *genres_polls.models* and *genres_polls.managers* 


## QuestionDTO
Data transfer object for question data.\
Has some data validations. \
Uses by question writer.
path: *genres_polls.question*


## Question writer
This component will load question data for user. \
Has deduplication questions policy.
path: genres_polls.question_writer
