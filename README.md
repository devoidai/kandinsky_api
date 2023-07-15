# Devoid Kandinsky Api
`RestApi for Kandinsky 2.1`
## Setup
Devoid Kandinsky Api requires [python 3.10.6](https://www.python.org/downloads/release/python-3106/) to run.

Install the dependencies:

```sh
cd kandinsky_api
pip install -r requirements.txt
```

Configure .env file:
```python
LOGGING_LEVEL=INFO
IMAGES_PATH=images/

TOKEN=AUTH_TOKEN

API_PORT=80
API_HOST=0.0.0.0
```

Run:

```sh
python src/main.py
```

If everything is done correctly, the server will be launched at http://localhost:80.


## Documentation

Documentation is available at http://localhost:80/docs.