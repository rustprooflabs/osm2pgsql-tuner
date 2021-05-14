# osm2pgsql-tuner

## Using the API

```python
import requests
api_endpoint = 'http://localhost:5000/recommendation/api/v1'
data = {'system_ram_gb': 64, 'osm_pbf_gb': 10.4, 'append': False,
        'pbf_filename': 'north-america-latest'}
```

Query the endpoint, check the status

```python
result = requests.get(api_endpoint, params=data)
print(f'Status code: {result.status_code}')
```

Get recommendation data.

```python
rec = result.json()['osm2pgsql']
```

Command is the most interesting part

```python
print(f"\nCommand:\n{rec['cmd']} ")
```

Other details returned used in decision making to determine the command `cmd`.

```python
print(rec.keys())
```


## Deployment Instructions

> Note:  Need to update the sub-version of Python over time.  Can use simply
`python3` but that can lead to using older unsupported versions based on distro-defaults.


```bash
cd ~/venv
python3.8 -m venv osm2pgsql-tuner
source ~/venv/osm2pgsql-tuner/bin/activate
```

Install requirements

```bash
source ~/venv/osm2pgsql-tuner/bin/activate
cd ~/git/osm2pgsql-tuner
pip install -r requirements.txt
```

Run web server w/ uWSGI.

```bash
source ~/venv/osm2pgsql-tuner/bin/activate
cd ~/git/osm2pgsql-tuner
python run_server.py
```


## Unit tests

Run unit tests.

```bash
python -m unittest tests/*.py
```

Or run unit tests with coverage.

```bash
coverage run -m unittest tests/*.py
```

Generate report.

```bash
coverage report -m webapp/*.py
```


Run pylint.

```bash
pylint --rcfile=./.pylintrc -f parseable ./webapp/*.py
```



