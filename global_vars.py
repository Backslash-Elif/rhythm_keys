import os, platform, json, pygame

def save_directory(dir_name: str): #gets the location for the save data
    if platform.system() == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), dir_name)
    elif platform.system() == "Darwin":
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', dir_name)
    elif platform.system() == "Linux":
        return os.path.join(os.path.expanduser('~'), '.config', dir_name)
    else:
        raise Exception("Unsupported operating system")

def fetch_settings(config_filepath: str):
    global user_name, user_dark_mode, user_bg_color, sys_screen_size_id
    if not os.path.exists(config_filepath): #if no settings are present
        if not os.path.exists(const_save_dir):
            os.makedirs(const_save_dir)
        print("config.json not found, defaults set.")
        with open(config_filepath, 'w') as config_file:
            json.dump(const_defaults, config_file, indent=4)
        return False
    else:
        with open(config_filepath, 'r') as config_file:
            settings = json.load(config_file)
            user_name = settings.get("user_name", "")
            user_dark_mode = settings.get("user_dark_mode", False)
            user_bg_color = settings.get("user_bg_color", "none")
            sys_screen_size_id = settings.get("sys_screen_size_id", 0)
        return True

def save_config():
    settings = {
        "user_name": user_name,
        "user_dark_mode": user_dark_mode,
        "user_bg_color": user_bg_color,
        "sys_screen_size_id": sys_screen_size_id
    }

    with open(const_config_file, 'w') as config_file:
        json.dump(settings, config_file, indent=4)
    print("Saved config.")

def get_mouse_pos():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    s_mouse_x = int((mouse_x / sys_current_screen_size[0]) * 1920)
    s_mouse_y = int((mouse_y / sys_current_screen_size[1]) * 1080)
    return (s_mouse_x, s_mouse_y)

#constants
const_defaults = {
    "user_name": "",
    "user_dark_mode": False,
    "user_bg_color": "none",
    "sys_screen_size_id": 0
}
const_rendersize = (1920, 1080)
const_os_name = platform.system()
const_save_dir_name = "rhythm_keys"
const_save_dir = save_directory(const_save_dir_name)
print("Local save directory located at: " + const_save_dir)
const_config_file = os.path.join(const_save_dir, "config.json")
const_editor_difficulty_names = ["beginner", "easy", "medium", "hard", "ultra"]
const_screen_sizes = ((1280, 720), (1920, 1080), (2560, 1440), (3840, 2160))
#user
user_name = ""
user_dark_mode = False
user_bg_color = "none"
#editor
editor_name = ""
editor_author = ""
editor_song_artist = ""
editor_length = 0
editor_difficulty = 0
editor_bpm = 0
editor_lvldat = {}
editor_filepath = ""
editor_startdelay_ms = 0
editor_load_vars = False
#system and misc
sys_screen_size_id = 0 #0=HD, 1=Full HD (Native), 2=QHD, 3=4K UHD
sys_current_screen_size = const_screen_sizes[sys_screen_size_id]
sys_oobe = False #out of box experience
sys_persistant_storage = {}
sys_debug_lvl = 2 #0=none, 1=minimal, 2=all

if not fetch_settings(const_config_file):
    sys_oobe = True
sys_current_screen_size = const_screen_sizes[sys_screen_size_id]