
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

Please add the following arguments to your pytest run configuration template (in Additional Arguments):

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

