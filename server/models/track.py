from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField)

class Track(Document):

    track_id = StringField(required=True)
    que_place = IntField()
    upvotes = IntField()

    meta = {
        'allow_inheritance': False,
        'indexes': [

            {'fields': ['track_id', 'upvotes']},
        ],
    }