import pygame, tools, global_vars
from decimal import Decimal
from scenes import scene

from components import debug, touchtrigger, text, bgstyle, button, card
from components.styles import text_size, card_themes, UI_colors, background_gradient, UIColorName, CardThemeName, TextSizeName

class EditorEditor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.sys_screen_size)

        self.exitbtn_buttonobject = button.Button("Exit", text_size[TextSizeName.TEXT], (40, 40), (100, 50), UI_colors[UIColorName.DANGER]) #no adjustments for eventual screensize change as the origin is top left

        #text
        self.title_textobject = text.Text(global_vars.editor_name, text_size[TextSizeName.TITLE], (1100, 80), (100, 100))
        self.subtitle_textobject = text.Text(global_vars.editor_song_artist, text_size[TextSizeName.SUBTITLE], (1100, 150), (100, 100))
        self.titledevider_cardobject = card.Card((1100, 180), (300, 6), card_themes[CardThemeName.LIGHT])

        self.tilebg_cardobject = card.Card((300, 0), (700, 1080), card_themes[CardThemeName.DARK])

        self.savebtn_buttonobject = button.Button("Save", text_size[TextSizeName.SUBTITLE], (1100, 200), (128, 64), UI_colors[UIColorName.PRIMARY])
        self.modebtn_buttonobject = button.Button("Switch to Replay Mode", text_size[TextSizeName.TEXT], (1100, 350), (320, 80), UI_colors[UIColorName.SECONDARY])
        self.testbtn_buttonobject = button.Button("Test", text_size[TextSizeName.TEXT], (1100, 450), (180, 80), UI_colors[UIColorName.SECONDARY])

        self.replaymode = False

        #speed & media control (replay mode only)
        self.mediactrl_cardobject = card.Card((1080, 750), (520, 250), card_themes[CardThemeName.DARK])
        self.mediactrllabel_textobject = text.Text("Speed & Media Control", text_size[TextSizeName.TEXT], (1100, 760), (100, 100))
        self.fastback_buttonobject = button.Button("<<", 48, (1100, 900), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.back_buttonobject = button.Button("<", 48, (1200, 900), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.playpause_buttonobject = button.Button("|| >", 48, (1300, 900), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.forward_buttonobject = button.Button(">", 48, (1400, 900), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.fastforward_buttonobject = button.Button(">>", 48, (1500, 900), (80, 80), UI_colors[UIColorName.SECONDARY])

        self.slower_buttonobject = button.Button("-", 48, (1200, 800), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.faster_buttonobject = button.Button("+", 48, (1400, 800), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.speedinfo_buttonobject = button.Button("1.0", 48, (1300, 800), (80, 80), UI_colors[UIColorName.SECONDARY])

        self.replay_speed = Decimal('1.0')

        #beatinfo (select mode only)
        self.advancebeats_buttonobject = button.Button("^", 48, (200, 10), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.deadvancebeats_buttonobject = button.Button("v", 48, (200, 990), (80, 80), UI_colors[UIColorName.SECONDARY])
        self.beatnrdisplay1_textobject = text.Text("0001", text_size[TextSizeName.SUBTITLE], (200, 890), (100, 100))
        self.beatnrdisplay2_textobject = text.Text("0002", text_size[TextSizeName.SUBTITLE], (200, 780), (100, 100))
        self.beatnrdisplay3_textobject = text.Text("0003", text_size[TextSizeName.SUBTITLE], (200, 670), (100, 100))
        self.beatnrdisplay4_textobject = text.Text("0004", text_size[TextSizeName.SUBTITLE], (200, 560), (100, 100))
        self.beatnrdisplay5_textobject = text.Text("0005", text_size[TextSizeName.SUBTITLE], (200, 450), (100, 100))
        self.beatnrdisplay6_textobject = text.Text("0006", text_size[TextSizeName.SUBTITLE], (200, 340), (100, 100))
        self.beatnrdisplay7_textobject = text.Text("0007", text_size[TextSizeName.SUBTITLE], (200, 230), (100, 100))
        self.beatnrdisplay8_textobject = text.Text("0008", text_size[TextSizeName.SUBTITLE], (200, 120), (100, 100))

    def handle_event(self, event):
        if self.modebtn_buttonobject.is_clicked(event):
            if self.replaymode:
                self.modebtn_buttonobject.set_text("Switch to Replay Mode")
            else:
                self.modebtn_buttonobject.set_text("Switch to Select Mode")
            self.replaymode = not self.replaymode
        if self.faster_buttonobject.is_clicked(event):
            self.replay_speed = min(self.replay_speed + Decimal('0.1'), Decimal('5.0'))
            self.speedinfo_buttonobject.set_text(str(self.replay_speed))
            print(self.replay_speed)
        if self.slower_buttonobject.is_clicked(event):
            self.replay_speed = max(self.replay_speed - Decimal('0.1'), Decimal('0.3'))
            self.speedinfo_buttonobject.set_text(str(self.replay_speed))
            print(self.replay_speed)
        if self.speedinfo_buttonobject.is_clicked(event):
            self.replay_speed = Decimal('1.0')
            self.speedinfo_buttonobject.set_text(str(self.replay_speed))
            print(self.replay_speed)

    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        self.exitbtn_buttonobject.draw(surface)
        self.title_textobject.draw(surface)
        self.subtitle_textobject.draw(surface)
        self.titledevider_cardobject.draw(surface)
        self.tilebg_cardobject.draw(surface)
        self.savebtn_buttonobject.draw(surface)
        self.modebtn_buttonobject.draw(surface)
        self.testbtn_buttonobject.draw(surface)
        if self.replaymode:
            self.mediactrl_cardobject.draw(surface)
            self.mediactrllabel_textobject.draw(surface)
            self.fastback_buttonobject.draw(surface)
            self.back_buttonobject.draw(surface)
            self.playpause_buttonobject.draw(surface)
            self.forward_buttonobject.draw(surface)
            self.fastforward_buttonobject.draw(surface)
            self.faster_buttonobject.draw(surface)
            self.slower_buttonobject.draw(surface)
            self.speedinfo_buttonobject.draw(surface)
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
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)