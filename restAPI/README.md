
## Getting started
##### First install the requirements:
    $ pip install -r requirements.txt
##### To launch the RestAPI:
    On linux:
        $ uvicorn main:app --reload
    On windows:
        $ python -m uvicorn main:app --reload
        OR
        $ python3 -m uvicorn main:app --reload
## Documentation
##### Once the server is running, the dynamic documentation can be accessed by going to:
    - http://127.0.0.1:8000/docs (Swagger UI)
    - http://127.0.0.1:8000/redoc (ReDoc)
##### Functions:
    - GET current mode
    - GET current state
    - GET current measures
    - GET last measures
    -
