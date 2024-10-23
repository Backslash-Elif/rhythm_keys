import global_vars, utils
from scenes import scene
import tkinter as tk
from tkinter import filedialog

from components import button, debug, text, bgstyle, card, alert
from components.styles import colors, UI_colors, background_gradient, text_size, ColorName, UIColorName, TextSizeName, card_themes, CardThemeName

class DataManager(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager
        
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        #texts to make it more readable
        importtext = "Import a level from a .zip compressed archive.\nOnce imported, the level can be played and edited as desired."
        exporttext = "Export a level to share or play with friends.\nIf you want to share your creations you can export them here and then share them with your buddies."
        deltext = "Delete a level. It will be GONE irreversably."

        #components
        self.fg_cardobject = card.Card((200, 100), (1500, 800), card_themes[CardThemeName.DYNAMIC])
        self.title_textobject = text.Text("Savedata Management", text_size[TextSizeName.TITLE], (300, 200), (1300, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.back_buttonobject = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
        self.import_buttonobject = button.Button("Import", text_size[TextSizeName.TEXT], (300, 400), (200, 50), UI_colors[UIColorName.PRIMARY])
        self.import_textobject = text.Text(importtext, text_size[TextSizeName.TEXT], (300, 450), (1300, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.export_buttonobject = button.Button("Export", text_size[TextSizeName.TEXT], (300, 600), (200, 50), UI_colors[UIColorName.PRIMARY])
        self.export_textobject = text.Text(exporttext, text_size[TextSizeName.TEXT], (300, 650), (1300, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.del_buttonobject = button.Button("Delete", text_size[TextSizeName.TEXT], (300, 800), (200, 50), UI_colors[UIColorName.DANGER])
        self.del_textobject = text.Text(deltext, text_size[TextSizeName.TEXT], (550, 800), (1000, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)
        self.alertobject = alert.Alert()

        
        if isinstance(utils.get_persistant_storage_item("exportfile"), str):#on return executes this function if user has picked level
            if utils.get_persistant_storage_item("remove_package"): #delete
                utils.del_package(utils.get_persistant_storage_item("exportfile"))
                self.alertobject.new_alert("Deletion was successful.")
                global_vars.sys_persistant_storage["remove_package"] = None
            else: #save
                self.save_as()
                self.alertobject.new_alert("Export was successful.")
        global_vars.sys_persistant_storage["exportfile"] = None

    
    def handle_event(self, event):
        if self.alertobject.is_active():
            self.alertobject.handle_events(event)
        else: #events aren't processed if alert is active
            if self.import_buttonobject.is_clicked(event): #import button
                selected_file = self.file_picker()
                utils.load_from_external_file(selected_file)
                utils.create_package(utils.generate_uuid())
                self.alertobject.new_alert("Import was successful!")

            if self.export_buttonobject.is_clicked(event): #export button
                global_vars.sys_persistant_storage["select_destination"] = 1
                self.manager.switch_to_scene("Level selector")

            if self.del_buttonobject.is_clicked(event): #delete button
                global_vars.sys_persistant_storage["select_destination"] = 1
                global_vars.sys_persistant_storage["remove_package"] = True
                self.manager.switch_to_scene("Level selector")

            if self.back_buttonobject.is_clicked(event): #back button
                global_vars.sys_persistant_storage["remove_package"] = False
                self.manager.switch_to_scene("Main menu")
    
    def draw(self, surface):
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws the background

        self.fg_cardobject.draw(surface)
        self.title_textobject.draw(surface)
        self.back_buttonobject.draw(surface)
        self.title_textobject.draw(surface)
        self.import_buttonobject.draw(surface)
        self.import_textobject.draw(surface)
        self.export_buttonobject.draw(surface)
        self.export_textobject.draw(surface)
        self.del_buttonobject.draw(surface)
        self.del_textobject.draw(surface)
        self.alertobject.draw(surface)

        #draws debug information
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)
    
    def file_picker(self):
    #make rootwindow and hide it
        root = tk.Tk()
        root.withdraw()

        #file allow list
        file_types = [("Compressed File Archive", "*.zip")]

        #file dialog
        file_path = filedialog.askopenfilename(title="Select an Zip Archive", filetypes=file_types)
        return file_path

    def save_as():#made by You AI-powered search engine (you.com)
        # Create a Tkinter root window
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        # Open the Save As dialog
        file_path = filedialog.asksaveasfilename(
            defaultextension=".zip",  # Default file extension
            filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")],  # File types
            title="Save as ZIP file"  # Dialog title
        )

        if file_path:  # Check if a file path was selected
            utils.export_package(global_vars.sys_persistant_storage["exportfile"], file_path)