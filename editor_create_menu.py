import pygame, scene, global_vars

from elements import button, text, inputbox, touchtrigger, fpscounter, bgstyle, display_image
from elements.styles import Styles
from tools import Tools

class EditorCreateMenu(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        global_vars.editor_name = ""
        global_vars.editor_author = global_vars.user_name
        global_vars.editor_song_artist = ""
        global_vars.editor_length = 0
        global_vars.editor_difficulty = "Beginner"
        #fps stuff
        self.fps_toggle = touchtrigger.Touchtrigger((0, 0), (256, 24))
        self.show_fps = False
        self.fps = fpscounter.Fpscounter()
        self.info_text = text.Text("loading", 24, (0, 0))
        #elements
        self.backbutton = button.Button("Back", 32, (64, 1080-128), 128, 64, Styles.button.danger())
        self.nametext = text.Text("Enter song name:", 32, (400, 300))
        self.nameinput = inputbox.InputBox(700, 64, 32, (650, 300-10), 32, Styles.inputbox.dark())
        self.artisttext = text.Text("Enter song artist:", 32, (400, 400))
        self.artistinput = inputbox.InputBox(700, 64, 32, (650, 400-10), 32, Styles.inputbox.dark())
        self.difficultytext = text.Text("Difficulty:", 32, (400, 500))
        self.star1 = display_image.DisplayImage("assets/icons/star.png", (650+20, 500-10), (48, 48))
        self.star2 = display_image.DisplayImage("assets/icons/star.png", (650+70, 500-10), (48, 48))
        self.star3 = display_image.DisplayImage("assets/icons/star.png", (650+120, 500-10), (48, 48))
        self.star4 = display_image.DisplayImage("assets/icons/star.png", (650+170, 500-10), (48, 48))
        self.star5 = display_image.DisplayImage("assets/icons/star.png", (650+220, 500-10), (48, 48))
    
    def handle_event(self, event):
        if self.fps_toggle.update(event):
            self.show_fps = not self.show_fps
        if self.backbutton.is_clicked(event):
            self.manager.switch_to_scene("Editor main menu")
        self.nameinput.handle_events(event)
        self.artistinput.handle_events(event)
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, Styles.bggradient.purple())
        if self.show_fps:
            self.info_text.set_text(f"FPS: {self.fps.get_fps()}, Mouse: X={pygame.mouse.get_pos()[0]} Y={pygame.mouse.get_pos()[1]}")
            self.info_text.draw(surface)
        self.backbutton.draw(surface)
        self.nametext.draw(surface)
        self.nameinput.draw(surface)
        self.artisttext.draw(surface)
        self.artistinput.draw(surface)
        self.difficultytext.draw(surface)
        self.star1.draw(surface)
        self.star2.draw(surface)
        self.star3.draw(surface)
        self.star4.draw(surface)
        self.star5.draw(surface)
    
    def update(self):
        self.fps.tick()