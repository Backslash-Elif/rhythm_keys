import global_vars, utils, sound_engine
from decimal import Decimal
from scenes import scene

from components import debug, touchtrigger, text, bgstyle, button, card, display_image, alert, key_reader, inputbox, rectangle
from components.styles import text_size, card_themes, UI_colors, background_gradient, UIColorName, CardThemeName, TextSizeName, colors, ColorName
from utils import hextobits, bitstohex, loadfromlvldat

class MainGame(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #text
        self.title_textobject = text.Text(global_vars.editor_name, text_size[TextSizeName.TITLE], (1050, 100), (700, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.subtitle_textobject = text.Text(global_vars.editor_song_artist, text_size[TextSizeName.SUBTITLE], (1050, 200), (700, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.titledevider_cardobject = card.Card((1050, 200), (300, 6), card_themes[CardThemeName.LIGHT] if global_vars.user_dark_mode else card_themes[CardThemeName.DARK])

        self.tilebg_cardobject = card.Card((300, 0), (650, 1080), card_themes[CardThemeName.DARK])
        self.lightmode_cardobject = card.Card((990, 40), (870, 970), card_themes[CardThemeName.DYNAMIC])

        self.pause_buttonobject = button.Button("Pause", text_size[TextSizeName.SUBTITLE], (1050, 300), (150, 50), UI_colors[UIColorName.PRIMARY])

        #arrows
        self.static_arrow_u_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/up.png", (350, 950), (100, 100))
        self.static_arrow_d_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/down.png", (500, 950), (100, 100))
        self.static_arrow_l_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/left.png", (650, 950), (100, 100))
        self.static_arrow_r_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/right.png", (800, 950), (100, 100))

        self.arrow_u_imageobject = display_image.DisplayImage("assets/arrows/smol/up.png", (350, 50), (100, 100))
        self.arrow_d_imageobject = display_image.DisplayImage("assets/arrows/smol/down.png", (500, 50), (100, 100))
        self.arrow_l_imageobject = display_image.DisplayImage("assets/arrows/smol/left.png", (650, 50), (100, 100))
        self.arrow_r_imageobject = display_image.DisplayImage("assets/arrows/smol/right.png", (800, 50), (100, 100))

        #paused
        self.paused_textobject = text.Text("Game paused.", text_size[TextSizeName.TITLE], (0, 250), (global_vars.const_rendersize[0], 100), colors[ColorName.DYNAMIC][0])
        self.resume_buttonobject = button.Button("Resume", text_size[TextSizeName.SUBTITLE], (850, 400), (200, 50), UI_colors[UIColorName.PRIMARY])
        self.restart_buttonobject = button.Button("Restart", text_size[TextSizeName.SUBTITLE], (850, 500), (200, 50), UI_colors[UIColorName.WARNING])
        self.exit_buttonobject = button.Button("Exit", text_size[TextSizeName.SUBTITLE], (850, 600), (200, 50), UI_colors[UIColorName.DANGER])

        #countdown
        self.countdown_rectangleobject = rectangle.Rectangle((550, 500), (150, 150), UI_colors[UIColorName.SECONDARY][0], 16)
        self.countdown_textobject = text.Text("", 200, (550, 500), (150, 150))
        self.countdown_counter = 91 #1.5s - one frame 

        #progress bar
        self.progresstxt1_textobject = text.Text("--:--", text_size[TextSizeName.TEXT], (1050, 850), (500, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.progresstxt2_textobject = text.Text("--:--", text_size[TextSizeName.TEXT], (1050, 850), (500, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.RIGHT)
        self.progressbg_rectangleobject = rectangle.Rectangle((1048, 898), (504, 54), UI_colors[UIColorName.SECONDARY][0], 10, 2, colors[ColorName.LIGHT_GREEN if global_vars.user_dark_mode else ColorName.GREEN][0])
        self.progressfg_rectangleobject = rectangle.Rectangle((1050, 900), (500, 50), colors[ColorName.LIGHT_GREEN if global_vars.user_dark_mode else ColorName.GREEN][0], 10, 2, UI_colors[UIColorName.SECONDARY][0])

        #misc
        self.soundengine = sound_engine.SoundEngine()
        self.soundengine.load(global_vars.editor_filepath)
        self.progresstxt2_textobject.set_text(self.soundengine.get_formated_len())

        self.alertobject = alert.Alert()
        self.keyreaderobject = key_reader.KeyReader()

        self.score = []
        self.score_textobject = text.Text("Score", text_size[TextSizeName.SMALL_TITLE], (1050, 500), (200, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.score_rating_imageobject = display_image.DisplayImage("assets/ranking/s.png", (1050, 600), (150, 150)) #C=0-39, B=40-64, A=65-89, S=90-100

        self.framekeys = set() #keyset for new inputs
        self.playing = True
        self.notes = 0
        self.missed = 0

    def handle_event(self, event):
        self.keyreaderobject.handle_events(event)
        self.soundengine.handle_events(event)

        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        else: #events aren't processed during alerts
            if self.playing:
                if self.pause_buttonobject.is_clicked(event): #pause button
                    self.playing = False
                    self.soundengine.pause()

                self.framekeys.add(self.keyreaderobject.get_pressed_key(event))#get newly pressed keys
                
            else:
                if self.resume_buttonobject.is_clicked(event): #resume button
                    self.playing = True
                    self.countdown_counter = 91

                if self.restart_buttonobject.is_clicked(event): #restart button
                    self.playing = True
                    self.countdown_counter = 91
                    self.score = []
                    utils.load_level()
                    self.soundengine.seek_to(0.0)
                    self.soundengine.pause()

                if self.exit_buttonobject.is_clicked(event): #exit button
                    self.soundengine.eject()
                    if utils.get_persistant_storage_item("editortest"):
                        utils.load_level()
                        self.manager.switch_to_scene("Editor")
                    else:
                        self.manager.switch_to_scene("Level selector")

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background
        if not global_vars.user_dark_mode: #helps the light mode stand out more
            self.lightmode_cardobject.draw(surface)

        if self.soundengine.get_play_state() == 3: #triggers when song finishes playing
            if utils.get_persistant_storage_item("editortest"):
                utils.load_level()
                self.manager.switch_to_scene("Editor")
            else:
                global_vars.sys_persistant_storage["songresult"] = [min(100, int(sum(self.score)/len(self.score))), self.missed]
                self.manager.switch_to_scene("Level results")

        if self.playing:
            self.title_textobject.draw(surface)
            self.subtitle_textobject.draw(surface)
            self.titledevider_cardobject.draw(surface)
            self.tilebg_cardobject.draw(surface)
            self.pause_buttonobject.draw(surface)
            self.static_arrow_u_imageobject.draw(surface)
            self.static_arrow_d_imageobject.draw(surface)
            self.static_arrow_l_imageobject.draw(surface)
            self.static_arrow_r_imageobject.draw(surface)

            #plot algorythm
            beat = float((self.soundengine.get_song_progress()+global_vars.editor_startdelay)*Decimal(str(global_vars.editor_bpm/60)))
            for key, value in global_vars.editor_lvldat.items():
                if key > beat-2 and key < beat+10:
                    tempdata = hextobits(value)
                    temppos = (beat - key) * 100 + 950
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
            
            #reader algorythm for correctly reading user input and giving fair points
            matches = 0
            for key, value in global_vars.editor_lvldat.items():
                if key+0.5 > beat and key-0.5 < beat:
                    matches+=1
                    tempkeys = list(self.framekeys)
                    tempdata = hextobits(loadfromlvldat(key))
                    for i in tempdata:
                        if i:
                            self.notes += 1
                    for tempkey, i in zip(("up", "down", "left", "right"), range(4)):
                        if tempkey in tempkeys:
                            if tempdata[i]:
                                tempdata[i] = False
                                self.score.append(min(110, int((1-abs(beat-key))*110+10))) #110 to allow player to catch up
                            else:
                                self.missed_note()
                            break
                    if True in tempdata:
                        global_vars.editor_lvldat[key] = bitstohex(tempdata)
                    else:
                        global_vars.editor_lvldat.pop(key) #fix this
            if not matches: #if user misses note
                tempkeys = list(self.framekeys)
                for i in ("up", "down", "left", "right"):
                    if i in tempkeys:
                        self.missed_note()
            
            temp_lvldat = {}
            for key, value in global_vars.editor_lvldat.items(): #making new dict so no runtime error
                if key+1<beat:
                    temp_lvldat[key] = value
                else:
                    break
            
            for key, value in temp_lvldat.items(): #this is responsible for punishing for missed notes while simoultaniously cleaning up the useless level data
                if key >= 0.0:
                    tempdata = hextobits(loadfromlvldat(key))
                    for i in tempdata:
                        if i:
                            self.missed_note()
                global_vars.editor_lvldat.pop(key)
            
            #progress bar
            corrected_song_progress = self.soundengine.get_song_progress()+global_vars.editor_startdelay if self.soundengine.get_song_progress()+global_vars.editor_startdelay >= Decimal('0.0') else Decimal('0.0') #compute the corrected song progress (compensating for song start delay)
            self.progresstxt1_textobject.set_text(f"{str(int(float(corrected_song_progress)/60)).zfill(2)}:{str(int(float(corrected_song_progress)%60)).zfill(2)}") #current progress
            self.progresstxt1_textobject.draw(surface)
            self.progresstxt2_textobject.draw(surface)
            self.progressfg_rectangleobject.set_size((min(500, max(10, (float(corrected_song_progress)/float(self.soundengine.get_song_len()))*500)), 50))
            self.progressbg_rectangleobject.draw(surface)
            self.progressfg_rectangleobject.draw(surface)
            
            #ranking logic
            if self.score:
                tempscore = min(100, int(sum(self.score)/len(self.score)))
                self.score_textobject.set_text(f"Score:\n{tempscore}")
                if tempscore<40:
                    self.score_rating_imageobject.set_image("assets/ranking/c.png")
                elif tempscore<65:
                    self.score_rating_imageobject.set_image("assets/ranking/b.png")
                elif tempscore<90:
                    self.score_rating_imageobject.set_image("assets/ranking/a.png")
                else:
                    self.score_rating_imageobject.set_image("assets/ranking/s.png")
                self.score_rating_imageobject.draw(surface)
                self.score_textobject.draw(surface)

            self.framekeys.clear()#clear newly pressed keys

            #countdown at beginning; it works by counting down 90 frames. @60fps that's 1.5 seconds so every number is displayed for 0.5 secs
            if self.countdown_counter > 0:
                self.countdown_rectangleobject.draw(surface)
                if self.countdown_counter > 60:
                    self.countdown_textobject.set_text("3")
                    self.countdown_textobject.set_color(UI_colors[UIColorName.SUCCESS][0])
                elif self.countdown_counter > 30:
                    self.countdown_textobject.set_text("2")
                    self.countdown_textobject.set_color(UI_colors[UIColorName.WARNING][0])
                else:
                    self.countdown_textobject.set_text("1")
                    self.countdown_textobject.set_color(UI_colors[UIColorName.DANGER][0])
                self.countdown_textobject.draw(surface)
                self.countdown_counter -= 1
                if self.countdown_counter == 0:
                    self.soundengine.play()
        else: #draw pause menu
            self.paused_textobject.draw(surface)
            self.resume_buttonobject.draw(surface)
            self.restart_buttonobject.draw(surface)
            self.exit_buttonobject.draw(surface)

        self.alertobject.draw(surface)

        #draws debug info
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)
    
    def missed_note(self): #shortcut for
        self.missed+=1
        self.score.append(0)