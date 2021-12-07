
### Setup

To set it up, you simple need to install the python dependencies. This codebases uses python 3.9 so create a venv with that in mind.

Note that this is NOT a flask application, but a FastAPI application.

### SQLAlchemy and migrations

Unlike a normal flask application, this uses SQLAlchemy more directly. This means that defining the engine and models 
works differently than it would in flask. You have to create the engine yourself and then manage the sessions. Here we 
manage the sessions using FastAPISessionMaker.

Intialize with the following commands:

`alembic init db-migrations`

Then edit alembic-ini and edit the sqlalchemy.uri directive. 

Now you can run following commands:

`alembic revision --autogenerate`

`alembic upgrade head`

Please read the alembic migration documentation for more info.

### Pytest setup

Please add the following arguments to your pytest run configuration template (in Additional Arguments):

