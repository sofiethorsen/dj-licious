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
    playlist.check_next_track()

    result = dict(
        playlist=str(playlist.id),
        currently_playing=str(playlist.currently_playing),
        next_track=str(playlist.next_track),
        tracks=str(playlist.tracks)
        )

    return jsonify(result=result)


@app.route('/api/add-track/')
def url_add_track():
    playlist_arg = request.args.get('playlist_id')
    facebook_id_arg = request.args.get('facebook_id')
    track_id_arg = request.args.get('track_id')
    track_arg = request.args.get('track')
    artist_arg = request.args.get('artist')
    album_arg = request.args.get('album')
    uri_arg = request.args.get('uri')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.add_track(facebook_id_arg, track_id_arg, track_arg, artist_arg, album_arg, uri_arg)
    return jsonify(result='Added track.')


@app.route('/api/next-track/')
def next_track():
    playlist_arg = request.args.get('playlist_id')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.check_next_track()
    next_track = playlist.next_track
    result = dict(track_id=next_track['track_id'], track=next_track['track'], artist=next_track['artist'], album=next_track['album'], uri=next_track['uri'])
    return jsonify(result=result)


@app.route('/api/vote/')
def add_vote():
    playlist_arg = request.args.get('playlist_id')
    track_id_arg = request.args.get('track_id')
    facebook_id_arg = request.args.get('facebook_id')
    vote_arg = request.args.get('vote')

    playlist = Playlist.objects(id=playlist_arg).first()
    playlist.vote(track_id_arg, facebook_id_arg, vote_arg)
    return jsonify(result='Voted on track.')


@app.route('/api/test/')
def test():
    result = dict(playlist=1, tracks=[dict(track_id=1, voters=['klas', 'erik'])])
    return jsonify(result=result)


@app.route('/client/')
def client():
     return render_template('app.html')



if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)