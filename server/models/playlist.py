from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField, ListField, DictField)


class Playlist(Document):
    backup_playlist = StringField()
    tracks = ListField()
    currently_playing = StringField()
    next_track = DictField()

    meta = {
        'allow_inheritance': False,
        'indexes': [
            {'fields': ['tracks']},
        ],
    }

    def __init__(self, *args, **kwargs):
            super(Playlist, self).__init__(*args, **kwargs)

    def add_track(self, facebook_id, track_id, track, artist, album, uri):
        matches = [track for track in self.tracks if track['track_id'] == track_id]
        print matches
        if len(matches) == 0:
            track = dict(
                track_id=track_id,
                artist=artist,
                album=album,
                track=track,
                uri=uri,
                voters=[dict(votee=facebook_id, vote=1)],
                vote_rating=0,
                added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

            self.tracks.append(track)
            self.update_que()
        super(Playlist, self).save()

    def vote(self, track_id, facebook_id, vote):
        track_matches = [track for track in self.tracks if track['track_id'] == track_id]
        # votee_matches = [votee for votee in track_matches if votee['votee'] == facebook_id]
        print track_matches
        # if len(votee_matches) == 0:
        #     for track in self.tracks:
        #         if track['track_id'] == track_id:
        #             track['voters'].append(dict(votee=facebook_id, vote=int(vote)))
        #             track['vote_rating'] += int(vote)

        # self.update_que()
        # super(Playlist, self).save()

    def check_next_track(self):
        if not self.tracks:
            next_track = dict(track_id='next track on spotify playlist')
        else:
            # print self.next_track
            # next_track = self.next_track
            self.update_que()

    def update_que(self):
        # self.tracks = sorted(self.tracks, key=lambda k: k['upvotes'])
        self.tracks = sorted(self.tracks, key=lambda k: (k['vote_rating'], k['added']))
        # self.currently_playing = self.tracks[0]
        # self.tracks.pop(0)
        print self.tracks[0]
        self.next_track = self.tracks[0]
        print self.next_track
        super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()