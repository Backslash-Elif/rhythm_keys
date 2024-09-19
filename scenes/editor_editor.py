import pygame, tools, global_vars
from decimal import Decimal
from scenes import scene

from components import fpscounter, touchtrigger, text, bgstyle, button, card
from components.styles import text_size, card_themes, UI_colors, background_gradient

class EditorEditor(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))

        self.exitbtn_buttonobject = button.Button("Exit", text_size["text"], (40, 40), (100, 50), UI_colors["danger"]) #no adjustments for eventual screensize change as the origin is top left

        #text
        self.title_textobject = text.Text(global_vars.editor_name, text_size["title"], (1100, 80))
        self.subtitle_textobject = text.Text(global_vars.editor_song_artist, text_size["subtitle"], (1100, 150))
        self.titledevider_cardobject = card.Card((1100, 180), (300, 6), card_themes["light"])

        self.tilebg_cardobject = card.Card((300, 0), (700, 1080), card_themes["dark"])

        self.savebtn_buttonobject = button.Button("Save", text_size["subtitle"], (1100, 200), (128, 64), UI_colors["primary"])
        self.modebtn_buttonobject = button.Button("Switch to Replay Mode", text_size["text"], (1100, 350), (320, 80), UI_colors["secondary"])
        self.testbtn_buttonobject = button.Button("Test", text_size["text"], (1100, 450), (180, 80), UI_colors["secondary"])

        self.replaymode = False

        #speed & media control (replay mode only)
        self.mediactrl_cardobject = card.Card((1080, 750), (520, 250), card_themes["primary"])
        self.mediactrllabel_textobject = text.Text("Speed & Media Control", text_size["text"], (1100, 760))
        self.fastback_buttonobject = button.Button("<<", 48, (1100, 900), (80, 80), UI_colors["secondary"])
        self.back_buttonobject = button.Button("<", 48, (1200, 900), (80, 80), UI_colors["secondary"])
        self.playpause_buttonobject = button.Button("|| >", 48, (1300, 900), (80, 80), UI_colors["secondary"])
        self.forward_buttonobject = button.Button(">", 48, (1400, 900), (80, 80), UI_colors["secondary"])
        self.fastforward_buttonobject = button.Button(">>", 48, (1500, 900), (80, 80), UI_colors["secondary"])

        self.slower_buttonobject = button.Button("-", 48, (1200, 800), (80, 80), UI_colors["secondary"])
        self.faster_buttonobject = button.Button("+", 48, (1400, 800), (80, 80), UI_colors["secondary"])
        self.speedinfo_buttonobject = button.Button("1.0", 48, (1300, 800), (80, 80), UI_colors["secondary"])

        self.replay_speed = Decimal('1.0')

        #beatinfo (select mode only)
        self.advancebeats_buttonobject = button.Button("^", 48, (200, 10), (80, 80), UI_colors["secondary"])
        self.deadvancebeats_buttonobject = button.Button("v", 48, (200, 990), (80, 80), UI_colors["secondary"])
        self.beatnrdisplay1_textobject = text.Text("0001", text_size["subtitle"], (200, 890))
        self.beatnrdisplay2_textobject = text.Text("0002", text_size["subtitle"], (200, 780))
        self.beatnrdisplay3_textobject = text.Text("0003", text_size["subtitle"], (200, 670))
        self.beatnrdisplay4_textobject = text.Text("0004", text_size["subtitle"], (200, 560))
        self.beatnrdisplay5_textobject = text.Text("0005", text_size["subtitle"], (200, 450))
        self.beatnrdisplay6_textobject = text.Text("0006", text_size["subtitle"], (200, 340))
        self.beatnrdisplay7_textobject = text.Text("0007", text_size["subtitle"], (200, 230))
        self.beatnrdisplay8_textobject = text.Text("0008", text_size["subtitle"], (200, 120))

    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
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
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
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

    def update(self):
        self.fps.tick()