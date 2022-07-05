## Complex Todo-list Project

A project for todo list

Stack to be used:

**Frontend** 

- Vue 
- Vuetify
- VueX
- Vue-router
- Jest-vue

**Backend** 

- FastAPI + pydantic
- Pytest
- Celery
- RESTful APIs

**Database**

- PostgreSQL via Docker
- Redis/RabbitMQ via Docker
- All DB operations via SQLalchemy

**Testing**
*Positive*
- Call the list API - assert that the number of items in list is n  - assert status code
- Call the api to create a new todo - assert status code
- Call the list api & assert the number of items is == n + 1 - assert status code
- Call the get item by ID api and ensure that the value of the item is correct - id exists, the properties are as expected - assert status code
- Call update api - status code check - get item by id again and validate that the update has actually worked
- Call the delete api - assert status code
- Call list api and check that the list count is again n

*Negative*
- First list all the existing ids
- call the get api with an invalid ID - assert status code = 404
- call the delete API with an invalid id - assert status code = 404
- call the create API with invalid parameters - assert status code = 409
- call update api with an invalid parameter - You can pass an invalid id here for example, you can pass a valid id but invalid parameter

This app is able to generate a PDF file of your todo list.

It uses Celery to manage PDF task queue asynchronously and RabbitMQ as a message broker.

To run this app locally →  

1. Git clone this
2. start rabbitmq using the command `sudo rabbitmq-server`
3. `cd backend 
celery -A tasks worker —loglevel=INFO`
4. `cd backend && pip3 install -r requirements.txt
uvicorn main:app —reload`
5. `cd frontend && npm install
npm run serve`
6. don't forget to create a docker container with postgresql image and connect it with sqlalchemy engine
