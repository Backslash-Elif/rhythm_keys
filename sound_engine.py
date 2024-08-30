import pygame

class SoundEngine:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.play_state = 0 #0= stopped, 1= playing, 2= paused
        self.sound = None

    def load(self, songpath: str): #load song from path
        self.eject()
        self.current_song = songpath
        pygame.mixer.music.load(songpath)
        self.sound = pygame.mixer.Sound(songpath) #get song details
    
    def eject(self): #unload song
        if self.play_state:
            self.stop()
        if self.current_song:
            pygame.mixer.music.unload()
            self.current_song = None
            self.sound = None

    def play(self): #play loaded song if any
        if self.current_song:
            if self.play_state == 2:
                pygame.mixer.music.unpause()
            else:
                pygame.mixer.music.play()
            self.play_state = 1

    def pause(self): #pause song
        if self.play_state == 1:
            pygame.mixer.music.pause()
            self.play_state = 2
    
    def stop(self): #stop song
        if self.play_state:
            pygame.mixer.music.stop()
            self.play_state = 0

    def get_song_progress(self): #get the progress of the played song
        if self.play_state:
            return pygame.mixer.music.get_pos()
        return 0

    def seek_to(self, seconds: float): #seek to position
        if self.current_song:
            pygame.mixer.music.set_pos(seconds)

    def get_song_len(self): #get length of loaded song
        if self.sound:
            return self.sound.get_length()  #return length in seconds as float
        return 0.0  #if no song loaded
    
    def get_play_state(self):
        return self.play_state
    
    def song_loaded(self):
        if self.current_song:
            return True
        else:
            return False