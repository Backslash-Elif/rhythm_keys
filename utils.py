import global_vars, os, platform, json, pygame, shutil, zipfile, uuid
from decimal import Decimal

def save_level():
    level = {
        "name": global_vars.editor_name,
        "author": global_vars.editor_author,
        "artist": global_vars.editor_song_artist,
        "length": global_vars.editor_length,
        "difficulty": global_vars.editor_difficulty,
        "bpm": global_vars.editor_bpm,
        "startdelay": str(global_vars.editor_startdelay),
        "snap": global_vars.editor_snap_value,
        "lvldat": global_vars.editor_lvldat
    }

    with open(os.path.join(global_vars.const_working_dir, "level.json"), 'w') as level_file:
        json.dump(level, level_file, indent=4)
    print("Saved level.")

def load_level():
    if not os.path.exists(os.path.join(global_vars.const_working_dir, "level.json")): #if no settings are present
        print("level.json not found!")
    else:
        with open(os.path.join(global_vars.const_working_dir, "level.json"), 'r') as level_file:
            level = json.load(level_file)
            global_vars.editor_name = level.get("name", "Error")
            global_vars.editor_author = level.get("author", "Error")
            global_vars.editor_song_artist = level.get("artist", "Error")
            global_vars.editor_length = level.get("length", 0)
            global_vars.editor_difficulty = level.get("difficulty", 0)
            global_vars.editor_bpm = level.get("bpm", 0)
            global_vars.editor_startdelay = Decimal(level.get("startdelay", Decimal('0.0')))
            global_vars.editor_snap_value = level.get("snap", 4)
            global_vars.editor_lvldat = level.get("lvldat", {})
            global_vars.editor_lvldat = {float(key): value for key, value in global_vars.editor_lvldat.items()} #converts the keys into floats
    
    for ext in ['mp3', 'ogg']:
        audio_file = os.path.join(global_vars.const_working_dir, f'audiotrack.{ext}')
        if os.path.isfile(audio_file):
            global_vars.editor_filepath = audio_file

def copy_audio_to_working_dir(filepath: str):
    try:
        #get file extension
        _, file_extension = os.path.splitext(filepath)

        filename = f"audiotrack{file_extension}"
        
        #make destination path
        destination = os.path.join(global_vars.const_working_dir, filename)
        
        #create destination dir if not exists
        if not os.path.exists(global_vars.const_working_dir):
            os.makedirs(global_vars.const_working_dir)
            print(f"Created directory {global_vars.const_working_dir}")
        
        #copy
        shutil.copy(filepath, destination)
        
        return destination
    except Exception as e:
        print("Error:", e)

def load_from_external_file(filepath: str):
    try:
        filename = "archive.zip"
        
        #make destination path
        destination = os.path.join(global_vars.const_working_dir, filename)
        
        #create destination dir if not exists
        if not os.path.exists(global_vars.const_working_dir):
            os.makedirs(global_vars.const_working_dir)
            print(f"Created directory {global_vars.const_working_dir}")
        
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
            archive.extractall(global_vars.const_working_dir)
    
    except Exception as e:
        print("Error:", e)
    
    os.remove(destination)
    load_level()

def clear_working_dir():
    try:
        # Iterate over all files in the directory
        for filename in os.listdir(global_vars.const_working_dir):
            file_path = os.path.join(global_vars.const_working_dir, filename)
            # Check if it's a file and remove it
            if os.path.isfile(file_path):
                os.remove(file_path)
        
    except Exception as e:
        print("Error:", e)

def save_lvl_list():
    try:
        with open(global_vars.const_lvl_list_file, 'w') as file:
            json.dump(global_vars.sys_lvl_list, file, indent=4)
    except Exception as e:
        print("Error saving sys_lvl_list:", e)

def load_lvl_list():
    try:
        if not os.path.isfile(global_vars.const_lvl_list_file):
            print(f"Error: The file {global_vars.const_lvl_list_file} does not exist.")
            global_vars.sys_lvl_list = {}
        
        with open(global_vars.const_lvl_list_file, 'r') as file:
            global_vars.sys_lvl_list = json.load(file)
            print(f"Loaded sys_lvl_list from {global_vars.const_lvl_list_file}")
            
    except Exception as e:
        print("Error loading sys_lvl_list:", e)
        global_vars.sys_lvl_list = {}

