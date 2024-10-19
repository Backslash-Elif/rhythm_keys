import global_vars
from scenes import scene

from components import button, debug, text, bgstyle, card, inputbox, alert, display_image
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName, card_themes, CardThemeName, BGGradientName, compute_dynamic_colors

class Results(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        points = global_vars.sys_persistant_storage["songresult"]

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Results", text_size[TextSizeName.TITLE], (300, 200), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.name_textobject = text.Text(f"{global_vars.editor_name} by {global_vars.editor_song_artist}", text_size[TextSizeName.SUBTITLE], (300, 350), (700, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.score_textobject = text.Text(f"You scored {points} points!", text_size[TextSizeName.TEXT], (300, 450), (400, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.score_rating_imageobject = display_image.DisplayImage("assets/ranking/s.png", (300, 450), (256, 256)) #C=0-39, B=40-64, A=65-89, S=90-100
        if points<40:
            self.score_rating_imageobject.set_image("assets/ranking/c.png")
        elif points<65:
            self.score_rating_imageobject.set_image("assets/ranking/b.png")
        elif points<90:
            self.score_rating_imageobject.set_image("assets/ranking/a.png")
        else:
            self.score_rating_imageobject.set_image("assets/ranking/s.png")
        
        self.exit_buttonobject = button.Button("Done", text_size[TextSizeName.SUBTITLE], (300, 750), (200, 50), UI_colors[UIColorName.PRIMARY])
        self.restart_buttonobject = button.Button("Restart", text_size[TextSizeName.SUBTITLE], (550, 750), (200, 50), UI_colors[UIColorName.SUCCESS])

    def handle_event(self, event):
        if self.exit_buttonobject.is_clicked(event):
            self.manager.switch_to_scene("Level selector")
        if self.restart_buttonobject.is_clicked(event):
            global_vars.load_level()
            self.manager.switch_to_scene("Game")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        self.name_textobject.draw(surface)
        self.score_textobject.draw(surface)
        self.score_rating_imageobject.draw(surface)
        self.exit_buttonobject.draw(surface)
        self.restart_buttonobject.draw(surface)
        
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)