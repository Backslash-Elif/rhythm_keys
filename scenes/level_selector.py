import global_vars, utils
from scenes import scene

from components import button, debug, text, touchtrigger, bgstyle, card, alert
from components.styles import colors, UI_colors, background_gradient, card_themes, ColorName, UIColorName, CardThemeName, text_size, TextSizeName

class LevelSelector(scene.Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.manager = manager

        utils.load_lvl_list()

        if "select_destination" not in global_vars.sys_persistant_storage:
            global_vars.sys_persistant_storage["select_destination"] = 0 #0 = editor, 1 = data manager, 2 = main game
        
        #components
        self.debug_text_debugobject = debug.DebugInfo()
        self.debug_grid_debugobject = debug.Grid(global_vars.const_rendersize)

        self.back_btn = button.Button("Back", text_size[TextSizeName.TEXT], (50, 950), (100, 50), UI_colors[UIColorName.DANGER])
        self.next_btn = button.Button("Select", text_size[TextSizeName.TEXT], (1750, 950), (100, 50), UI_colors[UIColorName.PRIMARY])

        self.lightmode_cardobject = card.Card((40, 40), (1820, 970), card_themes[CardThemeName.DYNAMIC])

        self.title_textobject = text.Text("Select a level", text_size[TextSizeName.LARGE_TITLE], (100, 50), (1700, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.LEFT)

        self.page_textobject = text.Text(f"Page\n1 of {int(len(global_vars.sys_lvl_list)/10)+1}", text_size[TextSizeName.TEXT], (1400, 950), (100, 50), colors[ColorName.DYNAMIC][0])
        self.page_next_buttonobject = button.Button("Next", text_size[TextSizeName.TEXT], (1500, 950), (150, 50), UI_colors[UIColorName.SECONDARY])
        self.page_prev_buttonobject = button.Button("Previous", text_size[TextSizeName.TEXT], (1250, 950), (150, 50), UI_colors[UIColorName.SECONDARY])

        self.orderby_buttonobject = button.Button("Sorting by name", text_size[TextSizeName.TEXT], (250, 950), (300, 50), UI_colors[UIColorName.SECONDARY])
        self.orderreverse_buttonobject = button.Button("Reverse", text_size[TextSizeName.TEXT], (600, 950), (150, 50), UI_colors[UIColorName.DANGER])

        self.alert_object = alert.Alert()
        self.alertid = 0

        self.switch_to_editor = 0 #loading the editor took long so added a messagebox to explain the waiting time. the alert has to be drawn first tho

        self.sorting_mode = 0 #0=name, 1=author, 2=highscore
        self.sorting_reverse = False
        
        self.page = 0

        #coordinates for items
        self.xcords = (100, 1000)
        self.ycords = (200, 350, 500, 650, 800)

        self.selected_item = None

        self.select_is_copy = False #another hack

        self.levelitem_cardobject = card.Card((90, 190), (820, 120), card_themes[CardThemeName.DYNAMIC])
        self.levelitem_title_textobject = text.Text("Level name", text_size[TextSizeName.SMALL_TITLE], (90, 190), (800, 100), colors[ColorName.DYNAMIC][0], text.TextAlign.TOP_LEFT)
        self.levelitem_author_textobject = text.Text("Author name", text_size[TextSizeName.TEXT], (100, 250), (400, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_LEFT)
        self.levelitem_highscore_textobject = text.Text("High score", text_size[TextSizeName.TEXT], (500, 250), (400, 50), colors[ColorName.DYNAMIC][0], text.TextAlign.BOTTOM_RIGHT)
        self.levelitem_triggerobject = touchtrigger.Touchtrigger((90, 190), (820, 120))
        self._sort_lvl_list()

    def handle_event(self, event):
        if self.alert_object.is_active():
            self.alert_object.handle_events(event)
        else:
            if self.back_btn.is_clicked(event): #back button
                if utils.get_persistant_storage_item("select_destination") == 1:
                    self.manager.switch_to_scene("Data manager")
                elif utils.get_persistant_storage_item("select_destination") == 2:
                    self.manager.switch_to_scene("Main menu")
                else:
                    self.manager.switch_to_scene("Editor main menu")

            if self.selected_item != None: #disables next button if nothing selected
                if self.next_btn.is_clicked(event): #next button
                    if global_vars.sys_persistant_storage["select_destination"] == 1: #redirect to data managed
                        global_vars.sys_persistant_storage["exportfile"] = str(list(self.sorting.values())[self.selected_item])
                        self.manager.switch_to_scene("Data manager")

                    if global_vars.sys_persistant_storage["select_destination"] == 2: #redirect to main game
                        utils.load_package(list(self.sorting.values())[self.selected_item]+".zip")
                        utils.load_level()
                        global_vars.editor_uuid = list(self.sorting.values())[self.selected_item]
                        self.switch_to_editor = 1
                        self.alert_object.new_alert("Please wait.\n\nLoading...")

                    if global_vars.sys_persistant_storage["select_destination"] == 0: #redirect to editor
                        self.alert_object.new_alert("Would you like to save a copy?\n\n(Press cancel to edit the original instead)", 1)
                        self.alertid = 1

            if self.orderby_buttonobject.is_clicked(event): #change order button
                self.sorting_mode += 1
                if self.sorting_mode > 2:
                    self.sorting_mode = 0
                self.orderby_buttonobject.set_text("Sorting by "+("name", "author", "high score")[self.sorting_mode])
                self._sort_lvl_list()
                self.selected_item = None

            if self.orderreverse_buttonobject.is_clicked(event): #reverse button
                self.sorting_reverse = not self.sorting_reverse
                self.orderreverse_buttonobject.set_color_scheme(UI_colors[UIColorName.SUCCESS] if self.sorting_reverse else UI_colors[UIColorName.DANGER])
                self._sort_lvl_list()
                self.selected_item = None

            if self.page_prev_buttonobject.is_clicked(event): #previous page button
                self.page = max(0, self.page-1)
                self.page_textobject.set_text(f"Page\n{self.page+1} of {int(len(global_vars.sys_lvl_list)/10)+1}")
                self._sort_lvl_list()
                self.selected_item = None

            if self.page_next_buttonobject.is_clicked(event): #next page button
                self.page = min(int(len(global_vars.sys_lvl_list)/10)+1, self.page+1)
                self.page_textobject.set_text(f"Page\n{self.page+1} of {int(len(global_vars.sys_lvl_list)/10)+1}")
                self._sort_lvl_list()
                self.selected_item = None
            
            #detection for when a user clicks on an item
            itemnum = self.page * 10
            for xcord in self.xcords:
                for ycord in self.ycords:
                    if itemnum > len(global_vars.sys_lvl_list) - 1:
                        break
                    self.levelitem_triggerobject.set_pos((xcord-10, ycord-10))
                    if self.levelitem_triggerobject.update(event):
                        self.selected_item = itemnum
                    itemnum += 1
    
    def draw(self, surface):
        #hack to make alert visible before scene transition
        if self.switch_to_editor > 1:
            utils.load_package(list(self.sorting.values())[self.selected_item]+".zip")
            utils.load_level()
            if self.select_is_copy: #makes copies have user's name
                global_vars.editor_author = global_vars.user_name
            self.manager.switch_to_scene("Game" if global_vars.sys_persistant_storage["select_destination"] == 2 else "Editor")
        if self.switch_to_editor > 0:
            self.switch_to_editor += 1
        if self.alertid == 1 and self.alert_object.get_result() != None:
            global_vars.editor_uuid = utils.generate_uuid() if self.alert_object.get_result() else list(self.sorting.values())[self.selected_item]
            if self.alert_object.get_result():
                self.select_is_copy = True
            self.alert_object.new_alert("Please wait.\n\nPreparing files & Initialising editor...")
            self.switch_to_editor = 1
        #====
        
        bgstyle.Bgstyle.draw_gradient(surface, background_gradient[global_vars.user_bg_color]) #draws background
        if not global_vars.user_dark_mode: #helps the light mode stand out more
            self.lightmode_cardobject.draw(surface)

        self.back_btn.draw(surface)
        self.title_textobject.draw(surface)
        self.page_textobject.draw(surface)
        self.page_next_buttonobject.draw(surface)
        self.page_prev_buttonobject.draw(surface)
        self.orderby_buttonobject.draw(surface)
        self.orderreverse_buttonobject.draw(surface)

        #drawing the different items
        itemnum = self.page * 10
        for xcord in self.xcords:
            for ycord in self.ycords:
                if itemnum > len(global_vars.sys_lvl_list) - 1:
                    break
                self.levelitem_cardobject.set_pos((xcord-10, ycord-10))
                self.levelitem_title_textobject.set_position((xcord, ycord))
                self.levelitem_author_textobject.set_position((xcord, ycord+50))
                self.levelitem_highscore_textobject.set_position((xcord+400, ycord+50))
                self.levelitem_title_textobject.set_text(global_vars.sys_lvl_list[list(self.sorting.values())[itemnum]]["name"])
                self.levelitem_author_textobject.set_text("By "+(global_vars.sys_lvl_list[list(self.sorting.values())[itemnum]]["author"]))
                self.levelitem_highscore_textobject.set_text("HI: "+str(global_vars.sys_lvl_list[list(self.sorting.values())[itemnum]]["highscore"]))
                self.levelitem_cardobject.set_color(card_themes[CardThemeName.PRIMARY] if self.selected_item == itemnum else card_themes[CardThemeName.DYNAMIC])
                self.levelitem_cardobject.draw(surface)
                self.levelitem_title_textobject.draw(surface)
                self.levelitem_author_textobject.draw(surface)
                self.levelitem_highscore_textobject.draw(surface)
                itemnum += 1

        self.next_btn.draw(surface)
        self.alert_object.draw(surface)

        #draws debug information
        if global_vars.sys_debug_lvl > 0:
            self.debug_text_debugobject.draw(surface)
        if global_vars.sys_debug_lvl > 1:
            self.debug_grid_debugobject.draw(surface)
    
    def _sort_lvl_list(self): #sorts the items by the selected category
        self.sorting = {}
        for id, (key, value) in zip(range(len(global_vars.sys_lvl_list)), global_vars.sys_lvl_list.items()):
            tempvalue = str(str(value[("name", "author", "highscore")[self.sorting_mode]]) + value["name"]).lower()#ad name at the end to make it somewhat sorted by name eg. in case of same author
            tempvalue = tempvalue+str(id) if tempvalue in self.sorting else tempvalue
            self.sorting[tempvalue] = key
        
        self.sorting = dict(sorted(self.sorting.items(), reverse=self.sorting_reverse))