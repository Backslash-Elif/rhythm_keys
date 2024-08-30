import os, platform

def save_directory(dir_name: str): #gets the location for the save data
    if platform.system() == "Windows":
        return os.path.join(os.getenv('LOCALAPPDATA'), dir_name)
    elif platform.system() == "Darwin":
        return os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', dir_name)
    elif platform.system() == "Linux":
        return os.path.join(os.path.expanduser('~'), '.config', dir_name)
    else:
        raise Exception("Unsupported operating system")

#user
user_name = "Backslash Elif"
user_theme = "dark"
user_color = "purple"
#editor
editor_name = ""
editor_author = ""
editor_song_artist = ""
editor_length = 0
editor_difficulty = 0
editor_bpm = 0
editor_lvldat = {}
editor_filepath = ""
#system and misc
sys_screen_size = (1920, 1080) #TODO make 720p mode

#constants
const_os_name = platform.system()
const_save_dir_name = "rhythm_keys"
const_save_dir = save_directory(const_save_dir_name)
const_editor_difficulty_names = ["beginner", "easy", "medium", "hard", "ultra"]