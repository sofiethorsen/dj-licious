from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField, ListField)


class Playlist(Document):
    backup_playlist = StringField()
    tracks = ListField()
    currently_playing = StringField()
    next_track = StringField()

    meta = {
        'allow_inheritance': False,
        'indexes': [
            {'fields': ['tracks']},
        ],
    }

    def __init__(self, *args, **kwargs):
            super(Playlist, self).__init__(*args, **kwargs)

    def add_track(track_id):
        track = dict(track_id=track_id, voters=[], added=datetime.utcnow())
        self.tracks.append(track)
        super(Playlist, self).save()

    def vote(track_id, facebook_id):
        for track in self.tracks:
            if track['track_id'] == track_id:
                track['voters'].append(facebook_id)

        self.update_que()
        super(Playlist, self).save()

    def next_track():
        if not self.tracks:
            next_track = 'next track on spotify playlist'
        else:
            next_track = self.next_track
            self.update_que()

    def update_que():
        self.tracks = sorted(self.tracks, key=lambda k: k['upvotes'])
        self.currently_playing = self.tracks[0]
        self.tracks.pop(0)
        self.next_track = self.tracks[0]
        super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()