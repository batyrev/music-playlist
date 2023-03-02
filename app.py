from flask import Flask, jsonify, request
from playlist import Playlist, Song

app = Flask(__name__)

# создаем плейлист и добавляем в него несколько песен для тестирования
playlist = Playlist()
playlist.add_song(Song(1, "Song 1", "Artist 1", 120))
playlist.add_song(Song(2, "Song 2", "Artist 2", 180))
playlist.add_song(Song(3, "Song 3", "Artist 3", 240))

# методы для управления плейлистом через API
@app.route("/playlist", methods=["GET"])
def get_playlist():
    return jsonify([song.__dict__ for song in playlist.get_songs()])

@app.route("/playlist", methods=["POST"])
def add_song():
    song_data = request.get_json()
    song = Song(song_data["id"], song_data["title"], song_data["artist"], song_data["duration"])
    playlist.add_song(song)
    return jsonify({"message": "Song added to the playlist."})

@app.route("/playlist/<int:song_id>", methods=["DELETE"])
def delete_song(song_id):
    try:
        playlist.delete_song(song_id)
        return jsonify({"message": "Song deleted from the playlist."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/playlist/<int:song_id>", methods=["GET"])
def get_song(song_id):
    try:
        return jsonify(playlist.get_song(song_id).__dict__)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/playlist/play", methods=["GET"])
def play_song():
    try:
        playlist.play()
        return jsonify({"message": "Song is playing."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/playlist/pause", methods=["GET"])
def pause_song():
    try:
        playlist.pause_playback()
        return jsonify({"message": "Song is paused."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/playlist/next", methods=["GET"])
def next_song():
    try:
        playlist.next()
        return jsonify({"message": "Next song is playing."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/playlist/prev", methods=["GET"])
def prev_song():
    try:
        playlist.prev()
        return jsonify({"message": "Previous song is playing."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    
@app.route("/playlist/stop", methods=["GET"])
def stop_song():
    try:
        playlist.stop()
        return jsonify({"message": "Song is stopped."})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.route("/playlist/current", methods=["GET"])
def get_current_song():
    try:
        return jsonify(playlist.get_current_song().__dict__)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
