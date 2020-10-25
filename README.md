# Lab 1:

## Variant 22:
### Report: [БД_КП81_ЛР1_Янковський_Дмитро.pdf](lab_reports/БД_КП81_ЛР1_Янковський_Дмитро.pdf)
### Screenshots:
![](lab_reports/db_schema.png)

![](lab_reports/sample_developers_data.png)

![](lab_reports/sample_developer_skill_data.png)

## Quickstart
```
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python  # poetry
```

## Useful Commands:

### Python Virtual Environment:

```
poetry shell  # activate python virtual environment
poetry install  # install dependencies
```

### Run Dev Server:

```
flask  # CLI commands
make idb # Setup and seed database
make run  # run flask dev server
```


### Database:
Using Postgresql.
```
createdb db_labs  # create DB
flask db upgrade  # run migrations
flask seed  # populate with sample data
flask db migrate  # generate new migration
flask db  # more migration commands
```

### API Documentation:

Once your flask dev server is running:

- [OpenAPI JSON](http://localhost:5000/api/openapi.json) (http://localhost:5000/api/openapi.json)
- [Swagger UI](http://localhost:5000/api/swagger) (http://localhost:5000/api/swagger)
