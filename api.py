from flask import Flask, jsonify, render_template, request
from models.playlist import Playlist
from models.track import Track

from mongoengine import connect

app = Flask(__name__)
db = connect('musichack', port=27017)

@app.route('/api/create-playlist/')
def create_playlist():
    backup_playlist_arg = request.args.get('backup_id')

    playlist_query = Playlist.objects(backup_playlist=backup_playlist_arg).first()
    if playlist_query:
        result = str(playlist_query.id)
    else:
        playlist = Playlist(backup_playlist=backup_playlist_arg).save()
        playlist_query = Playlist.objects(backup_playlist=backup_playlist_arg).first()
        result = str(playlist_query.id)
    # result='50faf48ccf1e8c4ad70aa464'
    return jsonify(result=result)


@app.route('/api/get-playlist/')
def get_playlist():
    playlist_arg = request.args.get('playlist_id')
    # sort_arg = request.args.get('sorted-by')
    # if sort_arg == 'date':
    #     pass

    #     playlist = Playlist.objects(playlist_id=playlist_id).first()
    #     playlist = sorted(playlist.tracks, key=lambda k: k['upvotes'])
    # else:
    #     playlist = Playlist.objects(playlist_id=playlist_id).first()
    playlist = Playlist.objects(id=playlist_arg).first()

    if playlist.next_track:        
        next_track = dict(
            adder=playlist.next_track['adder'],
            artist=playlist.next_track['artist'],
            album=playlist.next_track['album'],
            track=playlist.next_track['track'],
            added=playlist.next_track['added'],
            vote_rating=playlist.next_track['vote_rating'],
            voters=playlist.next_track['voters'],
            uri=playlist.next_track['uri'])
    else:
        next_track = dict(
            adder='',
            artist='',
            album='',
            track='',
            added='',
            vote_rating='',
            voters='',
            uri='')

    if playlist.currently_playing:        
        currently_playing = dict(
            adder=playlist.currently_playing['adder'],
            artist=playlist.currently_playing['artist'],
            album=playlist.currently_playing['album'],
            track=playlist.currently_playing['track'],
            added=playlist.currently_playing['added'],
            vote_rating=playlist.currently_playing['vote_rating'],
            voters=playlist.currently_playing['voters'],
            uri=playlist.currently_playing['uri'])
    else:
        currently_playing = dict(
            adder='',
            artist='',
            album='',
            track='',
            added='',
            vote_rating='',
            voters='',
            uri='')

    result = dict(
        playlist=str(playlist.id),
        currently_playing=currently_playing,
        next_track=next_track,
        tracks=playlist.tracks)

    return jsonify(result=result)


@app.route('/api/add-track/')
def url_add_track():
    playlist_arg = request.args.get('playlist_id')
    facebook_id_arg = request.args.get('facebook_id')
    track_arg = request.args.get('track')
    artist_arg = request.args.get('artist')
    album_arg = request.args.get('album')
    uri_arg = request.args.get('uri')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.add_track(facebook_id_arg, track_arg, artist_arg, album_arg, uri_arg)
    return jsonify(result='Added track.')


@app.route('/api/next-track/')
def next_track():
    playlist_arg = request.args.get('playlist_id')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.get_next_track()
    next_track = playlist.next_track
    result = dict(track=next_track['track'], artist=next_track['artist'], album=next_track['album'], uri=next_track['uri'])
    return jsonify(result=result)


@app.route('/api/vote/')
def add_vote():
    playlist_arg = request.args.get('playlist_id')
    uri_arg = request.args.get('uri')
    facebook_id_arg = request.args.get('facebook_id')
    vote_arg = request.args.get('vote')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.vote(uri_arg, facebook_id_arg, vote_arg)
    return jsonify(result='Voted on track.')


@app.route('/client/')
def client():
     return render_template('app.html')



if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)