import os, time, pygame, global_vars, tools
from scenes import scene

from components import button, text, inputbox, touchtrigger, fpscounter, bgstyle, display_image, card
from components.styles import Styles

import tkinter as tk
from tkinter import filedialog


def file_picker():
    #make rootwindow and hide it
    root = tk.Tk()
    root.withdraw()

    #file allow list
    file_types = [("All Audio Files", "*.wav;*.mp3;*.ogg;*.midi")]

    #file dialog
    file_path = filedialog.askopenfilename(title="Select an Audio File", filetypes=file_types)
    return file_path

class EditorCreateMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        global_vars.editor_name = ""
        global_vars.editor_author = global_vars.user_name
        global_vars.editor_song_artist = ""
        global_vars.editor_length = 0
        global_vars.editor_difficulty = 0
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        
        self.back_btn = button.Button("Back", 32, (64, 1080-128), (128, 64), Styles.button.danger())
        #inputs
        self.name_text = text.Text("Enter song name:", 24, (300+10, 300-24), Styles.colors.light_gray())
        self.name_input = inputbox.InputBox((700, 48), 32, (300, 300), 32, Styles.inputbox.dark())
        self.artist_text = text.Text("Enter song artist:", 24, (300+10, 400-24), Styles.colors.light_gray())
        self.artist_input = inputbox.InputBox((700, 48), 32, (300, 400), 32, Styles.inputbox.dark())
        #difficulty
        self.difficulty_bg_card = card.Card((300, 500), (450, 64), Styles.card.primary())
        self.difficulty_text = text.Text("Difficulty:", 24, (300+10, 500-24), Styles.colors.light_gray())
        self.difficulty_display_text = text.Text(str(global_vars.const_editor_difficulty_names[global_vars.editor_difficulty]).capitalize(), 32, (600, 0))
        self.difficulty_display_text.set_position((self.difficulty_display_text.get_position()[0], 500+tools.Screen.center_axis(self.difficulty_bg_card.get_size()[1], self.difficulty_display_text.get_size()[1])))
        #star icons
        self.star1 = display_image.DisplayImage("assets/icons/star.png", (320, 500+8), (48, 48))
        self.star2 = display_image.DisplayImage("assets/icons/star.png", (370, 500+8), (48, 48))
        self.star3 = display_image.DisplayImage("assets/icons/star.png", (420, 500+8), (48, 48))
        self.star4 = display_image.DisplayImage("assets/icons/star.png", (470, 500+8), (48, 48))
        self.star5 = display_image.DisplayImage("assets/icons/star.png", (520, 500+8), (48, 48))

        #star touch triggers
        self.star1tt = touchtrigger.Touchtrigger((320, 500+8), (48, 48))
        self.star2tt = touchtrigger.Touchtrigger((370, 500+8), (48, 48))
        self.star3tt = touchtrigger.Touchtrigger((420, 500+8), (48, 48))
        self.star4tt = touchtrigger.Touchtrigger((470, 500+8), (48, 48))
        self.star5tt = touchtrigger.Touchtrigger((520, 500+8), (48, 48))

        self.song_card = card.Card((1100, 300), (520, 600), Styles.card.light())
        self.songpicker_btn = button.Button("Pick song...", 32, (1120, 320), (480, 64), Styles.button.primary())
        self.song_file_text = text.Text("No song selected yet!", 32, (1120, 400))
        self.song_bpm_text = text.Text("BPM:", 32, (1120, 450))
        self.song_bpm_input = inputbox.InputBox((150, 48), 32, (1200, 450-12), 3, Styles.inputbox.dark())
        self.song_tap_btn = button.Button("Tap", 32, (1370, 450-12), (120, 48), Styles.button.primary())
        self.song_tap_reset_btn = button.Button("Reset", 24, (1510, 450-12), (64, 48), Styles.button.secondary())
        self.song_tap = [] #for bpm calculation
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.back_btn.is_clicked(event):
            self.manager.switch_to_scene("Editor main menu")
        self.name_input.handle_events(event)
        self.artist_input.handle_events(event)
        if self.star1tt.update(event):
            global_vars.editor_difficulty = 0
        if self.star2tt.update(event):
            global_vars.editor_difficulty = 1
        if self.star3tt.update(event):
            global_vars.editor_difficulty = 2
        if self.star4tt.update(event):
            global_vars.editor_difficulty = 3
        if self.star5tt.update(event):
            global_vars.editor_difficulty = 4
        if self.songpicker_btn.is_clicked(event):
            temp_file = file_picker()
            if temp_file:
                global_vars.editor_filepath = temp_file
                self.song_file_text.set_text(os.path.basename(temp_file))
        self.song_bpm_input.handle_events(event)
        if self.song_tap_btn.is_clicked(event):
            self.song_tap.append(time.time())
            if len(self.song_tap) >= 2:
                intervals = [self.song_tap[i+1] - self.song_tap[i] for i in range(len(self.song_tap)-1)] #get intervals with math magic
                average_interval = sum(intervals) / len(intervals)
                self.song_bpm_input.set_text(str(round(60 / average_interval)))
        if self.song_tap_reset_btn.is_clicked(event):
            self.song_tap = []
            self.song_bpm_input.set_text("")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.back_btn.draw(surface)
        self.name_text.draw(surface)
        self.name_input.draw(surface)
        self.artist_text.draw(surface)
        self.artist_input.draw(surface)
        self.difficulty_text.draw(surface)
        self.difficulty_bg_card.draw(surface)
        self.star1.draw(surface)
        self.star2.draw(surface)
        self.star3.draw(surface)
        self.star4.draw(surface)
        self.star5.draw(surface)
        self.difficulty_display_text.set_text(str(global_vars.const_editor_difficulty_names[global_vars.editor_difficulty]).capitalize())
        self.difficulty_display_text.draw(surface)
        self.song_card.draw(surface)
        self.songpicker_btn.draw(surface)
        self.song_file_text.draw(surface)
        self.song_bpm_text.draw(surface)
        self.song_bpm_input.draw(surface)
        self.song_tap_btn.draw(surface)
        self.song_tap_reset_btn.draw(surface)
    
    def update(self):
        self.fps.tick()