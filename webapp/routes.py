"""osm2pgsq-tuner webapp routes.
"""
import logging
from flask import render_template, abort, request, redirect, jsonify
from webapp import app, forms, osm2pgsql


@app.route('/', methods=['GET', 'POST'])
def view_root_path():
    app.logger.debug('Test messages from root path')
    form = forms.Osm2pgsqlTunerInput()

    if form.validate_on_submit():
        system_ram_gb = form.system_ram_gb.data
        osm_pbf_gb = form.osm_pbf_gb.data
        append = form.append.data
        url_params = f'system_ram_gb={system_ram_gb}'
        url_params += f'&osm_pbf_gb={osm_pbf_gb}'
        url_params += f'&append={append}'
        return redirect(f'/recommendation?{url_params}')

    return render_template('index.html', form=form)


def _get_recommendation(system_ram_gb, osm_pbf_gb, append, out_format):
    rec = osm2pgsql.recommendation(system_ram_gb=system_ram_gb,
                                   osm_pbf_gb=osm_pbf_gb,
                                   append=append)
    cmd = rec.get_osm2pgsql_command(out_format=out_format)
    rec_data = {'cmd': cmd,
                'osm2pgsql_run_in_ram': rec.osm2pgsql_run_in_ram,
                'osm2pgsql_noslim_cache': rec.osm2pgsql_noslim_cache,
                'osm2pgsql_cache_max': rec.osm2pgsql_cache_max,
                'osm2pgsql_slim_cache': rec.osm2pgsql_slim_cache,
                'osm2pgsql_drop': rec.osm2pgsql_drop,
                'osm2pgsql_flat_nodes': rec.osm2pgsql_flat_nodes,
                'osm2pgsql_limited_ram': rec.osm2pgsql_limited_ram}

    return rec_data

@app.route('/recommendation')
def view_recommendation():
    system_ram_gb = float(request.args.get('system_ram_gb'))
    osm_pbf_gb = float(request.args.get('osm_pbf_gb'))
    append_raw = request.args.get('append')

    if append_raw == 'True':
        append = True
    else:
        append = False

    rec_data = _get_recommendation(system_ram_gb, osm_pbf_gb, append,
                                   out_format='html')

    return render_template('recommendation.html', rec_data=rec_data)


@app.route('/recommendation/api/v1')
def view_recommendation_api():
    data = request.get_json()

    try:
        system_ram_gb = data['system_ram_gb']
        osm_pbf_gb = data['osm_pbf_gb']
    except KeyError:
        abort(400)

    try:
        append = data['append']
    except KeyError:
        append = False

    rec_data = _get_recommendation(system_ram_gb, osm_pbf_gb, append,
                                   out_format='nix')
    return jsonify(osm2pgsql=rec_data)


@app.route('/about')
def view_about():
    return render_template('about.html')

