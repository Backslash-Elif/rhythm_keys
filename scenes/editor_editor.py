import global_vars, sound_engine
from decimal import Decimal
from scenes import scene

from components import debug, touchtrigger, text, bgstyle, button, card, display_image, alert, key_reader
from components.styles import text_size, card_themes, UI_colors, background_gradient, UIColorName, CardThemeName, TextSizeName, colors, ColorName

def hextobits(hex:str):
    dec = int(hex, 16)
    bits = []
    for i in range(4):
        bits.append(True if dec%2 else False)
        dec = int(dec/2)
    return list(reversed(bits))

def bitstohex(bits:iter):
    bits = list(reversed(bits))
    dec = 0
    for i in range(4):
        dec += [1,2,4,8][i] if bits[i] else 0
    return str(hex(dec)[2:])

def loadfromlvldat(index:int):
    if index in global_vars.editor_lvldat:
        return global_vars.editor_lvldat[index]
    else:
        return '0'

class EditorEditor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        global_vars.editor_load_vars = True

        #text
        self.title_textobject = text.Text(global_vars.editor_name, text_size[TextSizeName.TITLE], (1050, 100), (700, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.subtitle_textobject = text.Text(global_vars.editor_song_artist, text_size[TextSizeName.SUBTITLE], (1050, 200), (700, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.titledevider_cardobject = card.Card((1050, 200), (300, 6), card_themes[CardThemeName.LIGHT] if global_vars.user_dark_mode else card_themes[CardThemeName.DARK])

        self.tilebg_cardobject = card.Card((300, 0), (650, 1080), card_themes[CardThemeName.DARK])

        self.savebtn_buttonobject = button.Button("Save", text_size[TextSizeName.SUBTITLE], (1050, 300), (130, 50), UI_colors[UIColorName.PRIMARY])
        self.exitbtn_buttonobject = button.Button("Exit", text_size[TextSizeName.TEXT], (1200, 300), (100, 50), UI_colors[UIColorName.DANGER])
        self.testbtn_buttonobject = button.Button("Test", text_size[TextSizeName.TEXT], (1400, 400), (100, 50), UI_colors[UIColorName.SECONDARY])

        #speed & media control (replay mode only)
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
        self.arrow_triggerobject = touchtrigger.Touchtrigger((350, 850), (100, 100)) #trigger for mouse

        self.snap_value = 4 # 4/4 (4 per beat)

        #misc
        self.soundengine = sound_engine.SoundEngine()
        self.soundengine.load(global_vars.editor_filepath)

        self.alertobject = alert.Alert()
        self.keyreaderobject = key_reader.KeyReader()

        self.framekeys = set() #keyset for new inputs

    def handle_event(self, event):
        self.keyreaderobject.handle_events(event)
        self.soundengine.handle_events(event)
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        else:
            if self.alertobject.get_result():
                if isinstance(self.alertobject.get_result(), str):
                    print(self.alertobject.get_result())
                if isinstance(self.alertobject.get_result(), bool) and self.alertobject.get_result():
                    self.manager.switch_to_scene("Editor create menu")
            if self.exitbtn_buttonobject.is_clicked(event):
                self.alertobject.new_alert("Are you sure you want to quit?\n\n\n(!!!All progress will be lost!!!)", 1)
            if self.fastback_buttonobject.is_clicked(event):
                self.soundengine.seek_to(max(self.soundengine.get_song_progress() - 10, 0.0))
            if self.back_buttonobject.is_clicked(event):
                self.soundengine.seek_to(max(self.soundengine.get_song_progress() - 5, 0.0))
            if self.playpause_buttonobject.is_clicked(event):
                if self.soundengine.get_play_state() == 1:
                    self.soundengine.pause()
                else:
                    self.soundengine.play()
            if self.fastforward_buttonobject.is_clicked(event):
                self.soundengine.seek_to(min(self.soundengine.get_song_progress() + 10, self.soundengine.get_song_len()))
            if self.forward_buttonobject.is_clicked(event):
                self.soundengine.seek_to(min(self.soundengine.get_song_progress() + 5, self.soundengine.get_song_len()))
            if self.savebtn_buttonobject.is_clicked(event):
                print(global_vars.editor_lvldat)
            self.framekeys.add(self.keyreaderobject.get_pressed_key(event))#get newly pressed keys

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        #print(self.keyreaderobject.get_keys())
        self.exitbtn_buttonobject.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.titledevider_cardobject.draw(surface)
        self.tilebg_cardobject.draw(surface)
        self.savebtn_buttonobject.draw(surface)
        self.testbtn_buttonobject.draw(surface)
        self.mediactrl_cardobject.draw(surface)
        self.mediactrllabel_textobject.draw(surface)
        self.mediaprogress1_textobject.set_text(f"{str(int(float(self.soundengine.get_song_progress())/60)).zfill(2)}:{str(int(float(self.soundengine.get_song_progress())%60)).zfill(2)}")
        self.mediaprogress2_textobject.set_text(f"Beat {int(float(self.soundengine.get_song_progress())*(global_vars.editor_bpm/60))}/{int(global_vars.editor_length*(global_vars.editor_bpm/60))}\n@{global_vars.editor_bpm}BPM")
        self.mediaprogress1_textobject.draw(surface)
        self.mediaprogress2_textobject.draw(surface)
        self.fastback_buttonobject.draw(surface)
        self.fastback_imageobject.draw(surface)
        self.back_buttonobject.draw(surface)
        self.back_imageobject.draw(surface)
        self.playpause_buttonobject.draw(surface)
        if self.soundengine.get_play_state() == 1:
            self.pause_imageobject.draw(surface)
        else:
            self.play_imageobject.draw(surface)
        self.forward_buttonobject.draw(surface)
        self.forward_imageobject.draw(surface)
        self.fastforward_buttonobject.draw(surface)
        self.fastforward_imageobject.draw(surface)
        self.static_arrow_u_imageobject.draw(surface)
        self.static_arrow_d_imageobject.draw(surface)
        self.static_arrow_l_imageobject.draw(surface)
        self.static_arrow_r_imageobject.draw(surface)
        #plot algorythm
        beat = float(self.soundengine.get_song_progress()*Decimal(global_vars.editor_bpm/60))
        for key, value in global_vars.editor_lvldat.items():
            if key > beat-10 and key < beat+2:
                tempdata = hextobits(value)
                temppos = (beat - key) * 100 + 50
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
        rounded_beat = round(beat * self.snap_value)/self.snap_value
        if self.soundengine.get_play_state() == 1:
            tempkeys = list(self.framekeys)
            tempdata = hextobits(loadfromlvldat(rounded_beat))
            tempdata[0] = True if "up" in tempkeys else tempdata[0]
            tempdata[1] = True if "down" in tempkeys else tempdata[1]
            tempdata[2] = True if "left" in tempkeys else tempdata[2]
            tempdata[3] = True if "right" in tempkeys else tempdata[3]
            if True in tempdata:
                global_vars.editor_lvldat[rounded_beat] = bitstohex(tempdata)
        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)
        self.framekeys.clear()#clear newly pressed keys