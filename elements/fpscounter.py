import time

class Fpscounter:
    def __init__(self) -> None:
        self.fps = 0
        self.frame_counter = 0
        self.current_second = 0
    
    def tick(self):
        if self.current_second < int(time.time()):
            self.fps = self.frame_counter
            self.frame_counter = 1
            self.current_second = int(time.time())
        else:
            self.frame_counter += 1
    
    def get_fps(self):
        return self.fps