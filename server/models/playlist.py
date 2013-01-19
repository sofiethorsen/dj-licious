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

    def add_track(self, facebook_id, track_id):
        track = dict(
            track_id=str(track_id),
            voters=[dict(votee=facebook_id, vote=1)],
            vote_rating=0,
            added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

        self.tracks.append(track)
        self.update_que()
        super(Playlist, self).save()

    def vote(self, track_id, facebook_id, vote):
        for track in self.tracks:
            if track['track_id'] == track_id:
                track['voters'].append(dict(votee=facebook_id, vote=int(vote)))

        self.update_que()
        super(Playlist, self).save()

    def check_next_track(self):
        if not self.tracks:
            next_track = 'next track on spotify playlist'
        else:
            next_track = self.next_track
            self.update_que()

    def update_que(self):
        for i, track in enumerate(self.tracks):
            print track['voters']
            # track['vote_rating'] += int(track['voters'][i]['vote'])
        # self.tracks = sorted(self.tracks, key=lambda k: k['upvotes'])
        # self.tracks = sorted(self.tracks, key=lambda k: (k['upvotes'], k['added']))
        # self.currently_playing = self.tracks[0]
        # self.tracks.pop(0)
        # self.next_track = self.tracks[0]
        # super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()