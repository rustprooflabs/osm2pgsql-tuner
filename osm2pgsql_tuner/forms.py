"""Provides Flask Forms related functionality."""
from wtforms import TextAreaField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm
from osm2pgsql_tuner import config


def _get_pbf_gb_choices():
    """Prepares list of PBF size choices for drop-down menu.

    Returns
    -------------------------
    pbf_gb_choices : list
        list of tuples
    """
    pbf_gb_choices = list()
    for key, value in config.PBF_GB_SIZES.items():
        choice = (key,
                  f"{key} ({value['size_gb']} GB)")
        pbf_gb_choices.append(choice)

    return pbf_gb_choices


class Osm2pgsqlTunerInput(FlaskForm):
    system_ram_gb = SelectField('System RAM (GB)',
                                default=64,
                                choices=[4, 8, 16, 32, 64, 128, 256])
    pbf_gb_choices = _get_pbf_gb_choices()
    osm_pbf = SelectField('OSM PBF size (GB)',
                          default='North America',
                          choices=pbf_gb_choices)
    append = BooleanField('Use Append?', default=False)
    ssd = SelectField('Using SSD?', default='Yes, SSD',
                       choices=['Yes, SSD'])
