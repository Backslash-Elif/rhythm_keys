import pygame

class SoundEngine:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.is_playing = False

    def load(self, songpath: str): #load song from path
        self.current_song = songpath
        pygame.mixer.music.load(songpath)

    def play(self): #play loaded song if any
        if self.current_song:
            pygame.mixer.music.play()
            self.is_playing = True

    def pause(self): #pause song
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def get_song_progress(self): #get the progress of the played song
        if self.is_playing:
            return pygame.mixer.music.get_pos()
        return 0

    def seek_to(self, seconds: float): #seek to position
        if self.current_song:
            pygame.mixer.music.set_pos(seconds)

    def get_song_len(self): #get length of loaded song
        if self.sound:
            return self.sound.get_length()  #return length in seconds as float
        return 0.0  #if no song loaded