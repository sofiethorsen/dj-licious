from flask import Flask, jsonify, render_template
from models.playlist import Playlist
from models.track import Track

from mongoengine import connect

app = Flask(__name__)
db = connect('musichack', port=27017)

@app.route('/api/create-playlist/<backup_id>/')
def create_playlist(backup_id):
    playlist_query = Playlist.objects(backup_playlist=backup_id).first()
    if playlist_query:
        result = str(playlist_query.id)
    else:
        playlist = Playlist(backup_playlist=backup_id).save()
        playlist_query = Playlist.objects(backup_playlist=backup_id).first()
        result = str(playlist_query.id)

    return jsonify(result=result)

@app.route('/api/get_next_song/<playlist_id>/')
def get_next_song(playlist_id):
    playlist = Playlist.objects(id=playlist_id).first()

    track = dict(
        name='I Turn My Camera On',
        artist='Spoon',
        album='Gimme Fiction',
        uri='spotify:track:09k5Qyysx5RnXLqamvdYEN')

    return jsonify(track=track)


@app.route('/api/get-playlist/<playlist_id>/')
def get_playlist(playlist_id):    
    # sort_arg = request.args.get('sorted-by')
    # if sort_arg == 'date':
    #     pass

    #     playlist = Playlist.objects(playlist_id=playlist_id).first()
    #     playlist = sorted(playlist.tracks, key=lambda k: k['upvotes'])
    # else:
    #     playlist = Playlist.objects(playlist_id=playlist_id).first()
    playlist = Playlist.objects(id=playlist_id).first()

    result = dict(
        playlist=str(playlist.id),
        currently_playing=str(playlist.currently_playing),
        next_track=str(playlist.next_track),
        tracks=str(playlist.tracks)
        )

    return jsonify(result=result)


@app.route('/api/add-track/<playlist_id>/<facebook_id>/<track_id>/')
def add_track(playlist_id, facebook_id, track_id):
    playlist = Playlist.objects(id=playlist_id).first()
    playlist.add_track(facebook_id, track_id)
    return jsonify(result='Added track.')


@app.route('/api/next-track/<playlist_id>')
def next_track(playlist_id):
    playlist = Playlist.objects(id=playlist_id).first()
    next_track = playlist.check_next_track()
    result = dict(track_name='', track_artist='', track_album='', track_uri='')
    return jsonify(result=result)


@app.route('/api/vote/<playlist_id>/<track_id>/<facebook_id>/<vote>')
def add_vote(playlist_id, track_id, facebook_id, vote):
    playlist = Playlist.objects(id=playlist_id).first()
    playlist.vote(track_id, facebook_id, vote)
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