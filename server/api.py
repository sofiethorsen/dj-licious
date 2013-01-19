from flask import Flask, jsonify, render_template
from models.playlist import Playlist
from models.track import Track

from mongoengine import connect

app = Flask(__name__)
db = connect('musichack', port=27017)

@app.route('/api/create-playlist/<backup_id>/')
def create_playlist(backup_id=None):
    playlist = Playlist(backup_playlist=backup_id).save()
    result = playlist._id
    return jsonify(result=result)


@app.route('/api/get-playlist/<playlist_id>/')
def get_playlist(playlist_id):    
    sort_arg = request.args.get('sorted-by')
    if sort_arg == 'date':
        pass

        playlist = Playlist.objects(playlist_id=playlist_id).first()
        playlist = sorted(playlist.tracks, key=lambda k: k['upvotes'])
    else:
        playlist = Playlist.objects(playlist_id=playlist_id).first()

    result = dict(
        playlist=playlist.playlist_id,
        currently_playing=playlist.currently_playing,
        next_track=playlist.next_track,
        tracks=playlist.tracks)

    return jsonify(result=result)


@app.route('/api/add-track/<playlist_id>/<track_id>/')
def add_track(playlist_id, track_id):
    playlist = Playlist.objects(playlist_id=playlist_id).first()
    playlist.add_track(track_id)
    return jsonify(result=None)


@app.route('/api/next-track/<playlist_id>')
def next_track(playlist_id):
    playlist = Playlist.objects(playlist_id=playlist_id).first()
    next_track = playlist.next_track()
    result = None
    return jsonify(result=result)


@app.route('/api/vote/<playlist_id>/<track_id>/<facebook_id>')
def vote(playlist_id, track_id, facebook_id):
    playlist = Playlist.objects(playlist_id=playlist_id).first()
    playlist.vote(track_id, facebook_id)
    return jsonify(result=None)



@app.route('/api/test/')
def test():
    result = dict(playlist=1, tracks=[dict(track_id=1, voters=['klas', 'erik'])])
    return jsonify(result=result)


@app.route('/client/')
def client():
     return render_template('app.html')



if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)