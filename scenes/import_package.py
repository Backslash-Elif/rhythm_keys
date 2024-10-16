import global_vars
from scenes import scene
import tkinter as tk
from tkinter import filedialog

from components import button, debug, text, bgstyle, card, inputbox, alert
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName, card_themes, CardThemeName, BGGradientName, compute_dynamic_colors

def file_picker():
    #make rootwindow and hide it
    root = tk.Tk()
    root.withdraw()

    #file allow list
    file_types = [("Compressed File Archive", "*.zip")]

    #file dialog
    file_path = filedialog.askopenfilename(title="Select an Zip Archive", filetypes=file_types)
    return file_path

class ImportPackage(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Import level", text_size[TextSizeName.TITLE], (300, 200), (400, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.back_buttonobject = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
        self.filepicker_buttonobject = button.Button("Pick a file...", text_size[TextSizeName.TEXT], (300, 400), (500, 100), UI_colors[UIColorName.PRIMARY])
        self.existing_buttonobject = button.Button("Level selecter", text_size[TextSizeName.TEXT], (1100, 400), (500, 100), UI_colors[UIColorName.PRIMARY])
        self.or_textobject = text.Text("or", text_size[TextSizeName.TEXT], (900, 400), (100, 100), colors[ColorName.DYNAMIC][0])
        self.alertobject = alert.Alert()
    
    def handle_event(self, event):
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        else:
            if self.filepicker_buttonobject.is_clicked(event):
                selected_file = file_picker()
                global_vars.load_from_external_file(selected_file)
                self.manager.switch_to_scene("Editor")
            if self.existing_buttonobject.is_clicked(event):
                print("not implemented")
            if self.back_buttonobject.is_clicked(event):
                self.manager.switch_to_scene("Editor main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color])
        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        self.back_buttonobject.draw(surface)
        self.title_textobject.draw(surface)
        self.filepicker_buttonobject.draw(surface)
        self.existing_buttonobject.draw(surface)
        self.or_textobject.draw(surface)
        self.alertobject.draw(surface)
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)