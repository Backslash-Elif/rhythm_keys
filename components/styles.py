import global_vars

def get_color_brightness(color: tuple):
    r, g, b = color
    return 0.299*color[0]/255 + 0.587*color[1]/255 + 0.114*color[2]/255 #0.299, 0.587, 0.114 perceived brightness of rgb

def change_color(color: tuple, difference: int):
    r, g, b = color
    return (min(255, max(0, r + difference)), min(255, max(0, g + difference)), min(255, max(0, b + difference))) #returns the changed color as tuple

def compute_accent(original_color: tuple) -> tuple[tuple, tuple, tuple]: #calculates the lighter or darker accent of a color
    brightness = get_color_brightness(original_color)
    
    difference = 20 #seems to be an universally good color difference
    if brightness >= 0.5:
        difference *= -1 #making negative for darkening
        text_color = (0, 0, 0)
    else:
        text_color = (255, 255, 255)
    #print(original_color, change_color(original_color, difference), text_color)
    return (original_color, change_color(original_color, difference), text_color) #returns both original and accent and text color

def compute_bg(start_color: tuple, end_color:tuple): #custom function to calculate darker color for bg
    change_value = 255 - max(start_color + end_color)
    if change_value > 0:
        start_color = change_color(start_color, change_value)
        end_color = change_color(end_color, change_value)
    brightness = 100 if global_vars.user_dark_mode else 200
    brightness /= 255
    return ((int(start_color[0]*brightness), int(start_color[1]*brightness), int(start_color[2]*brightness)), (int(end_color[0]*brightness), int(end_color[1]*brightness), int(end_color[2]*brightness)))

colors = { #original colors in format (R, G, B)
    "red": (255, 0, 0),
    "light_red": (255, 99, 71),
    "soft_red": (225, 18, 69),
    "dark_red": (139, 0, 0),
    "green": (0, 255, 0),
    "light_green": (0, 255, 127),
    "dark_green": (0, 100, 0),
    "blue": (0, 0, 255),
    "light_blue": (11, 87, 208),
    "dark_blue": (0, 0, 128),
    "sky_blue": (0, 191, 255),
    "purple": (132, 3, 252),
    "pink": (255, 20, 147),
    "magenta": (255, 0, 255),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0),
    "gray": (128, 128, 128),
    "light_gray": (212, 212, 212),
    "dark_gray": (58, 58, 58),
    "black_gray": (33, 33, 33),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

#pre-calculates auto-generated accented colors and their matching text-color, done to reduce redundant color calculations. in format {key, ((standard color), (accented color), (text color))}
for key, value in colors.items():
    colors[key] = compute_accent(value)

UI_colors = {} #unified shortcuts to various colors which are used for the UI
background_gradient = {}

def compute_dynamic_colors():
    UI_colors["primary"] = colors["light_blue"]
    UI_colors["secondary"] = colors["dark_gray"] if global_vars.user_dark_mode else colors["light_gray"] #automatically switch between themes depending on light or dark mode
    UI_colors["success"] = colors["light_green"]
    UI_colors["warning"] = colors["yellow"]
    UI_colors["danger"] = colors["soft_red"]

    
    background_gradient["midnight"] = (compute_bg(colors["dark_blue"][0], colors["purple"][0]))
    background_gradient["daybreak"] = (compute_bg(colors["purple"][0], colors["orange"][0]))
    background_gradient["orchids"] = (compute_bg(colors["pink"][0], colors["purple"][0]))
    background_gradient["peppermint"] = (compute_bg(colors["sky_blue"][0], colors["light_green"][0]))
    background_gradient["forrest"] = (compute_bg(colors["dark_green"][0], colors["light_green"][0]))
    background_gradient["ocean"] = (compute_bg(colors["sky_blue"][0], colors["blue"][0]))
    background_gradient["coral_reef"] = (compute_bg(colors["red"][0], colors["blue"][0]))
    background_gradient["stone"] = (compute_bg(colors["gray"][0], colors["black_gray"][0]))

compute_dynamic_colors()

card_themes = { #(R, G, B, A)
    "light": colors["white"][0]+(64, ),
    "dark": colors["black"][0]+(64, ),
    "primary": colors["light_blue"][0]+(64, ),
    "warning": colors["yellow"][0]+(64, ),
    "danger": colors["red"][0]+(64, )
}

text_size = {
    "large_title": 128,
    "title": 96,
    "small_title": 64,
    "subtitle": 48,
    "text": 32,
    "small_text": 24
}