from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField, ListField, DictField)


class Playlist(Document):
    backup_playlist = StringField()
    tracks = ListField()
    currently_playing = DictField()
    next_track = DictField()
    adder = StringField()

    meta = {
        'allow_inheritance': False,
        'indexes': [
            {'fields': ['tracks']},
        ],
    }

    def __init__(self, *args, **kwargs):
            super(Playlist, self).__init__(*args, **kwargs)

    def add_track(self, facebook_id, track, artist, album, uri):
        matches = [track for track in self.tracks if track['uri'] == uri]

        if len(matches) == 0:
            track = dict(
                adder=facebook_id,
                artist=artist,
                album=album,
                track=track,
                uri=uri,
                voters=[dict(votee=facebook_id, vote=1)],
                vote_rating=0,
                added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

            self.tracks.append(track)
        super(Playlist, self).save()


    def vote(self, uri, facebook_id, vote):
        for i, track in enumerate(self.tracks):
            if track['uri'] == uri:
                has_voted = False
                track['vote_rating'] = 0
                for i, votee in enumerate(track['voters']):
                    if votee['votee'] == facebook_id:
                        if int(vote) == 0:
                            self.tracks[0]['voters'].pop(i)
                            has_voted = True
                            print 'removed vote.'
                        else:
                            self.tracks[0]['voters'][i]['vote'] = int(vote)
                            has_voted = True
                            print 'updated vote.'

                if not has_voted:
                    track['voters'].append(dict(votee=facebook_id, vote=int(vote)))
                    print 'added vote.'
 
        for i, track in enumerate(self.tracks):
            track['vote_rating'] = 0
            for vote in track['voters']:
                print vote['vote']
                self.tracks[i]['vote_rating'] += int(vote['vote'])
        super(Playlist, self).save()

    def get_next_track(self):
        if len(self.tracks) <= 0:
            track = dict(
                artist='Basement Jaxx',
                adder='johan.brodin',
                album='Remedy',
                track='Gemilude',
                uri='spotify:track:0SNCZ71vAXD5cBJqOeTdT3',
                voters=[dict(votee='backup', vote=1)],
                vote_rating=0,
                added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

            self.currently_playing = track
        else:
            self.currently_playing = self.tracks[0]
            self.next_track = self.tracks[0]
            self.tracks.pop(0)
        super(Playlist, self).save()

    def update_que(self):
        # self.tracks = sorted(self.tracks, key=lambda k: (k['vote_rating'], k['added']))
        playlist = sorted(playlist.tracks, key=lambda k: k['upvotes'])

        # if len(self.tracks) <= 0:
        #     track = dict(
        #         artist='Basement Jaxx',
        #         album='Remedy',
        #         track='Gemilude',
        #         uri='spotify:track:0SNCZ71vAXD5cBJqOeTdT3',
        #         voters=[dict(votee='backup', vote=1)],
        #         vote_rating=0,
        #         added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

        #     self.currently_playing = self.tracks.append(track)
        #     self.next_track = self.tracks[0]
        # else:
        #     self.currently_playing = self.tracks[0]
        #     self.next_track = self.tracks[0]
        #     self.tracks.pop(0)

        super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()