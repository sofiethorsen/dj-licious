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
    result='50fb0245cf1e8c4d42b8b06b'
    return jsonify(result=result)


@app.route('/api/get-playlist/')
def get_playlist():
    playlist_arg = request.args.get('playlist_id')
    playlist = Playlist.objects(id=playlist_arg).first()

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
            adder=None,
            artist=None,
            album=None,
            track=None,
            added=None,
            vote_rating=None,
            voters=None,
            uri=None)

    result = dict(
        playlist=str(playlist.id),
        currently_playing=currently_playing,
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

    print 'track_arg', track_arg

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.add_track(facebook_id_arg, track_arg, artist_arg, album_arg, uri_arg)
    return jsonify(result='Added track.')


@app.route('/api/next-track/')
def next_track():
    playlist_arg = request.args.get('playlist_id')

    playlist = Playlist.objects(id=playlist_arg).first()
    next_track = playlist.get_next_track()
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


@app.route('/client/<playlist_id>')
def client(playlist_id):
     return render_template('app.html', playlist_id=playlist_id)


if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)
