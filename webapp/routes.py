"""osm2pgsq-tuner webapp routes.
"""
import logging
from flask import render_template, abort, request, redirect
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


@app.route('/recommendation')
def view_recommendation():
    system_ram_gb = float(request.args.get('system_ram_gb'))
    osm_pbf_gb = float(request.args.get('osm_pbf_gb'))
    append_raw = request.args.get('append')
    if append_raw == 'True':
        append = True
    else:
        append = False

    inputs = {'system_ram_gb': system_ram_gb,
              'osm_pbf_gb': osm_pbf_gb,
              'append': append}

    rec = osm2pgsql.recommendation(system_ram_gb=system_ram_gb,
                                   osm_pbf_gb=osm_pbf_gb,
                                   append=append)
    cmd = rec.get_osm2pgsql_command(out_format='html')
    rec_data = {'cmd': cmd,
                'osm2pgsql_noslim': rec.osm2pgsql_noslim,
                'osm2pgsql_noslim_cache': rec.osm2pgsql_noslim_cache,
                'osm2pgsql_cache_max': rec.osm2pgsql_cache_max}
    return render_template('recommendation.html', inputs=inputs,
                           rec_data=rec_data)

@app.route('/about')
def view_about():
    return render_template('about.html')

