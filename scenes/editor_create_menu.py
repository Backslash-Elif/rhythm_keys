import os, time, global_vars, utils, sound_engine
from scenes import scene

from components import button, debug, text, inputbox, touchtrigger, bgstyle, display_image, card, alert
from components.styles import colors, UI_colors, background_gradient, card_themes, ColorName, UIColorName, CardThemeName, text_size, TextSizeName

import tkinter as tk
from tkinter import filedialog


def file_picker():
    #make rootwindow and hide it
    root = tk.Tk()
    root.withdraw()

    #file allow list
    file_types = [("Compressed Audio Format", "*.mp3;*.ogg")]

    #file dialog
    file_path = filedialog.askopenfilename(title="Select an Audio File", filetypes=file_types)
    return file_path

class EditorCreateMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        utils.sanatize_editor_vars()
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        self.back_btn = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
        self.fg_cardobject = card.Card((200, 200), (1500, 600), card_themes[CardThemeName.DYNAMIC])

        #inputs
        self.name_text = text.Text("Enter song name:", text_size[TextSizeName.SMALL_TEXT], (300, 250), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.name_input = inputbox.InputBox((700, 48), text_size[TextSizeName.TEXT], (300, 300), 32, UI_colors[UIColorName.SECONDARY])
        self.artist_text = text.Text("Enter song artist:", text_size[TextSizeName.SMALL_TEXT], (300, 350), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.artist_input = inputbox.InputBox((700, 48), text_size[TextSizeName.TEXT], (300, 400), 32, UI_colors[UIColorName.SECONDARY])

        #difficulty
        self.difficulty_bg_card = card.Card((300-10, 500-10), (450+20, 100+20), card_themes[CardThemeName.PRIMARY])
        self.difficulty_text = text.Text("Difficulty", text_size[TextSizeName.SMALL_TEXT], (300, 500), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.TOP_LEFT)
        self.difficulty_display_text = text.Text(str(global_vars.const_editor_difficulty_names[global_vars.editor_difficulty]).capitalize(), 32, (600, 550), (100, 50), colors[ColorName.DYNAMIC][0])
        self.star_imageobject = display_image.DisplayImage("assets/icons/star.png", (300, 550), (49, 49))
        self.star_triggerobject = touchtrigger.Touchtrigger((300, 550), (49, 49))
        self.difficulty = 0

        #song selection
        self.songpicker_btn = button.Button("Pick song...", text_size[TextSizeName.TEXT], (1100, 300), (500, 50), UI_colors[UIColorName.PRIMARY])
        self.song_file_text = text.Text("No song selected yet!", text_size[TextSizeName.TEXT], (1100, 350), (500, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.song_bpm_text = text.Text("BPM:", text_size[TextSizeName.TEXT], (1100, 500), (100, 50), colors[ColorName.DYNAMIC][0])
        self.song_bpm_input = inputbox.InputBox((130, 50), text_size[TextSizeName.TEXT], (1200, 500), 3 , UI_colors[UIColorName.SECONDARY])
        self.song_tap_btn = button.Button("Tap", text_size[TextSizeName.TEXT], (1350, 500), (150, 50), UI_colors[UIColorName.PRIMARY])
        self.song_tap_reset_btn = button.Button("Reset", text_size[TextSizeName.SMALL_TEXT], (1520, 500), (80, 50), UI_colors[UIColorName.DANGER])
        self.song_tap = [] #for bpm calculation
        self.song_len_text = text.Text("Length:", text_size[TextSizeName.TEXT], (1100, 400), (500, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.song_test_btn = button.Button("Play", text_size[TextSizeName.TEXT], (1350, 650), (150, 50), UI_colors[UIColorName.PRIMARY])
        self.song_test_reset_btn = button.Button("Reset", text_size[TextSizeName.SMALL_TEXT], (1520, 650), (80, 50), UI_colors[UIColorName.DANGER])
        self.testprogress_textobject = text.Text("--:--", text_size[TextSizeName.TEXT], (1200, 650), (150, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.TOP)
        self.testbeat_textobject = text.Text("Beat --/--", text_size[TextSizeName.SMALL_TEXT], (1200, 650), (150, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM)

        self.next_btn = button.Button("Next", text_size[TextSizeName.TEXT], (1750, 950), (100, 50), UI_colors[UIColorName.PRIMARY])

        self.alert_object = alert.Alert()
        self.soundengine = sound_engine.SoundEngine()

        self.switch_to_editor = 0 #loading the editor took long so added a messagebox to explain the waiting time. the alert has to be drawn first tho
    
    def handle_event(self, event):
        self.soundengine.handle_events(event)
        if self.alert_object.is_active():
            self.alert_object.handle_events(event)

        else: #events aren't processed if the alert is active
            #general event handles
            self.name_input.handle_events(event)
            self.artist_input.handle_events(event)
            self.song_bpm_input.handle_events(event)

            if self.back_btn.is_clicked(event): #back button
                utils.sanatize_editor_vars()
                self.manager.switch_to_scene("Editor main menu")

            for i in range(5): #setting dificulty 
                self.star_triggerobject.set_pos((300+50*i, 550))
                if self.star_triggerobject.update(event):
                    self.difficulty = i

            if self.songpicker_btn.is_clicked(event): #select and load file
                temp_file = file_picker()
                if temp_file:
                    global_vars.editor_filepath = temp_file
                    self.song_file_text.set_text(os.path.basename(temp_file))
                    self.soundengine.load(temp_file)
                    song_m = int(self.soundengine.get_song_len() / 60)
                    song_s = int(self.soundengine.get_song_len() % 60)
                    if type(self.soundengine.get_song_len() == float):
                        self.song_len_text.set_text(f"Length: {song_m}min {song_s}sec ({round(self.soundengine.get_song_len(), 3)}sec)")
                    else:
                        self.song_len_text.set_text(f"Length: {song_m}min {song_s}sec ({int(self.soundengine.get_song_len())}sec)")
            
            if self.song_tap_btn.is_clicked(event): #bpm logic
                self.song_tap.append(time.time())
                if len(self.song_tap) >= 8:
                    intervals = [self.song_tap[i+1] - self.song_tap[i] for i in range(len(self.song_tap)-1)] #get intervals with math magic
                    average_interval = sum(intervals) / len(intervals)
                    self.song_bpm_input.set_text(str(round(60 / average_interval)))
                else:
                    self.song_bpm_input.set_text("Computing...")
            
            if self.song_tap_reset_btn.is_clicked(event): #bpm reset
                self.song_tap = []
                self.song_bpm_input.set_text("")
            
            if self.song_test_btn.is_clicked(event): #song preview button
                if self.soundengine.song_loaded():
                    if self.soundengine.get_play_state() == 1:
                        self.soundengine.pause()
                        self.song_test_btn.set_text("Resume")
                    else:
                        self.soundengine.play()
                        self.song_test_btn.set_text("Pause")
            
            if self.song_test_reset_btn.is_clicked(event): #song preview reset
                if self.soundengine.song_loaded():
                    self.soundengine.stop()
                    self.song_test_btn.set_text("Play")
            
            if self.next_btn.is_clicked(event): #next button trigger
                if self.name_input.get_text() and self.artist_input.get_text() and self.song_bpm_input.get_text().isnumeric() and global_vars.editor_filepath:
                    global_vars.editor_name = self.name_input.get_text()
                    global_vars.editor_author = global_vars.user_name
                    global_vars.editor_song_artist = self.artist_input.get_text()
                    global_vars.editor_length = self.soundengine.get_song_len()
                    global_vars.editor_difficulty = self.difficulty
                    global_vars.editor_bpm = int(self.song_bpm_input.get_text())
                    self.alert_object.new_alert("Please wait.\n\nPreparing files & Initialising editor...")
                    newfile = utils.copy_audio_to_working_dir(global_vars.editor_filepath)
                    global_vars.editor_filepath = newfile
                    self.switch_to_editor = 1
                else:
                    self.alert_object.new_alert("Fill out all fields!")
    
    def draw(self, surface):
        #this hack is here so the scene switch takes place one frame later so the alert has one frame where it can draw itself
        if self.switch_to_editor > 1:
            self.manager.switch_to_scene("Editor")
        if self.switch_to_editor > 0:
            self.switch_to_editor += 1
        
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background
        self.back_btn.draw(surface)
        self.fg_cardobject.draw(surface)
        self.name_text.draw(surface)
        self.name_input.draw(surface)
        self.artist_text.draw(surface)
        self.artist_input.draw(surface)
        self.difficulty_bg_card.draw(surface)
        self.difficulty_text.draw(surface)

        for i in range(5): #drawing stars 
            self.star_imageobject.set_pos((300+50*i, 550))
            if self.star_imageobject.draw(surface):
                self.difficulty = i

        if global_vars.sys_debug_lvl > 0:
            for i in range(5): #drawing stars 
                self.star_triggerobject.set_pos((300+50*i, 550))
                if self.star_triggerobject.draw_debug(surface):
                    self.difficulty = i

        self.difficulty_display_text.set_text(str(global_vars.const_editor_difficulty_names[self.difficulty]).capitalize()) #gets and sets the correct difficulty
        self.difficulty_display_text.draw(surface)

        self.songpicker_btn.draw(surface)
        self.song_file_text.draw(surface)
        self.song_bpm_text.draw(surface)
        self.song_bpm_input.draw(surface)
        self.song_tap_btn.draw(surface)
        self.song_tap_reset_btn.draw(surface)
        self.song_len_text.draw(surface)
        self.song_test_btn.draw(surface)
        self.song_test_reset_btn.draw(surface)

        self.testprogress_textobject.set_text(f"{str(int(float(self.soundengine.get_song_progress())/60)).zfill(2)}:{str(int(float(self.soundengine.get_song_progress())%60)).zfill(2)}" if global_vars.editor_filepath else "--:--") #setting the time display text
        self.testprogress_textobject.draw(surface)
        self.testbeat_textobject.set_text(f"Beat {int(float(self.soundengine.get_song_progress())*(int(self.song_bpm_input.get_text())/60))}/{int(self.soundengine.get_song_len()*(int(self.song_bpm_input.get_text())/60))}" if self.song_bpm_input.get_text().isnumeric() else "Beat --/--") #setting the beat display text
        self.testbeat_textobject.draw(surface)

        self.next_btn.draw(surface)
        self.alert_object.draw(surface)

        #draws debug information
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)