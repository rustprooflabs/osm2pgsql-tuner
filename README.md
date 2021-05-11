# osm2pgsql-tuner

## Using the API


```bash
curl -X GET -H 'Content-Type: application/json' \
    http://localhost:5000/recommendation/api/v1 \
    -d '{"system_ram_gb": 64, "osm_pbf_gb": 10.4}'
```

Optional, specify append (defaults to `false`) with the data passed with the request.

```bash
"append": true
```

Returns


```json
{
  "osm2pgsql": {
    "cmd": "osm2pgsql -d $PGOSM_CONN  --cache=0  --slim  --flat-nodes=/tmp/nodes  --output=flex --style=./run-all.lua  ~/pgosm-data/your-input.osm.pbf", 
    "osm2pgsql_cache_max": 42.24, 
    "osm2pgsql_drop": false, 
    "osm2pgsql_flat_nodes": true, 
    "osm2pgsql_limited_ram": false, 
    "osm2pgsql_noslim_cache": 27.0, 
    "osm2pgsql_run_in_ram": false, 
    "osm2pgsql_slim_cache": 20.25
  }
}
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



