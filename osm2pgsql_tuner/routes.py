"""osm2pgsq-tuner webapp routes.
"""
import logging
from flask import render_template, abort, request, redirect, jsonify
from osm2pgsql_tuner import app, forms, osm2pgsql, config

api_uri = '/api/v1'

@app.route('/', methods=['GET', 'POST'])
def view_root_path():
    app.logger.debug('Test messages from root path')
    form = forms.Osm2pgsqlTunerInput()

    if form.validate_on_submit():
        system_ram_gb = form.system_ram_gb.data
        osm_pbf = form.osm_pbf.data
        osm_pbf_details = config.PBF_GB_SIZES[osm_pbf]
        osm_pbf_gb = osm_pbf_details['size_gb']
        pbf_filename = osm_pbf_details['filename']
        append = form.append.data
        url_params = f'system_ram_gb={system_ram_gb}'
        url_params += f'&osm_pbf_gb={osm_pbf_gb}'
        url_params += f'&append={append}'
        url_params += f'&pbf_filename={pbf_filename}'
        url_params += f'&pgosm_layer_set=run-all'
        return redirect(f'/recommendation?{url_params}')

    return render_template('index.html', form=form)

def _get_api_params():
    try:
        system_ram_gb = float(request.args.get('system_ram_gb'))
        osm_pbf_gb = float(request.args.get('osm_pbf_gb'))
    except KeyError:
        abort(400)

    pbf_filename = request.args.get('pbf_filename')

    if pbf_filename is None:
        pbf_filename = config.DEFAULT_PBF_FILENAME

    append_raw = request.args.get('append')

    if append_raw == 'True':
        append = True
    else:
        append = False

    if request.args.get('pgosm_layer_set'):
        pgosm_layer_set = request.args.get('pgosm_layer_set')
    else:
        pgosm_layer_set = 'run-all'

    api_params = {'system_ram_gb': system_ram_gb,
                  'osm_pbf_gb': osm_pbf_gb,
                  'append': append,
                  'pbf_filename': pbf_filename,
                  'pgosm_layer_set': pgosm_layer_set}

    return api_params

def _get_recommendation(out_format):
    api_params = _get_api_params()

    rec = osm2pgsql.recommendation(system_ram_gb=api_params['system_ram_gb'],
                                   osm_pbf_gb=api_params['osm_pbf_gb'],
                                   append=api_params['append'],
                                   pgosm_layer_set=api_params['pgosm_layer_set'])
    cmd = rec.get_osm2pgsql_command(out_format=out_format,
                                    pbf_filename=api_params['pbf_filename'])
    rec_data = {'cmd': cmd, 'decisions': rec.decisions,
                'osm2pgsql_run_in_ram': rec.osm2pgsql_run_in_ram,
                'osm2pgsql_noslim_cache': rec.osm2pgsql_noslim_cache,
                'osm2pgsql_cache_max': rec.osm2pgsql_cache_max,
                'osm2pgsql_slim_cache': rec.osm2pgsql_slim_cache,
                'osm2pgsql_drop': rec.osm2pgsql_drop,
                'osm2pgsql_flat_nodes': rec.osm2pgsql_flat_nodes,
                'osm2pgsql_limited_ram': rec.osm2pgsql_limited_ram,
                'system_ram_gb': rec.system_ram_gb,
                'osm2pgsql_append': rec.append}

    return rec_data

@app.route('/recommendation')
def view_recommendation():
    rec_data = _get_recommendation(out_format='html')
    params = request.args
    return render_template('recommendation.html', rec_data=rec_data)


@app.route(api_uri)
def view_recommendation_api():
    rec_data = _get_recommendation(out_format='api')
    return jsonify(osm2pgsql= rec_data)


@app.route('/about')
def view_about():
    return render_template('about.html')

