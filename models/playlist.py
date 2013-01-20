from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField, ListField, DictField)
from random import choice
from utils import multikeysort
import hashlib

class Playlist(Document):
    backup_playlist = StringField()
    playlist_hash = StringField()
    tracks = ListField()
    currently_playing = DictField()
    adder = StringField()

    updated = DateTimeField(default=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

    meta = {
        'allow_inheritance': False,
        'indexes': [
            {'fields': ['tracks']},
        ],
    }

    def __init__(self, *args, **kwargs):
            super(Playlist, self).__init__(*args, **kwargs)
            playlist_hash = hashlib.sha1(self.backup_playlist).hexdigest()
            self.playlist_hash = playlist_hash[:4]
            self.save()

    def add_track(self, facebook_id, track, artist, album, uri):
        matches = 0
        for t in self.tracks:
            if t['uri'] == uri:
                matches += 1

        print 'add_track', track
        if matches == 0:
            track = dict(
                adder=facebook_id,
                artist=artist,
                album=album,
                track=track,
                uri=uri,
                voters=[dict(votee=facebook_id, vote=1)],
                vote_rating=1,
                added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))
            print track
            self.tracks.append(track)
            self.update_que()
        super(Playlist, self).save()


    def vote(self, uri, facebook_id, vote):
        for i, track in enumerate(self.tracks):
            if track['uri'] == uri:
                has_voted = False
                track['vote_rating'] = 0
                for j, votee in enumerate(track['voters']):
                    if votee['votee'] == facebook_id:
                        if int(vote) == 0:
                            self.tracks[i]['voters'].pop(i)
                            has_voted = True
                            print 'removed vote.'
                        else:
                            self.tracks[i]['voters'][j]['vote'] = int(vote)
                            has_voted = True
                            print 'updated vote.'

                if not has_voted:
                    track['voters'].append(dict(votee=facebook_id, vote=int(vote)))
                    print 'added vote.'

        for i, track in enumerate(self.tracks):
            track['vote_rating'] = 0
            for vote in track['voters']:
                self.tracks[i]['vote_rating'] += int(vote['vote'])

        self.update_que()
        super(Playlist, self).save()

    def get_next_track(self):
        if len(self.tracks) == 0:
            backup_playlist = [
                dict(
                    artist='Basement Jaxx',
                    adder=None,
                    album='Remedy',
                    track='Gemilude',
                    uri='spotify:track:0SNCZ71vAXD5cBJqOeTdT3',
                    voters=[dict(votee='backup', vote=1)],
                    vote_rating=0,
                    added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S')),
                dict(
                    artist='Basement Jaxx',
                    adder=None,
                    album='Remedy',
                    track='Bingo Bango',
                    uri='spotify:track:1xJW8GKZeugt3hdG1khWzr',
                    voters=[dict(votee='backup', vote=1)],
                    vote_rating=0,
                    added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))
            ]

            track = choice(backup_playlist)
        else:
            track = self.tracks.pop(0)
        self.currently_playing = track
        self.update_que()
        super(Playlist, self).save()
        return track


    def update_que(self):
        self.tracks = multikeysort(self.tracks, ['-vote_rating', 'added'])
        self.updated = datetime.utcnow()
        super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()
