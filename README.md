# Python Base Project

A Python and fastapi starter project

| Component             | Dependency                         | Setup                                   |
|-----------------------|------------------------------------|-----------------------------------------|
| webserver             | fastapi<br/>uvicorn                | FastAPI in main and APIRouter in routes |
| database              | psycopg2-binary                    | create db url from sqlmodel engine      |
| orm                   | sqlmodel                           | built on top of sql alchemy             |
| database migration    | alembic                            | use db url in env.py                    |
| security              | bcrypt<br/>passlib<br/>python-jose | authentication and authorization        |
| testing               | pytest<br/>six<br/>mockito         | unit testing by mocking dependencies    |
| logging               | loguru                             | simple logging                          |
| dependency management | NA                                 | NA                                      |
  