import global_vars, sound_engine
from decimal import Decimal
from scenes import scene

from components import debug, touchtrigger, text, bgstyle, button, card, display_image, alert, key_reader, inputbox, rectangle
from components.styles import text_size, card_themes, UI_colors, background_gradient, UIColorName, CardThemeName, TextSizeName, colors, ColorName
from game_utils import hextobits, bitstohex, loadfromlvldat

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

        #misc
        self.soundengine = sound_engine.SoundEngine()
        self.soundengine.load(global_vars.editor_filepath)
        #self.soundengine.play()

        #countdown
        self.countdown_rectangleobject = rectangle.Rectangle((550, 500), (150, 150), UI_colors[UIColorName.SECONDARY][0], 16)
        self.countdown_textobject = text.Text("", 200, (550, 500), (150, 150))
        self.countdown_counter = 91 #1.5 - one frame 

        self.alertobject = alert.Alert()
        self.keyreaderobject = key_reader.KeyReader()

        self.framekeys = set() #keyset for new inputs
        self.playing = True

        self.alertid = 0 #0=nothing, 1=exit, 2=restart

    def handle_event(self, event):
        self.keyreaderobject.handle_events(event)
        self.soundengine.handle_events(event)
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
            if self.alertobject.get_result() != None:
                if self.alertid == 1:
                    if self.alertobject.get_result():
                        global_vars.save_level()
                        global_vars.create_package(global_vars.editor_uuid)
                        global_vars.editor_uuid = ""
                        self.soundengine.eject()
                        self.manager.switch_to_scene("Editor main menu")
                if self.alertid == 2:
                    print()
                self.alertid = 0
        else:
            if self.playing:
                if self.pause_buttonobject.is_clicked(event):
                    self.playing = False
                    self.soundengine.pause()
                self.framekeys.add(self.keyreaderobject.get_pressed_key(event))#get newly pressed keys
                
            else:
                if self.resume_buttonobject.is_clicked(event):
                    self.playing = True
                    self.countdown_counter = 91
                if self.restart_buttonobject.is_clicked(event):
                    self.playing = True
                    self.countdown_counter = 91
                    self.soundengine.seek_to(0.0)
                    self.soundengine.pause()
                if self.exit_buttonobject.is_clicked(event):
                    self.soundengine.eject()
                    self.manager.switch_to_scene("Level selector")

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if self.playing:
            #print(self.keyreaderobject.get_keys())
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
            beat = float((self.soundengine.get_song_progress())*Decimal(global_vars.editor_bpm/60))
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
            
            #reader algorythm
            rounded_beat = round(beat * global_vars.editor_snap_value)/global_vars.editor_snap_value
            if self.soundengine.get_play_state() == 1:
                tempkeys = list(self.framekeys)
                tempdata = hextobits(loadfromlvldat(rounded_beat))
                tempdata[0] = True if "up" in tempkeys else tempdata[0]
                tempdata[1] = True if "down" in tempkeys else tempdata[1]
                tempdata[2] = True if "left" in tempkeys else tempdata[2]
                tempdata[3] = True if "right" in tempkeys else tempdata[3]
                if True in tempdata:
                    global_vars.editor_lvldat[rounded_beat] = bitstohex(tempdata)
            self.framekeys.clear()#clear newly pressed keys
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
        else:
            self.paused_textobject.draw(surface)
            self.resume_buttonobject.draw(surface)
            self.restart_buttonobject.draw(surface)
            self.exit_buttonobject.draw(surface)

        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)