import pygame, time

class SoundEngine:
    def __init__(self):
        pygame.mixer.init()
        self.current_song = None
        self.is_playing = False

    def load(self, songpath):
        """Load the song from the specified path."""
        self.current_song = songpath
        pygame.mixer.music.load(songpath)

    def play(self):
        """Play the loaded song."""
        if self.current_song:
            pygame.mixer.music.play()
            self.is_playing = True

    def pause(self):
        """Pause the currently playing song."""
        if self.is_playing:
            pygame.mixer.music.pause()
            self.is_playing = False

    def get_song_progress(self):
        """Get the progress of the currently playing song in miliseconds."""
        if self.is_playing:
            return pygame.mixer.music.get_pos()
        return 0

    def seek_to(self, seconds):
        """Seek to a specific time in the song."""
        if self.current_song:
            pygame.mixer.music.set_pos(seconds)

# Example usage

engine = SoundEngine()
engine.load('data/Wavetapper.mp3')
engine.play()
# Additional code to control playback can be added here

# 150, 151, 152

bpm = 112
beginning_delay = 0
steps = 4
first_step = 2

delay = 60 / bpm
timebuffer = time.time() + delay + beginning_delay
step = first_step

while True:
    while time.time() < timebuffer:
        time.sleep(0.001)

    # update display
    print(f"beat {step}/{steps} at:", timebuffer)

    #calculations for next beat, non-time-sensitive
    timebuffer += delay
    step += 1
    if step > steps:
        step = 1