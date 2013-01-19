from datetime import datetime
from mongoengine import (Document, DateTimeField, StringField, IntField, ListField, DictField)


class Playlist(Document):
    backup_playlist = StringField()
    tracks = ListField()
    currently_playing = DictField()
    next_track = DictField()

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

    # def remove_track(self, uri, facebook_id):
    #     for i, track in enumerate(self.tracks):
    #         if track['uri']


    def vote(self, uri, facebook_id, vote):
        # track_matches = [track for track in self.tracks if track['uri'] == uri]
        # for i, votee in enumerate(track_matches[0]['voters']):
        #     track_matches[0]['voters'][i]['vote'] = 
        # votee_matches = [votee['votee'] for votee in track_matches[0]['voters'] if votee['votee'] == facebook_id]

        # if len(votee_matches) == 0:
        for i, track in enumerate(self.tracks):
            if track['uri'] == uri:
                has_voted = False
                track['vote_rating'] = 0
                for i, votee in enumerate(track['voters']):
                    if votee['votee'] == facebook_id:
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
                # if track['voters'][0]['votee'] == facebook_id:
                #     self.tracks[i]['voters'][0]['vote'] = int(vote)
                #     print 'updated vote.'
                # else:
                #     votee_matches = [votee['votee'] for votee in track_matches[0]['voters'] if votee['votee'] == facebook_id]
                #     print 
                #     track['voters'].append(dict(votee=facebook_id, vote=int(vote)))
                #     print 'added vote.'
            # for votee in track['voters']:
            #     print votee
                # track['vote_rating'] += int(vote)

            # track['vote_rating'] += int(vote)

        self.update_que()
        super(Playlist, self).save()

    # def check_next_track(self):
    #     if not self.tracks:
    #         next_track = dict(uri='next track on spotify playlist')
    #     else:
    #         # print self.next_track
    #         # next_track = self.next_track
    #         self.update_que()

    def update_que(self):
        # self.tracks = sorted(self.tracks, key=lambda k: (k['vote_rating'], k['added']))

        if len(self.tracks) <= 0:
            pass
            # track = dict(
            #     artist='klas',
            #     album='best album',
            #     track='lat 1',
            #     uri='heftig uri',
            #     voters=[dict(votee='goran', vote=1)],
            #     vote_rating=0,
            #     added=datetime.utcnow().strftime('%Y-%-m-%d %H:%M:%S'))

            # self.currently_playing = self.tracks.append(track)
            # self.next_track = self.tracks[0]
        else:
            self.currently_playing = self.tracks[0]
            self.next_track = self.tracks[0]
            # self.tracks.pop(0)

        super(Playlist, self).save()


    def save(self):
        self.updated = datetime.utcnow()
        super(Playlist, self).save()