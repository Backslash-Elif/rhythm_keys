import global_vars, utils, sound_engine, pygame
from decimal import Decimal
from scenes import scene

from components import debug, touchtrigger, text, bgstyle, button, card, display_image, alert, key_reader, inputbox, rectangle
from components.styles import text_size, card_themes, UI_colors, background_gradient, UIColorName, CardThemeName, TextSizeName, colors, ColorName
from utils import hextobits, bitstohex, loadfromlvldat

class EditorEditor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #UI
        self.title_textobject = text.Text(global_vars.editor_name, text_size[TextSizeName.TITLE], (1050, 100), (700, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.subtitle_textobject = text.Text(global_vars.editor_song_artist, text_size[TextSizeName.SUBTITLE], (1050, 200), (700, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.titledevider_cardobject = card.Card((1050, 200), (300, 6), card_themes[CardThemeName.LIGHT] if global_vars.user_dark_mode else card_themes[CardThemeName.DARK])

        self.tilebg_cardobject = card.Card((300, 0), (650, 1080), card_themes[CardThemeName.DARK])

        self.savebtn_buttonobject = button.Button("Save", text_size[TextSizeName.SUBTITLE], (1050, 300), (130, 50), UI_colors[UIColorName.PRIMARY])
        self.exitbtn_buttonobject = button.Button("Exit", text_size[TextSizeName.TEXT], (1300, 300), (80, 50), UI_colors[UIColorName.DANGER])
        self.testbtn_buttonobject = button.Button("Test", text_size[TextSizeName.TEXT], (1200, 300), (80, 50), UI_colors[UIColorName.SUCCESS])
        self.settingsbtn_buttonobject = button.Button("Settings...", text_size[TextSizeName.TEXT], (1050, 400), (200, 50), UI_colors[UIColorName.SECONDARY])
        self.delscreen_buttonobject = button.Button("Delete all on screen", text_size[TextSizeName.TEXT], (1050, 500), (200, 50), UI_colors[UIColorName.DANGER])
        self.delscreen = False

        #speed & media control
        self.mediactrl_cardobject = card.Card((1040, 740), (520, 270), card_themes[CardThemeName.DARK])
        self.mediactrllabel_textobject = text.Text("Speed & Media Control", text_size[TextSizeName.TEXT], (1050, 750), (500, 50), colors[ColorName.DYNAMIC][1])
        self.mediaprogress1_textobject = text.Text("--:--", text_size[TextSizeName.SUBTITLE], (1100, 800), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.mediaprogress2_textobject = text.Text("beat --/--\n@--BPM", text_size[TextSizeName.TEXT], (1100, 800), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.RIGHT)
        self.fastback_buttonobject = button.Button("", text_size[TextSizeName.SUBTITLE], (1060, 910), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.fastback_imageobject = display_image.DisplayImage("assets/icons/fast-back.png", (1060, 910), (80, 80))
        self.back_buttonobject = button.Button("", text_size[TextSizeName.SUBTITLE], (1160, 910), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.back_imageobject = display_image.DisplayImage("assets/icons/back.png", (1160, 910), (80, 80))
        self.playpause_buttonobject = button.Button("", text_size[TextSizeName.SUBTITLE], (1260, 910), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.play_imageobject = display_image.DisplayImage("assets/icons/play.png", (1260, 910), (80, 80))
        self.pause_imageobject = display_image.DisplayImage("assets/icons/pause.png", (1260, 910), (80, 80))
        self.forward_buttonobject = button.Button("", text_size[TextSizeName.SUBTITLE], (1360, 910), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.forward_imageobject = display_image.DisplayImage("assets/icons/forward.png", (1360, 910), (80, 80))
        self.fastforward_buttonobject = button.Button("", text_size[TextSizeName.SUBTITLE], (1460, 910), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.fastforward_imageobject = display_image.DisplayImage("assets/icons/fast-forward.png", (1460, 910), (80, 80))

        #arrows
        self.static_arrow_u_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/up.png", (350, 50), (100, 100))
        self.static_arrow_d_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/down.png", (500, 50), (100, 100))
        self.static_arrow_l_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/left.png", (650, 50), (100, 100))
        self.static_arrow_r_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/right.png", (800, 50), (100, 100))

        self.arrow_u_imageobject = display_image.DisplayImage("assets/arrows/smol/up.png", (350, 50), (100, 100))
        self.arrow_d_imageobject = display_image.DisplayImage("assets/arrows/smol/down.png", (500, 50), (100, 100))
        self.arrow_l_imageobject = display_image.DisplayImage("assets/arrows/smol/left.png", (650, 50), (100, 100))
        self.arrow_r_imageobject = display_image.DisplayImage("assets/arrows/smol/right.png", (800, 50), (100, 100))

        #beat allign
        self.beatallign_rectangleobject = rectangle.Rectangle((350, 0), (550, 3), colors[ColorName.WHITE][0])
        
        #arrow selection
        self.tilebg_triggerobject = touchtrigger.Touchtrigger((300, 0), (650, 1080)) #trigger for mouse
        self.arrow_triggerobject = touchtrigger.Touchtrigger((0, 0), (100, 100)) #trigger for mouse
        self.select_imageobject = display_image.DisplayImage("assets/icons/selected.png", (0, 0), (100, 100))
        self.selected_arrow = None #if selected: [beat, track]

        #settings
        self.settings_cardobject = card.Card((200, 200), (1500, 600), card_themes[CardThemeName.DYNAMIC])
        self.settings_disclaimer_cardobject = card.Card((1090, 240), (520, 120), card_themes[CardThemeName.WARNING])
        self.settings_disclaimer_textobject = text.Text("WARNING: Those settings severely change\nhow the editor records input.\nA backup is recommended.", text_size[TextSizeName.TEXT], (1100, 250), (500, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.CENTER)
        self.name_textobject = text.Text("Song name", text_size[TextSizeName.SMALL_TEXT], (300, 250), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.name_inputobject = inputbox.InputBox((700, 48), text_size[TextSizeName.TEXT], (300, 300), 32, UI_colors[UIColorName.SECONDARY])
        self.artist_textobject = text.Text("Song artist", text_size[TextSizeName.SMALL_TEXT], (300, 350), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.artist_inputobject = inputbox.InputBox((700, 48), text_size[TextSizeName.TEXT], (300, 400), 32, UI_colors[UIColorName.SECONDARY])
        
        #difficulty
        self.difficulty_bg_cardobject = card.Card((300-10, 500-10), (450+20, 100+20), card_themes[CardThemeName.PRIMARY])
        self.difficulty_textobject = text.Text("Difficulty", text_size[TextSizeName.SMALL_TEXT], (300, 500), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.TOP_LEFT)
        self.difficulty_display_textobject = text.Text(str(global_vars.const_editor_difficulty_names[global_vars.editor_difficulty]).capitalize(), 32, (600, 550), (100, 50), colors[ColorName.DYNAMIC][0])
        self.star_imageobject = display_image.DisplayImage("assets/icons/star.png", (300, 550), (49, 49))
        self.star_triggerobject = touchtrigger.Touchtrigger((300, 550), (49, 49))
        
        #other settings
        self.bpm_textobject = text.Text("BPM", text_size[TextSizeName.SMALL_TEXT], (1100, 350), (100, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.bpm_inputobject = inputbox.InputBox((100, 48), text_size[TextSizeName.TEXT], (1100, 400), 3, UI_colors[UIColorName.SECONDARY])
        self.bpm_buttonobject = button.Button("?", text_size[TextSizeName.TEXT], (1550, 400), (50, 50), UI_colors[UIColorName.SECONDARY])

        self.snaps_textobject = text.Text("Snaps per beat", text_size[TextSizeName.SMALL_TEXT], (1100, 450), (200, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.snaps_inputobject = inputbox.InputBox((100, 48), text_size[TextSizeName.TEXT], (1100, 500), 2, UI_colors[UIColorName.SECONDARY])
        self.snaps_buttonobject = button.Button("?", text_size[TextSizeName.TEXT], (1550, 500), (50, 50), UI_colors[UIColorName.SECONDARY])

        self.delay_textobject = text.Text("Songdelay", text_size[TextSizeName.SMALL_TEXT], (1100, 550), (100, 50), colors[ColorName.DYNAMIC][1], text.TextAlign.BOTTOM_LEFT)
        self.delay_inputobject = inputbox.InputBox((100, 48), text_size[TextSizeName.TEXT], (1100, 600), 6, UI_colors[UIColorName.SECONDARY])
        self.delay_buttonobject = button.Button("?", text_size[TextSizeName.TEXT], (1550, 600), (50, 50), UI_colors[UIColorName.SECONDARY])
        self.ms_display_textobject = text.Text("ms", text_size[TextSizeName.TEXT], (1200, 600), (50, 50), colors[ColorName.DYNAMIC][0])

        #save & discard buttons
        self.savesettings_buttonobject = button.Button("Save", text_size[TextSizeName.TEXT], (1500, 700), (100, 50), UI_colors[UIColorName.PRIMARY])
        self.discardsettings_buttonobject = button.Button("Discard Settings", text_size[TextSizeName.TEXT], (1250, 700), (200, 50), UI_colors[UIColorName.DANGER])

        self.settings_hidden = True

        #misc
        self.soundengine = sound_engine.SoundEngine()
        self.soundengine.load(global_vars.editor_filepath)

        self.alertobject = alert.Alert()
        self.keyreaderobject = key_reader.KeyReader()

        self.framekeys = set() #keyset for new inputs

        self.alertid = 0 #0=nothing, 1=exit, 2=settings save, 3=settings discard

        utils.save_level() #init leveldata

        if global_vars.editor_uuid == "":
            global_vars.editor_uuid = utils.generate_uuid()

    def handle_event(self, event):
        self.keyreaderobject.handle_events(event)
        self.soundengine.handle_events(event)
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
            if self.alertobject.get_result() != None:
                if self.alertid == 1:
                    if self.alertobject.get_result():
                        utils.save_level()
                        utils.load_lvl_list()
                        utils.create_package(global_vars.editor_uuid)
                        global_vars.editor_uuid = ""
                        self.soundengine.eject()
                        self.manager.switch_to_scene("Editor main menu")
                if self.alertid == 2:
                    if self.alertobject.get_result():
                        if self.bpm_inputobject.get_text().isnumeric() and self.snaps_inputobject.get_text().isnumeric() and self.delay_inputobject.get_text().replace("-", "").isnumeric():
                            global_vars.editor_name = self.name_inputobject.get_text()
                            global_vars.editor_song_artist = self.artist_inputobject.get_text()
                            global_vars.editor_bpm = int(self.bpm_inputobject.get_text())
                            global_vars.editor_snap_value = int(self.snaps_inputobject.get_text())
                            global_vars.editor_startdelay = Decimal(self.delay_inputobject.get_text())/Decimal('1000.0')
                            self.title_textobject.set_text(global_vars.editor_name)
                            self.subtitle_textobject.set_text(global_vars.editor_song_artist)
                            self.settings_hidden = True
                        else:
                            self.alertobject.new_alert("Faulty input values!")
                if self.alertid == 3:
                    if self.alertobject.get_result():
                        self.settings_hidden = True
                self.alertid = 0
        else: #events aren't processed if the alert is active
            if self.settings_hidden:
                self.framekeys.add(self.keyreaderobject.get_pressed_key(event))#get newly pressed keys

                if self.exitbtn_buttonobject.is_clicked(event): #exit button
                    self.alertobject.new_alert("Are you sure you want to quit?\n\n\nYou will be able to find your\nlevel in the level selector", 1)
                    self.alertid = 1

                if self.testbtn_buttonobject.is_clicked(event): #test button
                    utils.save_level()
                    global_vars.sys_persistant_storage["editortest"] = True
                    self.manager.switch_to_scene("Game")

                #media controls
                if self.fastback_buttonobject.is_clicked(event):#back 10s
                    self.soundengine.seek_to(max(self.soundengine.get_song_progress() - 10, 0.0))
                if self.back_buttonobject.is_clicked(event):#back 5s
                    self.soundengine.seek_to(max(self.soundengine.get_song_progress() - 5, 0.0))
                if self.playpause_buttonobject.is_clicked(event) or self.keyreaderobject.get_pressed_key(event) == "space":#play/pause
                    self.soundengine.pause() if self.soundengine.get_play_state() == 1 else self.soundengine.play()
                if self.fastforward_buttonobject.is_clicked(event):#forward 5s
                    self.soundengine.seek_to(min(self.soundengine.get_song_progress() + 10, self.soundengine.get_song_len()))
                if self.forward_buttonobject.is_clicked(event):#forward 10s
                    self.soundengine.seek_to(min(self.soundengine.get_song_progress() + 5, self.soundengine.get_song_len()))

                if self.savebtn_buttonobject.is_clicked(event): #save button
                    utils.save_level()
                    self.alertobject.new_alert("Saved successfully!")

                if self.settingsbtn_buttonobject.is_clicked(event): #settings button
                    self.settings_hidden = False
                    #populate the inputs
                    self.name_inputobject.set_text(global_vars.editor_name)
                    self.artist_inputobject.set_text(global_vars.editor_song_artist)
                    self.bpm_inputobject.set_text(str(global_vars.editor_bpm))
                    self.snaps_inputobject.set_text(str(global_vars.editor_snap_value))
                    self.delay_inputobject.set_text(str(int(global_vars.editor_startdelay * Decimal('1000.0'))))
                
                if self.delscreen_buttonobject.is_clicked(event):
                    self.delscreen = True

                #arrow selection algorythm
                if self.tilebg_triggerobject.update(event) and self.soundengine.get_play_state() != 1:
                    beat = float((self.soundengine.get_song_progress())*Decimal(global_vars.editor_bpm/60))
                    tempselect = None
                    for key, value in global_vars.editor_lvldat.items(): #iterate over every level data item
                        if key > beat-10 and key < beat+2: #select only the visible ones
                            tempdata = hextobits(value) #unpackage data
                            temppos = (beat - key) * 100 + 50
                            for i, t in zip(range(4), tempdata): #plot the trigger and test for button press
                                if t:
                                    self.arrow_triggerobject.set_pos((350+150*i, temppos))
                                    if self.arrow_triggerobject.update(event):
                                        tempselect = [key, i]
                    self.selected_arrow = tempselect

                #scrolling
                if self.soundengine.get_play_state() > 1:
                    if event.type == pygame.MOUSEWHEEL:
                        if event.y > 0:
                            self.soundengine.seek_to(min(self.soundengine.get_song_progress() + Decimal(1/global_vars.editor_snap_value), self.soundengine.get_song_len()))
                        elif event.y < 0:
                            self.soundengine.seek_to(max(self.soundengine.get_song_progress() - Decimal(1/global_vars.editor_snap_value), 0.0))
                        self.soundengine.pause()

            else:
                self.name_inputobject.handle_events(event)
                self.artist_inputobject.handle_events(event)
                self.bpm_inputobject.handle_events(event)
                self.snaps_inputobject.handle_events(event)
                self.delay_inputobject.handle_events(event)

                for i in range(5): #setting dificulty 
                    self.star_triggerobject.set_pos((300+50*i, 550))
                    if self.star_triggerobject.update(event):
                        self.difficulty = i
                
                if self.bpm_buttonobject.is_clicked(event):
                    self.alertobject.new_alert("BPM stands for Beats Per Minute and\nis a measure of tempo in music.\n\nIt indicates how many\nbeats occur in one minute.")
                
                if self.snaps_buttonobject.is_clicked(event):
                    self.alertobject.new_alert("This value determines how often the\ninput aligns with the beat.\nFor example, if you set it to 4, the input\nwill adjust every 0.25 beats (or a quarter\nof a beat).\n\nIf you're unsure,\nset it to 4 as it works well with most songs.")
                
                if self.delay_buttonobject.is_clicked(event):
                    self.alertobject.new_alert("If the song doesn't lign up exactly with\nthe beat, you can delay or advance the song\nto better match the beat.")
                
                if self.savesettings_buttonobject.is_clicked(event):
                    self.alertobject.new_alert("Save settings and exit?", 1)
                    self.alertid = 2
                
                if self.discardsettings_buttonobject.is_clicked(event):
                    self.alertobject.new_alert("Revert back to old settings and exit?", 1)
                    self.alertid = 3

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background
        if self.settings_hidden:
            
            self.exitbtn_buttonobject.draw(surface)
            self.title_textobject.draw(surface)
            self.subtitle_textobject.draw(surface)
            self.titledevider_cardobject.draw(surface)
            self.tilebg_cardobject.draw(surface)
            self.savebtn_buttonobject.draw(surface)
            self.testbtn_buttonobject.draw(surface)
            self.settingsbtn_buttonobject.draw(surface)
            self.delscreen_buttonobject.draw(surface)
            self.mediactrl_cardobject.draw(surface)
            self.mediactrllabel_textobject.draw(surface)

            corrected_song_progress = self.soundengine.get_song_progress()+global_vars.editor_startdelay if self.soundengine.get_song_progress()+global_vars.editor_startdelay >= Decimal('0.0') else Decimal('0.0') #compute the corrected song progress (compensating for song start delay)
            self.mediaprogress1_textobject.set_text(f"{str(int(float(corrected_song_progress)/60)).zfill(2)}:{str(int(float(corrected_song_progress)%60)).zfill(2)}") #setting progress in s:m
            self.mediaprogress2_textobject.set_text(f"Beat {int(float(self.soundengine.get_song_progress()+global_vars.editor_startdelay)*(global_vars.editor_bpm/60))}/{int(global_vars.editor_length*(global_vars.editor_bpm/60))}\n@{global_vars.editor_bpm}BPM") #setting beat progress
            
            self.mediaprogress1_textobject.draw(surface)
            self.mediaprogress2_textobject.draw(surface)
            self.fastback_buttonobject.draw(surface)
            self.fastback_imageobject.draw(surface)
            self.back_buttonobject.draw(surface)
            self.back_imageobject.draw(surface)
            self.playpause_buttonobject.draw(surface)

            self.pause_imageobject.draw(surface) if self.soundengine.get_play_state() == 1 else self.play_imageobject.draw(surface)

            self.forward_buttonobject.draw(surface)
            self.forward_imageobject.draw(surface)
            self.fastforward_buttonobject.draw(surface)
            self.fastforward_imageobject.draw(surface)
            self.static_arrow_u_imageobject.draw(surface)
            self.static_arrow_d_imageobject.draw(surface)
            self.static_arrow_l_imageobject.draw(surface)
            self.static_arrow_r_imageobject.draw(surface)

            beat = float((self.soundengine.get_song_progress()+global_vars.editor_startdelay)*Decimal(str(global_vars.editor_bpm/60)))

            #beat allign
            beatoffset = int(str(beat).split('.')[1][0:2].ljust(2, "0"))
            for i in range(12):
                self.beatallign_rectangleobject.set_position((350, (-51)+100*i+beatoffset))
                self.beatallign_rectangleobject.draw(surface)

            #plot algorythm
            for key, value in global_vars.editor_lvldat.copy().items(): #iterate through all items
                if key > beat-10 and key < beat+2: #only select visible
                    if self.delscreen:
                        global_vars.editor_lvldat.pop(key) #removes all on screen
                    tempdata = hextobits(value) #unpack leveldata
                    temppos = (beat - key) * 100 + 50
                    #plot the arrows
                    if tempdata[0]:
                        self.arrow_u_imageobject.set_pos((350, temppos))
                        self.arrow_u_imageobject.draw(surface)
                    if tempdata[1]:
                        self.arrow_d_imageobject.set_pos((500, temppos))
                        self.arrow_d_imageobject.draw(surface)
                    if tempdata[2]:
                        self.arrow_l_imageobject.set_pos((650, temppos))
                        self.arrow_l_imageobject.draw(surface)
                    if tempdata[3]:
                        self.arrow_r_imageobject.set_pos((800, temppos))
                        self.arrow_r_imageobject.draw(surface)
            
            if self.delscreen:
                self.delscreen = False
                self.selected_arrow = None

            #arrow selection
            if self.selected_arrow:
                self.select_imageobject.set_pos((350+150*self.selected_arrow[1], (beat - self.selected_arrow[0]) * 100 + 50))
                self.select_imageobject.draw(surface)

            #arrow alteration
            if self.selected_arrow:
                tempkeys = list(self.framekeys) #get the newly pressed down keys
                if "up" in tempkeys: #moves the arow up one snapping position
                    tempdata = hextobits(loadfromlvldat(self.selected_arrow[0]))
                    tempdata[self.selected_arrow[1]] = False
                    newbeat = min(int(global_vars.editor_length*(global_vars.editor_bpm/60)), round((self.selected_arrow[0] + 1/global_vars.editor_snap_value) * global_vars.editor_snap_value)/global_vars.editor_snap_value)
                    if newbeat<beat: #only save newly calculated position if it is valid
                        newdata = hextobits(loadfromlvldat(newbeat))
                        newdata[self.selected_arrow[1]] = True
                        global_vars.editor_lvldat[self.selected_arrow[0]] = bitstohex(tempdata)
                        global_vars.editor_lvldat[newbeat] = bitstohex(newdata)
                        self.selected_arrow[0] = newbeat

                if "down" in tempkeys: #moves the arow up one snapping position
                    tempdata = hextobits(loadfromlvldat(self.selected_arrow[0]))
                    tempdata[self.selected_arrow[1]] = False
                    newbeat = max(0, round((self.selected_arrow[0] - 1/global_vars.editor_snap_value) * global_vars.editor_snap_value)/global_vars.editor_snap_value)
                    if newbeat>beat-10: #only save newly calculated position if it is valid
                        newdata = hextobits(loadfromlvldat(newbeat))
                        newdata[self.selected_arrow[1]] = True
                        global_vars.editor_lvldat[self.selected_arrow[0]] = bitstohex(tempdata)
                        global_vars.editor_lvldat[newbeat] = bitstohex(newdata)
                        self.selected_arrow[0] = newbeat
                
                if "left" in tempkeys: #moves the selected arrow one track to the left (if there is any)
                    tempdata = hextobits(loadfromlvldat(self.selected_arrow[0]))
                    tempdata[self.selected_arrow[1]] = False
                    tempdata[max(0, self.selected_arrow[1]-1)] = True
                    global_vars.editor_lvldat[self.selected_arrow[0]] = bitstohex(tempdata)
                    self.selected_arrow[1] = max(0, self.selected_arrow[1]-1)

                if "right" in tempkeys: #moves the selected arrow one track to the left (if there is any)
                    tempdata = hextobits(loadfromlvldat(self.selected_arrow[0]))
                    tempdata[self.selected_arrow[1]] = False
                    tempdata[min(3, self.selected_arrow[1]+1)] = True
                    global_vars.editor_lvldat[self.selected_arrow[0]] = bitstohex(tempdata)
                    self.selected_arrow[1] = min(3, self.selected_arrow[1]+1)
                
                for i in ("backspace", "delete"): #deletes the selected arrow
                    if i in tempkeys:
                        tempdata = hextobits(loadfromlvldat(self.selected_arrow[0]))
                        tempdata[self.selected_arrow[1]] = False
                        global_vars.editor_lvldat[self.selected_arrow[0]] = bitstohex(tempdata)
                        self.selected_arrow = None
                
                if "escape" in tempkeys:
                    self.selected_arrow = None
                        
            
            #reader algorythm
            rounded_beat = round(beat * global_vars.editor_snap_value)/global_vars.editor_snap_value #compute the beat (which snaps to the selected snap value)
            if self.soundengine.get_play_state() == 1: #if music is playing
                tempkeys = list(self.framekeys) #get the newly pressed keys
                tempdata = hextobits(loadfromlvldat(rounded_beat)) #unpack leveldata
                for i, direction in zip(range(4), ("up", "down", "left", "right")): #iterate through every direction and append a 
                    tempdata[i] = True if direction in tempkeys else tempdata[i]
                if True in tempdata: #discard data that's all 0
                    global_vars.editor_lvldat[rounded_beat] = bitstohex(tempdata) #repack leveldata

            self.framekeys.clear()#clear newly pressed keys
        else:
            self.settings_cardobject.draw(surface)
            self.settings_disclaimer_cardobject.draw(surface)
            self.name_textobject.draw(surface)
            self.name_inputobject.draw(surface)
            self.artist_textobject.draw(surface)
            self.artist_inputobject.draw(surface)

            #difficulty
            self.difficulty_bg_cardobject.draw(surface)
            self.difficulty_display_textobject.set_text(global_vars.const_editor_difficulty_names[global_vars.editor_difficulty].capitalize())
            self.difficulty_textobject.draw(surface)
            self.difficulty_display_textobject.draw(surface)

            #star icons
            for i in range(5): #drawing stars 
                self.star_imageobject.set_pos((300+50*i, 550))
                if self.star_imageobject.draw(surface):
                    self.difficulty = i
            
            self.settings_disclaimer_textobject.draw(surface)
            self.bpm_textobject.draw(surface)
            self.bpm_inputobject.draw(surface)
            self.bpm_buttonobject.draw(surface)
            self.snaps_textobject.draw(surface)
            self.snaps_inputobject.draw(surface)
            self.snaps_buttonobject.draw(surface)
            self.delay_textobject.draw(surface)
            self.delay_inputobject.draw(surface)
            self.delay_buttonobject.draw(surface)
            self.ms_display_textobject.draw(surface)
            self.savesettings_buttonobject.draw(surface)
            self.discardsettings_buttonobject.draw(surface)
            
            if global_vars.sys_debug_lvl > 0:
                for i in range(5): #drawing stars 
                    self.star_triggerobject.set_pos((300+50*i, 550))
                    if self.star_triggerobject.draw_debug(surface):
                        self.difficulty = i

        #draws debug information
        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)