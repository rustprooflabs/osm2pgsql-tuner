# osm2pgsql-tuner

## Using the API

```python
import requests

system_ram_gb = 64
osm_pbf_gb = 10.4
pbf_filename = 'north-america-latest'
append = False

api_endpoint = 'https://osm2pgsql-tuner.com/api/v1'
api_endpoint += f'?system_ram_gb={system_ram_gb}&osm_pbf_gb={osm_pbf_gb}&append={append}&pbf_filename={pbf_filename}'
```

Query the endpoint, check the status

```python
result = requests.get(api_endpoint)
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

## Using osm2pgsql via Python

To use the osm2pgsql recommendation without using the API/website, the
`osm2pgsql_tuner` package can be used.

Install `osm2pgsql-tuner` within an virtual environment.

```bash
pip install osm2pgsql-tuner
```

Import `osm2pgsql_tuner` and create an instance of the `recommendation` class.

```python
import osm2pgsql_tuner
rec = osm2pgsql_tuner.recommendation(system_ram_gb=8,
									 osm_pbf_gb=0.5,
									 pgosm_layer_set='run')
osm2pgsql_command = rec.get_osm2pgsql_command(out_format='api',
											  pbf_filename='example_file')
print(osm2pgsql_command)
```

Returns.

```bash
osm2pgsql -d $PGOSM_CONN  --output=flex --style=./run.lua  ~/pgosm-data/example_file.osm.pbf
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



