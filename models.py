"""
This file defines the database models
"""
import os
from .common import db, Field
from pydal.validators import *


### Define your table below
#
# db.define_table('thing', Field('name'))
#
## always commit your models to avoid problems later
#
# db.commit()
#

db.define_table('tipo_document',
                Field('name', 'string'),
                Field('description', 'text')
                )

db.define_table('documents',
                Field('tipodocument_id', 'reference tipo_document'),
                Field('title', 'string'),
                Field('description', 'text'),
                Field('file', 'upload'),
                Field('note', 'text')
                )