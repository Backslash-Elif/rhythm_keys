import os, time, pygame, global_vars, tools, sound_engine
from scenes import scene

from components import button, text, inputbox, touchtrigger, fpscounter, bgstyle, display_image, card, alert
from components.styles import colors, UI_colors, card_themes, background_gradient

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
        
        self.back_btn = button.Button("Back", 32, (64, global_vars.sys_screen_size[1]-128), (128, 64), UI_colors["danger"])
        #inputs
        self.name_text = text.Text("Enter song name:", 24, (300+10, 300-24), colors["light_gray"][0])
        self.name_input = inputbox.InputBox((700, 48), 32, (300, 300), 32, UI_colors["secondary"])
        self.artist_text = text.Text("Enter song artist:", 24, (300+10, 400-24), colors["light_gray"][0])
        self.artist_input = inputbox.InputBox((700, 48), 32, (300, 400), 32, UI_colors["secondary"])
        #difficulty
        self.difficulty_bg_card = card.Card((300, 500), (450, 64), card_themes["primary"])
        self.difficulty_text = text.Text("Difficulty:", 24, (300+10, 500-24), colors["light_gray"][0])
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

        self.difficulty = 0

        #song selection
        self.song_card = card.Card((1100, 300), (520, 400), card_themes["light"])
        self.songpicker_btn = button.Button("Pick song...", 32, (1120, 320), (480, 64), UI_colors["primary"])
        self.song_file_text = text.Text("No song selected yet!", 32, (1120, 400))
        self.song_bpm_text = text.Text("BPM:", 32, (1120, 450))
        self.song_bpm_input = inputbox.InputBox((150, 48), 32, (1200, 450-12), 3 , UI_colors["secondary"])
        self.song_tap_btn = button.Button("Tap", 32, (1370, 450-12), (130, 48), UI_colors["primary"])
        self.song_tap_reset_btn = button.Button("Reset", 24, (1520, 450-12), (80, 48), UI_colors["danger"])
        self.song_tap = [] #for bpm calculation
        self.song_test = sound_engine.SoundEngine()
        self.song_len_text = text.Text("Length:", 32, (1120, 500))
        self.song_test_btn = button.Button("Play", 32, (1370, 650-18), (130, 48), UI_colors["primary"])
        self.song_test_reset_btn = button.Button("Reset", 24, (1520, 650-18), (80, 48), UI_colors["danger"])

        self.next_btn = button.Button("Next", 32, (global_vars.sys_screen_size[0]-(64+128), global_vars.sys_screen_size[1]-128), (128, 64), UI_colors["primary"])

        self.alert_object = alert.Alert()
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.alert_object.is_active():
            self.alert_object.handle_events(event)
        else:
            if self.back_btn.is_clicked(event):
                self.manager.switch_to_scene("Editor main menu")
            self.name_input.handle_events(event)
            self.artist_input.handle_events(event)
            if self.star1tt.update(event):
                self.difficulty = 0
            if self.star2tt.update(event):
                self.difficulty = 1
            if self.star3tt.update(event):
                self.difficulty = 2
            if self.star4tt.update(event):
                self.difficulty = 3
            if self.star5tt.update(event):
                self.difficulty = 4
            if self.songpicker_btn.is_clicked(event): #load file
                temp_file = file_picker()
                if temp_file:
                    global_vars.editor_filepath = temp_file
                    self.song_file_text.set_text(os.path.basename(temp_file))
                    self.song_test.load(temp_file)
                    song_m = int(self.song_test.get_song_len() / 60)
                    song_s = int(self.song_test.get_song_len() % 60)
                    if type(self.song_test.get_song_len() == float):
                        self.song_len_text.set_text(f"Length: {song_m}min {song_s}sec ({round(self.song_test.get_song_len(), 3)}sec)")
                    else:
                        self.song_len_text.set_text(f"Length: {song_m}min {song_s}sec ({int(self.song_test.get_song_len())}sec)")
            self.song_bpm_input.handle_events(event)
            if self.song_tap_btn.is_clicked(event): #bpm logic
                self.song_tap.append(time.time())
                if len(self.song_tap) >= 8:
                    intervals = [self.song_tap[i+1] - self.song_tap[i] for i in range(len(self.song_tap)-1)] #get intervals with math magic
                    average_interval = sum(intervals) / len(intervals)
                    self.song_bpm_input.set_text(str(round(60 / average_interval)+1)) #+1 because it was always one too low
                else:
                    self.song_bpm_input.set_text("Computing...")
            if self.song_tap_reset_btn.is_clicked(event): #bpm reset
                self.song_tap = []
                self.song_bpm_input.set_text("")
            if self.song_test_btn.is_clicked(event):
                if self.song_test.song_loaded():
                    if self.song_test.get_play_state() == 1:
                        self.song_test.pause()
                        self.song_test_btn.set_text("Resume")
                    else:
                        self.song_test.play()
                        self.song_test_btn.set_text("Pause")
            if self.song_test_reset_btn.is_clicked(event):
                if self.song_test.song_loaded():
                    self.song_test.stop()
                    self.song_test_btn.set_text("Play")
            if self.next_btn.is_clicked(event): #next button trigger
                if self.name_input.get_text() and self.artist_input.get_text() and self.song_bpm_input.get_text().isnumeric() and global_vars.editor_filepath:
                    global_vars.editor_name = self.name_input.get_text()
                    global_vars.editor_author = global_vars.user_name
                    global_vars.editor_song_artist = self.artist_input.get_text()
                    global_vars.editor_length = self.song_test.get_song_len()
                    global_vars.editor_difficulty = self.difficulty
                    self.manager.switch_to_scene("Editor")
                else:
                    self.alert_object.new_alert("Fill out all fields!")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
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
        self.song_len_text.draw(surface)
        self.song_test_btn.draw(surface)
        self.song_test_reset_btn.draw(surface)
        self.next_btn.draw(surface)
        self.alert_object.draw(surface)
    
    def update(self):
        self.fps.tick()