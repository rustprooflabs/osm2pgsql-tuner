"""Provides Flask Forms related functionality."""
from wtforms import TextAreaField, DecimalField, SelectField, BooleanField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf import FlaskForm

class Osm2pgsqlTunerInput(FlaskForm):
    system_ram_gb = DecimalField('System RAM (GB)', places=None,
                            validators=[DataRequired(),
                                        NumberRange(min=0.5)],
                            default=64,
                            render_kw={"placeholder": 64})
    osm_pbf_gb = DecimalField('OSM PBF size (GB)', places=None,
                            validators=[DataRequired(),
                                        NumberRange(min=0)],
                            default=10.4,
                            render_kw={"placeholder": 10.4})
    append = BooleanField('Use Append?', default=False)
    ssd = SelectField('Using SSD?', default='Yes, SSD',
                       choices=['Yes, SSD'])
