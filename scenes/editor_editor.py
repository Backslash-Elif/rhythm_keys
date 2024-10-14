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
        global_vars.editor_lvldat[index] = '0'
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
        self.modebtn_buttonobject = button.Button("Switch to Replay Mode", text_size[TextSizeName.TEXT], (1050, 400), (330, 50), UI_colors[UIColorName.SECONDARY])
        self.testbtn_buttonobject = button.Button("Test", text_size[TextSizeName.TEXT], (1400, 400), (100, 50), UI_colors[UIColorName.SECONDARY])

        self.replaymode = False

        #speed & media control (replay mode only)
        self.inputrow_cardobject = card.Card((300, 450), (650, 100), card_themes[CardThemeName.PRIMARY])
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

        #beatinfo (select mode only)
        self.advancebeats_buttonobject = button.Button("^", text_size[TextSizeName.SUBTITLE], (210, 60), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.deadvancebeats_buttonobject = button.Button("v", text_size[TextSizeName.SUBTITLE], (210, 960), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.beatnrdisplay1_textobject = text.Text("0001", text_size[TextSizeName.SUBTITLE], (200, 850), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay2_textobject = text.Text("0002", text_size[TextSizeName.SUBTITLE], (200, 750), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay3_textobject = text.Text("0003", text_size[TextSizeName.SUBTITLE], (200, 650), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay4_textobject = text.Text("0004", text_size[TextSizeName.SUBTITLE], (200, 550), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay5_textobject = text.Text("0005", text_size[TextSizeName.SUBTITLE], (200, 450), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay6_textobject = text.Text("0006", text_size[TextSizeName.SUBTITLE], (200, 350), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay7_textobject = text.Text("0007", text_size[TextSizeName.SUBTITLE], (200, 250), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrdisplay8_textobject = text.Text("0008", text_size[TextSizeName.SUBTITLE], (200, 150), (100, 100), colors[ColorName.DYNAMIC][0])
        self.beatnrset = 0 #sets of 8

        self.arrow_imageobject = display_image.DisplayImage("assets/arrows/smol_dark/up.png", (350, 850), (100, 100))
        self.arrow_triggerobject = touchtrigger.Touchtrigger((350, 850), (100, 100))


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
            if self.exitbtn_buttonobject.is_clicked(event):
                if any("shift" in s for s in self.keyreaderobject.get_keys()):
                    self.manager.switch_to_scene("Editor create menu")
                else:
                    self.alertobject.new_alert("Are you sure you want to quit?\n\nIf you are, please press shift\nand press exit again.\n\n\n(!!!All progress will be lost!!!)")
            if self.modebtn_buttonobject.is_clicked(event):
                if self.replaymode:
                    self.modebtn_buttonobject.set_text("Switch to Replay Mode")
                else:
                    self.modebtn_buttonobject.set_text("Switch to Select Mode")
                self.replaymode = not self.replaymode
            if self.advancebeats_buttonobject.is_clicked(event):
                self.beatnrset += 1
                self.beatnrdisplay1_textobject.set_text(str(self.beatnrset * 8 + 1).zfill(4))
                self.beatnrdisplay2_textobject.set_text(str(self.beatnrset * 8 + 2).zfill(4))
                self.beatnrdisplay3_textobject.set_text(str(self.beatnrset * 8 + 3).zfill(4))
                self.beatnrdisplay4_textobject.set_text(str(self.beatnrset * 8 + 4).zfill(4))
                self.beatnrdisplay5_textobject.set_text(str(self.beatnrset * 8 + 5).zfill(4))
                self.beatnrdisplay6_textobject.set_text(str(self.beatnrset * 8 + 6).zfill(4))
                self.beatnrdisplay7_textobject.set_text(str(self.beatnrset * 8 + 7).zfill(4))
                self.beatnrdisplay8_textobject.set_text(str(self.beatnrset * 8 + 8).zfill(4))
            if self.deadvancebeats_buttonobject.is_clicked(event):
                if self.beatnrset > 0:
                    self.beatnrset -= 1
                    self.beatnrdisplay1_textobject.set_text(str(self.beatnrset * 8 + 1).zfill(4))
                    self.beatnrdisplay2_textobject.set_text(str(self.beatnrset * 8 + 2).zfill(4))
                    self.beatnrdisplay3_textobject.set_text(str(self.beatnrset * 8 + 3).zfill(4))
                    self.beatnrdisplay4_textobject.set_text(str(self.beatnrset * 8 + 4).zfill(4))
                    self.beatnrdisplay5_textobject.set_text(str(self.beatnrset * 8 + 5).zfill(4))
                    self.beatnrdisplay6_textobject.set_text(str(self.beatnrset * 8 + 6).zfill(4))
                    self.beatnrdisplay7_textobject.set_text(str(self.beatnrset * 8 + 7).zfill(4))
                    self.beatnrdisplay8_textobject.set_text(str(self.beatnrset * 8 + 8).zfill(4))
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
            for y, i in zip((850, 750, 650, 550, 450, 350, 250, 150), range(1, 9)):
                    tempdata = hextobits(loadfromlvldat(self.beatnrset*8+i))
                    for x, i2 in zip((350, 500, 650, 800), range(4)):
                        self.arrow_triggerobject.set_pos((x, y))
                        if self.arrow_triggerobject.update(event):
                            tempdata[i2] = not tempdata[i2]
                            global_vars.editor_lvldat[self.beatnrset*8+i] = bitstohex(tempdata)
            if self.savebtn_buttonobject.is_clicked(event):
                print(global_vars.editor_lvldat)
            #print(self.keyreaderobject.get_keys())
            self.framekeys.add(self.keyreaderobject.get_pressed_key(event))

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        #print(self.keyreaderobject.get_keys())
        self.exitbtn_buttonobject.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.titledevider_cardobject.draw(surface)
        self.tilebg_cardobject.draw(surface)
        self.savebtn_buttonobject.draw(surface)
        self.modebtn_buttonobject.draw(surface)
        self.testbtn_buttonobject.draw(surface)
        if self.replaymode:
            self.inputrow_cardobject.draw(surface)
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
            for y, i in zip((950, 850, 750, 650, 550, 450, 350, 250, 150, 50, -50), range(-5, 6)):
                beat = int(float(self.soundengine.get_song_progress())*(global_vars.editor_bpm/60))
                beat_float = int((str(float(self.soundengine.get_song_progress()*Decimal(global_vars.editor_bpm/60)))+"0").split(".")[1][:2])
                if beat + i < 1:
                    continue
                tempdata = loadfromlvldat(beat+i)
                for x, i2 in zip((350, 500, 650, 800), range(4)):
                    #print(y+beat_float, end=" ")
                    #print((x, y+beat_float), end=" ")
                    self.arrow_imageobject.set_pos((x, y+beat_float))
                    self.arrow_imageobject.set_image(f"assets/arrows/smol/{['up','down','left','right'][i2]}.png" if hextobits(tempdata)[i2] else f"assets/arrows/smol_dark/{['up','down','left','right'][i2]}.png")
                    self.arrow_imageobject.draw(surface)
            #print(beat_float)
            if self.soundengine.get_play_state() == 1:
                beat = int(float(self.soundengine.get_song_progress())*(global_vars.editor_bpm/60))
                beat_float = int((str(float(self.soundengine.get_song_progress()*Decimal(global_vars.editor_bpm/60)))+"0").split(".")[1][:2])
                if beat_float > 50:
                    beat += 1
                    tempkeys = list(self.framekeys)
                else:
                    tempkeys = self.keyreaderobject.get_keys()
                tempdata = hextobits(loadfromlvldat(beat))
                tempdata[0] = True if "up" in tempkeys else tempdata[0]
                tempdata[1] = True if "down" in tempkeys else tempdata[1]
                tempdata[2] = True if "left" in tempkeys else tempdata[2]
                tempdata[3] = True if "right" in tempkeys else tempdata[3]
                global_vars.editor_lvldat[beat] = bitstohex(tempdata)

        else:
            self.advancebeats_buttonobject.draw(surface)
            self.deadvancebeats_buttonobject.draw(surface)
            self.beatnrdisplay1_textobject.draw(surface)
            self.beatnrdisplay2_textobject.draw(surface)
            self.beatnrdisplay3_textobject.draw(surface)
            self.beatnrdisplay4_textobject.draw(surface)
            self.beatnrdisplay5_textobject.draw(surface)
            self.beatnrdisplay6_textobject.draw(surface)
            self.beatnrdisplay7_textobject.draw(surface)
            self.beatnrdisplay8_textobject.draw(surface)
            for y, i in zip((850, 750, 650, 550, 450, 350, 250, 150), range(1, 9)):
                tempdata = loadfromlvldat(self.beatnrset*8+i)
                for x, i2 in zip((350, 500, 650, 800), range(4)):
                    self.arrow_imageobject.set_pos((x, y))
                    self.arrow_imageobject.set_image(f"assets/arrows/smol/{['up','down','left','right'][i2]}.png" if hextobits(tempdata)[i2] else f"assets/arrows/smol_dark/{['up','down','left','right'][i2]}.png")
                    self.arrow_imageobject.draw(surface)
        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)
        self.framekeys.clear()