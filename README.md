
### Setup

To set it up, you simple need to install the python dependencies. This codebases uses python 3.9 so create a venv with that in mind.

Note that this is NOT a flask application, but a FastAPI application.

### SQLAlchemy and migrations

Unlike a normal flask application, this uses SQLAlchemy more directly. This means that defining the engine and models 
works differently than it would in flask. You have to create the engine yourself and then manage the sessions. Here we 
manage the sessions using FastAPISessionMaker.

Run following commands:

`alembic revision --autogenerate`

`alembic upgrade head`

Please read the alembic migration documentation for more info.

**In case of errors with migrations**

1. Truncate table alembic_version with command `truncate table alembic_version;`

2. Delete all files from alembic/version/ folder. NOTE: Do not delete the folder, just the files inside.

3. Run `alembic revision --autogenerate`

4. Run `alembic upgrade head`

### Pytest setup

Set default test runner to pytest

Go to Settings > Tools > Python Integregrated Tools. Under Testing, set default test runner to pytest

Please add the following arguments to your pytest run configuration template (in Additional Arguments):

--tb=native --capture=tee-sys 

### Handling validation errors

Standard way of handling errors is to raise an fastAPI.HTTPException

### for frontend- response handling code
    # for error
    if not stat:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder({"detail": "Error: " + msg, "body": "Error: " + msg})
        )

    # for success msg
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder({"detail": "Success: " + msg, "body": "Error: " + msg}))


### Pytest setup

Please add the following arguments to your pytest run configuration template (in Additional Arguments):

### DBApi Setup

Note that all write functions i.e. functions that write to the DB, must have two optional parameters:

1. `commit=True` (defaulted to True) so that if a caller wants to commit, they can do so without specifying

2. `session=None` This is to make sure that objects that need foriegn keys to also be saved can be saved appropriately in the same session / transaction

All read queries should have the session parameter.

### Sass/SCSS

https://www.digitalocean.com/community/tutorials/using-sass-with-the-angular-cli

https://sass-lang.com/guide

### Handling validation errors

Standard way of handling errors is to raise an fastAPI.HTTPException

### Structure

#### API

Will have all the API routes

Routes will have minimal code, it will call functions to execute main logic.

Many smaller files are better than bigger files

API - module - route files

Each module folder in the api folder will have a DTOs folder for DTOs

#### DATA


Anything to do with DB

models folder will have all the models

Each model will have its own file

DBAPi will have read modules and write modules. ALl code for read queries will be in separate packages from write queries.

Each function (read or write) will have the dbapi_exception_handler decorator

Each function will also have a session=None parameter

DB Session will be initialized using:

```
db = session
if session is None:
    db = next(get_db())

```

Each write query function will also have a commit=True parameter. Used as:

```
if commit:
    db.commit()
```

If a function has more than 5 args (including session and commit), use a DTO class

#### LOGIC

It will call the dbapi functions.

It will have requirements / business logic code.

Structure:

logic -> module name -> individual files



