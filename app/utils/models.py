import os

from pynamodb.attributes import UnicodeAttribute, UnicodeSetAttribute
from pynamodb.models import Model

from app.utils.common import str_uuid


class Distribution(Model):
    class Meta:
        table_name = os.getenv("MUSIC_DISTRIBUTION_TABLE_NAME", "fake_distributions")

    id = UnicodeAttribute(hash_key=True, default=str_uuid)
    student = UnicodeAttribute()
    method = UnicodeAttribute()
    pieces = UnicodeSetAttribute()
    parts = UnicodeSetAttribute()