def create_package(uuid):
    load_lvl_list()
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    try:
        # Prepare the archive name with a UUID
        archive_name = uuid + '.zip'
        archive_path = os.path.join(os.path.dirname(global_vars.const_working_dir), archive_name)
        
        # Create a ZIP archive
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            # Add level.json if it exists
            level_file = os.path.join(global_vars.const_working_dir, 'level.json')
            if os.path.isfile(level_file):
                archive.write(level_file, arcname='level.json')

            # Check for audiotrack.[mp3/ogg]
            for ext in ['mp3', 'ogg']:
                audio_file = os.path.join(global_vars.const_working_dir, f'audiotrack.{ext}')
                if os.path.isfile(audio_file):
                    archive.write(audio_file, arcname=os.path.basename(audio_file))
                    break  # Stop after adding the first existing audio file

        global_vars.sys_lvl_list[uuid] = {"name": global_vars.editor_name, "author": global_vars.editor_author, "highscore": 0}
        save_lvl_list()
        
    except Exception as e:
        print("Error:", e)

def export_package(uuid, destinationpath):
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    try:
        sourcepath = os.path.join(global_vars.const_save_dir, uuid+".zip")
        shutil.copy(sourcepath, destinationpath)
        
    except Exception as e:
        print("Error:", e)

def del_package(uuid):
    try:
        sourcepath = os.path.join(global_vars.const_save_dir, uuid+".zip")
        os.remove(sourcepath)
        
    except Exception as e:
        print("Error:", e)
    
    try:
        load_lvl_list()
        global_vars.sys_lvl_list.pop(uuid)
        save_lvl_list()
        
    except Exception as e:
        print("Error:", e)

def load_package(filename: str):
    #made by You AI-powered search engine (you.com) because I suck at zip archives and stuff
    try:
        # Construct the full path to the ZIP file
        zip_file_path = os.path.join(global_vars.const_save_dir, filename)
        
        # Check if the ZIP file exists
        if not os.path.isfile(zip_file_path):
            print(f"Error: The file {zip_file_path} does not exist.")
            return
        
        # Create the working directory if it doesn't exist
        if not os.path.exists(global_vars.const_working_dir):
            os.makedirs(global_vars.const_working_dir)
            print(f"Created directory {global_vars.const_working_dir}")
        
        # Unzip the file
        with zipfile.ZipFile(zip_file_path, 'r') as archive:
            archive.extractall(global_vars.const_working_dir)

    except Exception as e:
        print("Error:", e)

def generate_uuid():
    return str(uuid.uuid4())

def sanatize_editor_vars():
    global_vars.editor_name = ""
    global_vars.editor_author = global_vars.user_name
    global_vars.editor_song_artist = ""
    global_vars.editor_length = 0
    global_vars.editor_difficulty = 0
    global_vars.editor_bpm = 0
    global_vars.editor_filepath = ""
    global_vars.editor_startdelay = Decimal('0.0')
    global_vars.editor_snap_value = 4
    global_vars.editor_lvldat = {}
    global_vars.editor_uuid = ""

def get_persistant_storage_item(key):
    return global_vars.sys_persistant_storage[key] if key in global_vars.sys_persistant_storage else None #shortcut for correctly getting value without keyerror

def get_mouse_pos():
    mouse_x, mouse_y = pygame.mouse.get_pos()
    s_mouse_x = int((mouse_x / global_vars.sys_current_screen_size[0]) * 1920)
    s_mouse_y = int((mouse_y / global_vars.sys_current_screen_size[1]) * 1080)
    return (s_mouse_x, s_mouse_y)

def center_axis(surface_size: int, object_size: int, shift: int = 0): #returns the centered x cordinates
    centered_axis = (surface_size/2) - (object_size/2) + shift
    return centered_axis
    
def center_obj(surface_size: tuple, object_size: tuple, shift: tuple = (0, 0)): #returns the centered cordinates
    x_cor = center_axis(surface_size[0], object_size[0], shift[0])
    y_cor = center_axis(surface_size[1], object_size[1], shift[1])
    return (x_cor, y_cor)

def hextobits(hex:str):
    dec = int(hex, 16)
    bits = []
    for i in range(4):
        bits.append(True if dec%2 else False)
        dec = int(dec/2)
    return list(reversed(bits))

def bitstohex(bits:iter):
    bits = list(reversed(bits))
    dec = 0
    for i in range(4):
        dec += [1,2,4,8][i] if bits[i] else 0
    return str(hex(dec)[2:])

def loadfromlvldat(index:int):
    if index in global_vars.editor_lvldat:
        return global_vars.editor_lvldat[index]
    else:
        return '0'