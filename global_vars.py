import os, platform, json, pygame, shutil, zipfile, uuid
from decimal import Decimal

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

def save_level():
    level = {
        "name": editor_name,
        "author": editor_author,
        "artist": editor_song_artist,
        "length": editor_length,
        "difficulty": editor_difficulty,
        "bpm": editor_bpm,
        "startdelay": str(editor_startdelay),
        "snap": editor_snap_value,
        "lvldat": editor_lvldat
    }

    with open(os.path.join(const_working_dir, "level.json"), 'w') as level_file:
        json.dump(level, level_file, indent=4)
    print("Saved level.")

def load_level():
    global editor_name, editor_author, editor_song_artist, editor_length, editor_difficulty, editor_bpm, editor_startdelay, editor_snap_value, editor_lvldat, editor_filepath
    if not os.path.exists(os.path.join(const_working_dir, "level.json")): #if no settings are present
        print("level.json not found!")
    else:
        with open(os.path.join(const_working_dir, "level.json"), 'r') as level_file:
            level = json.load(level_file)
            editor_name = level.get("name", "Error")
            editor_author = level.get("author", "Error")
            editor_song_artist = level.get("artist", "Error")
            editor_length = level.get("length", 0)
            editor_difficulty = level.get("difficulty", 0)
            editor_bpm = level.get("bpm", 0)
            editor_startdelay = Decimal(level.get("startdelay", 0))
            editor_snap_value = level.get("snap", 4)
            editor_lvldat = level.get("lvldat", {})
            editor_lvldat = {float(key): value for key, value in editor_lvldat.items()}
    
    for ext in ['mp3', 'ogg']:
        audio_file = os.path.join(const_working_dir, f'audiotrack.{ext}')
        if os.path.isfile(audio_file):
            editor_filepath = audio_file

def copy_audio_to_working_dir(filepath: str):
    try:
        #get file extension
        _, file_extension = os.path.splitext(filepath)

        filename = f"audiotrack{file_extension}"
        
        #make destination path
        destination = os.path.join(const_working_dir, filename)
        
        #create destination dir if not exists
        if not os.path.exists(const_working_dir):
            os.makedirs(const_working_dir)
            print(f"Created directory {const_working_dir}")
        
        #copy
        shutil.copy(filepath, destination)
        
        return destination
    except Exception as e:
        print("Error:", e)

def load_from_external_file(filepath: str):
    global editor_filepath
    try:
        filename = "archive.zip"
        
        #make destination path
        destination = os.path.join(const_working_dir, filename)
        
        #create destination dir if not exists
        if not os.path.exists(const_working_dir):
            os.makedirs(const_working_dir)
            print(f"Created directory {const_working_dir}")
        
        #copy
        shutil.copy(filepath, destination)
    except Exception as e:
        print("Error:", e)
    
    try:
        # Construct the full path to the ZIP file
        zip_file_path = destination
        
        # Check if the ZIP file exists
        if not os.path.isfile(zip_file_path):
            print(f"Error: The file {zip_file_path} does not exist.")
            return
        
        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as archive:
            archive.extractall(const_working_dir)
    
    except Exception as e:
        print("Error:", e)
    
    os.remove(destination)
    load_level()

def clear_working_dir():
    try:
        # Iterate over all files in the directory
        for filename in os.listdir(const_working_dir):
            file_path = os.path.join(const_working_dir, filename)
            # Check if it's a file and remove it
            if os.path.isfile(file_path):
                os.remove(file_path)
        
    except Exception as e:
        print("Error:", e)

def save_lvl_list():
    global sys_lvl_list
    try:
        with open(const_lvl_list_file, 'w') as file:
            json.dump(sys_lvl_list, file, indent=4)
    except Exception as e:
        print("Error saving sys_lvl_list:", e)

def load_lvl_list():
    global sys_lvl_list
    try:
        if not os.path.isfile(const_lvl_list_file):
            print(f"Error: The file {const_lvl_list_file} does not exist.")
            sys_lvl_list = {}
        
        with open(const_lvl_list_file, 'r') as file:
            sys_lvl_list = json.load(file)
            print(f"Loaded sys_lvl_list from {const_lvl_list_file}")
            
    except Exception as e:
        print("Error loading sys_lvl_list:", e)
        sys_lvl_list = {}

def generate_uuid():
    return str(uuid.uuid4())

def create_package(uuid):
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    global sys_lvl_list
    try:
        # Prepare the archive name with a UUID
        archive_name = uuid + '.zip'
        archive_path = os.path.join(os.path.dirname(const_working_dir), archive_name)
        
        # Create a ZIP archive
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            # Add level.json if it exists
            level_file = os.path.join(const_working_dir, 'level.json')
            if os.path.isfile(level_file):
                archive.write(level_file, arcname='level.json')

            # Check for audiotrack.[mp3/ogg]
            for ext in ['mp3', 'ogg']:
                audio_file = os.path.join(const_working_dir, f'audiotrack.{ext}')
                if os.path.isfile(audio_file):
                    archive.write(audio_file, arcname=os.path.basename(audio_file))
                    break  # Stop after adding the first existing audio file

        sys_lvl_list[uuid] = {"name": editor_name, "author": editor_author, "highscore": 0}
        save_lvl_list()
        
    except Exception as e:
        print("Error:", e)

def export_package(uuid, destinationpath):
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    global sys_lvl_list
    try:
        sourcepath = os.path.join(const_save_dir, uuid+".zip")
        shutil.copy(sourcepath, destinationpath)
        
    except Exception as e:
        print("Error:", e)

def load_package(filename: str):
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    try:
        # Construct the full path to the ZIP file
        zip_file_path = os.path.join(const_save_dir, filename)
        
        # Check if the ZIP file exists
        if not os.path.isfile(zip_file_path):
            print(f"Error: The file {zip_file_path} does not exist.")
            return
        
        # Create the working directory if it doesn't exist
        if not os.path.exists(const_working_dir):
            os.makedirs(const_working_dir)
            print(f"Created directory {const_working_dir}")
        
        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as archive:
            archive.extractall(const_working_dir)

    except Exception as e:
        print("Error:", e)

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
#saving
const_save_dir_name = "rhythm_keys"
const_save_dir = save_directory(const_save_dir_name)
print("Local save directory located at: " + const_save_dir)
const_working_dir = os.path.join(const_save_dir, "working")
const_config_file = os.path.join(const_save_dir, "config.json")
const_lvl_list_file = os.path.join(const_save_dir, "lvl_list.json")
const_editor_difficulty_names = ["beginner", "easy", "medium", "hard", "ultra"]
const_screen_sizes = ((1280, 720), (1920, 1080), (2560, 1440), (3840, 2160))
#user
user_name = ""
user_dark_mode = False
user_bg_color = "none"
#editor
editor_name = "" #song name
editor_author = ""
editor_song_artist = ""
editor_length = 0
editor_difficulty = 0
editor_bpm = 0
editor_lvldat = {}
editor_filepath = ""
editor_startdelay = Decimal('0.0')
editor_snap_value = 4
editor_uuid = ""
#system and misc
sys_lvl_list = {} #lvl_list but it's a dict X3
sys_screen_size_id = 0 #0=HD, 1=Full HD (Native), 2=QHD, 3=4K UHD
sys_current_screen_size = const_screen_sizes[sys_screen_size_id]
sys_oobe = False #out of box experience
sys_persistant_storage = {}
sys_debug_lvl = 0 #0=none, 1=minimal, 2=all

if not fetch_settings(const_config_file):
    sys_oobe = True
sys_current_screen_size = const_screen_sizes[sys_screen_size_id]