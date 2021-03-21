# About
This is a simple project that I am writing for training: music quiz service.\
How will it work?
- The user begins to interact with the service using one of the interfaces: telegram or http web api
- The service prompts the user to log to Spotify
- The service loads data from user's Spotify recommendations and create questions for quiz based on recomendations info.
- After that service send a question to user and handle answer

Examples of questions:
- Who is the author of the album?
- What year was the album released?
- Which label released the album?
- What is the genre of the album?

Each question will contain an album cover

Question telegram example
![alt text](https://i.ibb.co/3Njmd63/demo-question.png)

# Roadmap & current status
The project is new and in the stage of active development.
Steps:
- Create Question model with required methods & Question http api
- Create Question writer \
  It is needed to load questions to the database for the user.
- Create telegram bot & auth mechanism ** <- I'm here **
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
# API description
