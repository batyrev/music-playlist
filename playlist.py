import time
import threading

class Song:
    def __init__(self, song_id, title, artist, duration):
        self.id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration

class Node:
    def __init__(self, song, next_node=None, prev_node=None):
        self.song = song
        self.next = next_node
        self.prev = prev_node

class Playlist:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current_node = None
        self.playing = False
        self.pause = False
        self.lock = threading.Lock()

    def add_song(self, song):
        with self.lock:
            new_node = Node(song)
            if self.head is None:
                self.head = new_node
                self.tail = new_node
                self.current_node = new_node
            else:
                self.tail.next = new_node
                new_node.prev = self.tail
                self.tail = new_node

    def play(self):
        if self.playing:
            return
        if self.current_node is None:
            return
        self.playing = True
        self.pause = False
        while self.current_node is not None and self.playing:
            if not self.pause:
                print(f"Now playing: {self.current_node.song.title}")
                time.sleep(self.current_node.song.duration)
                self.next()
            else:
                time.sleep(0.1)

    def pause_playback(self):
        self.pause = not self.pause

    def stop(self):
        self.playing = False
        self.current_node = self.head

    def next(self):
        with self.lock:
            if self.current_node is not None:
                if self.current_node.next is not None:
                    self.current_node = self.current_node.next
                    self.stop()
                    self.play()
                else:
                    self.stop()

    def prev(self):
        with self.lock:
            if self.current_node is not None:
                if self.current_node.prev is not None:
                    self.current_node = self.current_node.prev
                    self.stop()
                    self.play()
                else:
                    self.stop()

    def print_playlist(self):
        node = self.head
        while node is not None:
            print(f"{node.song.title} - {node.song.artist} - {node.song.duration}")
            node = node.next
    
    def get_songs(self):
        songs = []
        node = self.head
        while node is not None:
            songs.append(node.song)
            node = node.next
        return songs
    
    def delete_song(self, song_id):
        node = self.head
        while node is not None:
            if node.song.id == song_id:
                if node.prev is not None:
                    node.prev.next = node.next
                else:
                    self.head = node.next
                if node.next is not None:
                    node.next.prev = node.prev
                else:
                    self.tail = node.prev
                return
            node = node.next
        raise ValueError("Song not found")
    
    def get_current_song(self):
        if self.current_node is None:
            return None
        return self.current_node.song
    
    def get_song(self, song_id):
        node = self.head
        while node is not None:
            if node.song.id == song_id:
                return node.song
            node = node.next
        raise ValueError("Song not found")